#!/usr/bin/env python3
"""
下載每日課程 JSON 中的 image_url 圖片到本地指定資料夾
"""
import os
import json
import requests
from pathlib import Path
from datetime import datetime

def download_image(url: str, save_path: Path) -> bool:
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"下載失敗: {url} -> {e}")
        return False

def main():
    # 設定來源 JSON 路徑與圖片儲存資料夾
    date_str = datetime.now().strftime('%Y-%m-%d')
    json_path = Path(f"docs/{date_str}.json")
    image_dir = Path(f"docs/images/{date_str}")
    image_dir.mkdir(parents=True, exist_ok=True)

    if not json_path.exists():
        print(f"找不到 JSON 檔案: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lessons = data.get('lessons', [])
    for lesson in lessons:
        image_url = lesson.get('image_url')
        if not image_url or image_url.startswith('https://example.com/mock-images/'):
            print(f"跳過無效或模擬圖像: {image_url}")
            continue
        # 以課程 id 命名
        file_ext = os.path.splitext(image_url)[-1].split('?')[0] or '.jpg'
        file_name = f"{lesson.get('id', 'lesson')}{file_ext}"
        save_path = image_dir / file_name
        print(f"下載 {image_url} -> {save_path}")
        download_image(image_url, save_path)

if __name__ == "__main__":
    main()
