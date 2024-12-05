# Google Sheet Handler

[English](README.md)

一個用於處理 Google Sheets 操作的 Python 函式庫，提供了非同步操作、重試機制和完整的錯誤處理。

## 功能特點

- 非同步操作支援
- 自動重試機制
- 完整的錯誤處理
- 日誌記錄
- 資料驗證
- 執行狀態管理
- 支援現有和新建試算表

## 安裝

```bash
pip install -e .
```

## 設定

1. 建立 Google Cloud 專案並啟用 Google Sheets API

2. 建立服務帳號並下載憑證：

   - 訪問 [Google Cloud Console](https://console.cloud.google.com)
   - 建立新專案或選擇現有專案
   - 啟用 Google Sheets API
   - 建立服務帳號
   - 下載 JSON 格式的憑證檔案

3. 設定憑證：

   ```bash
   # 建立憑證目錄
   mkdir credentials

   # 將下載的憑證檔案重新命名並移動到憑證目錄
   mv path/to/downloaded-credentials.json credentials/service-account.json
   ```

4. 設定檔：

   ```bash
   # 複製範例設定檔
   cp config/config.yaml.example config/config.yaml

   # 編輯設定檔
   vim config/config.yaml
   ```

## 使用範例

### 建立新的試算表

```python
from src.services.sheet_management import SheetManagementService
import asyncio

async def main():
    # 初始化服務
    sheet_service = SheetManagementService()

    # 建立新的試算表
    spreadsheet_id = await sheet_service.create_spreadsheet("My Test Sheet")

    # 取得標題列
    headers = await sheet_service.get_headers(spreadsheet_id)
    print(f"Headers: {headers}")

    # 更新儲存格
    await sheet_service.update_cell(
        spreadsheet_id=spreadsheet_id,
        sheet_name="Sheet1",
        row=1,
        col=1,
        value="Test"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### 使用現有的試算表

```python
from src.services.sheet_management import SheetManagementService
import asyncio

async def main():
    sheet_service = SheetManagementService()

    # 使用現有的試算表 ID
    spreadsheet_id = "your-spreadsheet-id"

    # 取得所有工作表名稱
    sheet_names = await sheet_service.get_sheet_names(spreadsheet_id)
    print(f"Available sheets: {sheet_names}")

    # 如果需要，建立新的工作表
    if "NewSheet" not in sheet_names:
        sheet_id = await sheet_service.create_sheet(spreadsheet_id, "NewSheet")
        print(f"Created new sheet with ID: {sheet_id}")

    # 從特工作表讀取資料
    data = await sheet_service.get_sheet_data(
        spreadsheet_id=spreadsheet_id,
        sheet_name="NewSheet"
    )
    print(f"Sheet data: {data}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 執行測試

在執行測試之前，請確保：

1. 已安裝所有依賴：`pip install -e .[dev]`
2. 已正確設定憑證檔案：`credentials/service-account.json`
3. 已設定 `config.yaml`

然後執行測試：

```bash
pytest
```

## 專案結構

```bash
google-sheet-handler/
├── src/
│   ├── config/          # 設定管理
│   ├── services/        # 核心服務
│   └── utils/           # 工具類別
├── tests/               # 測試檔案
├── examples/            # 範例程式碼
├── config/              # 設定檔案
└── credentials/         # 憑證（需自行添加）
```

## 重要注意事項

1. 切勿將憑證檔案提交到版本控制系統
2. 在生產環境中使用時，建議透過環境變數設定敏感資訊
3. 注意 Google Sheets API 的使用配額限制
4. 使用現有試算表時，確保服務帳號具有適當的存取權限

## 授權條款

MIT
