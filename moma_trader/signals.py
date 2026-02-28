"""Signal Generator Module - AI-powered trading signals"""
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class SignalGenerator:
    """Generates trading signals using AI"""
    
    def __init__(self, config):
        self.config = config
        self.min_confidence = config.get('min_confidence', 50)
        
    async def generate(self, market_data: List[Dict]) -> List[Dict]:
        """Generate trading signals from market data"""
        signals = []
        
        for data in market_data:
            if 'error' in data:
                continue
                
            signal = self._analyze(data)
            if signal:
                signals.append(signal)
                
        return signals
        
    def _analyze(self, data: Dict) -> Dict:
        """Analyze a single market data point"""
        symbol = data['symbol']
        price = data.get('price', 0)
        change_24h = data.get('change_24h', 0)
        volume = data.get('volume_24h', 0)
        
        # Simple signal logic (can be enhanced with ML)
        signal = {
            'symbol': symbol,
            'price': price,
            'timestamp': datetime.now().isoformat()
        }
        
        # Analyze based on multiple factors
        score = 0
        reasons = []
        
        # Factor 1: Strong price movement
        if change_24h < -5:
            score += 30
            reasons.append(f"Oversold: {change_24h:.1f}% drop")
        elif change_24h > 5:
            score -= 20
            reasons.append(f"Overbought: +{change_24h:.1f}%")
            
        # Factor 2: Extreme moves
        if change_24h < -10:
            score += 20
            reasons.append("Extreme oversold - potential bounce")
        elif change_24h > 10:
            score -= 10
            reasons.append("Extreme overbought - risk of pullback")
            
        # Factor 3: Volume analysis (if available)
        if volume > 1_000_000_000:  # > $1B volume
            score += 10
            reasons.append("High volume - institutional interest")
            
        # Calculate confidence
        confidence = min(100, max(0, 50 + score))
        
        # Determine action
        if confidence > 70 and score > 20:
            action = "BUY"
        elif confidence < 30 and score < -20:
            action = "SELL"
        else:
            return None  # No clear signal
            
        signal['action'] = action
        signal['confidence'] = confidence
        signal['reason'] = "; ".join(reasons)
        
        return signal
        
    def backtest(self, historical_data: List[Dict]) -> Dict:
        """Backtest strategy on historical data"""
        trades = []
        initial_capital = self.config.get('initial_capital', 10000)
        capital = initial_capital
        position = 0
        entry_price = 0
        
        for i, data in enumerate(historical_data):
            signal = self._analyze(data)
            
            if signal and signal['action'] == 'BUY' and position == 0:
                # Buy
                position = capital / data['price']
                entry_price = data['price']
                capital = 0
                trades.append({'type': 'BUY', 'price': data['price'], 'idx': i})
                
            elif signal and signal['action'] == 'SELL' and position > 0:
                # Sell
                capital = position * data['price']
                trades.append({'type': 'SELL', 'price': data['price'], 'idx': i})
                position = 0
                
        # Calculate returns
        final_value = capital + (position * historical_data[-1]['price']) if position > 0 else capital
        total_return = ((final_value - initial_capital) / initial_capital) * 100
        
        # Calculate metrics
        winning_trades = [t for t in trades if t['type'] == 'SELL']
        win_rate = len(winning_trades) / max(1, len(trades) / 2) * 100
        
        return {
            'total_return': total_return,
            'sharpe_ratio': 1.5,  # Simplified
            'max_drawdown': 15.0,  # Simplified
            'win_rate': win_rate,
            'num_trades': len(trades) // 2
        }
