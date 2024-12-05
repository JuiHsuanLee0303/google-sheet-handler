import os
import yaml
from typing import Dict, Any
from pathlib import Path

class Settings:
    """Configuration settings manager"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.getenv('CONFIG_PATH', 'config/config.yaml')
        self.config: Dict[str, Any] = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Failed to load config: {e}")
    
    @property
    def credentials_path(self) -> str:
        return os.getenv('GOOGLE_CREDENTIALS_PATH') or self.config.get('credentials_path')
    
    @property
    def default_spreadsheet_id(self) -> str:
        return os.getenv('DEFAULT_SPREADSHEET_ID') or self.config.get('spreadsheet_id')
    
    @property
    def retry_config(self) -> Dict[str, Any]:
        return self.config.get('retry', {
            'max_attempts': 3,
            'delay': 1,
            'backoff': 2
        })

settings = Settings() 