import asyncio
from src.services.sheet_management import SheetManagementService
from src.services.run_status import RunStatusService
from src.utils.logger import setup_logger

# Setup logging
logger = setup_logger('examples')

async def main():
    # Initialize services
    sheet_service = SheetManagementService()
    run_status_service = RunStatusService()
    
    try:
        # Use existing spreadsheet ID
        spreadsheet_id = "your-spreadsheet-id"  # Replace with your spreadsheet ID
        
        # Get spreadsheet information
        spreadsheet = await sheet_service.get_spreadsheet(spreadsheet_id)
        logger.info(f"Spreadsheet title: {spreadsheet['properties']['title']}")
        
        # Get all sheet names
        sheet_names = await sheet_service.get_sheet_names(spreadsheet_id)
        logger.info(f"Available sheets: {sheet_names}")
        
        # Create new sheet if needed
        if "RunStatus" not in sheet_names:
            sheet_id = await sheet_service.create_sheet(spreadsheet_id, "RunStatus")
            logger.info(f"Created new sheet with ID: {sheet_id}")
        
        # Update run status in specific sheet
        await run_status_service.update_run_status(
            spreadsheet_id=spreadsheet_id,
            run_id="RUN001",
            status="COMPLETED",
            sheet_name="RunStatus"
        )
        
        # Get run status statistics
        status = await run_status_service.check_run_status(
            spreadsheet_id=spreadsheet_id,
            sheet_name="RunStatus"
        )
        
        logger.info("Run Status Summary:")
        logger.info(f"Total Runs: {status['total']}")
        logger.info(f"Completed: {status['completed']}")
        logger.info(f"Failed: {status['failed']}")
        logger.info(f"Pending: {status['pending']}")
        logger.info(f"Completion Rate: {status['completion_rate']:.2f}%")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 