"""
World Market Peak Timezone Engine
Monitors and analyzes global market peak trading sessions:
- US (New York / CME): 13:30 - 20:00 UTC (Peak volatility & volume)
- UK (London / Europe): 08:00 - 16:30 UTC (Heavy FX & Spot/Derivatives volume)
- Dubai (Middle East): 06:00 - 14:00 UTC (Institutional capital flow)
- Hong Kong: 01:30 - 08:00 UTC (Asian morning liquidity peak)
- Singapore: 01:00 - 09:00 UTC (Asia-Pacific derivatives hub)
- Australia (Sydney): 22:00 - 06:00 UTC (Early session momentum)
- Brazil (Sao Paulo / B3): 13:00 - 21:00 UTC (Latin America crypto volume)
"""

from datetime import datetime, timezone
from typing import Dict, List, Any

class WorldSessionEngine:
    def __init__(self):
        # Peak windows in UTC hours (start_hour, end_hour)
        self.sessions = {
            "US (New York)": {
                "timezone_name": "America/New_York (UTC-4/-5)",
                "start_utc": 13.5,  # 13:30 UTC
                "end_utc": 20.0,    # 20:00 UTC
                "base_volatility_multiplier": 1.45,
                "description": "High institutional derivatives flow & ETF market depth"
            },
            "UK (London)": {
                "timezone_name": "Europe/London (UTC+1/0)",
                "start_utc": 8.0,
                "end_utc": 16.5,
                "base_volatility_multiplier": 1.35,
                "description": "Major European cross-currency liquidity and spot settlement"
            },
            "Dubai (UAE)": {
                "timezone_name": "Asia/Dubai (UTC+4)",
                "start_utc": 6.0,
                "end_utc": 14.0,
                "base_volatility_multiplier": 1.15,
                "description": "Middle-East institutional wealth & OTC arbitrage flows"
            },
            "Hong Kong": {
                "timezone_name": "Asia/Hong_Kong (UTC+8)",
                "start_utc": 1.5,
                "end_utc": 8.0,
                "base_volatility_multiplier": 1.25,
                "description": "Greater China market open & altcoin momentum rallies"
            },
            "Singapore": {
                "timezone_name": "Asia/Singapore (UTC+8)",
                "start_utc": 1.0,
                "end_utc": 9.0,
                "base_volatility_multiplier": 1.20,
                "description": "Southeast Asia exchange servers & high-frequency algorithmic nodes"
            },
            "Australia (Sydney)": {
                "timezone_name": "Australia/Sydney (UTC+10/+11)",
                "start_utc": 22.0,
                "end_utc": 6.0,   # crosses midnight
                "base_volatility_multiplier": 1.10,
                "description": "Pacific opening bell and overnight Asian price discovery"
            },
            "Brazil (Sao Paulo)": {
                "timezone_name": "America/Sao_Paulo (UTC-3)",
                "start_utc": 13.0,
                "end_utc": 21.0,
                "base_volatility_multiplier": 1.15,
                "description": "Latin American retail & B3 crypto index peak activity"
            }
        }

    def get_current_utc_decimal_hour(self) -> float:
        now = datetime.now(timezone.utc)
        return now.hour + (now.minute / 60.0) + (now.second / 3600.0)

    def is_session_active(self, start: float, end: float, current_hour: float) -> bool:
        if start < end:
            return start <= current_hour <= end
        else:
            # Crosses midnight (e.g. 22:00 to 06:00)
            return current_hour >= start or current_hour <= end

    def evaluate_active_sessions(self) -> Dict[str, Any]:
        """Returns active sessions, overlap state, and dynamic market aggression multiplier."""
        now_utc = datetime.now(timezone.utc)
        current_hour = self.get_current_utc_decimal_hour()
        
        active_list = []
        total_multiplier = 1.0
        details = {}

        for name, data in self.sessions.items():
            active = self.is_session_active(data["start_utc"], data["end_utc"], current_hour)
            if active:
                active_list.append(name)
                total_multiplier *= data["base_volatility_multiplier"]
            
            details[name] = {
                "active": active,
                "timezone_name": data["timezone_name"],
                "hours_utc": f"{int(data['start_utc']):02d}:{(int((data['start_utc']%1)*60)):02d} - {int(data['end_utc']):02d}:{(int((data['end_utc']%1)*60)):02d} UTC",
                "volatility_weight": data["base_volatility_multiplier"],
                "description": data["description"]
            }

        # Normalize total multiplier so it scales smoothly between 1.0 and 2.5
        overlap_count = len(active_list)
        clamped_multiplier = min(2.5, max(1.0, 1.0 + (overlap_count * 0.22)))

        # Define session regime
        if "US (New York)" in active_list and "UK (London)" in active_list:
            regime = "Transatlantic Mega-Overlap (Peak Global Liquidity & Clean Trends)"
        elif "Hong Kong" in active_list and "Singapore" in active_list:
            regime = "Asia-Pacific Convergence (High Altcoin Momentum)"
        elif overlap_count >= 3:
            regime = "Multi-Continent Prime Window (Maximum Order Execution Depth)"
        elif overlap_count >= 1:
            regime = f"Single Region Active: {', '.join(active_list)}"
        else:
            regime = "Inter-Session Low-Volume Transition (Tightened Minimal-Loss Filters)"

        return {
            "current_utc_time": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "active_sessions": active_list,
            "active_count": overlap_count,
            "regime": regime,
            "volatility_boost_factor": round(clamped_multiplier, 2),
            "sessions_detail": details
        }
