#!/usr/bin/env python3
"""
MomaTrader - AI-Powered Trading Bot
Now with REAL AI using MiniMax-M2.5
"""
import requests
import json
from datetime import datetime

# MiniMax API
API_KEY = "sk-api-t3NvNNPlbsqIFLbqGrhlwMNTzUyPk2fqbGEg25SWSNSjgUPb9bl797i8tf53yqZfFAbwFxL9-89ioQ2U0vpWk_MR3gsDPXWHRBM_EaKCCmjEZL6GduxIn0k"

class MomaTraderAI:
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
            'sparkline': 'false'
        }
        r = requests.get(url, params=params, timeout=15)
        return r.json()
        
    def ask_ai(self, prompt):
        """Ask MiniMax AI"""
        url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": "MiniMax-M2.5",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        r = requests.post(url, headers=headers, json=data, timeout=30)
        result = r.json()
        if 'choices' in result and result['choices']:
            return result['choices'][0]['message']['content']
        return "AI unavailable"
        
    def analyze_with_ai(self, prices):
        """Use REAL AI to analyze market"""
        # Build market summary
        summary = "当前加密货币市场情况:\n"
        for coin in prices[:10]:
            name = coin.get('name', '')
            symbol = coin.get('symbol', '').upper()
            price = coin.get("current_price", 0) or 0
            change = coin.get('price_change_percentage_24h', 0) or 0
            summary += f"- {name} ({symbol}): ${price:.2f}, 24h {change:+.2f}%\n"
        
        # Ask AI for analysis
        prompt = f"""你是一个专业的加密货币分析师。请根据以下市场数据分析投资机会:

{summary}

请用中文给出:
1. 今日市场整体分析 (1-2句话)
2. 推荐的买入币种 (如果有)
3. 风险提示

回答要简洁明了。"""
        
        return self.ask_ai(prompt)
        
    def run(self, holdings=None):
        """Run trading bot"""
        if holdings is None:
            holdings = {}
            
        print("\n" + "="*70)
        print("🤖 MOMATRADER - AI-POWERED TRADING")
        print("="*70)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🧠 Model: MiniMax-M2.5")
        print("="*70)
        
        # Get prices
        print("\n📊 获取市场数据...")
        prices = self.get_prices()
        
        # Show prices
        print("\n💰 Market Prices:")
        print("-"*70)
        for coin in prices[:10]:
            name = coin.get('name', '')[:15]
            symbol = coin.get('symbol', '').upper()
            price = coin.get("current_price", 0) or 0 or 0
            change = coin.get('price_change_percentage_24h', 0) or 0
            
            emoji = "🟢" if change > 0 else "🔴"
            
            if price >= 1000:
                price_str = f"${price:,.0f}"
            elif price >= 1:
                price_str = f"${price:.2f}"
            else:
                price_str = f"${price:.4f}"
                
            print(f"{emoji} {symbol:6} {name:15} {price_str:>12}  {change:>+7.2f}%")
        
        # AI Analysis
        print("\n" + "="*70)
        print("🧠 AI 市场分析 (MiniMax-M2.5)")
        print("="*70)
        
        analysis = self.analyze_with_ai(prices)
        print(analysis)
        
        print("\n" + "="*70)
        
        return prices


if __name__ == "__main__":
    trader = MomaTraderAI()
    trader.run()
