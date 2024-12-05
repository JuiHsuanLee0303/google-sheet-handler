from typing import List, Any, Dict, Optional
from .base_service import BaseGoogleSheetService
from ..utils.retry import retry_on_exception
from ..utils.logger import logger
from ..utils.exceptions import SheetNotFoundError, APIError
from googleapiclient.errors import HttpError

class SheetManagementService(BaseGoogleSheetService):
    """Service class for managing Google Sheets with enhanced functionality"""
    
    @retry_on_exception(exceptions=(HttpError,))
    async def get_spreadsheet(self, spreadsheet_id: str) -> Dict[str, Any]:
        """Get existing spreadsheet information"""
        try:
            request = self.sheets.get(spreadsheetId=spreadsheet_id)
            response = await self._async_execute(request)
            logger.info(f"Retrieved spreadsheet with ID: {spreadsheet_id}")
            return response
        except Exception as e:
            logger.error(f"Failed to get spreadsheet: {e}")
            raise APIError(f"Spreadsheet retrieval failed: {e}")
    
    @retry_on_exception(exceptions=(HttpError,))
    async def get_sheet_names(self, spreadsheet_id: str) -> List[str]:
        """Get all sheet names in the spreadsheet"""
        try:
            spreadsheet = await self.get_spreadsheet(spreadsheet_id)
            sheet_names = [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
            logger.info(f"Retrieved sheet names: {sheet_names}")
            return sheet_names
        except Exception as e:
            logger.error(f"Failed to get sheet names: {e}")
            raise APIError(f"Sheet names retrieval failed: {e}")
    
    @retry_on_exception(exceptions=(HttpError,))
    async def create_sheet(self, spreadsheet_id: str, sheet_name: str) -> int:
        """Create a new sheet in the existing spreadsheet"""
        try:
            request = self.sheets.batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': sheet_name
                            }
                        }
                    }]
                }
            )
            response = await self._async_execute(request)
            sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
            logger.info(f"Created new sheet '{sheet_name}' with ID: {sheet_id}")
            return sheet_id
        except Exception as e:
            logger.error(f"Failed to create sheet: {e}")
            raise APIError(f"Sheet creation failed: {e}")
    
    @retry_on_exception(exceptions=(HttpError,))
    async def create_spreadsheet(self, title: str) -> str:
        """Create a new spreadsheet"""
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            request = self.sheets.create(body=spreadsheet)
            response = await self._async_execute(request)
            spreadsheet_id = response['spreadsheetId']
            logger.info(f"Created spreadsheet: {title} with ID: {spreadsheet_id}")
            return spreadsheet_id
        except Exception as e:
            logger.error(f"Failed to create spreadsheet: {e}")
            raise APIError(f"Spreadsheet creation failed: {e}")

    @retry_on_exception(exceptions=(HttpError,))
    async def get_headers(self, spreadsheet_id: str, sheet_name: str = 'Sheet1') -> List[str]:
        """Get headers from the first row"""
        try:
            range_name = f"{sheet_name}!A1:Z1"
            request = self.sheets.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            )
            result = await self._async_execute(request)
            
            values = result.get('values', [])
            if not values:
                raise SheetNotFoundError(f"No headers found in sheet: {sheet_name}")
                
            return values[0]
        except HttpError as e:
            logger.error(f"Failed to get headers: {e}")
            raise APIError(f"Header retrieval failed: {e}")

    @retry_on_exception(exceptions=(HttpError,))
    async def update_cell(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        row: int,
        col: int,
        value: Any
    ) -> None:
        """Update a single cell value"""
        try:
            range_name = f"{sheet_name}!{self._get_column_letter(col)}{row}"
            body = {
                'values': [[value]]
            }
            request = self.sheets.values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            )
            await self._async_execute(request)
            logger.info(f"Updated cell {range_name} with value: {value}")
        except Exception as e:
            logger.error(f"Failed to update cell: {e}")
            raise APIError(f"Cell update failed: {e}")

    @retry_on_exception(exceptions=(HttpError,))
    async def get_sheet_data(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        start_row: int = 1,
        end_row: Optional[int] = None
    ) -> List[List[Any]]:
        """Get sheet data with optional row range"""
        try:
            if end_row:
                range_name = f"{sheet_name}!A{start_row}:Z{end_row}"
            else:
                range_name = f"{sheet_name}!A{start_row}:Z"
            
            request = self.sheets.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            )
            result = await self._async_execute(request)
            return result.get('values', [])
        except Exception as e:
            logger.error(f"Failed to get sheet data: {e}")
            raise APIError(f"Data retrieval failed: {e}")

    def _get_column_letter(self, column: int) -> str:
        """Convert column number to letter (1 = A, 2 = B, etc.)"""
        result = ""
        while column > 0:
            column -= 1
            result = chr(column % 26 + 65) + result
            column //= 26
        return result 