# Google Sheet Handler

一个用于处理 Google Sheets 操作的 Python 库，提供了异步操作、重试机制和完整的错误处理。

## 功能特点

- 异步操作支持
- 自动重试机制
- 完整的错误处理
- 日志记录
- 数据验证
- 运行状态管理
- 支持现有和新建 spreadsheet

## 安装

```bash
pip install -e .
```

## 配置

1. 创建 Google Cloud 项目并启用 Google Sheets API

2. 创建服务账号并下载凭证：

   - 访问 [Google Cloud Console](https://console.cloud.google.com)
   - 创建新项目或选择现有项目
   - 启用 Google Sheets API
   - 创建服务账号
   - 下载 JSON 格式的凭证文件

3. 设置凭证：

   ```bash
   # 创建凭证目录
   mkdir credentials

   # 将下载的凭证文件重命名并移动到凭证目录
   mv path/to/downloaded-credentials.json credentials/service-account.json
   ```

4. 配置文件：

   ```bash
   # 复制示例配置文件
   cp config/config.yaml.example config/config.yaml

   # 编辑配置文件，设置你的配置
   vim config/config.yaml
   ```

## 使用示例

### 创建新的 Spreadsheet

```python
from src.services.sheet_management import SheetManagementService
import asyncio

async def main():
    # 初始化服务
    sheet_service = SheetManagementService()

    # 创建新的表格
    spreadsheet_id = await sheet_service.create_spreadsheet("My Test Sheet")

    # 获取表头
    headers = await sheet_service.get_headers(spreadsheet_id)
    print(f"Headers: {headers}")

    # 更新单元格
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

### 使用现有的 Spreadsheet

```python
from src.services.sheet_management import SheetManagementService
import asyncio

async def main():
    sheet_service = SheetManagementService()

    # 使用现有的 spreadsheet ID
    spreadsheet_id = "your-spreadsheet-id"

    # 获取所有工作表名称
    sheet_names = await sheet_service.get_sheet_names(spreadsheet_id)
    print(f"Available sheets: {sheet_names}")

    # 创建新的工作表
    if "NewSheet" not in sheet_names:
        sheet_id = await sheet_service.create_sheet(spreadsheet_id, "NewSheet")
        print(f"Created new sheet with ID: {sheet_id}")

    # 在特定工作表中读取数据
    data = await sheet_service.get_sheet_data(
        spreadsheet_id=spreadsheet_id,
        sheet_name="NewSheet"
    )
    print(f"Sheet data: {data}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 运行测试

在运行测试之前，确保：

1. 已安装所有依赖：`pip install -e .[dev]`
2. 已正确设置凭证文件：`credentials/service-account.json`
3. 已配置 `config.yaml`

然后运行测试：

```bash
pytest
```

## 项目结构

```bash
google-sheet-handler/
├── src/
│   ├── config/          # 配置管理
│   ├── services/        # 核心服务
│   └── utils/           # 工具类
├── tests/               # 测试文件
├── examples/            # 示例代码
├── config/              # 配置文件
└── credentials/         # 凭证文件（需自行添加）
```

## 注意事项

1. 不要提交凭证文件到版本控制系统
2. 在生产环境中使用时，建议通过环境变量设置敏感信息
3. 注意 Google Sheets API 的使用配额限制
4. 使用现有 spreadsheet 时，确保服务账号有适当的访问权限

## 许可证

MIT
