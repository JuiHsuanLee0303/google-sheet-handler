from typing import List, Any
from .sheet_management import SheetManagementService
from ..utils.logger import logger
from ..utils.exceptions import ValidationError

class DataValidationService(SheetManagementService):
    """Service class for data validation with enhanced error handling"""
    
    def validate_data(self, data: List[Any], headers: List[str]) -> None:
        """Validate data against headers"""
        if not isinstance(data, list):
            raise ValidationError("Data must be a list")
        
        if len(data) != len(headers):
            raise ValidationError(
                f"Data length ({len(data)}) does not match headers length ({len(headers)})"
            )
    
    async def batch_append_data(
        self,
        spreadsheet_id: str,
        data_rows: List[List[Any]],
        sheet_name: str = 'Sheet1'
    ) -> None:
        """Batch append multiple rows of data asynchronously"""
        headers = await self.get_headers(spreadsheet_id, sheet_name)
        
        for row in data_rows:
            self.validate_data(row, headers)
        
        # 使用批量寫入來提高效率
        body = {
            'values': data_rows,
            'majorDimension': 'ROWS'
        }
        
        try:
            await self.sheets.values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}!A:Z",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logger.info(f"Successfully appended {len(data_rows)} rows")
        except Exception as e:
            logger.error(f"Batch append failed: {e}")
            raise 