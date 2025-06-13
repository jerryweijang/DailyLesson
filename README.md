# AI Daily Lesson MVP — C# 版

本專案會每日自動抓取教育部 K-12 七年級教材，呼叫 GPT-4o 產生現代語譯、重點字詞、素養題，並輸出 JSON 至 GitHub Pages。

## 專案結構

```
/ (repo root)
├─ DailyLesson.csproj      # SDK‑style 專案
├─ Program.cs              # 主程式
├─ /docs                   # GitHub Pages 產出 (output JSON)
├─ .github/workflows/
│   └─ schedule.yml        # 每日觸發
└─ README.md
```

## 快速開始

1. `dotnet restore`
2. 設定 `OPENAI_API_KEY` 環境變數
3. `dotnet run`

## 自動化
- 每日 06:00 (台北) 由 GitHub Actions 產生新課文 JSON
- 結果存於 `/docs/YYYY-MM-DD.json`，可直接訂閱

---

詳細規格請見 `spec.md`。
