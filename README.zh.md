# CodeSentry

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)  
![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange)  
![License](https://img.shields.io/badge/License-MIT-green)

**CodeSentry** 是一款基於機器學習的桌面靜態分析工具，專為協助開發者與安全人員快速識別原始碼中可能洩漏的敏感資訊（例如 API 金鑰、權杖與其他憑證）而設計。

不同於僅依賴正則表達式的傳統掃描工具，CodeSentry 結合**統計特徵分析**（如 Shannon 熵）與 **XGBoost 機器學習模型**，能更有效識別高隨機性、具實際風險的憑證樣式，同時降低一般變數、測試字串或雜訊造成的誤報。

---
## 功能特色
- **機器學習驅動的憑證檢測**  
    透過 XGBoost 模型分析字串的熵值、字元分佈與結構特徵，評估其為敏感資訊的可能性。
    
- **現代化桌面圖形介面**  
    採用 PyQt6 打造深色主題介面，支援即時掃描進度與結果更新。
- **風險等級分類**
    - **CRITICAL**：高度可信，符合常見服務的憑證格式（如 AWS、OpenAI 金鑰）。
        
    - **HIGH**：高度可疑的高熵隨機字串。
        
    - **MEDIUM**：可能為憑證或具潛在風險的變數。
        
    - **LOW**：低風險內容，通常為雜訊或佔位字串。
        
- **遞迴專案掃描**  
    支援整個專案目錄掃描，並自動忽略 `.git`、`venv`、`__pycache__` 等常見非目標資料夾。
    
- **背景多執行緒處理**  
    掃描流程於背景執行緒執行，確保介面流暢與良好回應性。

---
## 技術概覽

- **前端**：Python（PyQt6）
    
- **核心模型**：XGBoost（Gradient Boosted Decision Trees）
    
### 特徵工程

模型在評估字串時，使用下列特徵：

1. **Shannon 熵**：衡量字串的隨機程度。
    
2. **正則預過濾**：快速篩選潛在候選字串以提升效能。
    
3. **結構比例分析**：分析數字、大寫字母與符號的分佈情形。
---
## 安裝

### 系統需求

- Python 3.10 或以上版本
- 建議使用虛擬環境
### 安裝步驟

**1. 複製專案**

`git clone https://github.com/Shi9870/Serect-huter.git cd Serect-huter`

**2. 建立並啟用虛擬環境**

Windows：

`python -m venv venv venv\Scripts\activate`

macOS / Linux：

`python3 -m venv venv source venv/bin/activate`

**3. 安裝依賴套件**

`pip install -r requirements.txt`

---

## 使用方式

### 啟動應用程式

`python main.py`

### 操作流程
1. 點擊 **Select Folder** 選擇目標專案目錄。
2. 點擊 **Start scanning** 開始掃描。
3. 掃描結果會即時顯示，並依風險等級分類。
4. 掃描完成後可檢視摘要並匯出報告。
---
## 壓力測試（使用合成資料）

為避免在測試過程中使用真實敏感資訊，CodeSentry 提供測試資料產生腳本，用於建立包含大量合成憑證樣本的測試環境。

1. **產生合成測試資料**  
    執行以下指令後，將建立 `stress_test_data` 目錄，內含多個檔案與不同風險等級的合成憑證樣本。
    `python generate_test_data.py`
    
2. **執行掃描測試**  
    啟動 CodeSentry，選擇 `stress_test_data` 作為掃描目標，以觀察模型在不同風險層級下的分類行為。
---
## 模型訓練與自訂

本專案提供完整的模型重新訓練流程。
### 1. 產生訓練資料

`python data_generator.py`

> 所有訓練資料皆為隨機合成字串，不包含任何真實或有效的憑證。
### 2. 訓練模型
`python model.py`
如需調整特徵提取邏輯（例如熵值計算或前綴規則），請修改 `main_function/utils.py` 後重新訓練。模型將輸出為 `ML/xgb_model.json`。

---
## 專案結構

```text
    Secret-Hunter/
    ├── main.py                     # Application entry point (PyQt6 GUI)
    ├── checkingFile/
    │   ├── generate_test_data.py   # Script for generating dummy test files
    ├── main_function/
    │   ├── detector.py             # ML Inference logic
    │   └── utils.py                # Feature extraction
    ├── resources/
    │   ├── languages.py            # Localization (English/Chinese)
    │   └── styles.py               # QSS Stylesheets
    ├── ML/
    │   ├── model.py                # Training script
    │   └── data_generator.py       # generate training data
    │   └── xgb_model.json          # Trained Model
    └── requirements.txt            # Dependencies
```

---
## 未來規劃
- CI/CD 整合（GitHub Actions / GitLab CI）
- 誤報回饋與模型再訓練機制
- SARIF 格式輸出以利整合 SonarQube、DefectDojo
---
## 安全聲明與法律免責

本工具僅用於防禦性安全分析、教育用途及經授權的測試環境。  
所有資料集均為合成內容，不對應任何實際服務或有效憑證。
本專案依 MIT License 以「按原樣」提供，不附任何擔保。使用者須自行確保其使用方式符合相關法律與規範。