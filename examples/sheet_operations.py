import asyncio
import logging
from src.services.run_status import RunStatusService
from src.services.data_validation import DataValidationService
from src.utils.logger import setup_logger

# Setup logging
logger = setup_logger('examples')

async def main():
    # Initialize services
    run_status_service = RunStatusService()
    data_validation_service = DataValidationService()
    
    try:
        # Create a new spreadsheet
        spreadsheet_id = await run_status_service.create_spreadsheet('Test Run Status')
        logger.info(f"Created spreadsheet with ID: {spreadsheet_id}")
        
        # Prepare test data
        test_data = [
            ['RUN', 'STATUS', 'TIMESTAMP'],  # Headers
            ['RUN001', 'PENDING', ''],
            ['RUN002', 'PENDING', ''],
            ['RUN003', 'PENDING', '']
        ]
        
        # Append data
        await data_validation_service.batch_append_data(
            spreadsheet_id=spreadsheet_id,
            data_rows=test_data[1:],  # Skip headers
            sheet_name='Sheet1'
        )
        
        # Update status for some runs
        await run_status_service.update_run_status(
            spreadsheet_id=spreadsheet_id,
            run_id='RUN001',
            status='COMPLETED'
        )
        
        await run_status_service.update_run_status(
            spreadsheet_id=spreadsheet_id,
            run_id='RUN002',
            status='FAILED'
        )
        
        # Check run status
        status_summary = await run_status_service.check_run_status(
            spreadsheet_id=spreadsheet_id
        )
        
        logger.info("Run Status Summary:")
        logger.info(f"Total Runs: {status_summary['total']}")
        logger.info(f"Completed: {status_summary['completed']}")
        logger.info(f"Failed: {status_summary['failed']}")
        logger.info(f"Pending: {status_summary['pending']}")
        logger.info(f"Completion Rate: {status_summary['completion_rate']:.2f}%")
        
    except Exception as e:
        logger.error(f"Error in example: {e}")
        raise

if __name__ == '__main__':
    asyncio.run(main()) 