from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Any, Optional
from ..utils.retry import retry_on_exception
from ..utils.logger import logger
from ..utils.exceptions import APIError
from ..config.settings import settings
import asyncio
from functools import partial

class BaseGoogleSheetService:
    """Base class for Google Sheet operations with retry and logging"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or settings.credentials_path
        self._init_service()
    
    def _init_service(self) -> None:
        """Initialize Google Sheets service with retry"""
        try:
            self.credentials = Credentials.from_service_account_file(self.credentials_path)
            self.service = build('sheets', 'v4', credentials=self.credentials)
            self.sheets = self.service.spreadsheets()
            logger.info("Google Sheets service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize service: {e}")
            raise APIError(f"Service initialization failed: {e}")
    
    @retry_on_exception(exceptions=(HttpError,))
    def read_range(self, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
        """Read data from specified range with retry"""
        try:
            logger.info(f"Reading range {range_name} from spreadsheet {spreadsheet_id}")
            result = self.sheets.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            return result.get('values', [])
        except HttpError as e:
            logger.error(f"Failed to read range: {e}")
            raise APIError(f"Read operation failed: {e}")
    
    async def _async_execute(self, request):
        """Execute Google API request asynchronously"""
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, request.execute)
        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise APIError(f"API request failed: {e}")
