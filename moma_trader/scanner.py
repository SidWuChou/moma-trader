"""Market Scanner Module"""
import logging
import asyncio
import aiohttp
from typing import Dict, List

logger = logging.getLogger(__name__)


class MarketScanner:
    """Scans market for trading opportunities"""
    
    def __init__(self, config):
        self.config = config
        self.watchlist = config.get('watchlist', [
            'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 
            'BNB/USDT', 'XRP/USDT', 'ADA/USDT',
            'DOGE/USDT', 'AVAX/USDT', 'DOT/USDT'
        ])
        
    async def scan_all(self) -> List[Dict]:
        """Scan all watchlist symbols"""
        results = []
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.scan_symbol(session, symbol) for symbol in self.watchlist]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        # Filter out errors
        return [r for r in results if isinstance(r, dict)]
        
    async def scan_symbol(self, session, symbol: str) -> Dict:
        """Scan a single symbol"""
        try:
            # Get price data (using CoinGecko free API)
            base, quote = symbol.split('/')
            coin_id = self._get_coin_id(base)
            
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true'
            }
            
            async with session.get(url, params=params, timeout=10) as resp:
                data = await resp.json()
                
            if coin_id in data:
                coin_data = data[coin_id]
                return {
                    'symbol': symbol,
                    'price': coin_data.get('usd', 0),
                    'change_24h': coin_data.get('usd_24h_change', 0),
                    'volume_24h': coin_data.get('usd_24h_vol', 0),
                    'timestamp': asyncio.get_event_loop().time()
                }
                
        except Exception as e:
            logger.warning(f"Failed to scan {symbol}: {e}")
            
        return {'symbol': symbol, 'error': str(e)}
        
    def _get_coin_id(self, symbol: str) -> str:
        """Map symbol to CoinGecko ID"""
        mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'SOL': 'solana',
            'BNB': 'binancecoin',
            'XRP': 'ripple',
            'ADA': 'cardano',
            'DOGE': 'dogecoin',
            'AVAX': 'avalanche-2',
            'DOT': 'polkadot',
            'MATIC': 'matic-network',
            'LINK': 'chainlink',
            'UNI': 'uniswap'
        }
        return mapping.get(symbol.upper(), symbol.lower())
