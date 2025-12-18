# resources/languages.py

class LanguageManager:
    """
    Manages the application's localization dictionaries.
    Allows switching between Traditional Chinese and English.
    """
    
    # Default language setting
    current_lang = "zh_TW"
    
    TEXTS = {
        "zh_TW": {
            "app_title": "Secret Hunter - 敏感資訊掃描工具",
            "select_folder": "選擇資料夾",
            "start_scan": "開始掃描",
            "stop_scan": "停止掃描",
            "export_report": "匯出報告",
            "scanning": "掃描中...",
            "ready": "準備就緒",
            "scan_complete": "掃描完成",
            "scan_stopped": "掃描已取消",
            "no_folder": "尚未選擇資料夾",
            "no_data": "沒有可匯出的資料",
            "export_success": "匯出成功",
            "export_success_msg": "報告已儲存至：\n{}",
            "export_error": "匯出失敗",
            "model_loaded": "模型已載入",
            "model_failed": "模型載入失敗",
            "tab_all": "全部紀錄",
            "tab_critical": "嚴重 (Critical)",
            "tab_high": "高風險 (High)",
            "tab_medium": "中風險 (Medium)",
            "tab_low": "低風險 (Low)",
            "col_risk": "風險等級",
            "col_file": "檔案名稱",
            "col_line": "行號",
            "col_content": "發現內容 (已遮蔽)",
            "col_score": "信賴度",
            "col_time": "時間",
            "stat_label": "此類別共有 {} 筆發現",
            "lang_en": "English",
            "lang_zh": "繁體中文"
        },
        "en_US": {
            "app_title": "Secret Hunter - Sensitive Data Scanner",
            "select_folder": "Select Folder",
            "start_scan": "Start Scan",
            "stop_scan": "Stop Scan",
            "export_report": "Export Report",
            "scanning": "Scanning...",
            "ready": "Ready",
            "scan_complete": "Scan Complete",
            "scan_stopped": "Scan Canceled",
            "no_folder": "No folder selected",
            "no_data": "No data to export",
            "export_success": "Export Successful",
            "export_success_msg": "Report saved to:\n{}",
            "export_error": "Export Failed",
            "model_loaded": "Model Loaded",
            "model_failed": "Model Failed",
            "tab_all": "All Logs",
            "tab_critical": "Critical",
            "tab_high": "High Risk",
            "tab_medium": "Medium Risk",
            "tab_low": "Low Risk",
            "col_risk": "Risk Level",
            "col_file": "File Name",
            "col_line": "Line",
            "col_content": "Content (Masked)",
            "col_score": "Confidence",
            "col_time": "Time",
            "stat_label": "Found {} items in this category",
            "lang_en": "English",
            "lang_zh": "Traditional Chinese"
        }
    }

    @classmethod
    def get(cls, key):
        """Retrieves the translation for the given key based on current_lang."""
        return cls.TEXTS[cls.current_lang].get(key, key)