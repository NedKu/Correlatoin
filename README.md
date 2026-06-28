# 股票相關係數分析工具 - Streamlit 版本

一個交互式的 Streamlit 應用程序，用於分析股票之間的相關係數。支持在線部署到 Streamlit Cloud。

## 功能特性

- 📊 **實時股票數據下載** - 使用 Yahoo Finance API
- 📈 **相關係數熱圖** - 使用 Plotly 進行互動式可視化
- 📅 **靈活的時間範圍** - 選擇自定義分析期間
- 📝 **自定義股票列表** - 動態添加或移除股票代號
- 📊 **詳細統計信息** - 平均、最高、最低相關係數
- 🎨 **現代化 UI 設計** - 自動響應式設計
- ☁️ **雲端部署** - 可直接在 Streamlit Cloud 上運行

## 系統要求

- Python 3.8 或更高版本
- pip 包管理器

## 快速開始

### 方法一：在線運行（推薦）

1. 訪問 [Streamlit Cloud](https://streamlit.io/cloud)
2. 連接您的 GitHub 帳戶
3. 選擇此倉庫
4. 輸入 `app_streamlit.py` 作為主文件
5. 點擊「Deploy」

### 方法二：本地運行

#### 1. 克隆倉庫

```bash
git clone https://github.com/NedKu/Stock_correlatoin_analyzer.git
cd Stock_correlatoin_analyzer
```

#### 2. 創建虛擬環境（推薦）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

#### 4. 運行應用

```bash
streamlit run app_streamlit.py
```

應用會在 `http://localhost:8501` 打開

## 使用說明

### 1. 選擇分析時間範圍
- 使用側邊欄中的滑塊選擇開始年份和結束年份

### 2. 管理股票列表
- **查看當前股票**：在側邊欄中查看
- **添加股票**：
  - 在側邊欄輸入框中輸入股票代號（如 AAPL, TSM）
  - 點擊「➕ 添加」按鈕
- **移除股票**：
  - 在側邊欄輸入框中輸入股票代號
  - 點擊「➖ 移除」按鈕
- **重置**：點擊「🔄 重置為預設」返回預設列表

### 3. 執行分析
- 點擊「🔍 開始分析」按鈕
- 等待數據下載和計算完成

### 4. 查看結果
- **分析股票數、時間範圍、數據點數**：頂部指標卡
- **相關係數熱圖**：互動式 Plotly 熱圖
  - 紅色表示正相關
  - 藍色表示負相關
- **統計信息**：平均、最高、最低相關係數
- **最強相關配對**：前 10 個最相關的股票對
- **完整矩陣表**：所有股票之間的相關係數
- **下載結果**：將結果下載為 CSV 文件

## 預設股票列表

| 類別 | 股票代號 | 說明 |
|------|--------|------|
| 美國指數 | SPY | S&P 500 |
| | QQQ | NASDAQ 100 |
| | VT | 全球股票市場 |
| 國際 ETF | CSPX.L | 核心 S&P 500（倫敦交易） |
| | VWRA.L | 全球股票 UCITS ETF（倫敦交易） |
| | INDA | 印度 ETF |
| 台灣股票 | 006207.TW | 台灣 ETF |
| | 0050.TW | 台灣 0050 |
| | 2330.TW | 台積電 |
| 中國 ETF | MCHI | iShares MSCI 中國 |
| 債券 ETF | TLT | 美國長期公債 |
| | SHY | 美國短期公債 |
| 能源 ETF | VDE | 能源 ETF |

## 技術架構

- **框架**：Streamlit
- **數據來源**：yfinance (Yahoo Finance API)
- **數據處理**：pandas、numpy
- **可視化**：Plotly
- **部署**：Streamlit Cloud

## 文件結構

```
Stock_correlatoin_analyzer/
├── app_streamlit.py           # Streamlit 主應用
├── requirements.txt           # Python 依賴
├── .streamlit/
│   └── config.toml           # Streamlit 配置
├── README.md                 # 此文件
└── static/                   # （舊文件，可忽略）
```

## 常見問題

### Q: 某些股票無法下載怎麼辦？
A: 這通常是因為：
1. 股票代號不正確（使用 Yahoo Finance 上的代號）
2. 該股票在指定時間範圍內無數據
3. 網絡連接問題

嘗試使用有效的股票代號，例如 AAPL、MSFT、TSLA 等。

### Q: 分析需要多長時間？
A: 取決於：
- 股票數量
- 時間範圍長度
- 網絡連接速度

通常需要 5-30 秒。

### Q: 在 Streamlit Cloud 上部署失敗怎麼辦？
A: 檢查以下事項：
1. `app_streamlit.py` 文件是否在倉庫根目錄
2. `requirements.txt` 是否包含所有必要的包
3. GitHub 倉庫是否公開

### Q: 可以分析多少只股票？
A: 建議不超過 50 只以保持最佳性能。

## 故障排除

### 錯誤：ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### 本地運行時無法訪問
```bash
# 確保 Streamlit 正確安裝
pip install --upgrade streamlit
```

### 無法連接到 Yahoo Finance
- 檢查互聯網連接
- 嘗試稍後再試（Yahoo Finance 可能偶爾不可用）

## 許可證

此項目為個人學習和使用。

## 更新日誌

### v2.0.0 (2026-06-27)
- 從 Flask 遷移到 Streamlit
- 添加支持 Streamlit Cloud 部署
- 改進用戶界面和體驗
- 添加數據下載功能

---

祝您使用愉快！📈

有任何問題或建議，歡迎提出 Issue 或 Pull Request！
