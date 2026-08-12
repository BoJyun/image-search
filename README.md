# Image Search

輸入關鍵字搜尋圖片的小網站，前端串接一個輕量 Python 後端，後端再呼叫 [Unsplash API](https://unsplash.com/developers) 取得搜尋結果。

## 專案結構

```
/
├── index.html          前端頁面
├── run.py               啟動伺服器的進入點
└── api/
    ├── config.py.example  Unsplash Access Key 設定範本
    └── handler.py          路由處理 + 搜尋邏輯
```

## 使用前準備

1. 到 [unsplash.com/developers](https://unsplash.com/developers) 申請一組 **Access Key**
2. 複製 `api/config.py.example` 為 `api/config.py`
3. 把 Key 填入 `api/config.py`：
   ```python
   UNSPLASH_ACCESS_KEY = '你的Access_Key'
   ```

`api/config.py` 已加入 `.gitignore`，不會被提交，Key 不會外流。

## 啟動方式

```
python run.py
```

啟動後開啟 http://localhost:8000

## 技術細節

後端只用 Python 標準庫（`http.server`、`urllib`），不需要另外安裝套件。
