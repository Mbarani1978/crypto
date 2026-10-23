# Autonomous Crypto Trading Terminal (Dynamic Trailing Engine)

An enterprise-grade autonomous crypto trading terminal with real-time exchange connectivity, pre-emptive market screening across 700+ pairs, low-latency execution, and institutional risk management.

---

## Key Features

- **Dynamic Chandelier Trailing Exit**: Volatility-scaled trailing stops ($1.8\times \text{ATR}$) that ratchet behind market peaks with super-runner profit harvesting.
- **Micro-Account Safety Gateway**: Hard capital ceilings, micro-slippage auditor, and zero-liquidation 2x leverage constraint.
- **Pre-Emptive Market Screener**: Continuously monitors top volume pairs for ADX volatility momentum and 1-hour macro trend clearance.
- **Multi-Exchange Compatibility**: Powered by CCXT (Binance, Bybit, OKX, Coinbase, KuCoin) with unified order execution and offsetting market closes.
- **Real-Time Interactive Terminal**: Web-based dashboard (`http://127.0.0.1:5055`) featuring live blotter, real-time equity curves, stress test console, and mobile push alerts.

---

## Quick Start

### 1. Installation
```bash
git clone https://github.com/Mbarani1978/crypto.git
cd crypto
pip install -r requirements.txt
```

### 2. Launch Terminal
```bash
python run.py
```
Open your browser at `http://127.0.0.1:5055` to view the live trading dashboard.

### 3. Execution Modes
- **Real-Time Simulation (Default)**: Connects to authentic Binance live market tick streams with zero risk virtual capital.
- **Live Exchange Trading**: Connect your Binance, Bybit, or OKX API Key & Secret with Futures permissions enabled. Withdrawals should always remain disabled.

---

## Security & Architecture
- **Secured Engine**: Core predictive heuristics and cognitive auditing modules are compiled into standalone bytecode distributions.
- **Zero-Drift Accounting**: Built-in financial conservation solvers verify equity and fee balance invariants on every closed trade.
