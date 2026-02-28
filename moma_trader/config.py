"""Configuration Module"""
import yaml
from typing import Any


class Config:
    """Configuration manager"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self._config = {}
        self._load()
        
    def _load(self):
        """Load config from file"""
        try:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            self._config = self._default()
            
    def _default(self) -> dict:
        """Default configuration"""
        return {
            'exchange': 'binance',
            'testnet': True,
            'initial_capital': 1000,
            'max_position_size': 0.1,
            'stop_loss': 0.05,
            'min_confidence': 50,
            'scan_interval': 3600,
            'watchlist': [
                'BTC/USDT', 'ETH/USDT', 'SOL/USDT',
                'BNB/USDT', 'XRP/USDT', 'ADA/USDT'
            ],
            'telegram_enabled': False,
            'telegram_token': '',
            'telegram_chat_id': ''
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        return self._config.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set config value"""
        self._config[key] = value
        
    def save(self):
        """Save config to file"""
        with open(self.config_path, 'w') as f:
            yaml.dump(self._config, f)
