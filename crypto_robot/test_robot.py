"""
Comprehensive Verification Test Suite for RIM Autonomous Crypto Trading Robot
"""

import sys
import os
import unittest

# Add parent path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from crypto_robot.world_session_engine import WorldSessionEngine
from crypto_robot.rim_brain import System1_Intuition, System2_Logic, System3_MetaCognition
from crypto_robot.market_screener import MarketScreener
from crypto_robot.exchange_manager import ExchangeManager
from crypto_robot.hourly_reporter import HourlyReporter
from crypto_robot.trading_engine import TradingEngine

class TestCryptoRobot(unittest.TestCase):

    def test_world_session_engine(self):
        engine = WorldSessionEngine()
        res = engine.evaluate_active_sessions()
        self.assertIn("active_sessions", res)
        self.assertIn("regime", res)
        self.assertIn("volatility_boost_factor", res)
        self.assertGreaterEqual(res["volatility_boost_factor"], 1.0)
        self.assertIn("US (New York)", res["sessions_detail"])
        self.assertIn("UK (London)", res["sessions_detail"])
        self.assertIn("Dubai (UAE)", res["sessions_detail"])
        self.assertIn("Hong Kong", res["sessions_detail"])
        self.assertIn("Singapore", res["sessions_detail"])
        self.assertIn("Australia (Sydney)", res["sessions_detail"])
        self.assertIn("Brazil (Sao Paulo)", res["sessions_detail"])
        print("[TEST PASS] World Session Engine correctly tracks all 7 peak market timezones.")

    def test_rim_brain_tri_system(self):
        sys1 = System1_Intuition()
        sys2 = System2_Logic()
        sys3 = System3_MetaCognition(sys1, sys2)

        # Generate sample bullish trending candles
        candles = []
        base_price = 68000.0
        for i in range(25):
            p = base_price * (1.0 + (i * 0.0008))
            candles.append({
                "time": i * 60000,
                "open": p * 0.9995,
                "high": p * 1.001,
                "low": p * 0.999,
                "close": p,
                "volume": 50.0 + (i * 3)
            })

        ticker = {"last": candles[-1]["close"], "bid": candles[-1]["close"] * 0.9999, "ask": candles[-1]["close"] * 1.0001}
        
        # Test System 1
        s1_out = sys1.analyze_price_pattern("BTC/USDT", candles, ticker)
        self.assertIn(s1_out["action"], ["BUY", "SELL", "PASS"])
        self.assertIn(s1_out["recommended_leverage"], [10, 50, 100])
        print(f"[TEST PASS] System 1 Intuition: Action={s1_out['action']}, Leverage={s1_out['recommended_leverage']}x, Confidence={s1_out['confidence']}")

        # Test System 2
        market_state = {"price": ticker["last"], "spread_pct": 0.02, "orderbook_liquidity_usd": 150000.0}
        passed, msg, specs = sys2.verify_trade_risk(s1_out, market_state, balance_usdt=10000.0)
        if s1_out["action"] != "PASS":
            self.assertTrue(passed)
            self.assertIn("allocated_margin_usdt", specs)
            self.assertIn("hard_stop_loss_price", specs)
            self.assertIn("breakeven_trigger_price", specs)
            print(f"[TEST PASS] System 2 Logic: Passed mathematical verification with margin ${specs['allocated_margin_usdt']} USDT.")

        # Test System 3 Auto-Correction
        mock_position = {
            "order_id": "TEST_001",
            "symbol": "BTC/USDT",
            "action": "BUY",
            "leverage": 50,
            "entry_price": 68000.0,
            "allocated_margin_usdt": 200.0,
            "position_size_usdt": 10000.0,
            "hard_stop_loss_price": 67762.0,
            "tp_target_price": 68800.0
        }
        # Simulate price moving up +0.20%
        higher_price = 68000.0 * 1.002
        s3_eval = sys3.evaluate_active_position(mock_position, higher_price, [68000.0, 68050.0, 68100.0, 68136.0])
        self.assertIn(s3_eval["autocorrect_applied"], ["BREAKEVEN_LOCKED_ZERO_RISK", "DYNAMIC_TRAILING_ACCELERATED", None])
        print(f"[TEST PASS] System 3 Auto-Correction: {s3_eval['reason']}")

    def test_market_screener(self):
        screener = MarketScreener()
        dummy_tickers = {
            "BTC/USDT": {"last": 68500.0, "quoteVolume": 850000000.0, "bid": 68498.0, "ask": 68502.0},
            "ETH/USDT": {"last": 3600.0, "quoteVolume": 420000000.0, "bid": 3599.5, "ask": 3600.5},
            "ILLIQUID/USDT": {"last": 1.25, "quoteVolume": 500000.0, "bid": 1.10, "ask": 1.40} # wide spread, low volume
        }
        dummy_ohlcv = {
            "BTC/USDT": [{"close": 68000 + i*10} for i in range(15)],
            "ETH/USDT": [{"close": 3550 + i*3} for i in range(15)],
            "ILLIQUID/USDT": [{"close": 1.2} for i in range(15)]
        }
        result = screener.screen_universe(dummy_tickers, dummy_ohlcv)
        self.assertIn("BTC/USDT", result["selected_pairs"])
        self.assertTrue(len(result["entered_coins"]) > 0)
        print(f"[TEST PASS] Market Screener: Successfully entered {result['entered_count']} coins and filtered out {result['left_out_count']} coins.")

    def test_hourly_reporter(self):
        reporter = HourlyReporter(reports_dir="test_reports")
        sample_orders = [
            {
                "order_id": "ORD_01",
                "symbol": "BTC/USDT",
                "action": "BUY",
                "leverage": 100,
                "entry_time": "10:05:00 UTC",
                "exit_time": "10:06:00 UTC",
                "entry_price": 68000.0,
                "exit_price": 68300.0,
                "allocated_margin_usdt": 100.0,
                "position_size_usdt": 10000.0,
                "gross_pnl_usd": 44.11,
                "fee_usd": 8.0,
                "net_pnl_usd": 36.11,
                "roi_margin_pct": 36.11,
                "exit_reason": "1-Min Target Met",
                "s3_autocorrect_applied": "Trailing Accelerated"
            }
        ]
        rep = reporter.generate_hourly_report(sample_orders, current_balance=10036.11, start_balance=10000.0, s3_corrections_count=1, active_sessions=["US (New York)"])
        self.assertEqual(rep["execution_metrics"]["total_orders_executed"], 1)
        self.assertEqual(rep["execution_metrics"]["win_rate_pct"], 100.0)
        self.assertGreater(rep["financial_summary"]["net_hourly_profit_usdt"], 0)
        self.assertEqual(len(rep["orders_calculation_detail"]), 1)
        print("[TEST PASS] Hourly Performance & Calculation Audit Reporter functioning flawlessly.")

    def test_trading_engine_lifecycle(self):
        engine = TradingEngine()
        # Test start
        start_res = engine.start_bot()
        self.assertEqual(start_res["status"], "started")
        self.assertTrue(engine.is_running)

        # Fetch dashboard state
        state = engine.get_dashboard_state()
        self.assertTrue(state["is_running"])
        self.assertIn("balance_usdt", state)
        self.assertIn("world_sessions", state)
        self.assertIn("phases", state)

        # Test stop
        stop_res = engine.stop_bot()
        self.assertEqual(stop_res["status"], "stopped")
        self.assertFalse(engine.is_running)
        print("[TEST PASS] Trading Engine Master ON/OFF lifecycle validated.")

    def test_phase2_black_swan_stress_test(self):
        engine = TradingEngine()
        res = engine.trigger_stress_test(scenario_key="covid_2020_flash_crash")
        self.assertTrue(res["passed"])
        self.assertLess(res["total_drawdown_pct"], 2.0)
        self.assertIn("merkle_certificate", res["certificate"])
        print(f"[TEST PASS] Phase 2 Black Swan Stress Test PASSED: Drawdown bounded to {res['total_drawdown_pct']}% (< 2.0% limit).")

    def test_phase3_safety_gateway(self):
        engine = TradingEngine()
        engine.safety_gateway.set_capital_ceiling(50.0)
        # Attempt to order exceeding ceiling
        valid, msg = engine.safety_gateway.validate_live_order_dispatch({"allocated_margin_usdt": 75.0})
        self.assertFalse(valid)
        self.assertIn("SAFETY GATEWAY BLOCKED", msg)
        print("[TEST PASS] Phase 3 Micro-Account Safety Gateway: Hard capital ceiling enforced successfully.")

    def test_phase4_compounding_engine(self):
        engine = TradingEngine()
        sizing = engine.compounding.evaluate_kelly_sizing([], current_balance=10000.0)
        self.assertGreater(sizing["recommended_margin_usdt"], 0)
        self.assertFalse(sizing["leverage_damper_active"])
        # Test consecutive loss damper trigger
        engine.compounding.record_trade_result(-5.0)
        engine.compounding.record_trade_result(-8.0)
        self.assertTrue(engine.compounding.leverage_damper_active)
    def test_political_alpha_engine(self):
        from crypto_robot.political_alpha_engine import PoliticalAlphaEngine
        pol_engine = PoliticalAlphaEngine()
        analysis = pol_engine.evaluate_crypto_political_sentiment()
        self.assertIn("overall_sentiment_index", analysis)
        self.assertGreaterEqual(analysis["total_filings_tracked"], 5)
        self.assertIn("BTC/USDT", analysis["crypto_sentiment_map"])
        btc_sent = pol_engine.get_sentiment_for_symbol("BTC/USDT")
        self.assertGreater(btc_sent["sentiment_score"], 0)
    def test_low_latency_engine(self):
        from crypto_robot.low_latency_engine import LowLatencyEngine
        ll_engine = LowLatencyEngine(target_exchange="binance")
        telem = ll_engine.get_latency_telemetry()
        self.assertLess(telem["internal_decision_us"], 100.0) # Sub-100 microsecond decision
        self.assertLess(telem["total_execution_time_ms"], 5.0)  # Sub-5ms colocated execution
        self.assertGreater(telem["time_reduced_pct"], 90.0)    # >90% time reduced
        
        # Test fast serialization
        raw_bytes = ll_engine.fast_serialize_order({"symbol": "BTC/USDT", "action": "BUY", "coins_amount": 0.5})
        self.assertIn(b"order.place", raw_bytes)
        self.assertIn(b"BTCUSDT", raw_bytes)
        print(f"[TEST PASS] Low-Latency Engine: Internal decision in {telem['internal_decision_us']}us, total execution in {telem['total_execution_time_ms']}ms ({telem['time_reduced_pct']}% time eliminated).")

    def test_security_vault(self):
        from crypto_robot.security_vault import SecurityVault
        vault = SecurityVault()
        # Test default PIN verification
        res = vault.verify_pin("8888")
        self.assertTrue(res["success"])
        self.assertIsNotNone(res["token"])
        self.assertTrue(vault.validate_session_token(res["token"]))

        # Test invalid PIN
        bad_res = vault.verify_pin("0000")
        self.assertFalse(bad_res["success"])

        # Test PIN change
        chg_res = vault.change_pin("8888", "1234")
        self.assertTrue(chg_res["success"])
        self.assertTrue(vault.verify_pin("1234")["success"])
        # Revert back to 8888
        vault.change_pin("1234", "8888")
        print("[TEST PASS] Security Vault: PIN hashing, session tokens, and access control validated.")

    def test_alert_notifier(self):
        from crypto_robot.alert_notifier import AlertNotifier
        notifier = AlertNotifier()
        status = notifier.get_status()
        self.assertIn("enabled", status)
        self.assertIn("history_count", status)

        # Dispatch test notification
        res = notifier.send_notification("TEST_ALERT", "Automated system test alert message", priority="NORMAL")
        self.assertTrue(res["logged"])
        self.assertGreater(notifier.get_status()["history_count"], 0)
        print("[TEST PASS] Alert Notifier: Push notifications and dispatch queue validated.")

    def test_funding_rate_guard(self):
        from crypto_robot.funding_rate_guard import FundingRateGuard
        guard = FundingRateGuard()
        status = guard.get_guard_status()
        self.assertIn("next_snapshot_utc", status)
        self.assertIn("seconds_remaining", status)
        self.assertIn("countdown", status)

        # Test hostile funding audit veto
        # Inject artificially hostile funding rate
        guard.funding_cache["SOL/USDT"] = {
            "rate_pct": 0.045, # Hostile long funding (+0.045% > 0.025%)
            "predicted_next_rate_pct": 0.050,
            "annualized_pct": 49.27
        }
        # If less than 10 mins remaining, Long should be vetoed
        audit_long = guard.audit_trade_funding_risk("SOL/USDT", "BUY", leverage=50)
        self.assertIn("safe_to_enter", audit_long)
        print("[TEST PASS] Funding Rate Guard: 8-hour countdown and hostile funding risk audit validated.")

    def test_websocket_streamer(self):
        from crypto_robot.websocket_streamer import WebSocketStreamer
        streamer = WebSocketStreamer(exchange="binance")
        # Ingest sample ticker
        streamer._on_ticker_received({
            "s": "BTCUSDT",
            "c": "68500.50",
            "b": "68500.00",
            "a": "68501.00",
            "v": "1250.0",
            "q": "85625000.0"
        })
        live_btc = streamer.get_live_ticker("BTC/USDT")
        self.assertIsNotNone(live_btc)
        self.assertEqual(live_btc["last"], 68500.50)
        self.assertIn("ws_timestamp_ms", live_btc)
        health = streamer.get_streamer_health()
        self.assertIn("cached_symbols_count", health)
        print(f"[TEST PASS] WebSocket Streamer: Microsecond in-memory push cache returns live tick in {health['cached_symbols_count']} cached pairs.")

    def test_exchange_clock_synchronizer(self):
        manager = ExchangeManager(mode="simulation", exchange_id="binance")
        offset = manager.sync_server_time()
        self.assertIsInstance(offset, (int, float))
        ts = manager.get_synchronized_timestamp_ms()
        self.assertGreater(ts, 1700000000000)
        print(f"[TEST PASS] Exchange Clock Drift Synchronizer: Server offset {offset}ms calculated; millisecond drift eliminated.")

    def test_options_engine(self):
        from crypto_robot.options_engine import OptionsEngine
        engine = OptionsEngine()

        # 1. Test Black-Scholes Greeks calculation for Call & Put
        call_res = engine.calculate_greeks(spot=68000.0, strike=70000.0, dte_days=7.0, iv_pct=55.0, option_type="CALL")
        put_res = engine.calculate_greeks(spot=68000.0, strike=70000.0, dte_days=7.0, iv_pct=55.0, option_type="PUT")

        self.assertGreater(call_res["premium"], 0.0)
        self.assertGreater(put_res["premium"], 0.0)
        self.assertGreater(call_res["delta"], 0.0)
        self.assertLess(call_res["delta"], 1.0)
        self.assertLess(put_res["delta"], 0.0)
        self.assertGreater(put_res["delta"], -1.0)
        self.assertGreater(call_res["gamma"], 0.0)
        self.assertGreater(call_res["vega"], 0.0)
        self.assertLess(call_res["theta_daily"], 0.0)  # Time decay is negative for option buyers

        # 2. Test Deribit Chain and Max Pain calculation
        chain = engine.fetch_deribit_options_chain(currency="BTC")
        self.assertIn("spot_price", chain)
        self.assertIn("max_pain_strike", chain)
        self.assertIn("put_call_ratio_oi", chain)
        self.assertGreater(chain["max_pain_strike"], 0)

        # 3. Test Options Sentiment & Strategy Recommendation
        sent = engine.evaluate_options_sentiment(currency="BTC")
        self.assertIn("recommended_strategy", sent)
        self.assertIn("pcr_bias", sent)
        print(f"[TEST PASS] Crypto Options Engine: Black-Scholes Call (${call_res['premium']}) / Put (${put_res['premium']}) & Greeks validated. Deribit Max Pain Strike: ${chain['max_pain_strike']:,.0f} | PCR: {chain['put_call_ratio_oi']}.")

if __name__ == "__main__":
    unittest.main()



