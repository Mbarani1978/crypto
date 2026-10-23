# RIM Cognitive Crypto Exchange Automatic Trading Robot

An enterprise-grade, 24x7 autonomous crypto trading robot powered by the **RIM Tri-System AI Cognitive Brain Architecture**.

---

## 🌟 Key Functional Highlights

1. **Market Price Movement & Trend Analysis**:
   - Multi-timeframe trend momentum analysis (1m, 5m, 15m) using EMA crossovers (EMA 9 / 21), RSI momentum divergence, and Bollinger Band volatility squeeze.
2. **1-Minute Pre-Emptive Execution**:
   - Analyzes pattern confluence 15 seconds prior to 1-minute candle close, deploying buy/sell orders ahead of the crowd before the minute concludes.
3. **USDT as Base Currency**:
   - Universal quotes across all pairs against USDT (`BTC/USDT`, `ETH/USDT`, `SOL/USDT`, `BNB/USDT`, `XRP/USDT`, `DOGE/USDT`, `ADA/USDT`, `AVAX/USDT`, `SUI/USDT`, `NEAR/USDT`, etc.).
4. **Dynamic 10x, 50x, and 100x Leverage**:
   - **10x Leverage**: Deployed during standard baseline trend continuations (Score: 0.65 – 0.79).
   - **50x Leverage**: Deployed during high-momentum breakouts with aligned EMAs & RSI (Score: 0.80 – 0.91).
   - **100x Leverage**: Pin-point deployment on Grade-A Bollinger Band squeeze expansions + volume surges (> 1.3x) (Score > 0.91).
5. **Zero / Minimal-Loss Protection Mandate**:
   - **Guaranteed Breakeven Stop**: When price reaches +0.12% profit, stop-loss automatically elevates to entry price + 0.06% (locking in guaranteed non-negative return).
   - **Accelerated Trailing Stop**: Locks in 80% of peak unrealized profit as the trade advances.
   - **Hard Micro-Stop**: Maximum risk strictly bounded per leverage tier.
6. **World Peak Timezones Tracking Engine**:
   - Monitors active global sessions and calculates dynamic market aggression multipliers:
     - **US (New York / CME)**: 13:30 – 20:00 UTC
     - **UK (London / Europe)**: 08:00 – 16:30 UTC
     - **Dubai (UAE)**: 06:00 – 14:00 UTC
     - **Hong Kong**: 01:30 – 08:00 UTC
     - **Singapore**: 01:00 – 09:00 UTC
     - **Australia (Sydney)**: 22:00 – 06:00 UTC
     - **Brazil (Sao Paulo / B3)**: 13:00 – 21:00 UTC
     - Detects **Transatlantic Mega-Overlaps** and **Asia-Pacific Convergence** windows.
7. **1-Hour Automated Performance & Calculation Audit Reports**:
   - Automatically generated every 60 minutes.
   - Exact mathematical breakdown for every single order:
     - Entry Price, Exit Price, Side, Leverage (10x, 50x, 100x)
     - Initial Margin, Position Notional Size
     - Price Delta %, Gross PnL, Exchange Trading Fees, Net PnL, ROI %
     - System 3 Anomaly Defense status.
8. **Self-Correction (S3 Neuroplastic Auto-Correction)**:
   - Detects adverse wicks, flash spikes, and sudden orderbook vacuums in sub-second intervals.
   - Executes defensive early exit or moves stops before losses can expand.
9. **24x7 Autonomous Operation (Human Intervention ONLY for ON / OFF)**:
   - Master Control Switch: Turn ON to engage 24x7 autonomous trading; Turn OFF to safely pause.
   - Bot operates completely unsupervised in the background.
10. **Smart Coin Screener (Enter vs Leave Out)**:
    - Ranks candidate coins by 24h volume (> $20M), bid-ask spread (< 0.038%), and chop index.
    - Selects prime coins for trade entry while filtering out illiquid or choppy pairs.
11. **Multi-Exchange Compatibility**:
    - Supports **Binance**, **Bybit**, **OKX**, **Coinbase Advanced**, **KuCoin**, and **Bitget** via unified CCXT.
    - Includes **Live Public Feeds Simulation Mode** (runs out of the box with real-time live market ticks without needing API keys).

---

## 🧠 The RIM Brain Architecture

```
                  ┌──────────────────────────────────────────────┐
                  │          UNSTRUCTURED MARKET DATA            │
                  │   (Live Tickers, 1m OHLCV, Orderbook Depth)  │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
   ┌────────────────────────────────────────────────────────────────────────────┐
   │                       SYSTEM 1: NEURAL INTUITION                           │
   │  • Multi-timeframe trend extraction (EMA 9/21, RSI 14, BB Squeeze)         │
   │  • 1-minute pre-emptive candle trajectory prediction                       │
   │  • Leverage assignment (10x / 50x / 100x based on confluence score)        │
   └─────────────────────────────────────┬──────────────────────────────────────┘
                                         │  (Proposed Trade Action & Leverage)
                                         ▼
   ┌────────────────────────────────────────────────────────────────────────────┐
   │                   SYSTEM 2: DETERMINISTIC LOGIC ENGINE                     │
   │  • Zero/Minimal-Loss Mathematical Risk Verification                        │
   │  • Max spread check (< 0.038%) & Slippage gate                             │
   │  • Liquidation price calculation & dynamic margin allocation               │
   │  • Hard Micro Stop-Loss & Breakeven Trigger Assignment                     │
   └─────────────────────────────────────┬──────────────────────────────────────┘
                                         │  (Approved Order Specs)
                                         ▼
   ┌────────────────────────────────────────────────────────────────────────────┐
   │                 SYSTEM 3: META-COGNITIVE AUTO-CORRECTOR                    │
   │  • Continuous sub-second position trajectory supervisor                    │
   │  • Dynamic Breakeven Lock (+0.12% move -> SL moved to Entry + 0.06%)       │
   │  • Accelerated Profit Trailing (locks in 80% of peak gains)                │
   │  • Adverse Wick / Flash Impulse Cut (Emergency Zero-Loss Exit)             │
   │  • Real-time parameter rewrites and volatility self-healing                │
   └────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 How to Run the Web Application

1. **Start the Web App Server**:
   ```powershell
   python crypto_robot/app.py
   ```
2. **Access the Web Dashboard**:
   Open your browser to:
   ```
   http://localhost:5055
   ```
3. **Control**:
   - Click the green **"TURN BOT ON"** button in the header. The bot begins autonomous 24x7 analysis and execution.
   - To stop, simply click **"TURN BOT OFF"**.

---

## 🔑 Step-by-Step Guide: How to Get Exchange API Keys

### Binance
1. Log in to your Binance account on desktop.
2. Click your **Profile** icon -> navigate to **API Management**.
3. Click **Create API** -> Select **System generated API Key**.
4. Name the key label (e.g., `RIM-Crypto-Trading-Robot`).
5. Complete 2FA (Email, SMS, or Google Authenticator).
6. Click **Edit Restrictions**:
   - Check **Enable Reading**
   - Check **Enable Spot & Margin Trading**
   - Check **Enable Futures** (required for 10x, 50x, 100x leverage)
   - **CRITICAL**: Ensure **Enable Withdrawals** is **UNCHECKED**.
7. Enable **IP Whitelisting** (Recommended: add your host IP).
8. Copy the **API Key** and **Secret Key** into the bot's Exchange Setup tab.

### Bybit
1. Log in to Bybit -> Click Profile -> **API**.
2. Click **Create New Key** -> **System-generated API Keys**.
3. Select **API Transaction** type.
4. Set permissions to **Read-Write**.
5. Check **Contract: Orders & Positions** and **Spot: Trade**.
6. Ensure **Assets - Transfer / Withdraw** is **DISABLED**.
7. Submit 2FA and copy your API Key and Secret.

### OKX
1. Log in to OKX -> Profile -> **API Keys**.
2. Click **Create V5 API Key**.
3. Enter API Name and choose a custom **Passphrase**.
4. Select **Read** and **Trade** permissions. Leave **Withdraw** unticked.
5. Save API Key, Secret, and Passphrase.

### Coinbase Advanced
1. Log in to Coinbase -> **Settings** -> **API** / **Developer Platform**.
2. Click **Create API Key**.
3. Assign permissions: `wallet:trades:create`, `wallet:accounts:read`.
4. Ensure fund transfers are disabled.
5. Save your API credentials securely.

### KuCoin
1. Log in to KuCoin -> Profile -> **API Management**.
2. Click **Create API** -> Select **Futures / Spot Trading**.
3. Set your custom **API Passphrase**.
4. Check **General** and **Trade** permissions; disable **Transfer**.
5. Complete 2FA and save your keys.
