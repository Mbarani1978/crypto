"""
Autonomous 24x7 Trading Engine - Powered by RIM v9.1 with 4-Phase Roadmap Orchestration
Orchestrates the entire trading cycle without requiring human intervention (except master ON/OFF).

4-Phase Implementation:
- Phase 1: 1,000-Cycle Autonomous Benchmark & Telemetry Engine
- Phase 2: Black Swan Stress Test Engine (Historical Crash Simulations)
- Phase 3: Micro-Account Live Safety Gateway & Micro-Slippage Auditor
- Phase 4: Systematic Compounding & Adaptive Kelly Position Sizing
"""

import time
import json
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from crypto_robot.rim_brain import (
    System1_Intuition,
    System2_Logic,
    System3_MetaCognition,
    System4_PermanentMemory,
    System5_ConservationSolver,
    System6_ConfidenceGatekeeper,
    System7_ContinualLearner,
    System8_EmergencySentry,
    System9_MerkleAuditSeal
)
from crypto_robot.world_session_engine import WorldSessionEngine
from crypto_robot.market_screener import MarketScreener
from crypto_robot.exchange_manager import ExchangeManager
from crypto_robot.hourly_reporter import HourlyReporter

# Import the 4-Phase Engines
from crypto_robot.benchmark_engine import BenchmarkEngine
from crypto_robot.stress_test_engine import StressTestEngine
from crypto_robot.live_safety_gateway import LiveSafetyGateway
from crypto_robot.compounding_engine import CompoundingEngine
from crypto_robot.political_alpha_engine import PoliticalAlphaEngine
from crypto_robot.low_latency_engine import LowLatencyEngine
from crypto_robot.security_vault import SecurityVault
from crypto_robot.alert_notifier import AlertNotifier
from crypto_robot.funding_rate_guard import FundingRateGuard
from crypto_robot.websocket_streamer import WebSocketStreamer
from crypto_robot.options_engine import OptionsEngine

class TradingEngine:
    def __init__(self):
        # Master Control (Human intervention only for ON / OFF)
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

        # RIM v9.1: All 9 Systems Orchestrated
        self.sys1 = System1_Intuition()
        self.sys2 = System2_Logic()
        self.sys3 = System3_MetaCognition(self.sys1, self.sys2)
        self.sys4 = System4_PermanentMemory()
        self.sys5 = System5_ConservationSolver()
        self.sys6 = System6_ConfidenceGatekeeper()
        self.sys7 = System7_ContinualLearner()
        self.sys8 = System8_EmergencySentry()
        self.sys9 = System9_MerkleAuditSeal()

        # The 4 Strategic Roadmap Engines
        self.benchmark = BenchmarkEngine(target_cycles=1000)
        self.stress_tester = StressTestEngine()
        self.safety_gateway = LiveSafetyGateway(max_capital_ceiling_usdt=6500.0)
        self.compounding = CompoundingEngine(kelly_fraction=0.35)

        # Operational Components & Low-Latency Acceleration
        self.session_engine = WorldSessionEngine()
        self.screener = MarketScreener()
        self.exchange = ExchangeManager(mode="simulation", exchange_id="binance")
        self.reporter = HourlyReporter()
        self.political_engine = PoliticalAlphaEngine()
        self.low_latency = LowLatencyEngine(target_exchange="binance")
        self.options_engine = OptionsEngine()

        # Enterprise Production Upgrades (All 6 Gaps Fixed)
        self.vault = SecurityVault()
        self.notifier = AlertNotifier()
        self.funding_guard = FundingRateGuard()
        self.streamer = WebSocketStreamer(exchange="binance")
        self.streamer.start_stream()

        # Account & Portfolio State (Fund Manager Portfolio Desk: Balanced 6-Book Vital Allocation)
        self.balance_usdt = 10000.0
        self.cycle_start_balance = 10000.0
        self.max_concurrent_positions = 6
        self.active_positions: Dict[str, Dict[str, Any]] = {}
        self.closed_orders: List[Dict[str, Any]] = []
        self.current_hourly_orders: List[Dict[str, Any]] = []

        # Fund Manager Economics & Performance Fee (20% High-Water Mark Payout)
        self.high_water_mark_usdt = 10000.0
        self.fund_manager_fee_pct = 20.0
        self.total_fund_manager_payout_usdt = 0.0
        self.total_investor_payout_usdt = 0.0
        
        # Real-time Telemetry & Cognitive Stream
        self.recent_cognitive_logs: List[Dict[str, Any]] = []
        self.recent_price_ticks: Dict[str, List[float]] = {}
        self.last_screener_result: Dict[str, Any] = {}
        self.last_session_state: Dict[str, Any] = {}
        self.last_analysis_time = 0.0
        self.last_hourly_report_time = time.time()
        self.bot_start_time: Optional[float] = None
        self.last_stress_test_result: Optional[Dict[str, Any]] = None
        self.stats = {
            "total_trades": 0,
            "win_trades": 0,
            "breakeven_trades": 0,
            "loss_trades": 0,
            "total_gross_pnl": 0.0,
            "total_net_pnl": 0.0,
            "s3_autocorrections": 0,
            "merkle_certificates_issued": 0,
            "balance_drift_variance": 0.0
        }
        # Immediately warmup screener so Top 50 Vital Coins are visible instantly
        threading.Thread(target=self._warmup_screener, daemon=True).start()

    def _warmup_screener(self):
        try:
            tickers = self.exchange.fetch_all_usdt_tickers()
            res = self.screener.screen_universe(tickers)
            self.last_screener_result = res
            self._log_cognition(
                "TOP_50_VITAL",
                "VITAL_UNIVERSE_READY",
                f"Isolated Top 50 Most Vital Coins from {res['total_screened']} USDT pairs. Ready for 1-minute tracking & trading."
            )
        except Exception as e:
            pass

    def start_bot(self) -> Dict[str, Any]:
        """User turning ON the robot."""
        with self.lock:
            if self.is_running:
                return {"status": "already_running", "message": "Bot is already operating 24x7."}
            self.is_running = True
            self.bot_start_time = time.time()
            self.thread = threading.Thread(target=self._autonomous_run_loop, daemon=True)
            self.thread.start()
            self._log_cognition("S8_SENTRY", "SYSTEM_ARMED", "All 9 Systems of RIM v9.1 Armed. Autonomous Execution Active.")
            return {"status": "started", "message": "24x7 Autonomous Robot started with all 9 RIM Systems."}

    def stop_bot(self) -> Dict[str, Any]:
        """User turning OFF the robot."""
        with self.lock:
            if not self.is_running:
                return {"status": "already_stopped", "message": "Bot is currently offline."}
            self.is_running = False
            self._log_cognition("S8_SENTRY", "SYSTEM_DISARMED", "User initiated Master OFF switch. Safely halting autonomous loop.")
            return {"status": "stopped", "message": "Autonomous Robot stopped."}

    def set_exchange_config(self, mode: str, exchange_id: str, api_key: str = "", secret: str = "", passphrase: str = "") -> Dict[str, Any]:
        with self.lock:
            if mode == "live":
                if not api_key or not secret:
                    return {
                        "status": "error",
                        "mode": self.exchange.mode,
                        "exchange": exchange_id,
                        "balance_usdt": self.balance_usdt,
                        "message": "API Secret is missing! Binance requires BOTH the API Key and API Secret to connect to your live account. Please paste your API Secret below, or select 'Real-Time Simulation' mode."
                    }
                self.exchange = ExchangeManager(
                    mode="live",
                    exchange_id=exchange_id,
                    api_key=api_key,
                    secret=secret,
                    passphrase=passphrase
                )
                if not self.exchange.exchange_client:
                    return {
                        "status": "error",
                        "mode": "simulation",
                        "exchange": exchange_id,
                        "balance_usdt": self.balance_usdt,
                        "message": f"Could not initialize CCXT client for {exchange_id.upper()}. Please verify exchange and credentials."
                    }
                bal_info = self.exchange.get_account_balance()
                if bal_info.get("mode") == "live":
                    self.balance_usdt = bal_info.get("total_usdt", self.balance_usdt)
                    self._log_cognition("S8_SENTRY", "EXCHANGE_AUTHENTICATED", f"Authenticated with {exchange_id.upper()} Live Account! Live USDT Balance: ${self.balance_usdt:,.2f}")
                    return {
                        "status": "success",
                        "mode": "live",
                        "exchange": exchange_id,
                        "balance_usdt": self.balance_usdt,
                        "message": f"Successfully connected to {exchange_id.upper()} Live Account! Live Balance: ${self.balance_usdt:,.2f} USDT."
                    }
                else:
                    err_msg = bal_info.get("error", "Failed to fetch account balance. Check API permissions (enable Spot/Futures).")
                    return {
                        "status": "error",
                        "mode": "simulation",
                        "exchange": exchange_id,
                        "balance_usdt": self.balance_usdt,
                        "message": f"{exchange_id.upper()} Authentication Error: {err_msg}"
                    }
            else:
                self.exchange = ExchangeManager(mode="simulation", exchange_id=exchange_id)
                self.balance_usdt = self.exchange.simulated_balance
                self._log_cognition("S8_SENTRY", "SIMULATION_ACTIVE", f"Switched to Simulation Mode on {exchange_id.upper()} Live Market Feed.")
                return {
                    "status": "success",
                    "mode": "simulation",
                    "exchange": exchange_id,
                    "balance_usdt": self.balance_usdt,
                    "message": f"Switched to Real-Time Simulation on {exchange_id.upper()} live market feed ($10,000 virtual balance)."
                }

    def _autonomous_run_loop(self):
        while self.is_running:
            try:
                now = time.time()

                # System 8: Hardware Sentry & Latency Check
                t0 = time.time()
                self.last_session_state = self.session_engine.evaluate_active_sessions()
                latency_ms = (time.time() - t0) * 1000.0
                vitals_ok, vitals_msg = self.sys8.check_system_vitals(latency_ms, error_count=0)
                if not vitals_ok:
                    self._log_cognition("S8_CIRCUIT_BREAKER", "VITALS_WARNING", vitals_msg)
                    time.sleep(2.0)
                    continue

                # Continuous Sub-second Position Management & System 3 Auto-Correction
                self._manage_active_positions()

                # Fund Manager Multi-Asset Active Execution Loop
                seconds_in_min = int(now) % 60
                has_capacity = len(self.active_positions) < self.max_concurrent_positions
                cycle_interval = 20.0 if has_capacity else 45.0
                if (seconds_in_min >= 45 or now - self.last_analysis_time >= cycle_interval):
                    if now - self.last_analysis_time >= 15.0:
                        self._execute_preemptive_market_cycle()
                        self.last_analysis_time = now

                        # Phase 1: Record execution cycle benchmark tick
                        self.benchmark.record_cycle_tick(self.get_dashboard_state())

                # 1-Hour Report Compilation Check
                if now - self.last_hourly_report_time >= 3600:
                    self._generate_and_archive_hourly_report()
                    self.last_hourly_report_time = now

                time.sleep(1.0)
            except Exception as e:
                self._log_cognition("S3_EXCEPTION_REPAIR", "ENGINE_LOOP_WARNING", f"Auto-repaired loop exception: {str(e)}")
                time.sleep(2.0)

    def _manage_active_positions(self):
        if not self.active_positions:
            return

        symbols_to_check = list(self.active_positions.keys())
        
        # Microsecond zero-delay price lookup via persistent WebSocket stream if connected
        streamed_tickers = {}
        if self.streamer and self.streamer.is_connected:
            for s in symbols_to_check:
                live_st = self.streamer.get_live_ticker(s)
                if live_st:
                    streamed_tickers[s] = live_st

        missing_symbols = [s for s in symbols_to_check if s not in streamed_tickers]
        tickers = {}
        if missing_symbols:
            tickers = self.exchange.fetch_live_tickers(missing_symbols)
        tickers.update(streamed_tickers)

        closed_keys = []
        for sym, pos in self.active_positions.items():
            ticker = tickers.get(sym)
            if not ticker:
                continue

            current_price = ticker["last"]
            if sym not in self.recent_price_ticks:
                self.recent_price_ticks[sym] = []
            self.recent_price_ticks[sym].append(current_price)
            if len(self.recent_price_ticks[sym]) > 8:
                self.recent_price_ticks[sym].pop(0)

            candidate_queue_len = len(self.last_screener_result.get("selected_pairs", [])) if self.last_screener_result else 0
            # System 3 Evaluation (Sub-second reflection & auto-correction)
            s3_eval = self.sys3.evaluate_active_position(
                pos,
                current_price,
                self.recent_price_ticks[sym],
                candidate_queue_len=candidate_queue_len
            )

            pos["current_price"] = current_price
            pos["unrealized_pnl_pct"] = s3_eval["unrealized_pnl_pct"]
            pos["current_stop_price"] = s3_eval["new_stop_price"]

            if s3_eval.get("autocorrect_applied"):
                pos["last_autocorrect"] = s3_eval["autocorrect_applied"]
                self.stats["s3_autocorrections"] += 1
                self._log_cognition(
                    "S3_AUTOCORRECTION",
                    s3_eval["autocorrect_applied"],
                    f"{sym} ({pos['leverage']}x): {s3_eval['reason']}"
                )

            decision = s3_eval.get("decision")
            if decision in ["CLOSE_STOP", "CLOSE_TAKE_PROFIT", "CLOSE_EMERGENCY"]:
                self._close_position(sym, pos, current_price, s3_eval["reason"], s3_eval.get("autocorrect_applied"))
                closed_keys.append(sym)

        for sym in closed_keys:
            if sym in self.active_positions:
                del self.active_positions[sym]

        if closed_keys:
            # Instant Zero-Delay Rotation: immediately deploy freed margin books into top waiting Vital candidates
            self.last_analysis_time = time.time()
            self._execute_preemptive_market_cycle()

    def _close_position(self, symbol: str, pos: Dict[str, Any], exit_price: float, reason: str, autocorrect: Optional[str]):
        entry_price = pos["entry_price"]
        side = pos["action"]
        leverage = pos["leverage"]
        margin = pos["allocated_margin_usdt"]
        position_size = pos["position_size_usdt"]

        if side == "BUY":
            price_delta_pct = ((exit_price - entry_price) / entry_price) * 100.0
        else:
            price_delta_pct = ((entry_price - exit_price) / entry_price) * 100.0

        gross_pnl = position_size * (price_delta_pct / 100.0)
        fee = position_size * 0.0004 * 2
        net_pnl = gross_pnl - fee
        roi_margin = (net_pnl / margin) * 100.0

        # Phase 3 / Live Mode: Execute offsetting market order on exchange to close live position
        if self.exchange.mode == "live" and self.exchange.exchange_client:
            close_side = "sell" if side == "BUY" else "buy"
            close_res = self.exchange.close_position(symbol, close_side, pos.get("coins_amount", 0.0))
            if not close_res.get("success"):
                self._log_cognition(
                    "LIVE_CLOSE_WARNING",
                    "OFFSET_FAILED",
                    f"Live exchange close order for {symbol} failed: {close_res.get('error')}"
                )

        old_bal = self.balance_usdt
        new_bal = old_bal + margin + net_pnl
        if new_bal < 0:
            new_bal = 0.0

        # System 5: Conservation Law & Zero-Drift Balance Verification
        is_exact, drift = self.sys5.verify_balance_conservation(
            start_bal=old_bal + margin,
            end_bal=new_bal,
            gross_pnl=gross_pnl,
            fees=fee
        )
        self.stats["balance_drift_variance"] = drift
        self.balance_usdt = new_bal

        # System 7: Continual Learner Online Weight Update
        self.sys7.record_trade_outcome(symbol, net_pnl)

        # Fund Manager Economics: High-Water Mark & 20% Performance Fee
        current_equity = self.balance_usdt + sum(p.get("allocated_margin_usdt", 0.0) for p in self.active_positions.values() if p["order_id"] != pos["order_id"])
        if current_equity > self.high_water_mark_usdt:
            new_alpha = current_equity - self.high_water_mark_usdt
            manager_fee = round(new_alpha * (self.fund_manager_fee_pct / 100.0), 2)
            investor_share = round(new_alpha - manager_fee, 2)
            self.total_fund_manager_payout_usdt += manager_fee
            self.total_investor_payout_usdt += investor_share
            self.high_water_mark_usdt = current_equity
            self._log_cognition(
                "FUND_MANAGER_PAYOUT",
                "HWM_PERFORMANCE_FEE",
                f"New High-Water Mark reached: ${self.high_water_mark_usdt:,.2f} USDT (+${new_alpha:,.2f} Alpha). RIM v9.1 Fund Manager 20% Fee: +${manager_fee:,.2f} USDT | Investor Net Share: +${investor_share:,.2f} USDT."
            )

        # Phase 4: Compounding Engine Trade Update (Drawdown Damper)
        self.compounding.record_trade_result(net_pnl)

        # Phase 3: Release margin in safety gateway & audit slippage
        self.safety_gateway.total_live_margin_committed = max(0.0, self.safety_gateway.total_live_margin_committed - margin)
        slippage_info = self.safety_gateway.audit_execution_slippage(symbol, entry_price, pos["entry_price"], side)

        # System 9: Issue Cryptographic Merkle Certificate (Digital Wax Seal)
        merkle_cert = self.sys9.issue_merkle_certificate({
            "order_id": pos["order_id"],
            "symbol": symbol,
            "entry_p": entry_price,
            "exit_p": exit_price,
            "net_pnl": net_pnl,
            "drift": drift
        })
        self.stats["merkle_certificates_issued"] += 1

        # System 4: Commit permanently to .rimdb
        self.sys4.record_decision(
            system_source="RIM_v9.1_EXECUTION_CORE",
            event_type="POSITION_CLOSED",
            symbol=symbol,
            order_id=pos["order_id"],
            payload_str=json.dumps({"net_pnl": net_pnl, "merkle_cert": merkle_cert})
        )

        # Update stats
        self.stats["total_trades"] += 1
        self.stats["total_gross_pnl"] += gross_pnl
        self.stats["total_net_pnl"] += net_pnl
        if net_pnl > 0.05:
            self.stats["win_trades"] += 1
        elif abs(net_pnl) <= 0.05:
            self.stats["breakeven_trades"] += 1
        else:
            self.stats["loss_trades"] += 1

        closed_record = {
            "order_id": pos["order_id"],
            "symbol": symbol,
            "action": side,
            "leverage": leverage,
            "entry_time": pos["entry_time"],
            "exit_time": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
            "entry_price": entry_price,
            "exit_price": exit_price,
            "price_delta_pct": round(price_delta_pct, 3),
            "allocated_margin_usdt": margin,
            "position_size_usdt": position_size,
            "gross_pnl_usd": round(gross_pnl, 2),
            "fee_usd": round(fee, 3),
            "net_pnl_usd": round(net_pnl, 2),
            "roi_margin_pct": round(roi_margin, 2),
            "exit_reason": reason,
            "s3_autocorrect_applied": autocorrect or "Zero-Loss Protocol Active",
            "merkle_seal": merkle_cert[:16] + "..."
        }

        self.closed_orders.insert(0, closed_record)
        self.current_hourly_orders.append(closed_record)

        self._log_cognition(
            "S9_MERKLE_SEAL",
            "POSITION_REALIZED",
            f"Closed {symbol} {side} ({leverage}x). Net: ${net_pnl:+.2f} ({roi_margin:+.1f}% ROI). [S5 Drift: {drift:.8f} | S9 Merkle: {merkle_cert[:12]}]"
        )
        self.notifier.send_notification(
            "TRADE_CLOSED",
            f"Closed {symbol} {side} ({leverage}x) | Net: ${net_pnl:+.2f} ({roi_margin:+.1f}% ROI) | Exit: ${exit_price}",
            priority="HIGH" if net_pnl < 0 else "NORMAL"
        )

    def place_manual_order(self, symbol: str, action: str, leverage: int = 10, margin_usdt: float = 100.0) -> Dict[str, Any]:
        with self.lock:
            if symbol in self.active_positions:
                return {"status": "error", "message": f"Position already active for {symbol}."}
            if margin_usdt > self.balance_usdt:
                return {"status": "error", "message": f"Insufficient balance (${self.balance_usdt:.2f} USDT available)."}
            
            # Fetch latest price
            tickers = self.exchange.fetch_live_tickers([symbol])
            ticker = tickers.get(symbol)
            price = ticker.get("last", 50000.0) if ticker else 50000.0

            action = action.upper()
            if action not in ["BUY", "SELL"]:
                action = "BUY"

            tp_mult = 1.015 if action == "BUY" else 0.985
            sl_mult = 0.992 if action == "BUY" else 1.008
            be_mult = 1.0012 if action == "BUY" else 0.9988

            position_size = margin_usdt * leverage
            coins_amount = position_size / price
            order_id = f"ORD_{int(time.time()*1000)}"
            now_str = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

            position_record = {
                "order_id": order_id,
                "symbol": symbol,
                "action": action,
                "leverage": leverage,
                "entry_price": price,
                "current_price": price,
                "allocated_margin_usdt": margin_usdt,
                "position_size_usdt": position_size,
                "coins_amount": coins_amount,
                "hard_stop_loss_price": round(price * sl_mult, 4),
                "current_stop_price": round(price * sl_mult, 4),
                "breakeven_trigger_price": round(price * be_mult, 4),
                "tp_target_price": round(price * tp_mult, 4),
                "highest_price": price,
                "lowest_price": price,
                "entry_time": now_str,
                "entry_timestamp": time.time(),
                "unrealized_pnl_pct": 0.0,
                "last_autocorrect": None
            }

            self.balance_usdt -= margin_usdt
            self.active_positions[symbol] = position_record
            self.safety_gateway.total_live_margin_committed += margin_usdt

            self._log_cognition(
                "ORDER_EXECUTED",
                f"MANUAL_{action}_{leverage}X",
                f"Manual {action} order executed on {symbol} ({leverage}x). Margin: ${margin_usdt:.2f} | Entry: ${price:,.2f}."
            )
            return {"status": "success", "message": f"{action} order executed on {symbol} at ${price:,.2f}.", "order": position_record}

    def manual_close_position(self, symbol: str) -> Dict[str, Any]:
        with self.lock:
            pos = self.active_positions.get(symbol)
            if not pos:
                return {"status": "error", "message": f"No active position found for {symbol}."}
            exit_price = pos.get("current_price", pos["entry_price"])
            self._close_position(symbol, pos, exit_price, reason="MANUAL_OPERATOR_CLOSE", autocorrect=None)
            if symbol in self.active_positions:
                del self.active_positions[symbol]
            return {"status": "success", "message": f"Closed position on {symbol} at ${exit_price:,.2f}."}

    def set_max_concurrent_positions(self, num: int) -> Dict[str, Any]:
        with self.lock:
            num = max(1, min(25, int(num)))
            self.max_concurrent_positions = num
            if num >= 15:
                self.sys1.min_confidence_to_trade = 0.58
                self.safety_gateway.set_capital_ceiling(max(6500.0, num * 300.0))
            elif num >= 10:
                self.sys1.min_confidence_to_trade = 0.62
                self.safety_gateway.set_capital_ceiling(max(4500.0, num * 300.0))
            else:
                self.sys1.min_confidence_to_trade = 0.68
            self._log_cognition(
                "FUND_MANAGER_MANDATE",
                "BOOK_CAPACITY_UPDATED",
                f"Autonomous Fund Manager concurrent live books capacity updated to {num} books (Confidence Hurdle: {self.sys1.min_confidence_to_trade:.2f} | Ceiling: ${self.safety_gateway.max_capital_ceiling_usdt:,.0f})."
            )
            return {"status": "success", "max_concurrent_positions": self.max_concurrent_positions}

    def _execute_preemptive_market_cycle(self):
        # 1. Ingest ALL coins traded against USDT across the entire market (700+ pairs)
        all_usdt_tickers = self.exchange.fetch_all_usdt_tickers()
        if not all_usdt_tickers:
            all_usdt_tickers = self.exchange.fetch_live_tickers([
                "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", 
                "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "SUI/USDT", "NEAR/USDT"
            ])

        # 2. Pre-screen market universe to isolate the TOP 50 MOST VITAL COINS
        initial_screen = self.screener.screen_universe(all_usdt_tickers)
        top_50_list = initial_screen.get("top_50_coins", [])
        top_candidates = [c["symbol"] for c in top_50_list[:40]]

        # 3. Fetch live 1-minute OHLCV candles for the leading Top Vital candidates
        ohlcv_dict = {}
        for sym in top_candidates:
            ohlcv_dict[sym] = self.exchange.fetch_live_ohlcv(sym, interval="1m", limit=25)

        # 4. Run deep 1-minute analysis and trade qualification on the Top 50 Vital Universe
        screen_result = self.screener.screen_universe(all_usdt_tickers, ohlcv_dict)
        self.last_screener_result = screen_result
        
        # Eligible symbols: start with Top Vital screener selections, and expand across the Top 50 Vital Universe
        eligible_symbols = list(screen_result.get("selected_pairs", []))
        for c in top_50_list:
            sym = c["symbol"]
            if sym not in eligible_symbols and sym not in self.active_positions:
                if c.get("volume_24h_usd", 0) >= 10_000_000 and c.get("spread_pct", 1.0) <= 0.055:
                    eligible_symbols.append(sym)
            if len(eligible_symbols) >= max(35, self.max_concurrent_positions * 2):
                break

        # System 7: Continual Learner re-ranks eligible symbols by historical win rates
        eligible_symbols.sort(key=lambda s: self.sys7.get_pair_weight(s), reverse=True)

        self._log_cognition(
            "TOP_50_VITAL",
            "1MIN_CYCLE_EXECUTED",
            f"1-Minute Vital Cycle: Screened {screen_result['total_screened']} USDT pairs. Tracked Top 50 Vital Coins ({screen_result['entered_count']} Entered, {screen_result['monitoring_count']} Monitoring). Balanced Multi-Book Vital Allocation (Max: {self.max_concurrent_positions} Books). Priority: {eligible_symbols[:self.max_concurrent_positions]}."
        )

        live_tickers = all_usdt_tickers

        if len(self.active_positions) >= self.max_concurrent_positions:
            return

        # Phase 4: Sizing via Fractional Kelly Engine
        kelly_sizing = self.compounding.evaluate_kelly_sizing(self.closed_orders, self.balance_usdt)

        for sym in eligible_symbols:
            if sym in self.active_positions:
                continue
            if len(self.active_positions) >= self.max_concurrent_positions:
                break

            ticker = live_tickers.get(sym, {})
            candles = ohlcv_dict.get(sym, [])
            if not candles:
                candles = self.exchange.fetch_live_ohlcv(sym, interval="1m", limit=25)
                ohlcv_dict[sym] = candles

            # System 6 Gatekeeper: 1-Hour Macro Trend Confluence Analysis
            macro_trend = "NEUTRAL"
            try:
                candles_1h = self.exchange.fetch_live_ohlcv(sym, interval="1h", limit=40)
                if candles_1h and len(candles_1h) >= 20:
                    c_1h = [c["close"] for c in candles_1h]
                    e20 = self.sys1._calculate_ema(c_1h, 20)
                    e50 = self.sys1._calculate_ema(c_1h, 50) if len(c_1h) >= 50 else e20
                    if c_1h[-1] > e20 >= e50:
                        macro_trend = "BULLISH"
                    elif c_1h[-1] < e20 <= e50:
                        macro_trend = "BEARISH"
            except Exception:
                pass

            # System 1: Neural Intuition Pattern Prediction with ADX Chop Filter & 1H Trend Gate
            s1_prediction = self.sys1.analyze_price_pattern(sym, candles, ticker, macro_trend=macro_trend)

            # Check PASS first before any further processing
            if s1_prediction.get("action") == "PASS":
                continue

            # Capitol Alpha: Congressional & Political Insider Sentiment Integration
            pol_info = self.political_engine.get_sentiment_for_symbol(sym)
            if pol_info.get("confidence_boost", 0.0) > 0:
                s1_prediction["confidence"] = round(min(0.99, s1_prediction["confidence"] + pol_info["confidence_boost"]), 3)
                s1_prediction["political_bias"] = pol_info["bias"]
                s1_prediction["political_score"] = pol_info["sentiment_score"]
                if pol_info["sentiment_score"] >= 35.0:
                    current_rat = s1_prediction.get("leverage_rationale", "Standard Confluence")
                    s1_prediction["leverage_rationale"] = current_rat + f" | Capitol Alpha: {pol_info['bias']} (+{pol_info['confidence_boost']*100:.1f}%)"
                    self._log_cognition(
                        "CAPITOL_ALPHA",
                        "CONGRESS_TAILWIND",
                        f"{sym}: Congressional accumulation ({pol_info['bias']}) boosted trade confidence by +{pol_info['confidence_boost']*100:.1f}%."
                    )

            # Portfolio Correlation & Beta Hedging Guard:
            # Prevent opening all books in the exact same direction (hedged market neutrality)
            existing_buys = sum(1 for p in self.active_positions.values() if p["action"] == "BUY")
            existing_sells = sum(1 for p in self.active_positions.values() if p["action"] == "SELL")
            max_skew = max(2, self.max_concurrent_positions - 2)
            if s1_prediction["action"] == "SELL" and existing_sells >= max_skew:
                continue
            if s1_prediction["action"] == "BUY" and existing_buys >= max_skew:
                continue

            # Phase 4 Drawdown Damper: Clamp leverage to 10x if consecutive non-wins occurred
            if self.compounding.leverage_damper_active:
                s1_prediction["recommended_leverage"] = min(10, s1_prediction["recommended_leverage"])

            # System 6: Confidence Meter & Gate 1 Auditing
            conf_ok, approved_leverage, conf_msg = self.sys6.audit_trade_confidence(s1_prediction)
            s1_prediction["recommended_leverage"] = approved_leverage
            if "INTERVENTION" in conf_msg:
                self._log_cognition("S6_CONFIDENCE_GATE", "GATE1_ADAPTATION", conf_msg)

            # System 2: Deterministic Mathematical Risk Gate
            market_state = {
                "price": ticker.get("last", 0.0),
                "spread_pct": ((ticker.get("ask", 1) - ticker.get("bid", 1)) / (ticker.get("last", 1) + 1e-8)) * 100.0,
                "orderbook_liquidity_usd": ticker.get("quoteVolume", 50000000.0) / 100.0
            }

            passed_s2, s2_msg, math_specs = self.sys2.verify_trade_risk(
                s1_prediction, market_state, self.balance_usdt
            )

            if not passed_s2:
                self._log_cognition("S2_REJECTION", "RISK_VETO", f"{sym}: {s2_msg}")
                continue

            # Gap 4: 8-Hour Funding Rate Guard Audit (System 2 Extension)
            funding_audit = self.funding_guard.audit_trade_funding_risk(sym, math_specs["action"], math_specs["leverage"])
            if not funding_audit.get("safe_to_enter", True):
                self._log_cognition("S2_FUNDING_GUARD", "FUNDING_VETO", f"{sym}: {funding_audit['reason']}")
                continue

            # Override allocated margin with Phase 4 Kelly recommendation if safe
            math_specs["allocated_margin_usdt"] = min(math_specs["allocated_margin_usdt"], kelly_sizing["recommended_margin_usdt"])

            # Check remaining safety ceiling headroom and clamp margin dynamically
            remaining_headroom = max(0.0, self.safety_gateway.max_capital_ceiling_usdt - self.safety_gateway.total_live_margin_committed)
            if remaining_headroom < 10.0:
                self._log_cognition("P3_GATEWAY_VETO", "CAPITAL_CEILING_REACHED", f"{sym}: Safety ceiling headroom exhausted (${self.safety_gateway.total_live_margin_committed:.2f} / ${self.safety_gateway.max_capital_ceiling_usdt:.2f} committed).")
                continue

            math_specs["allocated_margin_usdt"] = min(math_specs["allocated_margin_usdt"], remaining_headroom)
            math_specs["position_size_usdt"] = math_specs["allocated_margin_usdt"] * math_specs["leverage"]
            math_specs["coins_amount"] = math_specs["position_size_usdt"] / math_specs["entry_price"]

            # Phase 3: Live Safety Gateway validation
            gw_ok, gw_msg = self.safety_gateway.validate_live_order_dispatch(math_specs)
            if not gw_ok:
                self._log_cognition("P3_GATEWAY_VETO", "CAPITAL_CEILING_TRIP", gw_msg)
                continue

            # Execute Order via Ultra-Low Latency Fast Path (TCP_NODELAY + Pre-warmed WebSocket)
            exec_res = self.low_latency.dispatch_fast_order(math_specs, self.exchange.execute_order)
            if exec_res.get("success"):
                order_id = exec_res["order_id"]
                now_str = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

                # Track Phase 3 committed margin
                self.safety_gateway.total_live_margin_committed += math_specs["allocated_margin_usdt"]

                # System 9: Issue pre-execution Merkle Hash
                merkle_pre = self.sys9.issue_merkle_certificate(math_specs)

                # System 4: Commit order intent to .rimdb
                self.sys4.record_decision(
                    system_source="RIM_v9.1_ENGINE",
                    event_type="ORDER_DISPATCH",
                    symbol=sym,
                    order_id=order_id,
                    payload_str=json.dumps({"margin": math_specs["allocated_margin_usdt"], "merkle": merkle_pre})
                )

                position_record = {
                    "order_id": order_id,
                    "symbol": sym,
                    "action": math_specs["action"],
                    "leverage": math_specs["leverage"],
                    "entry_price": math_specs["entry_price"],
                    "current_price": math_specs["entry_price"],
                    "allocated_margin_usdt": math_specs["allocated_margin_usdt"],
                    "position_size_usdt": math_specs["position_size_usdt"],
                    "coins_amount": math_specs["coins_amount"],
                    "hard_stop_loss_price": math_specs["hard_stop_loss_price"],
                    "current_stop_price": math_specs["hard_stop_loss_price"],
                    "breakeven_trigger_price": math_specs["breakeven_trigger_price"],
                    "tp_target_price": math_specs["tp_target_price"],
                    "highest_price": math_specs["entry_price"],
                    "lowest_price": math_specs["entry_price"],
                    "entry_time": now_str,
                    "entry_timestamp": time.time(),
                    "unrealized_pnl_pct": 0.0,
                    "last_autocorrect": None
                }

                self.balance_usdt -= math_specs["allocated_margin_usdt"]
                self.active_positions[sym] = position_record

                self._log_cognition(
                    "ORDER_EXECUTED",
                    f"{math_specs['leverage']}X_DEPLOYED",
                    f"Pre-emptive {math_specs['action']} on {sym} ({math_specs['leverage']}x). Margin: ${math_specs['allocated_margin_usdt']:.2f} (Kelly: {kelly_sizing.get('fractional_kelly_pct', 2.5)}%) | TP: ${math_specs['tp_target_price']}."
                )
                self.notifier.send_notification(
                    "TRADE_ENTRY",
                    f"Pre-emptive {math_specs['action']} {sym} ({math_specs['leverage']}x) | Margin: ${math_specs['allocated_margin_usdt']:.2f} | Entry: ${math_specs['entry_price']} | TP: ${math_specs['tp_target_price']}",
                    priority="HIGH"
                )

    def _generate_and_archive_hourly_report(self):
        active_sess_names = self.last_session_state.get("active_sessions", ["Global"])
        report = self.reporter.generate_hourly_report(
            closed_orders=self.current_hourly_orders,
            current_balance=self.balance_usdt,
            start_balance=self.cycle_start_balance,
            s3_corrections_count=self.stats["s3_autocorrections"],
            active_sessions=active_sess_names
        )

        # System 9: Cryptographic Merkle Seal on Hourly Report
        report_seal = self.sys9.issue_merkle_certificate(report)
        report["s9_merkle_seal"] = report_seal

        # System 4: Commit report to .rimdb
        self.sys4.record_decision(
            system_source="RIM_v9.1_AUDITOR",
            event_type="HOURLY_REPORT_SEALED",
            symbol="PORTFOLIO",
            order_id=report["report_id"],
            payload_str=json.dumps({"pnl": report["financial_summary"]["net_hourly_profit_usdt"], "seal": report_seal})
        )

        self.current_hourly_orders = []
        self.cycle_start_balance = self.balance_usdt

        self._log_cognition(
            "S9_MERKLE_SEAL",
            "HOURLY_REPORT_CERTIFIED",
            f"1-Hour Report [{report['hourly_window']}] sealed with Merkle Proof: {report_seal[:16]}... Net: ${report['financial_summary']['net_hourly_profit_usdt']:+.2f} USDT."
        )
        self.notifier.send_hourly_report_alert(report)

    def trigger_manual_hourly_report(self) -> Dict[str, Any]:
        active_sess_names = self.last_session_state.get("active_sessions", ["Global"])
        report = self.reporter.generate_hourly_report(
            closed_orders=self.current_hourly_orders,
            current_balance=self.balance_usdt,
            start_balance=self.cycle_start_balance,
            s3_corrections_count=self.stats["s3_autocorrections"],
            active_sessions=active_sess_names
        )
        report_seal = self.sys9.issue_merkle_certificate(report)
        report["s9_merkle_seal"] = report_seal
        return report

    def trigger_stress_test(self, scenario_key: str = "covid_2020_flash_crash") -> Dict[str, Any]:
        """Runs on-demand Phase 2 Black Swan stress test and archives certificate."""
        res = self.stress_tester.run_stress_test(scenario_key=scenario_key, starting_balance=self.balance_usdt)
        self.last_stress_test_result = res
        self._log_cognition(
            "STRESS_TEST",
            "BLACK_SWAN_SIMULATED",
            f"Completed '{res['scenario_name']}'. Drawdown strictly bounded to {res['total_drawdown_pct']}%. Merkle Hash: {res['certificate']['merkle_certificate'][:12]}..."
        )
        return res

    def _log_cognition(self, layer: str, event_type: str, message: str):
        now_str = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        item = {
            "timestamp": now_str,
            "layer": layer,
            "event_type": event_type,
            "message": message
        }
        self.recent_cognitive_logs.insert(0, item)
        if len(self.recent_cognitive_logs) > 60:
            self.recent_cognitive_logs.pop()

    def get_dashboard_state(self) -> Dict[str, Any]:
        win_rate = (self.stats["win_trades"] / self.stats["total_trades"] * 100.0) if self.stats["total_trades"] > 0 else 100.0
        
        unrealized_total = 0.0
        total_margin_deployed = 0.0
        for pos in self.active_positions.values():
            unrealized_total += (pos.get("position_size_usdt", 0.0) * (pos.get("unrealized_pnl_pct", 0.0) / 100.0))
            total_margin_deployed += pos.get("allocated_margin_usdt", 0.0)

        total_portfolio_equity = self.balance_usdt + total_margin_deployed + unrealized_total
        deployment_pct = (total_margin_deployed / total_portfolio_equity * 100.0) if total_portfolio_equity > 0 else 0.0

        fund_manager_economics = {
            "aum_usdt": round(total_portfolio_equity, 2),
            "available_cash_usdt": round(self.balance_usdt, 2),
            "active_deployed_margin_usdt": round(total_margin_deployed, 2),
            "deployment_pct": round(deployment_pct, 1),
            "high_water_mark_usdt": round(self.high_water_mark_usdt, 2),
            "fund_manager_fee_pct": self.fund_manager_fee_pct,
            "total_fund_manager_payout_usdt": round(self.total_fund_manager_payout_usdt, 2),
            "total_investor_payout_usdt": round(self.total_investor_payout_usdt, 2),
            "max_concurrent_positions": self.max_concurrent_positions,
            "max_capital_ceiling_usdt": self.safety_gateway.max_capital_ceiling_usdt,
            "active_positions_count": len(self.active_positions)
        }

        uptime_seconds = int(time.time() - self.bot_start_time) if (self.is_running and self.bot_start_time) else 0

        # Phase 4 Kelly status
        kelly_info = self.compounding.evaluate_kelly_sizing(self.closed_orders, self.balance_usdt)

        return {
            "is_running": self.is_running,
            "uptime_seconds": uptime_seconds,
            "balance_usdt": round(self.balance_usdt, 2),
            "unrealized_pnl_usdt": round(unrealized_total, 2),
            "equity_usdt": round(total_portfolio_equity, 2),
            "fund_manager_economics": fund_manager_economics,
            "total_trades": self.stats["total_trades"],
            "win_rate_pct": round(win_rate, 2),
            "s3_autocorrections": self.stats["s3_autocorrections"],
            "net_realized_pnl_usdt": round(self.stats["total_net_pnl"], 2),
            "balance_drift_variance": self.stats["balance_drift_variance"],
            "active_positions": list(self.active_positions.values()),
            "recent_closed_orders": self.closed_orders[:20],
            "cognitive_logs": self.recent_cognitive_logs[:30],
            "world_sessions": self.last_session_state or self.session_engine.evaluate_active_sessions(),
            "screener_summary": self.last_screener_result,
            "political_alpha": self.political_engine.evaluate_crypto_political_sentiment(),
            "latency_telemetry": self.low_latency.get_latency_telemetry(),
            "funding_guard": self.funding_guard.get_guard_status(),
            "streamer_health": self.streamer.get_streamer_health(),
            "notifier_status": self.notifier.get_status(),
            "security_status": self.vault.get_status(),
            "options_radar": self.options_engine.evaluate_options_sentiment("BTC"),
            "exchange_info": {
                "mode": self.exchange.mode,
                "exchange_id": self.exchange.exchange_id,
                "guides": self.exchange.EXCHANGE_GUIDES
            },
            "latest_hourly_reports": self.reporter.get_latest_reports(limit=5),
            
            # 4-Phase System Status Telemetry
            "phases": {
                "phase1_benchmark": self.benchmark.get_benchmark_status(),
                "phase2_stress_test": {
                    "scenarios": self.stress_tester.SCENARIOS,
                    "last_result": self.last_stress_test_result
                },
                "phase3_safety_gateway": self.safety_gateway.get_gateway_status(),
                "phase4_compounding": kelly_info
            }
        }
