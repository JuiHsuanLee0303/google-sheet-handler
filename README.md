# Google Sheet Handler

[繁體中文](README_zh_TW.md)

A Python library for handling Google Sheets operations with async support, retry mechanism, and comprehensive error handling.

## Features

- Asynchronous operation support
- Automatic retry mechanism
- Comprehensive error handling
- Logging system
- Data validation
- Run status management
- Support for both existing and new spreadsheets

## Installation

```bash
pip install -e .
```

## Configuration

1. Create a Google Cloud project and enable Google Sheets API

2. Create a service account and download credentials:

   - Visit [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable Google Sheets API
   - Create a service account
   - Download the JSON format credentials file

3. Set up credentials:

   ```bash
   # Create credentials directory
   mkdir credentials

   # Move and rename the downloaded credentials file
   mv path/to/downloaded-credentials.json credentials/service-account.json
   ```

4. Configuration file:

   ```bash
   # Copy example configuration file
   cp config/config.yaml.example config/config.yaml

   # Edit configuration file
   vim config/config.yaml
   ```

## Usage Examples

### Creating a New Spreadsheet

```python
from src.services.sheet_management import SheetManagementService
import asyncio

async def main():
    # Initialize service
    sheet_service = SheetManagementService()

    # Create new spreadsheet
    spreadsheet_id = await sheet_service.create_spreadsheet("My Test Sheet")

    # Get headers
    headers = await sheet_service.get_headers(spreadsheet_id)
    print(f"Headers: {headers}")

    # Update cell
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

### Using an Existing Spreadsheet

```python
from src.services.sheet_management import SheetManagementService
import asyncio

async def main():
    sheet_service = SheetManagementService()

    # Use existing spreadsheet ID
    spreadsheet_id = "your-spreadsheet-id"

    # Get all sheet names
    sheet_names = await sheet_service.get_sheet_names(spreadsheet_id)
    print(f"Available sheets: {sheet_names}")

    # Create new sheet if needed
    if "NewSheet" not in sheet_names:
        sheet_id = await sheet_service.create_sheet(spreadsheet_id, "NewSheet")
        print(f"Created new sheet with ID: {sheet_id}")

    # Read data from specific sheet
    data = await sheet_service.get_sheet_data(
        spreadsheet_id=spreadsheet_id,
        sheet_name="NewSheet"
    )
    print(f"Sheet data: {data}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Running Tests

Before running tests, ensure:

1. All dependencies are installed: `pip install -e .[dev]`
2. Credentials file is properly set up: `credentials/service-account.json`
3. Configuration file is set up: `config.yaml`

Then run tests:

```bash
pytest
```

## Project Structure

```bash
google-sheet-handler/
├── src/
│   ├── config/          # Configuration management
│   ├── services/        # Core services
│   └── utils/           # Utility classes
├── tests/               # Test files
├── examples/            # Example code
├── config/              # Configuration files
└── credentials/         # Credentials (add manually)
```

## Important Notes

1. Never commit credential files to version control
2. Use environment variables for sensitive information in production
3. Be aware of Google Sheets API usage quotas
4. Ensure proper access permissions when using existing spreadsheets

## License

MIT
