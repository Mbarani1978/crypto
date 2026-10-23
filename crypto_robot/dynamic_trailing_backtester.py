"""
Comparative Quant Study: Fixed Pre-defined Targets vs Dynamic Trailing ATR Exits
Tests both approaches on authentic Binance historical candlestick data side-by-side.
"""

import time
import json
import urllib.request
from typing import Dict, List, Any, Tuple
import numpy as np

class StrategyComparisonBacktester:
    def __init__(self, initial_capital_usdt: float = 10000.0, leverage: int = 2):
        self.initial_capital = initial_capital_usdt
        self.leverage = leverage
        self.slot_allocation_pct = 0.16
        self.maker_fee_rate = 0.0001 * 2 # 0.02% roundtrip

    def fetch_historical_klines(self, symbol: str, interval: str = "15m", limit: int = 1000) -> List[Dict[str, Any]]:
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
        if len(series) < span: return series
        ema = [series[0]]
        mult = 2.0 / (span + 1.0)
        for val in series[1:]:
            ema.append((val - ema[-1]) * mult + ema[-1])
        return ema

    def calculate_atr(self, candles: List[Dict[str, Any]], period: int = 14) -> List[float]:
        if len(candles) < 2: return [0.0] * len(candles)
        tr = [candles[0]["high"] - candles[0]["low"]]
        for i in range(1, len(candles)):
            h = candles[i]["high"]
            l = candles[i]["low"]
            c_prev = candles[i-1]["close"]
            tr.append(max(h - l, abs(h - c_prev), abs(l - c_prev)))
        
        atr = []
        for i in range(len(tr)):
            if i < period:
                atr.append(float(np.mean(tr[:i+1])))
            else:
                atr.append((atr[-1] * (period - 1) + tr[i]) / period)
        return atr

    def calculate_adx(self, candles: List[Dict[str, Any]], period: int = 14) -> List[float]:
        if len(candles) < period * 2: return [20.0] * len(candles)
        plus_dm, minus_dm = [0.0], [0.0]
        tr = [candles[0]["high"] - candles[0]["low"]]

        for i in range(1, len(candles)):
            up_move = candles[i]["high"] - candles[i-1]["high"]
            down_move = candles[i-1]["low"] - candles[i]["low"]
            plus_dm.append(up_move if (up_move > down_move and up_move > 0) else 0.0)
            minus_dm.append(down_move if (down_move > up_move and down_move > 0) else 0.0)
            h, l, c_prev = candles[i]["high"], candles[i]["low"], candles[i-1]["close"]
            tr.append(max(h - l, abs(h - c_prev), abs(l - c_prev)))

        atr_s = [float(np.mean(tr[:period]))]
        p_dm_s = [float(np.mean(plus_dm[:period]))]
        m_dm_s = [float(np.mean(minus_dm[:period]))]

        for i in range(period, len(candles)):
            atr_s.append((atr_s[-1] * (period - 1) + tr[i]) / period)
            p_dm_s.append((p_dm_s[-1] * (period - 1) + plus_dm[i]) / period)
            m_dm_s.append((m_dm_s[-1] * (period - 1) + minus_dm[i]) / period)

        dx = []
        for i in range(len(atr_s)):
            atr_val = atr_s[i] if atr_s[i] > 0 else 1e-8
            p_di = (p_dm_s[i] / atr_val) * 100.0
            m_di = (m_dm_s[i] / atr_val) * 100.0
            diff = abs(p_di - m_di)
            tot = p_di + m_di
            dx.append((diff / tot * 100.0) if tot > 0 else 0.0)

        adx = [float(np.mean(dx[:period]))]
        for i in range(period, len(dx)):
            adx.append((adx[-1] * (period - 1) + dx[i]) / period)

        pad = len(candles) - len(adx)
        return ([20.0] * pad) + adx

    def run_backtest(self, symbol: str, use_dynamic_trailing: bool = False) -> Dict[str, Any]:
        candles_15m = self.fetch_historical_klines(symbol, interval="15m", limit=1000)
        candles_1h = self.fetch_historical_klines(symbol, interval="1h", limit=300)

        if len(candles_15m) < 80 or len(candles_1h) < 50:
            return {"error": "Insufficient data"}

        c_1h = [c["close"] for c in candles_1h]
        t_1h = [c["time"] for c in candles_1h]
        ema50_1h = self.calculate_ema(c_1h, 50)
        ema200_1h = self.calculate_ema(c_1h, 200)

        def get_1h_trend(ts_15m: int) -> str:
            matching_idx = -1
            for idx, t in enumerate(t_1h):
                if t <= ts_15m: matching_idx = idx
                else: break
            if matching_idx < 50: return "NEUTRAL"
            c = c_1h[matching_idx]
            e50 = ema50_1h[matching_idx]
            e200 = ema200_1h[matching_idx] if len(ema200_1h) > matching_idx else e50
            if c > e50 > e200: return "BULLISH"
            elif c < e50 < e200: return "BEARISH"
            return "NEUTRAL"

        closes = [c["close"] for c in candles_15m]
        highs = [c["high"] for c in candles_15m]
        lows = [c["low"] for c in candles_15m]
        volumes = [c["volume"] for c in candles_15m]
        times = [c["time"] for c in candles_15m]

        ema20 = self.calculate_ema(closes, 20)
        ema50 = self.calculate_ema(closes, 50)
        atr_series = self.calculate_atr(candles_15m, 14)
        adx_series = self.calculate_adx(candles_15m, 14)

        balance = self.initial_capital
        trades = []
        in_pos = False
        pos_action = "BUY"
        pos_entry_price = 0.0
        pos_stop_price = 0.0
        pos_tp1_price = 0.0
        pos_tp2_price = 0.0
        pos_highest_price = 0.0
        pos_lowest_price = 0.0
        pos_scaled_out = False
        margin_allocated = 0.0
        position_size = 0.0

        for i in range(50, len(candles_15m)):
            curr_c = closes[i]
            curr_h = highs[i]
            curr_l = lows[i]
            curr_atr = atr_series[i]
            curr_adx = adx_series[i]
            macro_trend = get_1h_trend(times[i])

            if in_pos:
                if pos_action == "BUY":
                    pos_highest_price = max(pos_highest_price, curr_h)
                else:
                    pos_lowest_price = min(pos_lowest_price, curr_l)

                # --- EXIT EVALUATION ---
                stopped_out = (pos_action == "BUY" and curr_l <= pos_stop_price) or (pos_action == "SELL" and curr_h >= pos_stop_price)
                if stopped_out:
                    exit_price = pos_stop_price
                    rem_frac = (0.7 if use_dynamic_trailing else 0.5) if pos_scaled_out else 1.0
                    price_delta = (exit_price - pos_entry_price) if pos_action == "BUY" else (pos_entry_price - exit_price)
                    delta_pct = (price_delta / pos_entry_price) * 100.0

                    gross_pnl = position_size * rem_frac * (delta_pct / 100.0)
                    fee = (position_size * rem_frac) * self.maker_fee_rate
                    net_pnl = gross_pnl - fee
                    balance += (margin_allocated * rem_frac) + net_pnl

                    trades.append({
                        "symbol": symbol,
                        "type": "DYNAMIC_TRAILING_EXIT" if (use_dynamic_trailing and pos_scaled_out) else "STOP_LOSS",
                        "net_pnl_usd": round(net_pnl, 2),
                        "roi_pct": round((net_pnl / (margin_allocated * rem_frac)) * 100.0, 2)
                    })
                    in_pos = False
                    continue

                # Scale Out Trigger
                tp1_hit = (pos_action == "BUY" and curr_h >= pos_tp1_price) or (pos_action == "SELL" and curr_l <= pos_tp1_price)
                if not pos_scaled_out and tp1_hit:
                    scale_frac = 0.3 if use_dynamic_trailing else 0.5
                    exit_price = pos_tp1_price
                    s_margin = margin_allocated * scale_frac
                    s_size = position_size * scale_frac

                    price_delta = (exit_price - pos_entry_price) if pos_action == "BUY" else (pos_entry_price - exit_price)
                    delta_pct = (price_delta / pos_entry_price) * 100.0

                    gross_pnl = s_size * (delta_pct / 100.0)
                    fee = s_size * self.maker_fee_rate
                    net_pnl = gross_pnl - fee
                    balance += s_margin + net_pnl

                    trades.append({
                        "symbol": symbol,
                        "type": f"SCALE_OUT ({int(scale_frac*100)}% Banked)",
                        "net_pnl_usd": round(net_pnl, 2),
                        "roi_pct": round((net_pnl / s_margin) * 100.0, 2)
                    })
                    pos_scaled_out = True

                    # Elevate Stop to Breakeven (+0.25% fee buffer)
                    if pos_action == "BUY":
                        pos_stop_price = max(pos_stop_price, pos_entry_price * 1.0025)
                    else:
                        pos_stop_price = min(pos_stop_price, pos_entry_price * 0.9975)

                # DYNAMIC TRAILING VS FIXED TARGET 2
                if use_dynamic_trailing:
                    # Dynamically ratchet stop behind highest peak (Chandelier Leash: 2.0x ATR)
                    if pos_scaled_out:
                        if pos_action == "BUY":
                            new_trail = pos_highest_price - (2.0 * curr_atr)
                            pos_stop_price = max(pos_stop_price, new_trail)
                        else:
                            new_trail = pos_lowest_price + (2.0 * curr_atr)
                            pos_stop_price = min(pos_stop_price, new_trail)
                else:
                    # Static Fixed Target 2 (+5.0x ATR)
                    tp2_hit = (pos_action == "BUY" and curr_h >= pos_tp2_price) or (pos_action == "SELL" and curr_l <= pos_tp2_price)
                    if pos_scaled_out and tp2_hit:
                        rem_frac = 0.5
                        exit_price = pos_tp2_price
                        r_margin = margin_allocated * rem_frac
                        r_size = position_size * rem_frac

                        price_delta = (exit_price - pos_entry_price) if pos_action == "BUY" else (pos_entry_price - exit_price)
                        delta_pct = (price_delta / pos_entry_price) * 100.0

                        gross_pnl = r_size * (delta_pct / 100.0)
                        fee = r_size * self.maker_fee_rate
                        net_pnl = gross_pnl - fee
                        balance += r_margin + net_pnl

                        trades.append({
                            "symbol": symbol,
                            "type": "FIXED_TP2 (100% Target Met)",
                            "net_pnl_usd": round(net_pnl, 2),
                            "roi_pct": round((net_pnl / r_margin) * 100.0, 2)
                        })
                        in_pos = False
                        continue

            # --- ENTRY CONDITION ---
            if not in_pos:
                if curr_adx < 25.0: continue
                prev_15_high = max(highs[i-15:i])
                prev_15_low = min(lows[i-15:i])
                vol_avg = np.mean(volumes[i-10:i])
                has_vol = volumes[i] >= vol_avg * 1.25

                if macro_trend == "BULLISH" and ema20[i] > ema50[i] and curr_c > prev_15_high and has_vol:
                    in_pos = True
                    pos_action = "BUY"
                    pos_entry_price = curr_c
                    pos_highest_price = curr_c
                    pos_scaled_out = False
                    pos_stop_price = pos_entry_price - (1.8 * curr_atr)
                    pos_tp1_price = pos_entry_price + (2.0 * curr_atr)
                    pos_tp2_price = pos_entry_price + (5.0 * curr_atr)
                    margin_allocated = balance * self.slot_allocation_pct
                    position_size = margin_allocated * self.leverage
                    balance -= margin_allocated

                elif macro_trend == "BEARISH" and ema20[i] < ema50[i] and curr_c < prev_15_low and has_vol:
                    in_pos = True
                    pos_action = "SELL"
                    pos_entry_price = curr_c
                    pos_lowest_price = curr_c
                    pos_scaled_out = False
                    pos_stop_price = pos_entry_price + (1.8 * curr_atr)
                    pos_tp1_price = pos_entry_price - (2.0 * curr_atr)
                    pos_tp2_price = pos_entry_price - (5.0 * curr_atr)
                    margin_allocated = balance * self.slot_allocation_pct
                    position_size = margin_allocated * self.leverage
                    balance -= margin_allocated

        return {"trades": trades}

    def run_comparison(self, symbols: List[str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        print("=== Comparing Static Fixed Targets vs Dynamic Trailing ATR Exits ===")
        print(f"Testing across {len(symbols)} Top Crypto Assets on 15m/1h authentic historical data...\n")

        all_fixed_trades = []
        all_dynamic_trades = []

        for s in symbols:
            print(f"Testing {s}...")
            res_fixed = self.run_backtest(s, use_dynamic_trailing=False)
            res_dyn = self.run_backtest(s, use_dynamic_trailing=True)

            if "error" not in res_fixed: all_fixed_trades.extend(res_fixed["trades"])
            if "error" not in res_dyn: all_dynamic_trades.extend(res_dyn["trades"])

        def calc_stats(trades_list, label):
            wins = [t for t in trades_list if t["net_pnl_usd"] > 0]
            losses = [t for t in trades_list if t["net_pnl_usd"] <= 0]
            total_won = sum(t["net_pnl_usd"] for t in wins)
            total_lost = sum(t["net_pnl_usd"] for t in losses)
            net = total_won + total_lost
            win_rate = (len(wins) / len(trades_list) * 100.0) if trades_list else 0.0
            avg_w = (total_won / len(wins)) if wins else 0.0
            avg_l = (abs(total_lost) / len(losses)) if losses else 0.0
            pf = (total_won / abs(total_lost)) if total_lost != 0 else float("inf")
            return {
                "name": label,
                "total_trades": len(trades_list),
                "win_rate": round(win_rate, 2),
                "wins": len(wins),
                "losses": len(losses),
                "net_pnl": round(net, 2),
                "total_return_pct": round((net / self.initial_capital) * 100.0, 2),
                "avg_win": round(avg_w, 2),
                "avg_loss": round(avg_l, 2),
                "reward_to_risk": round(avg_w / max(avg_l, 0.01), 2),
                "profit_factor": round(pf, 2)
            }

        stats_fixed = calc_stats(all_fixed_trades, "Static Fixed Targets (5x ATR Cap)")
        stats_dyn = calc_stats(all_dynamic_trades, "Dynamic Trailing Stop (Chandelier Runner)")

        return stats_fixed, stats_dyn


if __name__ == "__main__":
    comp = StrategyComparisonBacktester(initial_capital_usdt=10000.0, leverage=2)
    symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "AVAX/USDT", "NEAR/USDT"]
    fixed_rep, dyn_rep = comp.run_comparison(symbols)

    print("\n" + "="*65)
    print("      HEAD-TO-HEAD COMPARISON: FIXED TARGETS VS DYNAMIC EXITS   ")
    print("="*65)
    print(f"{'METRIC':<25} | {'STATIC FIXED TARGETS':<18} | {'DYNAMIC TRAILING EXITS':<18}")
    print("-" * 65)
    print(f"{'Win Rate':<25} | {fixed_rep['win_rate']:>17}% | {dyn_rep['win_rate']:>17}%")
    print(f"{'Total Closed Exits':<25} | {fixed_rep['total_trades']:>18} | {dyn_rep['total_trades']:>18}")
    print(f"{'Winning Exits':<25} | {fixed_rep['wins']:>18} | {dyn_rep['wins']:>18}")
    print(f"{'Losing Exits':<25} | {fixed_rep['losses']:>18} | {dyn_rep['losses']:>18}")
    print(f"{'Average Win ($)':<25} | ${fixed_rep['avg_win']:>17.2f} | ${dyn_rep['avg_win']:>17.2f}")
    print(f"{'Average Loss ($)':<25} | ${fixed_rep['avg_loss']:>17.2f} | ${dyn_rep['avg_loss']:>17.2f}")
    print(f"{'Reward-to-Risk Ratio':<25} | {fixed_rep['reward_to_risk']:>17.2f}x | {dyn_rep['reward_to_risk']:>17.2f}x")
    print(f"{'Profit Factor':<25} | {fixed_rep['profit_factor']:>18.2f} | {dyn_rep['profit_factor']:>18.2f}")
    print(f"{'Net Realized PnL':<25} | ${fixed_rep['net_pnl']:>+17.2f} | ${dyn_rep['net_pnl']:>+17.2f}")
    print("="*65)
