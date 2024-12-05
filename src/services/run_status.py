from typing import List, Dict, Any, Optional
from datetime import datetime
from .sheet_management import SheetManagementService
from ..utils.logger import logger
from ..utils.exceptions import ValidationError

class RunStatusService(SheetManagementService):
    """Service class for handling run status operations"""
    
    async def check_run_status(
        self,
        spreadsheet_id: str,
        sheet_name: str = 'Sheet1',
        run_column: str = 'RUN',
        status_column: str = 'STATUS'
    ) -> Dict[str, Any]:
        """Check run status from specified columns"""
        try:
            headers = await self.get_headers(spreadsheet_id, sheet_name)
            
            # Get column indices
            run_index = headers.index(run_column)
            status_index = headers.index(status_column)
            
            # Get all data
            data = await self.get_sheet_data(spreadsheet_id, sheet_name)
            
            # Skip header row
            data = data[1:] if len(data) > 1 else []
            
            # Process status
            total_runs = len(data)
            completed = sum(1 for row in data if row[status_index].upper() == 'COMPLETED')
            failed = sum(1 for row in data if row[status_index].upper() == 'FAILED')
            pending = total_runs - completed - failed
            
            status_summary = {
                'total': total_runs,
                'completed': completed,
                'failed': failed,
                'pending': pending,
                'completion_rate': (completed / total_runs * 100) if total_runs > 0 else 0
            }
            
            logger.info(f"Run status summary: {status_summary}")
            return status_summary
            
        except ValueError as e:
            logger.error(f"Column not found: {e}")
            raise ValidationError(f"Invalid column name: {e}")
        except Exception as e:
            logger.error(f"Failed to check run status: {e}")
            raise

    async def update_run_status(
        self,
        spreadsheet_id: str,
        run_id: str,
        status: str,
        sheet_name: str = 'Sheet1',
        run_column: str = 'RUN',
        status_column: str = 'STATUS',
        timestamp_column: Optional[str] = 'TIMESTAMP'
    ) -> None:
        """Update status for a specific run ID"""
        try:
            headers = await self.get_headers(spreadsheet_id, sheet_name)
            data = await self.get_sheet_data(spreadsheet_id, sheet_name)
            
            # Get column indices
            run_index = headers.index(run_column)
            status_index = headers.index(status_column)
            timestamp_index = headers.index(timestamp_column) if timestamp_column in headers else None
            
            # Find row with matching run ID
            for row_num, row in enumerate(data[1:], start=2):
                if row[run_index] == run_id:
                    # Update status
                    await self.update_cell(
                        spreadsheet_id,
                        sheet_name,
                        row_num,
                        status_index + 1,
                        status
                    )
                    
                    # Update timestamp if column exists
                    if timestamp_index is not None:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        await self.update_cell(
                            spreadsheet_id,
                            sheet_name,
                            row_num,
                            timestamp_index + 1,
                            current_time
                        )
                    
                    logger.info(f"Updated run {run_id} status to {status}")
                    return
                    
            raise ValidationError(f"Run ID {run_id} not found")
            
        except ValueError as e:
            logger.error(f"Column not found: {e}")
            raise ValidationError(f"Invalid column name: {e}")
        except Exception as e:
            logger.error(f"Failed to update run status: {e}")
            raise 