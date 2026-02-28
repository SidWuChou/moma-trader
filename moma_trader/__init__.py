#!/usr/bin/env python3
"""
MomaTrader - AI-Powered Trading Bot
Real implementation with working strategies
"""
import requests
import json
import time
from datetime import datetime
from collections import defaultdict

class MomaTrader:
    def __init__(self):
        self.watchlist = ['bitcoin', 'ethereum', 'solana', 'binancecoin', 'ripple', 'cardano', 'dogecoin', 'avalanche-2', 'polkadot', 'matic-network']
        
    def get_prices(self):
        """Get real prices from CoinGecko"""
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'ids': ','.join(self.watchlist),
            'order': 'market_cap_desc',
            'per_page': 20,
            'page': 1,
            'sparkline': 'false',
            'price_change_percentage': '24h'
        }
        try:
            r = requests.get(url, params=params, timeout=15)
            return r.json()
        except Exception as e:
            print(f"Error: {e}")
            return []
            
    def analyze_market(self):
        """Real market analysis with multiple indicators"""
        coins = self.get_prices()
        if not coins:
            return None
            
        analysis = []
        
        for coin in coins:
            price = coin.get('current_price', 0) or 0
            change = coin.get('price_change_percentage_24h', 0) or 0
            vol = coin.get('total_volume', 0) or 0
            cap = coin.get('market_cap', 0) or 0
            symbol = coin.get('symbol', '').upper()
            
            # Technical analysis
            signals = []
            
            # RSI-like: extreme moves
            if change < -10:
                signals.append('DEEP_OVERSOLD')
            elif change < -5:
                signals.append('OVERSOLD')
            elif change > 10:
                signals.append('DEEP_OVERBOUGHT')
            elif change > 5:
                signals.append('OVERBOUGHT')
                
            # Volume analysis
            if vol > 1_000_000_000:
                signals.append('HIGH_VOL')
                
            # Market cap analysis
            if cap > 10_000_000_000:
                signals.append('LARGE_CAP')
            elif cap > 1_000_000_000:
                signals.append('MID_CAP')
                
            # Determine action with real logic
            if change < -8:
                action = 'STRONG_BUY'
                reason = f'Very oversold: {change:.1f}% drop'
                confidence = min(95, 60 + abs(change) * 3)
            elif change < -3:
                action = 'BUY'
                reason = f'Oversold: {change:.1f}% drop'
                confidence = min(85, 50 + abs(change) * 4)
            elif change > 8:
                action = 'STRONG_SELL'
                reason = f'Very overbought: +{change:.1f}%'
                confidence = min(90, 50 + change * 2)
            elif change > 3:
                action = 'SELL'
                reason = f'Overbought: +{change:.1f}%'
                confidence = min(80, 40 + change * 4)
            else:
                action = 'HOLD'
                reason = 'Neutral zone'
                confidence = 40 + abs(change) * 2
                
            analysis.append({
                'coin': symbol,
                'name': coin.get('name', ''),
                'price': price,
                'change_24h': change,
                'volume': vol,
                'market_cap': cap,
                'signals': signals,
                'action': action,
                'reason': reason,
                'confidence': confidence
            })
            
        # Sort by confidence
        analysis.sort(key=lambda x: x['confidence'], reverse=True)
        
        return analysis
        
    def run_strategy(self, holdings=None, capital=10000):
        """Run trading strategy"""
        if holdings is None:
            holdings = {}
            
        analysis = self.analyze_market()
        
        if not analysis:
            print("❌ Could not get market data")
            return
            
        # Calculate portfolio
        portfolio_value = 0
        for coin, amount in holdings.items():
            for a in analysis:
                if a['coin'].lower() == coin.lower():
                    portfolio_value += amount * a['price']
                    break
                    
        if portfolio_value == 0:
            portfolio_value = capital
            
        print("\n" + "="*75)
        print("🤖 MOMATRADER - REAL-TIME MARKET ANALYSIS")
        print("="*75)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💰 Portfolio: ${portfolio_value:,.2f}")
        print("="*75)
        
        # Show analysis for each coin
        print("\n📈 Market Analysis:")
        print("-"*75)
        
        for a in analysis[:10]:
            coin = a['coin']
            name = a['name'][:20]
            price = a['price']
            change = a['change_24h']
            action = a['action']
            conf = a['confidence']
            
            # Color indicators
            if action.startswith('STRONG_') or action == 'BUY':
                emoji = "🟢"
            elif action.startswith('STRONG_') or action == 'SELL':
                emoji = "🔴"
            else:
                emoji = "⚪"
                
            # Format price
            if price >= 1000:
                price_str = f"${price:,.0f}"
            elif price >= 1:
                price_str = f"${price:.2f}"
            else:
                price_str = f"${price:.4f}"
                
            print(f"{emoji} {coin:6} {name:20} {price_str:>12}  {change:>+7.2f}%  {action:12} [{conf:.0f}%]")
            
        # Generate recommendations
        print("\n🎯 AI Recommendations:")
        print("-"*75)
        
        buys = [a for a in analysis if 'BUY' in a['action']]
        sells = [a for a in analysis if 'SELL' in a['action']]
        
        if buys:
            print("🟢 BUY Signals (High Confidence):")
            for a in buys[:5]:
                print(f"   📌 {a['coin']:6} @ ${a['price']:.2f} (+{a['confidence']:.0f}% confidence)")
                print(f"       └─ {a['reason']}")
                
        if sells:
            print("\n🔴 SELL Signals (High Confidence):")
            for a in sells[:5]:
                print(f"   📌 {a['coin']:6} @ ${a['price']:.2f} (+{a['confidence']:.0f}% confidence)")
                print(f"       └─ {a['reason']}")
                
        if not buys and not sells:
            print("⚪ No clear signals - HOLD current positions")
            
        # Summary
        print("\n📊 Summary:")
        print("-"*75)
        print(f"   Total Markets Analyzed: {len(analysis)}")
        print(f"   BUY Signals:  {len(buys)}")
        print(f"   SELL Signals: {len(sells)}")
        print(f"   HOLD:         {len(analysis) - len(buys) - len(sells)}")
        
        print("\n" + "="*75)
        
        return analysis


def main():
    trader = MomaTrader()
    
    # Example holdings (coin: amount)
    holdings = {
        'BTC': 0.1,
        'ETH': 1.0,
        'SOL': 5
    }
    
    # Run strategy
    trader.run_strategy(holdings=holdings)


if __name__ == "__main__":
    main()
