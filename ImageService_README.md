# ImageService 實作說明

本檔案說明新增的 ImageService 功能，實現了根據 `ImageService.instructions.md` 規範的教育圖像生成服務。

## 功能概述

ImageService 為現有的每日課程系統新增了圖像生成功能：

1. **自動圖像生成** - 使用 GitHub Models API (DALL-E 3) 為課程內容生成相關圖像
2. **多科目支援** - 針對自然、國文、歷史、地理、公民等科目提供專門的圖像風格
3. **JSON 輸出** - 生成包含圖像 URL 的結構化資料
4. **向後兼容** - 保持原有 HTML 重定向功能不變

## 檔案結構

```
├── image_service.py              # 圖像生成服務類別
├── main_with_images.py          # 整合腳本（課程抓取 + 圖像生成）
├── demo.py                      # 演示腳本
├── requirements.txt             # Python 依賴套件
└── .github/workflows/
    └── daily-lesson-with-images.yml  # GitHub Actions 工作流程
```

## 使用方式

### 1. 本地測試

```bash
# 安裝依賴
pip install -r requirements.txt

# 執行演示
python demo.py

# 執行完整流程（需要 GITHUB_TOKEN 環境變數）
python main_with_images.py
```

### 2. GitHub Actions 自動執行

1. 在 GitHub Repository Settings > Secrets 中設定 `GITHUB_TOKEN`
2. 啟用 `daily-lesson-with-images.yml` 工作流程
3. 系統每日自動執行，生成包含圖像的課程內容

## 輸出格式

### JSON 格式 (新增)
```json
{
  "date": "2025-07-04",
  "lessons": [
    {
      "id": "civics_1",
      "subject": "公民",
      "title": "【1-1】個人與社會",
      "content": "探討個人在社會中的角色與責任",
      "source_url": "https://www.learnmode.net/course/638741/content",
      "image_url": "https://example.com/generated-image.jpg",
      "image_generated_at": "2025-07-04T09:37:26.943962"
    }
  ],
  "generated_at": "2025-07-04T09:37:26.944126"
}
```

### HTML 格式 (保持不變)
原有的 HTML 重定向功能完全保留，確保向後兼容性。

## 技術特點

1. **智能提示詞生成** - 根據不同科目生成適合的圖像提示詞
2. **錯誤處理** - 完整的錯誤處理和日誌記錄
3. **速率限制** - 避免 API 使用超限
4. **非同步支援** - 支援批量圖像生成
5. **模組化設計** - 可獨立使用或整合到現有系統

## 演示輸出

執行 `python demo.py` 可看到完整的功能演示，包括：

- 每日課程選擇算法
- 圖像生成流程
- JSON 輸出格式
- HTML 兼容性

## 部署注意事項

1. **GitHub Token** - 需要具備 GitHub Models 存取權限的 PAT
2. **API 使用量** - 監控 DALL-E 3 API 使用量避免超限
3. **圖像儲存** - 生成的圖像 URL 有時效性，建議定期備份
4. **中文支援** - 所有檔案使用 UTF-8 編碼確保中文正常顯示

## 維護

- 定期更新依賴套件版本
- 監控 API 使用狀況
- 根據需要調整圖像生成提示詞
- 檢查生成圖像的品質和適用性