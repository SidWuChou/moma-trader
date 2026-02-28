"""Notification Service - Telegram, Discord, Email"""
import logging
import aiohttp
from typing import List, Dict

logger = logging.getLogger(__name__)


class NotificationService:
    """Sends notifications to various platforms"""
    
    def __init__(self, config):
        self.config = config
        self.telegram_enabled = config.get('telegram_enabled', False)
        self.telegram_token = config.get('telegram_token', '')
        self.telegram_chat_id = config.get('telegram_chat_id', '')
        
    async def send_signals(self, signals: List[Dict]):
        """Send trading signals to notification channels"""
        if not signals:
            return
            
        message = self._format_message(signals)
        
        if self.telegram_enabled:
            await self._send_telegram(message)
            
    def _format_message(self, signals: List[Dict]) -> str:
        """Format signals as message"""
        lines = ["🤖 *MomaTrader Signals*\n"]
        
        for s in signals:
            emoji = "🟢" if s['action'] == "BUY" else "🔴"
            lines.append(f"{emoji} *{s['symbol']}* - {s['action']}")
            lines.append(f"   Confidence: {s['confidence']:.0f}%")
            lines.append(f"   Price: ${s['price']}")
            lines.append(f"   Reason: {s['reason']}")
            lines.append("")
            
        return "\n".join(lines)
        
    async def _send_telegram(self, message: str):
        """Send message to Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            logger.warning("Telegram not configured")
            return
            
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        data = {
            'chat_id': self.telegram_chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as resp:
                    if resp.status == 200:
                        logger.info("Telegram notification sent")
                    else:
                        logger.error(f"Telegram error: {resp.status}")
        except Exception as e:
            logger.error(f"Failed to send Telegram: {e}")
