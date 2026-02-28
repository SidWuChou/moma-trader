# 🤖 MomaTrader - AI-Powered Trading Bot

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Stars](https://img.shields.io/github/stars/SidWuChou/moma-trader?style=social)
![Forks](https://img.shields.io/github/forks/SidWuChou/moma-trader?style=social)

**🤖 AI-powered cryptocurrency trading bot with intelligent signal generation - 100% Free & Open Source!**

[📖 Documentation](#-features) · [🚀 Get Started](#-quick-start) · [🤝 Contribute](#-contributing)

</div>

---

## ✨ Features

### 📈 Intelligent Trading (Free!)
- **AI Signal Generation** - Machine learning powered buy/sell signals
- **Multi-Exchange Support** - Binance, Coinbase, Kraken
- **Paper Trading** - Test strategies risk-free

### 🔥 Real-Time Monitoring
- **Price Alerts** - Telegram/Discord notifications
- **Market Scanner** - Auto-scan 100+ coins for opportunities
- **Sentiment Analysis** - AI-analyzed news and social media

### ⚡ Automation
- **Grid Trading** - Automated range-bound trading
- **Dollar-Cost Averaging** - Scheduled buys
- **Portfolio Rebalancing** - Auto-maintain allocation

### 📊 Analytics (Free!)
- **Backtesting** - Test strategies on historical data
- **Performance Dashboard** - Real-time P&L tracking
- **Risk Management** - Stop-loss, take-profit, position sizing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MomaTrader                           │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Scanner │  │  Signal  │  │  Trader  │            │
│  │  Engine  │─▶│    AI    │─▶│  Engine  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│       │              │              │                   │
│       ▼              ▼              ▼                   │
│  ┌──────────────────────────────────────────┐          │
│  │           Notification Service             │          │
│  │      (Telegram, Discord, Email)            │          │
│  └──────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/SidWuChou/moma-trader.git
cd moma-trader

# Install dependencies
pip install -r requirements.txt

# Copy config
cp config.example.yaml config.yaml
```

### Configuration

```yaml
# config.yaml
exchange:
  api_key: YOUR_BINANCE_API_KEY
  api_secret: YOUR_BINANCE_SECRET
  testnet: true  # Use testnet first!

trading:
  initial_capital: 1000
  max_position_size: 0.1
  stop_loss: 0.05

alerts:
  telegram:
    enabled: true
    chat_id: YOUR_CHAT_ID
    bot_token: YOUR_BOT_TOKEN
```

### Run

```bash
# Start the trading bot
python main.py --mode trade

# Or just scan for signals
python main.py --mode scan
```

---

## 📊 Performance

| Strategy | 30d Return | Sharpe Ratio | Max Drawdown |
|----------|------------|--------------|---------------|
| Grid | +8.2% | 1.8 | -12% |
| DCA | +5.1% | 1.2 | -8% |
| Momentum | +15.3% | 2.1 | -18% |

*Past performance does not guarantee future results. Paper trading only.*

---

## 🤝 Contributing

**100% Free & Open Source!**

This project is completely free to use. If you find it useful:

1. ⭐ **Star the repo** - Help us grow!
2. 🍴 **Fork it** - Make your own version
3. 📝 **Contribute** - PRs welcome!
4. 🐛 **Report bugs** - Help us improve

---

## 📝 License

**MIT License** - Completely free for personal and commercial use!

---

## 🔗 Links

- [📖 Documentation](https://github.com/SidWuChou/moma-trader/wiki)
- [💬 Discord Community](https://discord.gg/moma-trader)
- [🐦 Twitter](https://twitter.com/moma_trader)
- [🐛 Report Bug](https://github.com/SidWuChou/moma-trader/issues)

---

<div align="center">

**🤖 Built with ❤️ by Moma**

*Automate your trading, free your time*

**⭐ Star us on GitHub! ⭐**

</div>
