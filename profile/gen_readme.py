#!/usr/bin/env python3
"""Generate the organized GitHub profile README from the full repo list."""

U = "https://github.com/lilaclilac09"

def repo(name, desc="", lang="", site=""):
    return (name, desc, lang, site)

# ---------------- OWNED PROJECTS ----------------
owned = {
    "🌊 Solana Prop-AMM Research & Simulation": [
        repo("pamm-a", "research & implementation sandbox for prop AMMs, market making, and Solana simulation", "Rust"),
        repo("solana-pamm-MEV-binary-monte-analysis-contagious-pools", "Monte-Carlo / binary analysis of MEV contagion across pools", "Jupyter", "https://solana-pamm-mev-binary-monte-analys.vercel.app"),
        repo("solana-pamm-MEV-binary-monte-analysis-w-o-rawdata", "the analysis pipeline, raw data stripped", "Jupyter"),
        repo("Prop-AMM-Toxic-Flow-Guard-1230-w-o-jito-bundle-w-pretty-front", "toxic-flow guard for prop AMMs with a clean front-end", "TypeScript"),
        repo("Prop-AMM-Toxic-Order-Monitor", "real-time toxic-order monitoring for prop AMMs", "TypeScript"),
        repo("propamm-laserstream-bot", "prop-AMM bot built on a Helius LaserStream feed", "TypeScript"),
    ],
    "🤖 Trading Bots & On-Chain Tools": [
        repo("HumidiFi-Sentinel-Bot_with-bundle-detection-ugly-front", "HumidiFi sentinel bot with bundle detection (Helius API)"),
        repo("Hyperliquid-HYPE-Whale-Tracker", "tracks HYPE whale activity on Hyperliquid", "TypeScript"),
        repo("jupiter-swap-w-o-wallet-price-feed", "Jupiter swap price feed and pairs, no wallet required", "TypeScript"),
        repo("BNB-Memecoin-Copy-Trade-Architect", "copy-trading architecture for BNB memecoins", "TypeScript"),
        repo("RPCsol_pnl", "Solana RPC-based PnL tracker", "JavaScript"),
        repo("MPPSOL-agents", "agent framework for Solana market-making", "JavaScript"),
    ],
    "💵 Perena / Stablecoin Dashboards": [
        repo("perena-dashboard0615", "dashboard for the Perena USD* stablecoin", "TypeScript"),
        repo("perena-dashboard0615_1", "first desktop upload of the Perena dashboard", "TypeScript"),
        repo("perena-dashboard0615_0", "Perena dashboard work-in-progress"),
        repo("penera", "Perena protocol experiments", "JavaScript"),
        repo("penera_USD_STAR", "Perena USD* stablecoin experiments"),
    ],
    "🔐 Security & Reverse Engineering": [
        repo("re-agent", "RE agent: Binary Ninja bridge + Claude tool-calling loop for stateful binary analysis", "Python"),
        repo("keyshield", "key management & sync worker", "TypeScript", "https://keyshield-sync-worker.vercel.app"),
        repo("keyshield_font", "keyshield front-end", "TypeScript"),
        repo("hideaway", "experiments in secret hiding / obfuscation", "Rust"),
    ],
    "🧠 AI Agents & Automation": [
        repo("multiagentclaw", "multi-agent orchestration experiments", "Python"),
        repo("Vibe-Coding-Task-Manager", "task manager for vibe-coding workflows"),
        repo("tamagochi-agent-interface", "playful tamagotchi-style agent UI"),
        repo("tamagochi-aget-interface", "tamagotchi agent UI (early version)"),
    ],
    "📚 Interactive Courses": [
        repo("solana-speed-demons", "7-module course on Solana validator internals: Firedancer, Samba MEV, Delorean, pmm-sim", "HTML"),
        repo("autoresearch-course", "4-module course on autonomous LLM-driven research loops", "HTML"),
        repo("US-STOCKS-DEEP-ANALYSIS", "deep-dive analysis of US equities", "HTML", "https://us-stocks-deep-analysis.vercel.app"),
    ],
    "🎨 Web Apps & Fun": [
        repo("aileen_machina_01", "personal site for tech blogs", "TypeScript", "https://aileen-machina-01.vercel.app"),
        repo("aileen_machina_020", "personal site, iteration 020", "TypeScript"),
        repo("Zen-Fortune-Cookie", "a zen fortune-cookie web app", "TypeScript"),
        repo("fortune_cookie", "fortune-cookie web app", "TypeScript", "https://fortune-cookie-sand.vercel.app"),
        repo("meme.vote", "vote on memes, tally the results"),
        repo("dart-watch", "dart / watch experiment", "TypeScript"),
        repo("demo", "demo sandbox", "JavaScript"),
    ],
    "🧪 Experiments & Sandbox": [
        repo("project001", "Solidity smart-contract sandbox", "Solidity"),
        repo("puku_2", "scratch project", "TypeScript"),
        repo("puku3", "scratch project", "TypeScript"),
        repo("puku4", "scratch project", "HTML"),
    ],
}

# ---------------- FORKS / REFERENCES ----------------
forks = {
    "Solana & Prop-AMM ecosystem": [
        repo("kora", "Solana relayer — lib + cli for gasless signing experiences"),
        repo("plasma_jerry", "sandwich-resistant AMM reference implementation for Solana"),
        repo("pmm-sim", "simulation environment for Solana prop AMMs (SolFi, HumidiFi, Tessera, GoonFi, ...)"),
        repo("solfi-sim", "LiteSVM black-box simulations of the SolFi DEX pricing curves"),
        repo("pxsol", "human-friendly interfaces for common Solana operations"),
        repo("gg-program-resurrect", "reconstruct historical Solana program binaries from upgrade buffers"),
        repo("humidifi_invoke_deobfuscation", "deobfuscation of HumidiFi invoke logic", "Rust"),
        repo("DEX-Router-Solana-V1", "Solana DEX router contracts"),
        repo("Confidential-Balances-Sample", "Rust end-to-end demo of confidential transfers"),
        repo("jito-programs", "Jito on-chain programs"),
        repo("stakenet", "Jito StakeNet"),
        repo("pinocchio-never-nonce", "program rejecting an advance-nonce first instruction"),
        repo("noir-examples", "Noir + Sunspot ZK proof examples on Solana"),
        repo("solana-awesome", "curated Solana learning resource hub"),
        repo("solana-dev-skill", "Claude Code skill for modern Solana development"),
        repo("numeraire-sdk", "Numeraire SDK"),
        repo("order_book_server", "order-book server reference"),
        repo("salsa_harmonic", "Solana experiment"),
        repo("prop-amm-ben", "prop-AMM benchmark"),
        repo("prop-amm-challenge-houseofjiao", "prop-AMM challenge solution"),
    ],
    "MEV & Flashbots": [
        repo("mev-flood", "simulates MEV activity from an array of unique searchers"),
        repo("mev-share", "protocol for orderflow auctions"),
        repo("mev-share-client-ts", "client library for Flashbots MEV-share Matchmaker"),
        repo("mev-share-rs", "Rust client library for Flashbots MEV-share"),
        repo("mev-bundle-generator", "graph-based, trait-pluggable MEV bundle generator"),
        repo("renegade", "on-chain dark pool — MPC for anonymous midpoint crosses"),
    ],
    "DeFi, Trading & Crypto data": [
        repo("porto", "authentication & payments on the web"),
        repo("cryo", "extract blockchain data to parquet / csv / json / dataframes"),
        repo("cow-dex-solver", "CoW Protocol DEX solver"),
        repo("1inch-swap", "minimal 1inch integration example for smart contracts"),
        repo("Uniswap", "Uniswap source-code study (v2 core + periphery)"),
        repo("EconomicCalender", "economic calendar for forex & stock traders"),
        repo("AI-Trader", "AI-Trader — can AI beat the market? live trading bench"),
        repo("TradingAgents_tauricresearch", "multi-agent LLM financial trading framework"),
        repo("tradingview-mcp", "AI-assisted TradingView chart analysis via MCP"),
        repo("unstock-signals", "Day1Global signals: US stock, macro, crypto"),
        repo("ARK-Invest-Mach-33-SpaceX-Valuation-Model", "ARK Invest SpaceX valuation model excerpt"),
        repo("awesome-smart-contracts", "curated list of the best smart contracts"),
        repo("awesome-blockchain", "curated list of blockchain services and exchanges"),
        repo("full-blockchain-solidity-course-js", "full-stack Web3 + Solidity course (JS)"),
        repo("bitcoin_book_2nd", "Mastering Bitcoin, 2nd edition"),
        repo("SolarBatteryBitcoin", "solar / battery / bitcoin experiment"),
        repo("dapp-forge", "dApp scaffolding toolkit"),
        repo("one-cart-extension", "Chrome extension to cart & checkout Zora NFTs"),
        repo("meme-tinder", "swipe to vote on memes"),
        repo("x-wallet-homepage", "wallet landing page"),
    ],
    "DeFi insurance & smart contracts": [
        repo("aave-utilities", "Aave protocol utilities"),
        repo("gif-contracts", "Generic Insurance Framework (GIF) core contracts"),
        repo("nft-insurance", "forkable Ethereum dev stack for NFT insurance"),
        repo("functions-hardhat-starter-kit", "Chainlink Functions Hardhat starter kit"),
        repo("functions-insurance", "Chainlink Functions insurance example"),
        repo("cozy-triggers-v2-simulation", "triggers and templates for Cozy V2"),
        repo("DeFi-Lending-Insurance", "DeFi lending insurance contracts"),
        repo("Parametric-Crop-Insurance", "parametric crop insurance"),
        repo("insurance-product", "insurance product contracts"),
        repo("insuralink-contracts", "Insuralink contracts (ETHDenver hackathon)"),
    ],
    "AI agents & Claude skills": [
        repo("hammock-skill--disciplined-agent", "Hammock-driven development as a coding-agent skill"),
        repo("agentic-wallet-skills", "Coinbase agentic wallet skills"),
        repo("babyagi", "autonomous task-driven agent"),
        repo("gstack", "Garry Tan's opinionated Claude Code setup"),
        repo("k-dense-byok", "AI co-scientist powered by Claude Scientific Skills"),
        repo("lenny-skills", "86 product-management skills from Lenny's Podcast"),
        repo("gaslighting_ai_skills", "playful 'P8 engineer' AI skill"),
        repo("space-engineering-skills", "space-engineering skills for AI"),
        repo("ui-ux-pro-max-skill", "design-intelligence skill for UI/UX"),
        repo("system-prompts-and-models-of-ai-tools", "collected system prompts of AI tools"),
        repo("repomix-code-to-llm-prompt", "pack a repo into a single AI-friendly file"),
        repo("PocketTutorial-Codebase-Knowledge", "Pocket Flow: codebase to tutorial"),
        repo("json-render", "AI -> JSON -> UI"),
        repo("sfp", "benchmark & method for catastrophic forgetting in LLMs"),
    ],
    "Data engineering, learning & misc": [
        repo("py4e", "Python for Everybody textbook site"),
        repo("PY4E-1", "Python for Everybody assignments"),
        repo("data_engineering_book", "data engineering book"),
        repo("ETL-and-Data-Pipelines-with-Shell-Airflow-and-Kafka", "ETL & data pipelines with Shell, Airflow, Kafka"),
        repo("bads", "Business Analytics & Data Science lecture material"),
        repo("react-saas-template", "React + Material-UI SaaS/admin template"),
        repo("crimpdeq-case", "OpenSCAD 3D-printable case for Crimpdeq"),
        repo("rust-pcg64-py", "Rust PCG64 reimplemented in Python"),
    ],
}


def fmt_owned(name, desc, lang, site):
    label = name.replace("_", "\\_")
    line = f"- **[{label}]({U}/{name})**"
    if desc:
        line += f" — {desc}"
    if site:
        line += f" · [site]({site})"
    if lang:
        line += f" `{lang}`"
    return line


def fmt_fork(name, desc, lang, site):
    label = name.replace("_", "\\_")
    line = f"- [{label}]({U}/{name})"
    if desc:
        line += f" — {desc}"
    return line


out = []
out.append('<h1 align="center">Hi, I\'m Aileen 👋</h1>')
out.append("")
out.append('<p align="center">')
out.append("  Solana / DeFi research · prop-AMM &amp; MEV simulation · on-chain trading bots · AI agents")
out.append("</p>")
out.append("")
out.append('<p align="center">')
out.append('  <a href="https://github.com/lilaclilac09?tab=repositories"><img src="https://img.shields.io/badge/repos-101-8957e5?style=flat-square" alt="repos"></a>')
out.append('  <img src="https://img.shields.io/badge/focus-Solana%20%C2%B7%20MEV%20%C2%B7%20AI%20agents-14b8a6?style=flat-square" alt="focus">')
out.append("</p>")
out.append("")
out.append("---")
out.append("")
out.append("## 🛠️ My Projects")
out.append("")
for section, repos in owned.items():
    out.append(f"### {section}")
    out.append("")
    for r in repos:
        out.append(fmt_owned(*r))
    out.append("")

out.append("---")
out.append("")
out.append("## 📌 Forks, References & Learning")
out.append("")
out.append("<sub>Projects I study, fork, and build on — grouped by theme.</sub>")
out.append("")
for section, repos in forks.items():
    out.append("<details>")
    out.append(f"<summary><b>{section}</b> ({len(repos)})</summary>")
    out.append("")
    for r in repos:
        out.append(fmt_fork(*r))
    out.append("")
    out.append("</details>")
    out.append("")

out.append("---")
out.append("")
out.append('<p align="center"><sub>📍 Mars · Building at the intersection of Solana, MEV, and AI agents</sub></p>')
out.append("")

readme = "\n".join(out)
with open("profile/README.md", "w") as f:
    f.write(readme)

n_owned = sum(len(v) for v in owned.values())
n_forks = sum(len(v) for v in forks.values())
print(f"owned={n_owned} forks={n_forks} total={n_owned + n_forks}")
