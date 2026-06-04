<h1 align="center">Hi, I'm Aileen 👋</h1>

<p align="center">
  Solana / DeFi research · prop-AMM &amp; MEV simulation · on-chain trading bots · AI agents
</p>

<p align="center">
  <a href="https://github.com/lilaclilac09?tab=repositories"><img src="https://img.shields.io/badge/repos-101-8957e5?style=flat-square" alt="repos"></a>
  <img src="https://img.shields.io/badge/focus-Solana%20%C2%B7%20MEV%20%C2%B7%20AI%20agents-14b8a6?style=flat-square" alt="focus">
</p>

---

## ⭐ Featured — KeyShield · *spec-driven*

> **[keyshield](https://github.com/lilaclilac09/keyshield)** — *"iCloud Keychain for your API keys."*  A zero-knowledge vault that stores your API keys as ciphertext, hands agents **scoped session tokens** instead of raw keys, and accelerates calls through a Rust proxy.

🔗 [Live site](https://keyshield-sync-worker.vercel.app) · 📄 [SPEC.md](https://github.com/lilaclilac09/keyshield/blob/main/SPEC.md) · 📝 [**Build process & spec-driven write-up →**](./keyshield-process.md)

- 🔐 **Zero-knowledge** — AES-256-GCM encryption in the browser (WebAuthn PRF / wallet signature → HKDF-SHA256); the server only ever stores ciphertext and *cannot* decrypt at rest
- 🎫 **Scoped delegation** — agents receive `ksv2_…` session tokens with per-agent scopes, spending caps, and expiry; revocation is immediate (next request → `401`)
- ⚡ **Fast** — Rust reverse proxy with a two-tier cache (memory + disk) + single-flight dedup → **50–80 ms** hot path for Solana RPCs
- 🧩 **Spec-first** — `SPEC.md` (v0.1) pinned the protocol and invariants *before* code; the TypeScript vault, Rust proxy, Python SDK, MCP server, and Solana on-chain program all trace back to it

<sub>Stack: `TypeScript` · `Rust` · `Python` · MCP · Solana</sub>

---

## 🛠️ My Projects

### 🌊 Solana Prop-AMM Research & Simulation

- **[pamm-a](https://github.com/lilaclilac09/pamm-a)** — research & implementation sandbox for prop AMMs, market making, and Solana simulation `Rust`
- **[solana-pamm-MEV-binary-monte-analysis-contagious-pools](https://github.com/lilaclilac09/solana-pamm-MEV-binary-monte-analysis-contagious-pools)** — Monte-Carlo / binary analysis of MEV contagion across pools · [site](https://solana-pamm-mev-binary-monte-analys.vercel.app) `Jupyter`
- **[solana-pamm-MEV-binary-monte-analysis-w-o-rawdata](https://github.com/lilaclilac09/solana-pamm-MEV-binary-monte-analysis-w-o-rawdata)** — the analysis pipeline, raw data stripped `Jupyter`
- **[Prop-AMM-Toxic-Flow-Guard-1230-w-o-jito-bundle-w-pretty-front](https://github.com/lilaclilac09/Prop-AMM-Toxic-Flow-Guard-1230-w-o-jito-bundle-w-pretty-front)** — toxic-flow guard for prop AMMs with a clean front-end `TypeScript`
- **[Prop-AMM-Toxic-Order-Monitor](https://github.com/lilaclilac09/Prop-AMM-Toxic-Order-Monitor)** — real-time toxic-order monitoring for prop AMMs `TypeScript`
- **[propamm-laserstream-bot](https://github.com/lilaclilac09/propamm-laserstream-bot)** — prop-AMM bot built on a Helius LaserStream feed `TypeScript`

### 🤖 Trading Bots & On-Chain Tools

- **[HumidiFi-Sentinel-Bot\_with-bundle-detection-ugly-front](https://github.com/lilaclilac09/HumidiFi-Sentinel-Bot_with-bundle-detection-ugly-front)** — HumidiFi sentinel bot with bundle detection (Helius API)
- **[Hyperliquid-HYPE-Whale-Tracker](https://github.com/lilaclilac09/Hyperliquid-HYPE-Whale-Tracker)** — tracks HYPE whale activity on Hyperliquid `TypeScript`
- **[jupiter-swap-w-o-wallet-price-feed](https://github.com/lilaclilac09/jupiter-swap-w-o-wallet-price-feed)** — Jupiter swap price feed and pairs, no wallet required `TypeScript`
- **[BNB-Memecoin-Copy-Trade-Architect](https://github.com/lilaclilac09/BNB-Memecoin-Copy-Trade-Architect)** — copy-trading architecture for BNB memecoins `TypeScript`
- **[RPCsol\_pnl](https://github.com/lilaclilac09/RPCsol_pnl)** — Solana RPC-based PnL tracker `JavaScript`
- **[MPPSOL-agents](https://github.com/lilaclilac09/MPPSOL-agents)** — agent framework for Solana market-making `JavaScript`

### 💵 Perena / Stablecoin Dashboards

- **[perena-dashboard0615](https://github.com/lilaclilac09/perena-dashboard0615)** — dashboard for the Perena USD* stablecoin `TypeScript`
- **[perena-dashboard0615\_1](https://github.com/lilaclilac09/perena-dashboard0615_1)** — first desktop upload of the Perena dashboard `TypeScript`
- **[perena-dashboard0615\_0](https://github.com/lilaclilac09/perena-dashboard0615_0)** — Perena dashboard work-in-progress
- **[penera](https://github.com/lilaclilac09/penera)** — Perena protocol experiments `JavaScript`
- **[penera\_USD\_STAR](https://github.com/lilaclilac09/penera_USD_STAR)** — Perena USD* stablecoin experiments

### 🔐 Security & Reverse Engineering

- **[re-agent](https://github.com/lilaclilac09/re-agent)** — RE agent: Binary Ninja bridge + Claude tool-calling loop for stateful binary analysis `Python`
- **[keyshield\_font](https://github.com/lilaclilac09/keyshield_font)** — KeyShield front-end / vault UI `TypeScript`
- **[hideaway](https://github.com/lilaclilac09/hideaway)** — experiments in secret hiding / obfuscation `Rust`

### 🧠 AI Agents & Automation

- **[multiagentclaw](https://github.com/lilaclilac09/multiagentclaw)** — multi-agent orchestration experiments `Python`
- **[Vibe-Coding-Task-Manager](https://github.com/lilaclilac09/Vibe-Coding-Task-Manager)** — task manager for vibe-coding workflows
- **[tamagochi-agent-interface](https://github.com/lilaclilac09/tamagochi-agent-interface)** — playful tamagotchi-style agent UI
- **[tamagochi-aget-interface](https://github.com/lilaclilac09/tamagochi-aget-interface)** — tamagotchi agent UI (early version)

### 📚 Interactive Courses

- **[solana-speed-demons](https://github.com/lilaclilac09/solana-speed-demons)** — 7-module course on Solana validator internals: Firedancer, Samba MEV, Delorean, pmm-sim `HTML`
- **[autoresearch-course](https://github.com/lilaclilac09/autoresearch-course)** — 4-module course on autonomous LLM-driven research loops `HTML`
- **[US-STOCKS-DEEP-ANALYSIS](https://github.com/lilaclilac09/US-STOCKS-DEEP-ANALYSIS)** — deep-dive analysis of US equities · [site](https://us-stocks-deep-analysis.vercel.app) `HTML`

### 🎨 Web Apps & Fun

- **[aileen\_machina\_01](https://github.com/lilaclilac09/aileen_machina_01)** — personal site for tech blogs · [site](https://aileen-machina-01.vercel.app) `TypeScript`
- **[aileen\_machina\_020](https://github.com/lilaclilac09/aileen_machina_020)** — personal site, iteration 020 `TypeScript`
- **[Zen-Fortune-Cookie](https://github.com/lilaclilac09/Zen-Fortune-Cookie)** — a zen fortune-cookie web app `TypeScript`
- **[fortune\_cookie](https://github.com/lilaclilac09/fortune_cookie)** — fortune-cookie web app · [site](https://fortune-cookie-sand.vercel.app) `TypeScript`
- **[meme.vote](https://github.com/lilaclilac09/meme.vote)** — vote on memes, tally the results
- **[dart-watch](https://github.com/lilaclilac09/dart-watch)** — dart / watch experiment `TypeScript`
- **[demo](https://github.com/lilaclilac09/demo)** — demo sandbox `JavaScript`

### 🧪 Experiments & Sandbox

- **[project001](https://github.com/lilaclilac09/project001)** — Solidity smart-contract sandbox `Solidity`
- **[puku\_2](https://github.com/lilaclilac09/puku_2)** — scratch project `TypeScript`
- **[puku3](https://github.com/lilaclilac09/puku3)** — scratch project `TypeScript`
- **[puku4](https://github.com/lilaclilac09/puku4)** — scratch project `HTML`

---

## 📌 Forks, References & Learning

<sub>Projects I study, fork, and build on — grouped by theme.</sub>

<details>
<summary><b>Solana & Prop-AMM ecosystem</b> (20)</summary>

- [kora](https://github.com/lilaclilac09/kora) — Solana relayer — lib + cli for gasless signing experiences
- [plasma\_jerry](https://github.com/lilaclilac09/plasma_jerry) — sandwich-resistant AMM reference implementation for Solana
- [pmm-sim](https://github.com/lilaclilac09/pmm-sim) — simulation environment for Solana prop AMMs (SolFi, HumidiFi, Tessera, GoonFi, ...)
- [solfi-sim](https://github.com/lilaclilac09/solfi-sim) — LiteSVM black-box simulations of the SolFi DEX pricing curves
- [pxsol](https://github.com/lilaclilac09/pxsol) — human-friendly interfaces for common Solana operations
- [gg-program-resurrect](https://github.com/lilaclilac09/gg-program-resurrect) — reconstruct historical Solana program binaries from upgrade buffers
- [humidifi\_invoke\_deobfuscation](https://github.com/lilaclilac09/humidifi_invoke_deobfuscation) — deobfuscation of HumidiFi invoke logic
- [DEX-Router-Solana-V1](https://github.com/lilaclilac09/DEX-Router-Solana-V1) — Solana DEX router contracts
- [Confidential-Balances-Sample](https://github.com/lilaclilac09/Confidential-Balances-Sample) — Rust end-to-end demo of confidential transfers
- [jito-programs](https://github.com/lilaclilac09/jito-programs) — Jito on-chain programs
- [stakenet](https://github.com/lilaclilac09/stakenet) — Jito StakeNet
- [pinocchio-never-nonce](https://github.com/lilaclilac09/pinocchio-never-nonce) — program rejecting an advance-nonce first instruction
- [noir-examples](https://github.com/lilaclilac09/noir-examples) — Noir + Sunspot ZK proof examples on Solana
- [solana-awesome](https://github.com/lilaclilac09/solana-awesome) — curated Solana learning resource hub
- [solana-dev-skill](https://github.com/lilaclilac09/solana-dev-skill) — Claude Code skill for modern Solana development
- [numeraire-sdk](https://github.com/lilaclilac09/numeraire-sdk) — Numeraire SDK
- [order\_book\_server](https://github.com/lilaclilac09/order_book_server) — order-book server reference
- [salsa\_harmonic](https://github.com/lilaclilac09/salsa_harmonic) — Solana experiment
- [prop-amm-ben](https://github.com/lilaclilac09/prop-amm-ben) — prop-AMM benchmark
- [prop-amm-challenge-houseofjiao](https://github.com/lilaclilac09/prop-amm-challenge-houseofjiao) — prop-AMM challenge solution

</details>

<details>
<summary><b>MEV & Flashbots</b> (6)</summary>

- [mev-flood](https://github.com/lilaclilac09/mev-flood) — simulates MEV activity from an array of unique searchers
- [mev-share](https://github.com/lilaclilac09/mev-share) — protocol for orderflow auctions
- [mev-share-client-ts](https://github.com/lilaclilac09/mev-share-client-ts) — client library for Flashbots MEV-share Matchmaker
- [mev-share-rs](https://github.com/lilaclilac09/mev-share-rs) — Rust client library for Flashbots MEV-share
- [mev-bundle-generator](https://github.com/lilaclilac09/mev-bundle-generator) — graph-based, trait-pluggable MEV bundle generator
- [renegade](https://github.com/lilaclilac09/renegade) — on-chain dark pool — MPC for anonymous midpoint crosses

</details>

<details>
<summary><b>DeFi, Trading & Crypto data</b> (20)</summary>

- [porto](https://github.com/lilaclilac09/porto) — authentication & payments on the web
- [cryo](https://github.com/lilaclilac09/cryo) — extract blockchain data to parquet / csv / json / dataframes
- [cow-dex-solver](https://github.com/lilaclilac09/cow-dex-solver) — CoW Protocol DEX solver
- [1inch-swap](https://github.com/lilaclilac09/1inch-swap) — minimal 1inch integration example for smart contracts
- [Uniswap](https://github.com/lilaclilac09/Uniswap) — Uniswap source-code study (v2 core + periphery)
- [EconomicCalender](https://github.com/lilaclilac09/EconomicCalender) — economic calendar for forex & stock traders
- [AI-Trader](https://github.com/lilaclilac09/AI-Trader) — AI-Trader — can AI beat the market? live trading bench
- [TradingAgents\_tauricresearch](https://github.com/lilaclilac09/TradingAgents_tauricresearch) — multi-agent LLM financial trading framework
- [tradingview-mcp](https://github.com/lilaclilac09/tradingview-mcp) — AI-assisted TradingView chart analysis via MCP
- [unstock-signals](https://github.com/lilaclilac09/unstock-signals) — Day1Global signals: US stock, macro, crypto
- [ARK-Invest-Mach-33-SpaceX-Valuation-Model](https://github.com/lilaclilac09/ARK-Invest-Mach-33-SpaceX-Valuation-Model) — ARK Invest SpaceX valuation model excerpt
- [awesome-smart-contracts](https://github.com/lilaclilac09/awesome-smart-contracts) — curated list of the best smart contracts
- [awesome-blockchain](https://github.com/lilaclilac09/awesome-blockchain) — curated list of blockchain services and exchanges
- [full-blockchain-solidity-course-js](https://github.com/lilaclilac09/full-blockchain-solidity-course-js) — full-stack Web3 + Solidity course (JS)
- [bitcoin\_book\_2nd](https://github.com/lilaclilac09/bitcoin_book_2nd) — Mastering Bitcoin, 2nd edition
- [SolarBatteryBitcoin](https://github.com/lilaclilac09/SolarBatteryBitcoin) — solar / battery / bitcoin experiment
- [dapp-forge](https://github.com/lilaclilac09/dapp-forge) — dApp scaffolding toolkit
- [one-cart-extension](https://github.com/lilaclilac09/one-cart-extension) — Chrome extension to cart & checkout Zora NFTs
- [meme-tinder](https://github.com/lilaclilac09/meme-tinder) — swipe to vote on memes
- [x-wallet-homepage](https://github.com/lilaclilac09/x-wallet-homepage) — wallet landing page

</details>

<details>
<summary><b>DeFi insurance & smart contracts</b> (10)</summary>

- [aave-utilities](https://github.com/lilaclilac09/aave-utilities) — Aave protocol utilities
- [gif-contracts](https://github.com/lilaclilac09/gif-contracts) — Generic Insurance Framework (GIF) core contracts
- [nft-insurance](https://github.com/lilaclilac09/nft-insurance) — forkable Ethereum dev stack for NFT insurance
- [functions-hardhat-starter-kit](https://github.com/lilaclilac09/functions-hardhat-starter-kit) — Chainlink Functions Hardhat starter kit
- [functions-insurance](https://github.com/lilaclilac09/functions-insurance) — Chainlink Functions insurance example
- [cozy-triggers-v2-simulation](https://github.com/lilaclilac09/cozy-triggers-v2-simulation) — triggers and templates for Cozy V2
- [DeFi-Lending-Insurance](https://github.com/lilaclilac09/DeFi-Lending-Insurance) — DeFi lending insurance contracts
- [Parametric-Crop-Insurance](https://github.com/lilaclilac09/Parametric-Crop-Insurance) — parametric crop insurance
- [insurance-product](https://github.com/lilaclilac09/insurance-product) — insurance product contracts
- [insuralink-contracts](https://github.com/lilaclilac09/insuralink-contracts) — Insuralink contracts (ETHDenver hackathon)

</details>

<details>
<summary><b>AI agents & Claude skills</b> (14)</summary>

- [hammock-skill--disciplined-agent](https://github.com/lilaclilac09/hammock-skill--disciplined-agent) — Hammock-driven development as a coding-agent skill
- [agentic-wallet-skills](https://github.com/lilaclilac09/agentic-wallet-skills) — Coinbase agentic wallet skills
- [babyagi](https://github.com/lilaclilac09/babyagi) — autonomous task-driven agent
- [gstack](https://github.com/lilaclilac09/gstack) — Garry Tan's opinionated Claude Code setup
- [k-dense-byok](https://github.com/lilaclilac09/k-dense-byok) — AI co-scientist powered by Claude Scientific Skills
- [lenny-skills](https://github.com/lilaclilac09/lenny-skills) — 86 product-management skills from Lenny's Podcast
- [gaslighting\_ai\_skills](https://github.com/lilaclilac09/gaslighting_ai_skills) — playful 'P8 engineer' AI skill
- [space-engineering-skills](https://github.com/lilaclilac09/space-engineering-skills) — space-engineering skills for AI
- [ui-ux-pro-max-skill](https://github.com/lilaclilac09/ui-ux-pro-max-skill) — design-intelligence skill for UI/UX
- [system-prompts-and-models-of-ai-tools](https://github.com/lilaclilac09/system-prompts-and-models-of-ai-tools) — collected system prompts of AI tools
- [repomix-code-to-llm-prompt](https://github.com/lilaclilac09/repomix-code-to-llm-prompt) — pack a repo into a single AI-friendly file
- [PocketTutorial-Codebase-Knowledge](https://github.com/lilaclilac09/PocketTutorial-Codebase-Knowledge) — Pocket Flow: codebase to tutorial
- [json-render](https://github.com/lilaclilac09/json-render) — AI -> JSON -> UI
- [sfp](https://github.com/lilaclilac09/sfp) — benchmark & method for catastrophic forgetting in LLMs

</details>

<details>
<summary><b>Data engineering, learning & misc</b> (8)</summary>

- [py4e](https://github.com/lilaclilac09/py4e) — Python for Everybody textbook site
- [PY4E-1](https://github.com/lilaclilac09/PY4E-1) — Python for Everybody assignments
- [data\_engineering\_book](https://github.com/lilaclilac09/data_engineering_book) — data engineering book
- [ETL-and-Data-Pipelines-with-Shell-Airflow-and-Kafka](https://github.com/lilaclilac09/ETL-and-Data-Pipelines-with-Shell-Airflow-and-Kafka) — ETL & data pipelines with Shell, Airflow, Kafka
- [bads](https://github.com/lilaclilac09/bads) — Business Analytics & Data Science lecture material
- [react-saas-template](https://github.com/lilaclilac09/react-saas-template) — React + Material-UI SaaS/admin template
- [crimpdeq-case](https://github.com/lilaclilac09/crimpdeq-case) — OpenSCAD 3D-printable case for Crimpdeq
- [rust-pcg64-py](https://github.com/lilaclilac09/rust-pcg64-py) — Rust PCG64 reimplemented in Python

</details>

---

<p align="center"><sub>📍 Mars · Building at the intersection of Solana, MEV, and AI agents</sub></p>
