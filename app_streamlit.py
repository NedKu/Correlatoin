import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# 設置頁面配置
st.set_page_config(
    page_title="股票相關係數分析工具",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    .stat-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 預設股票列表
DEFAULT_STOCKS = [
    'SPY', 'CSPX.L', 'QQQ', 'VT', 'VWRA.L', 'INDA', 
    '006207.TW', 'MCHI', '0050.TW', '2330.TW', 'TLT', 'SHY', 'VDE'
]

def fetch_stock_data(symbols, start_date, end_date):
    """
    從 Yahoo Finance 下載股票數據
    """
    prices = pd.DataFrame()
    failed_symbols = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, symbol in enumerate(symbols):
        try:
            status_text.text(f"正在下載 {symbol}...")
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            if len(data) > 0:
                # 處理 yfinance 返回格式
                if isinstance(data, pd.Series):
                    prices[symbol] = data
                elif 'Adj Close' in data.columns:
                    prices[symbol] = data['Adj Close']
                elif 'Close' in data.columns:
                    prices[symbol] = data['Close']
                else:
                    numeric_cols = data.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        prices[symbol] = data[numeric_cols[0]]
                    else:
                        failed_symbols.append(symbol)
                        continue
            else:
                failed_symbols.append(symbol)
        except Exception as e:
            failed_symbols.append(symbol)
        
        progress_bar.progress((idx + 1) / len(symbols))
    
    progress_bar.empty()
    status_text.empty()
    
    return prices, failed_symbols

def calculate_correlation_matrix(prices_df):
    """
    計算股票價格的相關係數矩陣
    """
    returns = prices_df.pct_change().dropna()
    correlation_matrix = returns.corr()
    return correlation_matrix

def create_heatmap(correlation_matrix):
    """
    創建相關係數熱圖
    """
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1,
        text=np.round(correlation_matrix.values, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="相關係數"),
        hovertemplate='%{y} - %{x}: %{z:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='股票相關係數熱圖',
        xaxis_title='股票',
        yaxis_title='股票',
        width=900,
        height=800,
        font=dict(size=12)
    )
    
    return fig

def calculate_stats(correlation_matrix):
    """
    計算統計信息
    """
    # 獲取上三角矩陣（避免重複計算和對角線）
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)
    values = correlation_matrix.values[mask]
    
    stats = {
        'average': np.mean(values),
        'max': np.max(values),
        'min': np.min(values),
        'std': np.std(values)
    }
    
    return stats

def get_strongest_correlations(correlation_matrix, n=5):
    """
    獲取最強的相關係數配對
    """
    # 獲取上三角矩陣
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)
    
    pairs = []
    for i in range(len(correlation_matrix)):
        for j in range(i+1, len(correlation_matrix)):
            pairs.append({
                'stock1': correlation_matrix.index[i],
                'stock2': correlation_matrix.index[j],
                'correlation': correlation_matrix.iloc[i, j],
                'abs_correlation': abs(correlation_matrix.iloc[i, j])
            })
    
    # 按絕對值排序
    pairs_sorted = sorted(pairs, key=lambda x: x['abs_correlation'], reverse=True)
    
    return pairs_sorted[:n]

# 主應用
def main():
    st.markdown("<div class='header'><h1>📈 股票相關係數分析工具</h1><p>使用 Yahoo Finance API 分析股票之間的相關係數</p></div>", unsafe_allow_html=True)
    
    # 側邊欄設置
    st.sidebar.markdown("## ⚙️ 設置")
    
    # 日期範圍選擇
    st.sidebar.markdown("### 📅 時間範圍")
    current_year = datetime.now().year
    start_year = st.sidebar.slider("開始年份", 2004, current_year, current_year - 7)
    end_year = st.sidebar.slider("結束年份", start_year, current_year, current_year)
    
    # 股票管理
    st.sidebar.markdown("### 📊 股票管理")
    
    # 初始化session state
    if 'current_stocks' not in st.session_state:
        st.session_state.current_stocks = DEFAULT_STOCKS.copy()
    
    # 顯示當前股票
    st.sidebar.markdown(f"**當前股票數: {len(st.session_state.current_stocks)}**")
    
    stock_list_display = ", ".join(st.session_state.current_stocks)
    st.sidebar.text_area("當前股票列表", stock_list_display, height=100, disabled=True)
    
    # 添加股票
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        add_symbol = st.text_input("添加股票代號", placeholder="例如: AAPL, TSLA")
    with col2:
        if st.button("➕ 添加"):
            symbol = add_symbol.strip().upper()
            if symbol and symbol not in st.session_state.current_stocks:
                st.session_state.current_stocks.append(symbol)
                st.success(f"✓ 已添加 {symbol}")
                st.rerun()
            elif symbol in st.session_state.current_stocks:
                st.warning(f"⚠️ {symbol} 已在列表中")
    
    # 移除股票
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        remove_symbol = st.text_input("移除股票代號", placeholder="例如: AAPL")
    with col2:
        if st.button("➖ 移除"):
            symbol = remove_symbol.strip().upper()
            if symbol in st.session_state.current_stocks:
                st.session_state.current_stocks.remove(symbol)
                st.success(f"✓ 已移除 {symbol}")
                st.rerun()
            elif symbol:
                st.warning(f"⚠️ {symbol} 不在列表中")
    
    # 重置按鈕
    if st.sidebar.button("🔄 重置為預設", use_container_width=True):
        st.session_state.current_stocks = DEFAULT_STOCKS.copy()
        st.rerun()
    
    # 驗證輸入
    if len(st.session_state.current_stocks) < 2:
        st.warning("⚠️ 至少需要 2 只股票進行相關係數分析")
        return
    
    if start_year > end_year:
        st.error("❌ 開始年份不能晚於結束年份")
        return
    
    # 分析按鈕
    if st.button("🔍 開始分析", use_container_width=True, key="analyze_btn", type="primary"):
        st.session_state.analyze = True
    
    # 執行分析
    if st.session_state.get('analyze', False):
        st.session_state.analyze = False
        
        # 計算日期範圍
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        
        st.markdown("---")
        st.markdown("## 📊 分析結果")
        
        # 下載數據
        with st.spinner("正在下載股票數據..."):
            stock_data, failed = fetch_stock_data(st.session_state.current_stocks, start_date, end_date)
        
        if len(failed) > 0:
            st.warning(f"⚠️ 無法下載以下股票: {', '.join(failed)}")
        
        if len(stock_data.columns) < 2:
            st.error("❌ 無法獲得足夠的股票數據，請更改時間範圍或股票列表")
            return
        
        # 計算相關係數
        correlation_matrix = calculate_correlation_matrix(stock_data)
        
        # 信息面板
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 分析股票數", len(correlation_matrix))
        with col2:
            st.metric("📅 時間範圍", f"{start_date.strftime('%Y-%m-%d')} 到 {end_date.strftime('%Y-%m-%d')}")
        with col3:
            st.metric("📈 數據點", len(stock_data))
        with col4:
            st.metric("✅ 成功下載", len(stock_data.columns))
        
        # 顯示熱圖
        st.markdown("### 🔥 相關係數熱圖")
        fig_heatmap = create_heatmap(correlation_matrix)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # 統計信息
        st.markdown("### 📈 統計信息")
        stats = calculate_stats(correlation_matrix)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("平均相關係數", f"{stats['average']:.4f}")
        with col2:
            st.metric("最高相關係數", f"{stats['max']:.4f}")
        with col3:
            st.metric("最低相關係數", f"{stats['min']:.4f}")
        with col4:
            st.metric("標準差", f"{stats['std']:.4f}")
        
        # 最強相關配對
        st.markdown("### 🔗 最強相關配對")
        strongest = get_strongest_correlations(correlation_matrix, n=10)
        
        strongest_df = pd.DataFrame([
            {
                '股票 1': pair['stock1'],
                '股票 2': pair['stock2'],
                '相關係數': f"{pair['correlation']:.4f}",
                '絕對值': f"{pair['abs_correlation']:.4f}"
            }
            for pair in strongest
        ])
        
        st.dataframe(strongest_df, use_container_width=True, hide_index=True)
        
        # 相關係數矩陣表格
        st.markdown("### 📋 完整相關係數矩陣")
        
        # 格式化相關係數矩陣
        correlation_display = correlation_matrix.copy()
        correlation_display = correlation_display.round(4)
        
        st.dataframe(
            correlation_display.style.format("{:.4f}").background_gradient(
                cmap='RdBu', vmin=-1, vmax=1
            ),
            use_container_width=True
        )
        
        # 下載按鈕
        st.markdown("### 📥 下載結果")
        
        # 將相關係數矩陣轉換為CSV
        csv = correlation_matrix.to_csv()
        st.download_button(
            label="📥 下載相關係數矩陣 (CSV)",
            data=csv,
            file_name=f"correlation_matrix_{start_year}_{end_year}.csv",
            mime="text/csv"
        )

if __name__ == '__main__':
    main()
