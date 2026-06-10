<h1 align="center">Hi, I'm Aileen 👋</h1>

<p align="center">
  Solana / DeFi research · prop-AMM &amp; MEV simulation · on-chain trading bots · AI agents
</p>

---

## ⭐ KeyShield — *spec-driven*

> **[keyshield](https://github.com/lilaclilac09/keyshield)** — *"iCloud Keychain for your API keys."* A zero-knowledge vault that stores API keys as ciphertext, hands agents **scoped session tokens** instead of raw keys, and accelerates calls through a Rust proxy.

🔗 [Live site](https://keyshield-sync-worker.vercel.app) · 📄 [SPEC.md](https://github.com/lilaclilac09/keyshield/blob/main/SPEC.md) · 📝 [Build & spec-driven write-up →](https://github.com/lilaclilac09/lilaclilac09/blob/main/keyshield-process.md)

- 🔐 Zero-knowledge — AES-256-GCM in the browser; the server only ever stores ciphertext
- 🎫 Scoped delegation — agents get `ksv2_…` tokens with per-agent scopes, spend caps, expiry
- ⚡ Fast — Rust proxy, two-tier cache + single-flight dedup, ~50–80 ms hot path
- 🛣️ In design — x402 pay-per-call so `spend_cap_usd` becomes a hard, autonomous budget

`TypeScript` · `Rust` · `Python` · MCP · Solana

---

## 🌊 Solana Prop-AMM & MEV

- **[pamm-a](https://github.com/lilaclilac09/pamm-a)** — research & implementation sandbox for prop AMMs, market making, and Solana simulation
- **[solana-pamm-MEV-binary-monte-analysis](https://github.com/lilaclilac09/solana-pamm-MEV-binary-monte-analysis-contagious-pools)** — Monte-Carlo / binary analysis of MEV contagion across pools · [site](https://solana-pamm-mev-binary-monte-analys.vercel.app)
- **[Prop-AMM-Toxic-Flow-Guard](https://github.com/lilaclilac09/Prop-AMM-Toxic-Flow-Guard-1230-w-o-jito-bundle-w-pretty-front)** — toxic-flow guard for prop AMMs, with dashboard
- **[Prop-AMM-Toxic-Order-Monitor](https://github.com/lilaclilac09/Prop-AMM-Toxic-Order-Monitor)** — real-time toxic-order monitoring
- **[propamm-laserstream-bot](https://github.com/lilaclilac09/propamm-laserstream-bot)** — prop-AMM bot on a Helius LaserStream feed

## 🤖 Trading Bots & On-Chain Tools

- **[HumidiFi-Sentinel-Bot](https://github.com/lilaclilac09/HumidiFi-Sentinel-Bot_with-bundle-detection-ugly-front)** — HumidiFi sentinel bot with bundle detection
- **[Hyperliquid-HYPE-Whale-Tracker](https://github.com/lilaclilac09/Hyperliquid-HYPE-Whale-Tracker)** — tracks HYPE whale activity on Hyperliquid
- **[jupiter-swap-price-feed](https://github.com/lilaclilac09/jupiter-swap-w-o-wallet-price-feed)** — Jupiter swap price feed & pairs, no wallet required
- **[BNB-Memecoin-Copy-Trade-Architect](https://github.com/lilaclilac09/BNB-Memecoin-Copy-Trade-Architect)** — copy-trading architecture for BNB memecoins
- **[RPCsol_pnl](https://github.com/lilaclilac09/RPCsol_pnl)** — Solana RPC-based PnL tracker
- **[perena-dashboard](https://github.com/lilaclilac09/perena-dashboard0615)** — dashboard for the Perena USD\* stablecoin

## 🔐 Security & Reverse Engineering

- **[re-agent](https://github.com/lilaclilac09/re-agent)** — RE agent: Binary Ninja bridge + Claude tool-calling loop for stateful binary analysis
- **[hideaway](https://github.com/lilaclilac09/hideaway)** — experiments in secret hiding / obfuscation

## 📚 Interactive Courses

- **[solana-speed-demons](https://github.com/lilaclilac09/solana-speed-demons)** — Solana validator internals: Firedancer, Samba MEV, Delorean, pmm-sim
- **[autoresearch-course](https://github.com/lilaclilac09/autoresearch-course)** — autonomous LLM-driven research loops
- **[US-STOCKS-DEEP-ANALYSIS](https://github.com/lilaclilac09/US-STOCKS-DEEP-ANALYSIS)** — deep-dive analysis of US equities · [site](https://us-stocks-deep-analysis.vercel.app)

---

<p align="center"><sub>📍 Mars · Solana · MEV · AI agents</sub></p>
