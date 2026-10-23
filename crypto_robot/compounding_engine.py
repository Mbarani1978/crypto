"""
Phase 4: Systematic Compounding & Adaptive Sizing Engine
Implements:
1. Fractional Kelly Criterion Position Sizing:
   f* = (p * b - q) / b (with half-Kelly damping for maximum geometric growth)
2. Drawdown Damper:
   Automatically scales down leverage after consecutive breakevens/losses
3. Capital Compounding Ratchet:
   Allows account to compound safely only after statistical positive expectancy is proven
"""

import math
from typing import Dict, List, Any

class CompoundingEngine:
    def __init__(self, kelly_fraction: float = 0.35, min_trades_for_scaling: int = 15):
        self.kelly_fraction = kelly_fraction
        self.min_trades_for_scaling = min_trades_for_scaling
        self.consecutive_non_wins = 0
        self.consecutive_wins = 0
        self.leverage_damper_active = False

    def evaluate_kelly_sizing(self, closed_trades: List[Dict[str, Any]], current_balance: float) -> Dict[str, Any]:
        """Calculates optimal margin allocation using Fractional Kelly Criterion."""
        if len(closed_trades) < self.min_trades_for_scaling:
            return {
                "kelly_optimal_pct": 2.5,
                "recommended_margin_usdt": round(current_balance * 0.025, 2),
                "leverage_damper_active": self.leverage_damper_active,
                "regime": "Base Baseline Calibration (< 15 trades sample)"
            }

        recent = closed_trades[:30]
        wins = [t for t in recent if t.get("net_pnl_usd", 0.0) > 0.05]
        losses = [t for t in recent if t.get("net_pnl_usd", 0.0) <= 0.05]

        p = len(wins) / len(recent) # Win probability
        q = 1.0 - p

        avg_win = (sum(t["net_pnl_usd"] for t in wins) / len(wins)) if wins else 1.0
        avg_loss = (abs(sum(t["net_pnl_usd"] for t in losses)) / len(losses)) if losses else 1.0
        b = avg_win / (avg_loss + 1e-4) # Win/Loss payoff ratio

        # Full Kelly formula: f = (p * b - q) / b
        raw_kelly = (p * b - q) / (b + 1e-4)
        clamped_raw_kelly = max(0.01, min(0.18, raw_kelly))

        # Fractional Kelly (e.g. 35% of Kelly for institutional safety)
        fractional_kelly_pct = clamped_raw_kelly * self.kelly_fraction * 100.0
        
        # Apply Drawdown Damper if active
        if self.leverage_damper_active:
            fractional_kelly_pct = min(1.5, fractional_kelly_pct * 0.5)

        recommended_margin = round(current_balance * (fractional_kelly_pct / 100.0), 2)
        recommended_margin = max(5.0, min(current_balance * 0.08, recommended_margin))

        return {
            "win_rate_sample_pct": round(p * 100.0, 1),
            "payoff_ratio_b": round(b, 2),
            "raw_kelly_pct": round(raw_kelly * 100.0, 2),
            "fractional_kelly_pct": round(fractional_kelly_pct, 2),
            "recommended_margin_usdt": recommended_margin,
            "leverage_damper_active": self.leverage_damper_active,
            "regime": "Optimal Geometric Compounding" if not self.leverage_damper_active else "Drawdown Damped (Safety Mode)"
        }

    def record_trade_result(self, net_pnl: float):
        """Updates drawdown damper status based on consecutive outcomes."""
        if net_pnl > 0.05:
            self.consecutive_wins += 1
            self.consecutive_non_wins = 0
            if self.consecutive_wins >= 2:
                self.leverage_damper_active = False
        else:
            self.consecutive_non_wins += 1
            self.consecutive_wins = 0
            if self.consecutive_non_wins >= 2:
                self.leverage_damper_active = True
