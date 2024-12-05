class GoogleSheetError(Exception):
    """Base exception for Google Sheet operations"""
    pass

class SheetNotFoundError(GoogleSheetError):
    """Raised when sheet is not found"""
    pass

class ValidationError(GoogleSheetError):
    """Raised when data validation fails"""
    pass

class ConfigurationError(GoogleSheetError):
    """Raised when configuration is invalid"""
    pass

class APIError(GoogleSheetError):
    """Raised when Google API request fails"""
    pass 