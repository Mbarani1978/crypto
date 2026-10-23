"""
RIM Autonomous Crypto Robot - Web Application Server
Flask web server powering the 24x7 autonomous crypto trading terminal.
Exposes clean REST APIs for:
- Master Bot Control (Turn ON / Turn OFF)
- Real-time Dashboard State (telemetry, positions, orders, screener, world peak timezones, 4-phase metrics)
- Phase 2 Black Swan Stress Test Execution
- Phase 3 Capital Ceiling Configuration
- 1-Hour Report Compilation & Calculations
- Exchange API Connector configuration (Binance, Bybit, OKX, Coinbase, KuCoin)
"""

import os
import sys
from flask import Flask, render_template, jsonify, request

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from crypto_robot.trading_engine import TradingEngine

app = Flask(__name__, template_folder=os.path.join(current_dir, "templates"))
engine = TradingEngine()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(engine.get_dashboard_state())

@app.route("/api/bot/start", methods=["POST"])
def start_bot():
    res = engine.start_bot()
    return jsonify(res)

@app.route("/api/bot/stop", methods=["POST"])
def stop_bot():
    res = engine.stop_bot()
    return jsonify(res)

@app.route("/api/exchange/configure", methods=["POST"])
def configure_exchange():
    data = request.get_json() or {}
    mode = data.get("mode", "simulation")
    exchange_id = data.get("exchange_id", "binance")
    api_key = data.get("api_key", "").strip()
    secret = data.get("secret", "").strip()
    passphrase = data.get("passphrase", "").strip()

    res = engine.set_exchange_config(
        mode=mode,
        exchange_id=exchange_id,
        api_key=api_key,
        secret=secret,
        passphrase=passphrase
    )
    return jsonify(res)

@app.route("/api/stress-test/run", methods=["POST"])
def run_stress_test():
    data = request.get_json() or {}
    scenario = data.get("scenario", "covid_2020_flash_crash")
    res = engine.trigger_stress_test(scenario_key=scenario)
    return jsonify(res)

@app.route("/api/safety/ceiling", methods=["POST"])
def set_capital_ceiling():
    data = request.get_json() or {}
    ceiling = float(data.get("ceiling_usdt", 100.0))
    engine.safety_gateway.set_capital_ceiling(ceiling)
    return jsonify({"status": "success", "new_ceiling_usdt": engine.safety_gateway.max_capital_ceiling_usdt})

@app.route("/api/reports/trigger", methods=["POST"])
def trigger_report():
    report = engine.trigger_manual_hourly_report()
    return jsonify({"status": "success", "report": report})

@app.route("/api/reports/list", methods=["GET"])
def list_reports():
    reports = engine.reporter.get_latest_reports(limit=20)
    return jsonify({"reports": reports})

# --- Production Gap Fix Endpoints: Auth, Alerting, Candlesticks ---

@app.route("/api/auth/verify", methods=["POST"])
def verify_auth_pin():
    data = request.get_json() or {}
    pin = data.get("pin", "")
    res = engine.vault.verify_pin(pin)
    return jsonify(res)

@app.route("/api/auth/pin", methods=["POST"])
def change_auth_pin():
    data = request.get_json() or {}
    old_pin = data.get("old_pin", "")
    new_pin = data.get("new_pin", "")
    res = engine.vault.change_pin(old_pin, new_pin)
    return jsonify(res)

@app.route("/api/notifier/configure", methods=["POST"])
def configure_notifier():
    data = request.get_json() or {}
    tg_token = data.get("telegram_token", "")
    tg_chat = data.get("telegram_chat_id", "")
    discord = data.get("discord_webhook", "")
    enabled = data.get("enabled", True)
    res = engine.notifier.configure(
        telegram_token=tg_token,
        telegram_chat_id=tg_chat,
        discord_webhook_url=discord,
        enabled=enabled
    )
    return jsonify(res)

@app.route("/api/notifier/test", methods=["POST"])
def test_notifier():
    res = engine.notifier.send_test_alert()
    return jsonify(res)

@app.route("/api/chart/candles", methods=["GET"])
def get_chart_candles():
    sym = request.args.get("symbol", "BTC/USDT")
    limit = int(request.args.get("limit", 30))
    candles = engine.exchange.fetch_live_ohlcv(sym, interval="1m", limit=limit)
    return jsonify({"symbol": sym, "candles": candles})

@app.route("/api/options/chain", methods=["GET"])
def get_options_chain():
    currency = request.args.get("currency", "BTC").upper()
    data = engine.options_engine.evaluate_options_sentiment(currency=currency)
    return jsonify(data)

@app.route("/api/order/manual", methods=["POST"])
def place_manual_order():
    data = request.get_json() or {}
    symbol = data.get("symbol", "BTC/USDT")
    action = data.get("action", "BUY").upper()
    leverage = int(data.get("leverage", 10))
    margin = float(data.get("margin_usdt", 100.0))
    res = engine.place_manual_order(symbol=symbol, action=action, leverage=leverage, margin_usdt=margin)
    return jsonify(res)

@app.route("/api/order/close", methods=["POST"])
def close_order():
    data = request.get_json() or {}
    symbol = data.get("symbol", "")
    res = engine.manual_close_position(symbol=symbol)
    return jsonify(res)

@app.route("/api/config/books", methods=["POST"])
def set_books_capacity():
    data = request.get_json() or {}
    books = int(data.get("max_books", 6))
    res = engine.set_max_concurrent_positions(books)
    return jsonify(res)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5055))
    print(f"============================================================")
    print(f"  RIM CRYPTO AUTONOMOUS TRADING ROBOT WEB APP STARTED")
    print(f"  Access UI at: http://localhost:{port}")
    print(f"============================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
