#!/bin/bash
# Quick demo of MomaTrader

echo "🤖 MomaTrader Demo"
echo "=================="
echo ""

# Run in scan mode
echo "📊 Running market scan..."
python3 -m moma_trader --mode scan

echo ""
echo "✅ Demo complete!"
echo ""
echo "Next steps:"
echo "1. Copy config.example.yaml to config.yaml"
echo "2. Add your API keys"
echo "3. Run: python3 -m moma_trader --mode trade"
