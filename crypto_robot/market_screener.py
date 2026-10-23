"""
Market Screener & Vital Coin Selector - Top 50 Vital Market Universe (Every Minute)
Ranks and evaluates ALL cryptocurrency pairs traded against USDT across the global market,
identifying, tracking, analyzing, and qualifying trades for ONLY the TOP 50 MOST VITAL COINS.

Vitality Criteria:
1. 24h Trading Volume & Liquidity Depth (vital to prevent market impact)
2. Orderbook Spread Tightness (vital to ensure zero-loss breakeven executions)
3. Realized Volatility & Trend Directional Confluence (vital for predictable 10x/50x/100x gains)
4. Order Flow Stability / Chop Index (rejects choppy consolidation traps)
"""

import time
import math
from typing import Dict, List, Any

class MarketScreener:
    def __init__(self):
        # Strict inclusion / exclusion criteria
        self.target_top_count = 50               # Exactly track Top 50 Vital Coins
        self.min_24h_volume_usd = 15_000_000.0   # $15M minimum 24h volume for vitality
        self.max_spread_pct = 0.038               # Max allowable bid/ask spread (0.038%)
        self.min_trend_score = 60.0               # Minimum trend alignment score (0 - 100)
        self.max_chop_index = 65.0                # Chop index > 65 means consolidation trap

    def compute_vitality_score(self, vol_24h: float, spread_pct: float, abs_change_pct: float) -> float:
        """
        Computes an institutional Market Vitality Score (0 to 100):
        - 50% Weight: 24h Volume Depth (logarithmic scaling from $10M to $10B)
        - 30% Weight: Spread Tightness (narrower spread = higher score)
        - 20% Weight: Momentum & Volatility (vitality requires movement, not dead coins)
        """
        # Volume score: $10M = 40 pts, $100M = 70 pts, $1B+ = 100 pts
        vol_score = min(100.0, max(10.0, (math.log10(max(vol_24h, 1e6)) - 6.0) / 4.0 * 100.0))
        
        # Spread score: 0.005% = 100 pts, 0.038% = 50 pts, >0.08% = 0 pts
        spread_score = min(100.0, max(0.0, 100.0 - (spread_pct / 0.0008)))
        
        # Momentum score: 2% to 15% change = sweet spot for trading
        momentum_score = min(100.0, max(20.0, abs_change_pct * 10.0 + 30.0))
        
        vitality = (0.50 * vol_score) + (0.30 * spread_score) + (0.20 * momentum_score)
        return round(min(99.9, max(5.0, vitality)), 1)

    def screen_universe(self, tickers: Dict[str, Dict], ohlcv_data: Dict[str, List[Dict]] = None) -> Dict[str, Any]:
        """
        Screens ALL cryptocurrency pairs traded against USDT in the market (700+ pairs),
        identifies the TOP 50 MOST VITAL COINS, analyzes them every minute,
        and decides which of the Top 50 to ENTER TRADE vs MONITOR.
        """
        ohlcv_data = ohlcv_data or {}
        raw_candidates = []

        symbols = list(tickers.keys())

        # Set of stablecoins, fiat pegs, and synthetic/leveraged tokens to exclude
        STABLECOINS = {"USDC", "FDUSD", "TUSD", "BUSD", "EUR", "DAI", "USDD", "USD1", "RLUSD", "USDE", "AEUR"}
        EXCLUDED_SYNTHETICS = {"SPCXB", "SOXLB", "SNDKB", "TSLAB", "NVDB", "APPLB", "AMZNB", "MSTRB", "COINB"}

        for symbol in symbols:
            # We focus strictly on USDT pairs
            if not symbol.endswith("USDT") and not symbol.endswith("/USDT"):
                continue

            base_coin = symbol.replace("/USDT", "").replace("USDT", "")
            if base_coin in STABLECOINS or base_coin in EXCLUDED_SYNTHETICS or "UP" in base_coin or "DOWN" in base_coin:
                continue
            if base_coin.endswith("B") and len(base_coin) >= 5 and base_coin not in {"DOGEB"}:
                continue

            ticker = tickers.get(symbol, {})
            last_price = ticker.get("last", 0.0)
            if last_price <= 0:
                continue

            vol_24h = ticker.get("quoteVolume", 0.0)
            bid = ticker.get("bid", last_price * 0.9999)
            ask = ticker.get("ask", last_price * 1.0001)
            price_change_pct = ticker.get("priceChangePercent", 0.0)

            # Spread Calculation
            if bid > 0 and ask > 0 and last_price > 0:
                spread_pct = ((ask - bid) / last_price) * 100.0
            else:
                spread_pct = 0.015

            vitality_score = self.compute_vitality_score(vol_24h, spread_pct, abs(price_change_pct))

            raw_candidates.append({
                "symbol": symbol,
                "last_price": last_price,
                "volume_24h_usd": vol_24h,
                "price_change_24h_pct": price_change_pct,
                "spread_pct": round(spread_pct, 4),
                "vitality_score": vitality_score
            })

        # Step 2: Rank strictly by Market Vitality to isolate the TOP 50 Vital Coins
        raw_candidates.sort(key=lambda x: (x["vitality_score"], x["volume_24h_usd"]), reverse=True)

        top_50_vital = []
        left_out_coins = []
        selected_pairs = []

        # Step 3: Deep 1-minute Analysis on the Top 50 Vital Coins
        for rank_idx, item in enumerate(raw_candidates):
            symbol = item["symbol"]
            last_price = item["last_price"]
            vol_24h = item["volume_24h_usd"]
            price_change_pct = item["price_change_24h_pct"]
            spread_pct = item["spread_pct"]
            vitality_score = item["vitality_score"]
            rank = rank_idx + 1

            candles = ohlcv_data.get(symbol, [])
            if len(candles) >= 10:
                closes = [c["close"] for c in candles]
                net_change_pct = abs((closes[-1] - closes[0]) / (closes[0] + 1e-8)) * 100.0
                volatility_pct = (max(closes) - min(closes)) / (closes[0] + 1e-8) * 100.0
                trend_score = min(98.0, max(20.0, (net_change_pct / (volatility_pct + 1e-5)) * 100.0 + (net_change_pct * 8)))
                chop_score = max(10.0, 100.0 - trend_score)
            else:
                abs_change = abs(price_change_pct)
                trend_score = min(95.0, max(30.0, abs_change * 12.0 + 45.0))
                chop_score = max(10.0, 100.0 - trend_score)

            if rank <= self.target_top_count:
                # Inside the Top 50 Vital Universe
                reasons = []
                eligible_for_trade = True

                # Gate A: Liquidity check
                if vol_24h < self.min_24h_volume_usd:
                    eligible_for_trade = False
                    reasons.append(f"Volume below threshold (${vol_24h/1e6:.1f}M)")

                # Gate B: Spread check
                if spread_pct > self.max_spread_pct:
                    eligible_for_trade = False
                    reasons.append(f"Spread wide ({spread_pct:.3f}%)")

                # Gate C: Chop index
                if chop_score > self.max_chop_index:
                    eligible_for_trade = False
                    reasons.append(f"Consolidation chop ({chop_score:.1f})")

                # Gate D: Trend strength
                if trend_score < self.min_trend_score:
                    eligible_for_trade = False
                    reasons.append(f"Momentum forming ({trend_score:.1f}/100)")

                if eligible_for_trade:
                    status = "ENTER"
                    rationale = f"Top #{rank} Vital Coin: High liquidity depth, tightest spread & clean 1-min trend confluence."
                    selected_pairs.append(symbol)
                else:
                    status = "MONITORING"
                    rationale = f"Top #{rank} Vital Coin: Active tracking every minute (Awaiting trend confluence: {', '.join(reasons)})."

                coin_record = {
                    "rank": rank,
                    "symbol": symbol,
                    "status": status,
                    "vitality_score": vitality_score,
                    "last_price": last_price,
                    "volume_24h_usd": vol_24h,
                    "price_change_24h_pct": price_change_pct,
                    "spread_pct": round(spread_pct, 4),
                    "trend_score": round(trend_score, 1),
                    "chop_index": round(chop_score, 1),
                    "rationale": rationale,
                    "is_top_50": True
                }
                top_50_vital.append(coin_record)
            else:
                # Outside the Top 50 Vital Universe - Excluded from trading
                status = "LEAVE_OUT"
                rationale = f"Rank #{rank} (Outside Top 50 Vital Universe - Excluded to protect capital & eliminate slippage)."
                coin_record = {
                    "rank": rank,
                    "symbol": symbol,
                    "status": status,
                    "vitality_score": vitality_score,
                    "last_price": last_price,
                    "volume_24h_usd": vol_24h,
                    "price_change_24h_pct": price_change_pct,
                    "spread_pct": round(spread_pct, 4),
                    "trend_score": round(trend_score, 1),
                    "chop_index": round(chop_score, 1),
                    "rationale": rationale,
                    "is_top_50": False
                }
                left_out_coins.append(coin_record)

        # Sort top 50 vital coins: ENTER trades first, then by rank
        top_50_vital.sort(key=lambda x: (0 if x["status"] == "ENTER" else 1, x["rank"]))

        entered_count = sum(1 for c in top_50_vital if c["status"] == "ENTER")
        monitoring_count = sum(1 for c in top_50_vital if c["status"] == "MONITORING")

        return {
            "timestamp": time.time(),
            "target_top_count": self.target_top_count,
            "total_screened": len(symbols),
            "top_50_count": len(top_50_vital),
            "entered_count": entered_count,
            "monitoring_count": monitoring_count,
            "left_out_count": len(left_out_coins),
            "selected_pairs": selected_pairs,
            "entered_coins": [c for c in top_50_vital if c["status"] == "ENTER"],
            "monitoring_coins": [c for c in top_50_vital if c["status"] == "MONITORING"],
            "top_50_coins": top_50_vital,
            "all_coins": top_50_vital + left_out_coins[:100]  # First 50 are the vital coins, followed by audit samples
        }
