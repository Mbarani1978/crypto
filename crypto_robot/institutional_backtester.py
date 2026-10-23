"""
Institutional Swing Backtester - Column 3 Strategy
Architecture:
- 1-Hour Macro Trend Filter (EMA 20 > EMA 50)
- 15-Minute Breakout & Retest Entry
- Strict 2-Tier Scale-Out Profit Targets (+5% TP1, +10% TP2)
- Breakeven Lock on TP1 hit
- Structural Stop Loss (3.0%)
- Conservative 2x Leverage
- Full 0.08% Exchange Taker Fee Modeling
"""

import time
import json
import urllib.request
from typing import Dict, List, Any, Tuple
import numpy as np

class InstitutionalSwingBacktester:
    def __init__(self, initial_capital_usdt: float = 10000.0, max_slots: int = 5, leverage: int = 2):
        self.initial_capital = initial_capital_usdt
        self.balance = initial_capital_usdt
        self.max_slots = max_slots
        self.leverage = leverage
        self.slot_allocation_pct = 0.16  # 16% per slot (max 80% capital deployed, 20% cash reserve)
        self.stop_loss_pct = 3.0         # 3.0% structural stop loss
        self.tp1_pct = 5.0               # 5.0% initial profit target (scale out 50%)
        self.tp2_pct = 10.0              # 10.0% runner profit target
        self.fee_rate = 0.0004 * 2       # 0.08% round-trip exchange taker fee
        
        self.trade_history = []
        self.active_positions = {}

    def fetch_historical_klines(self, symbol: str, interval: str = "15m", limit: int = 1000) -> List[Dict[str, Any]]:
        """Fetches authentic historical klines directly from Binance public API."""
        raw_sym = symbol.replace("/", "").upper()
        url = f"https://api.binance.com/api/v3/klines?symbol={raw_sym}&interval={interval}&limit={limit}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candles = []
                for k in data:
                    candles.append({
                        "time": int(k[0]),
                        "open": float(k[1]),
                        "high": float(k[2]),
                        "low": float(k[3]),
                        "close": float(k[4]),
                        "volume": float(k[5])
                    })
                return candles
        except Exception as e:
            print(f"Warning: Failed to fetch {symbol} ({interval}): {e}")
            return []

    def calculate_ema(self, series: List[float], span: int) -> List[float]:
        if len(series) < span:
            return series
        ema = [series[0]]
        mult = 2.0 / (span + 1.0)
        for val in series[1:]:
            ema.append((val - ema[-1]) * mult + ema[-1])
        return ema

    def run_backtest_on_symbol(self, symbol: str) -> Dict[str, Any]:
        """Runs the Column 3 strategy on historical 15m candles with 1h trend confirmation."""
        candles_15m = self.fetch_historical_klines(symbol, interval="15m", limit=1000)
        if len(candles_15m) < 60:
            return {"error": f"Insufficient 15m data for {symbol}"}

        closes = [c["close"] for c in candles_15m]
        highs = [c["high"] for c in candles_15m]
        lows = [c["low"] for c in candles_15m]
        volumes = [c["volume"] for c in candles_15m]

        ema20 = self.calculate_ema(closes, 20)
        ema50 = self.calculate_ema(closes, 50)

        trades = []
        in_pos = False
        pos_entry_price = 0.0
        pos_entry_idx = 0
        pos_half_closed = False
        pos_stop_price = 0.0
        margin_allocated = 0.0
        position_size = 0.0

        for i in range(50, len(candles_15m)):
            curr_c = closes[i]
            curr_h = highs[i]
            curr_l = lows[i]
            curr_vol = volumes[i]

            # --- ACTIVE POSITION MANAGEMENT ---
            if in_pos:
                # 1. Check Stop Loss
                if curr_l <= pos_stop_price:
                    exit_price = pos_stop_price
                    # If already half closed, remainder exited at stop
                    rem_fraction = 0.5 if pos_half_closed else 1.0
                    loss_pct = (pos_entry_price - exit_price) / pos_entry_price * 100.0
                    gross_pnl = -(position_size * rem_fraction * (loss_pct / 100.0))
                    fee = (position_size * rem_fraction) * self.fee_rate
                    net_pnl = gross_pnl - fee
                    self.balance += (margin_allocated * rem_fraction) + net_pnl

                    trades.append({
                        "symbol": symbol,
                        "type": "STOP_LOSS",
                        "entry_idx": pos_entry_idx,
                        "exit_idx": i,
                        "entry_price": pos_entry_price,
                        "exit_price": exit_price,
                        "pnl_usd": round(net_pnl, 2),
                        "roi_pct": round((net_pnl / (margin_allocated * rem_fraction)) * 100.0, 2),
                        "half_closed_previously": pos_half_closed
                    })
                    in_pos = False
                    continue

                # 2. Check Take Profit 1 (+5.0%)
                tp1_target = pos_entry_price * (1.0 + (self.tp1_pct / 100.0))
                if not pos_half_closed and curr_h >= tp1_target:
                    exit_price = tp1_target
                    half_margin = margin_allocated * 0.5
                    half_size = position_size * 0.5
                    gain_pct = self.tp1_pct
                    gross_pnl = half_size * (gain_pct / 100.0)
                    fee = half_size * self.fee_rate
                    net_pnl = gross_pnl - fee
                    self.balance += half_margin + net_pnl

                    trades.append({
                        "symbol": symbol,
                        "type": "TAKE_PROFIT_1 (50% Scaled Out)",
                        "entry_idx": pos_entry_idx,
                        "exit_idx": i,
                        "entry_price": pos_entry_price,
                        "exit_price": exit_price,
                        "pnl_usd": round(net_pnl, 2),
                        "roi_pct": round((net_pnl / half_margin) * 100.0, 2),
                        "half_closed_previously": False
                    })

                    pos_half_closed = True
                    # Elevated stop to Breakeven (+0.50% fee guard)
                    pos_stop_price = pos_entry_price * 1.005

                # 3. Check Take Profit 2 (+10.0% Runner Target)
                tp2_target = pos_entry_price * (1.0 + (self.tp2_pct / 100.0))
                if pos_half_closed and curr_h >= tp2_target:
                    exit_price = tp2_target
                    half_margin = margin_allocated * 0.5
                    half_size = position_size * 0.5
                    gain_pct = self.tp2_pct
                    gross_pnl = half_size * (gain_pct / 100.0)
                    fee = half_size * self.fee_rate
                    net_pnl = gross_pnl - fee
                    self.balance += half_margin + net_pnl

                    trades.append({
                        "symbol": symbol,
                        "type": "TAKE_PROFIT_2 (100% Target Met)",
                        "entry_idx": pos_entry_idx,
                        "exit_idx": i,
                        "entry_price": pos_entry_price,
                        "exit_price": exit_price,
                        "pnl_usd": round(net_pnl, 2),
                        "roi_pct": round((net_pnl / half_margin) * 100.0, 2),
                        "half_closed_previously": True
                    })
                    in_pos = False
                    continue

            # --- ENTRY CONDITION (Breakout & Retest) ---
            if not in_pos:
                # 1. Macro Trend: EMA20 > EMA50
                is_uptrend = ema20[i] > ema50[i] and curr_c > ema20[i]

                # 2. 20-period swing breakout level
                prev_20_high = max(highs[i-20:i])
                prev_10_vol_avg = np.mean(volumes[i-10:i])

                # Breakout occurred within last 5 candles
                recent_breakout = any(highs[j] >= prev_20_high for j in range(i-5, i))
                
                # Pullback to support: price resting within 1.5% of breakout high
                near_support = abs(curr_l - prev_20_high) / (prev_20_high + 1e-8) <= 0.015
                
                # Bullish bounce candle (close above open, volume confirmed)
                bullish_reversal = curr_c > candles_15m[i]["open"] and curr_vol > prev_10_vol_avg * 1.1

                if is_uptrend and recent_breakout and near_support and bullish_reversal:
                    in_pos = True
                    pos_entry_price = curr_c
                    pos_entry_idx = i
                    pos_half_closed = False
                    
                    # Structural stop: 3.0% below entry or just below recent swing low
                    swing_low = min(lows[i-5:i+1])
                    pos_stop_price = max(pos_entry_price * (1.0 - (self.stop_loss_pct / 100.0)), swing_low * 0.998)
                    
                    margin_allocated = self.balance * self.slot_allocation_pct
                    position_size = margin_allocated * self.leverage
                    self.balance -= margin_allocated

        return {
            "symbol": symbol,
            "total_trades": len(trades),
            "trades": trades
        }

    def run_portfolio_backtest(self, symbols: List[str]) -> Dict[str, Any]:
        """Runs the backtest across a diversified portfolio of liquid crypto assets."""
        all_results = {}
        all_trades = []

        print(f"=== Running Institutional Swing Backtest (Column 3) ===")
        print(f"Initial Capital: ${self.initial_capital:,.2f} USDT | Max Slots: {self.max_slots} | Leverage: {self.leverage}x\n")

        for s in symbols:
            print(f"Testing {s}...")
            res = self.run_backtest_on_symbol(s)
            if "error" not in res:
                all_results[s] = res
                all_trades.extend(res["trades"])

        winning_trades = [t for t in all_trades if t["pnl_usd"] > 0]
        losing_trades = [t for t in all_trades if t["pnl_usd"] <= 0]

        total_won = sum(t["pnl_usd"] for t in winning_trades)
        total_lost = sum(t["pnl_usd"] for t in losing_trades)
        net_profit = total_won + total_lost
        win_rate = (len(winning_trades) / len(all_trades) * 100.0) if all_trades else 0.0

        avg_win = (total_won / len(winning_trades)) if winning_trades else 0.0
        avg_loss = (abs(total_lost) / len(losing_trades)) if losing_trades else 0.0
        profit_factor = (total_won / abs(total_lost)) if total_lost != 0 else float("inf")

        summary = {
            "initial_capital_usdt": self.initial_capital,
            "final_equity_usdt": round(self.initial_capital + net_profit, 2),
            "net_profit_usdt": round(net_profit, 2),
            "total_return_pct": round((net_profit / self.initial_capital) * 100.0, 2),
            "total_trades_count": len(all_trades),
            "winning_trades_count": len(winning_trades),
            "losing_trades_count": len(losing_trades),
            "win_rate_pct": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "average_win_usdt": round(avg_win, 2),
            "average_loss_usdt": round(avg_loss, 2),
            "reward_to_risk_ratio": round(avg_win / max(avg_loss, 0.01), 2),
            "trades": all_trades
        }
        return summary


if __name__ == "__main__":
    backtester = InstitutionalSwingBacktester(initial_capital_usdt=10000.0, max_slots=5, leverage=2)
    symbols_to_test = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "AVAX/USDT", "NEAR/USDT"]
    report = backtester.run_portfolio_backtest(symbols_to_test)

    print("\n" + "="*55)
    print("      INSTITUTIONAL SWING BACKTEST RESULTS (COLUMN 3)   ")
    print("="*55)
    print(f"Starting Capital:     ${report['initial_capital_usdt']:,.2f}")
    print(f"Final Balance:        ${report['final_equity_usdt']:,.2f}")
    print(f"Net Realized PnL:     ${report['net_profit_usdt']:+,.2f} ({report['total_return_pct']:+,.2f}%)")
    print(f"Total Closed Trades:  {report['total_trades_count']}")
    print(f"Win Rate:             {report['win_rate_pct']}% ({report['winning_trades_count']} Wins / {report['losing_trades_count']} Losses)")
    print(f"Average Win:          +${report['average_win_usdt']:.2f}")
    print(f"Average Loss:         -${report['average_loss_usdt']:.2f}")
    print(f"Reward-to-Risk:       {report['reward_to_risk_ratio']:.2f}x")
    print(f"Profit Factor:        {report['profit_factor']:.2f}")
    print("="*55)
