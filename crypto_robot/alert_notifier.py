"""
Remote Mobile Alerting & Notification Engine
Sends real-time 24x7 push notifications to the user's mobile phone via:
1. Telegram Bot API (Chat ID + Bot Token)
2. Discord Webhook URL
Notifications dispatched for:
- 1-Hour Performance Audit Summaries (Net PnL, Win Rate, ROI)
- System 8 Emergency Sentry Alarms (Circuit breakers, adverse wick cuts)
- Trade Executions (10x/50x/100x entry, Breakeven Ratchet engaged, Target met)
"""

import requests
import time
from typing import Dict, Any, List

class AlertNotifier:
    def __init__(self, telegram_token: str = "", telegram_chat_id: str = "", discord_webhook: str = ""):
        self.telegram_token = telegram_token.strip()
        self.telegram_chat_id = telegram_chat_id.strip()
        self.discord_webhook = discord_webhook.strip()
        self.recent_alerts: List[Dict[str, Any]] = []
        self.enabled = bool(self.telegram_token or self.discord_webhook)

    def configure(self, telegram_token: str = "", telegram_chat_id: str = "", discord_webhook_url: str = "", enabled: bool = True) -> Dict[str, Any]:
        self.telegram_token = telegram_token.strip()
        self.telegram_chat_id = telegram_chat_id.strip()
        self.discord_webhook = discord_webhook_url.strip()
        self.enabled = enabled and bool(self.telegram_token or self.discord_webhook)
        return {
            "status": "configured",
            "enabled": self.enabled,
            "telegram_active": bool(self.telegram_token and self.telegram_chat_id),
            "discord_active": bool(self.discord_webhook)
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "telegram_active": bool(self.telegram_token and self.telegram_chat_id),
            "discord_active": bool(self.discord_webhook),
            "history_count": len(self.recent_alerts),
            "recent_alerts": self.recent_alerts[:10]
        }

    def send_test_alert(self) -> Dict[str, Any]:
        return self.send_notification(
            title="🔔 PING TEST: RIM v9.1 Mobile Notifier",
            message="Test communication link active! 24x7 autonomous trade notifications and 1-hour reports are live.",
            alert_type="INFO",
            priority="HIGH"
        )

    def send_notification(self, title: str, message: str, alert_type: str = "INFO", priority: str = "NORMAL") -> Dict[str, Any]:
        """Dispatches notification to all active mobile channels."""
        now_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        formatted_text = f"🤖 [RIM v9.1 CRYPTO ROBOT]\n🚨 {title}\n🕒 {now_str}\n\n{message}"
        
        status_res = {"telegram": "skipped", "discord": "skipped", "logged": True, "priority": priority}

        # 1. Telegram Dispatch
        if self.telegram_token and self.telegram_chat_id:
            try:
                url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
                payload = {
                    "chat_id": self.telegram_chat_id,
                    "text": formatted_text,
                    "parse_mode": "Markdown"
                }
                resp = requests.post(url, json=payload, timeout=4)
                status_res["telegram"] = "sent" if resp.status_code == 200 else f"failed_{resp.status_code}"
            except Exception as e:
                status_res["telegram"] = f"error_{str(e)[:30]}"

        # 2. Discord Dispatch
        if self.discord_webhook:
            try:
                color = 0x22c55e if alert_type == "PROFIT" else (0xef4444 if alert_type == "ALARM" else 0x0284c7)
                embed_payload = {
                    "username": "RIM v9.1 Trading Robot",
                    "embeds": [{
                        "title": title,
                        "description": message,
                        "color": color,
                        "footer": {"text": f"RIM v9.1 Autonomous Core • {now_str}"}
                    }]
                }
                resp = requests.post(self.discord_webhook, json=embed_payload, timeout=4)
                status_res["discord"] = "sent" if resp.status_code in [200, 204] else f"failed_{resp.status_code}"
            except Exception as e:
                status_res["discord"] = f"error_{str(e)[:30]}"

        # Archive recent alert
        record = {
            "title": title,
            "message": message,
            "type": alert_type,
            "timestamp": now_str,
            "status": status_res
        }
        self.recent_alerts.insert(0, record)
        if len(self.recent_alerts) > 40:
            self.recent_alerts.pop()

        return status_res

    def send_hourly_report_alert(self, report_summary: Dict[str, Any]):
        title = f"📊 1-Hour Performance Audit: Net PnL ${report_summary.get('net_hourly_profit_usdt', 0.0):+.2f} USDT"
        msg = (
            f"*Hourly Window*: {report_summary.get('hourly_window')}\n"
            f"*Net Profit*: ${report_summary.get('net_hourly_profit_usdt', 0.0):+.2f} USDT ({report_summary.get('roi_hourly_pct', 0.0):+.2f}% ROI)\n"
            f"*Trades Executed*: {report_summary.get('total_orders_executed', 0)} (Win Rate: {report_summary.get('win_rate_pct', 100.0)}%)\n"
            f"*Trading Fees Paid*: ${report_summary.get('total_fees_paid_usdt', 0.0):.3f} USDT\n"
            f"*S3 Auto-Corrections*: {report_summary.get('s3_corrections_in_window', 0)}\n"
            f"*Merkle Proof*: `{report_summary.get('s9_merkle_seal', 'Verified')[:16]}...`"
        )
        return self.send_notification(title, msg, alert_type="PROFIT")

    def send_emergency_sentry_alarm(self, reason: str, details: str):
        title = "⚠️ EMERGENCY SENTRY CIRCUIT BREAKER TRIPPED"
        msg = f"*Reason*: {reason}\n*Telemetry*: {details}\n*Action*: System 8 safe halt engaged to protect capital."
        return self.send_notification(title, msg, alert_type="ALARM")
