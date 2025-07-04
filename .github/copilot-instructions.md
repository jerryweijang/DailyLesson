# GitHub Copilot 指令

這是一個自動化的台灣國中教育內容網站，每日抓取課程標題並產生學習連結到 GitHub Pages。

## 專案架構

**核心工作流程**：
1. `fetch_lesson_titles.py` - 使用 Selenium 抓取五大科目課程標題
2. GitHub Actions 每日執行 (`link-only.yml`) - 台北時間 06:00 (UTC 22:00)
3. 輸出 HTML 重定向檔案到 `docs/` 供 GitHub Pages 使用

**重要：專案實際使用 Python，而非 README 提到的 C#**

## 資料擷取模式

使用學科特定的篩選器從 learnmode.net 抓取內容：
```python
subjects = [
    {'name': '自然', 'filter': filter_nature},    # 【數字-數字】格式
    {'name': '國文', 'filter': filter_chinese},   # 含【】符號
    {'name': '歷史', 'filter': filter_history},   # 【數字-數字】格式
    # ... 其他科目
]
```

每個科目有固定的課程 URL 和 CSS 選擇器 `h3.chapter-name`。

## 自動化工作流程

**日選算法**：使用一年中的第幾天 (`date +%j`) 模除總課程數，確保每日不同內容且年度循環：
```bash
day_of_year=$(TZ=Asia/Taipei date +%j)
day_idx=$(( (10#$day_of_year - 1) % total ))
```

**輸出格式**：生成 `docs/YYYY-MM-DD.html` 重定向到 Perplexity AI 搜尋，包含台灣教育格式的提示詞。

## 關鍵檔案結構

- `fetch_lesson_titles.py` - 資料擷取邏輯
- `.github/workflows/link-only.yml` - 自動化流程
- `docs/index.html` - 智慧重定向到最新課程（使用 JavaScript 回溯查找）
- `docs/YYYY-MM-DD.html` - 每日課程重定向頁面

## 開發約定

**Selenium 設定**：使用 headless Chrome，包含 `--no-sandbox` 和 `--disable-dev-shm-usage` 參數以支援 CI 環境。

**時區處理**：所有日期計算使用 `TZ=Asia/Taipei` 確保台灣時區一致性。

**錯誤處理**：GitHub Actions 包含 fallback 機制，若 HTTP 請求失敗則生成靜態重定向頁面。

**命名規範**：
- 科目名稱使用繁體中文（自然、國文、歷史、地理、公民）
- 檔案輸出使用 ISO 日期格式 (`YYYY-MM-DD`)
- Git 提交訊息格式：`docs: add lesson link YYYY-MM-DD`

## 環境需求

- Python 3.x + Selenium + BeautifulSoup4
- Chrome/Chromium 瀏覽器（CI 環境）
- GitHub Token 用於自動 commit 和 push

**注意**：此專案不使用 OpenAI API，而是生成到 Perplexity AI 的重定向連結。
