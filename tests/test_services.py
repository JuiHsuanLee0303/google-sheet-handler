import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from src.services.sheet_management import SheetManagementService
from src.services.run_status import RunStatusService
from src.services.data_validation import DataValidationService
from src.utils.exceptions import ValidationError, SheetNotFoundError
from src.config.settings import settings

# 使用真实的 credentials
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'service-account.json')

# 测试用的表头和默认值
TEST_HEADERS = [['RUN', 'STATUS', 'TIMESTAMP']]
DEFAULT_SHEET_NAME = 'Sheet1'

@pytest.fixture
def sheet_service():
    return SheetManagementService(CREDENTIALS_PATH)

@pytest.fixture
def run_status_service():
    return RunStatusService(CREDENTIALS_PATH)

@pytest.fixture
def data_validation_service():
    return DataValidationService(CREDENTIALS_PATH)

async def initialize_sheet(service, spreadsheet_id, include_test_data=False):
    """初始化表格，添加表头和测试数据"""
    # 添加表头
    range_name = f'{DEFAULT_SHEET_NAME}!A1:C1'
    request = service.sheets.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body={'values': TEST_HEADERS}
    )
    await service._async_execute(request)
    
    # 如果需要，添加测试数据
    if include_test_data:
        test_data = [
            ['RUN001', 'PENDING', ''],
            ['RUN002', 'PENDING', ''],
            ['RUN003', 'PENDING', ''],
            ['TEST001', 'PENDING', '']
        ]
        range_name = f'{DEFAULT_SHEET_NAME}!A2:C5'
        request = service.sheets.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body={'values': test_data}
        )
        await service._async_execute(request)

class TestSheetManagementService:
    @pytest.mark.asyncio
    async def test_create_spreadsheet(self, sheet_service):
        # 创建新的 spreadsheet
        title = "Test Sheet"
        spreadsheet_id = await sheet_service.create_spreadsheet(title)
        assert spreadsheet_id is not None
        assert isinstance(spreadsheet_id, str)

    @pytest.mark.asyncio
    async def test_get_headers(self, sheet_service):
        # 首先创建一个测试表格
        spreadsheet_id = await sheet_service.create_spreadsheet("Test Headers")
        
        # 初始化表头
        await initialize_sheet(sheet_service, spreadsheet_id)
        
        # 获取表头
        headers = await sheet_service.get_headers(spreadsheet_id, DEFAULT_SHEET_NAME)
        assert isinstance(headers, list)
        assert headers == TEST_HEADERS[0]

    @pytest.mark.asyncio
    async def test_get_headers_empty(self, sheet_service):
        # 创建一个新的空表格
        spreadsheet_id = await sheet_service.create_spreadsheet("Test Empty Headers")
        
        with pytest.raises(SheetNotFoundError):
            await sheet_service.get_headers(spreadsheet_id, DEFAULT_SHEET_NAME)

class TestRunStatusService:
    @pytest.mark.asyncio
    async def test_check_run_status(self, run_status_service):
        # 创建测试表格并添加测试数据
        spreadsheet_id = await run_status_service.create_spreadsheet("Test Run Status")
        
        # 初始化表头和测试数据
        await initialize_sheet(run_status_service, spreadsheet_id, include_test_data=True)
        
        # 更新一些测试状态
        await run_status_service.update_run_status(spreadsheet_id, "RUN001", "COMPLETED", DEFAULT_SHEET_NAME)
        await run_status_service.update_run_status(spreadsheet_id, "RUN002", "FAILED", DEFAULT_SHEET_NAME)
        
        # 检查状态
        status = await run_status_service.check_run_status(spreadsheet_id, DEFAULT_SHEET_NAME)
        assert status['total'] >= 3
        assert status['completed'] >= 1
        assert status['failed'] >= 1
        assert status['pending'] >= 1

    @pytest.mark.asyncio
    async def test_update_run_status(self, run_status_service):
        # 创建测试表格
        spreadsheet_id = await run_status_service.create_spreadsheet("Test Status Update")
        
        # 初始化表头和测试数据
        await initialize_sheet(run_status_service, spreadsheet_id, include_test_data=True)
        
        # 更新状态
        run_id = "TEST001"
        await run_status_service.update_run_status(spreadsheet_id, run_id, "COMPLETED", DEFAULT_SHEET_NAME)
        
        # 验证更新
        data = await run_status_service.get_sheet_data(spreadsheet_id, DEFAULT_SHEET_NAME)
        assert len(data) > 0
        assert data[0] == TEST_HEADERS[0]  # 验证表头
        
        # 找到并验证更新的行
        updated_row = next((row for row in data if row[0] == run_id), None)
        assert updated_row is not None
        assert updated_row[1] == "COMPLETED"

class TestDataValidationService:
    def test_validate_data(self, data_validation_service):
        # Valid data
        service = data_validation_service
        service.validate_data(['1', 'test'], ['col1', 'col2'])
        
        # Invalid data length
        with pytest.raises(ValidationError):
            service.validate_data(['1'], ['col1', 'col2'])
        
        # Invalid data type
        with pytest.raises(ValidationError):
            service.validate_data('not a list', ['col1'])