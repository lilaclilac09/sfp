# Building KeyShield, Spec-First

> *How I designed an agent-grade API-key vault by writing the protocol before the code.*

KeyShield is *"iCloud Keychain for your API keys."* You store a key once, and from then on you plug into a vault instead of copy-pasting `.env` files — calls get encrypted, delegated, and accelerated on the way out. This is the story of how it was built **spec-driven**: the contract came first, the code followed.

---

## Why spec-first

KeyShield is not one app — it's six surfaces that all have to agree on the same security model:

- a **browser vault UI** (TypeScript),
- a **control-plane backend** (TypeScript),
- a **hot-path Rust proxy**,
- a **browser extension**,
- a **Python SDK / CLI**, and
- an **MCP server** so AI agents can use it.

When six components share one trust boundary, "we'll figure out the interface as we go" is how you end up with a vault that leaks. So before writing a feature, I wrote **`SPEC.md` (v0.1)** — a protocol for *agent credential delegation* — and locked down a short list of invariants. Everything else is downstream of that document.

---

## The invariants (the part that can never regress)

These were written into the spec on day one and treated as non-negotiable:

1. **Raw keys never leave the vault.** The server stores *ciphertext only* and cannot decrypt at rest.
2. **Agents get tokens, not keys.** Agents receive scoped, short-lived session tokens — never the underlying API key.
3. **Raw keys never persist in logs or agent processes.**
4. **Per-agent spending caps are enforced at the proxy**, not on the honor system.
5. **Revocation is immediate** — no TTL window. The next request after revocation returns `401`.

Every later design decision had to be checkable against this list. If a feature couldn't preserve all five, the feature changed — not the invariant.

---

## The protocol, in three primitives

The spec reduces the whole system to three objects:

### 1. Vault — encrypted client-side storage
Encryption happens **in the browser**, never on the server:

```
device credential (WebAuthn PRF / wallet signature)
        │
        ▼
   HKDF-SHA256  ──►  32-byte key
        │
        ▼
   AES-256-GCM.encrypt(api_key, nonce)  ──►  ciphertext
```

The server receives and stores only the ciphertext. Decryption requires the user's device, which gives KeyShield its zero-knowledge property: a server compromise leaks ciphertext, not keys.

### 2. Session tokens — short-lived bearer credentials
Tokens look like:

```
ksv2_<base58(random_32_bytes)>
```

Server-side, each token carries a payload: user ID, vault-key reference, provider, **scopes**, **spending cap**, and **expiry**. Tokens are verified on *every* proxy request — there is no "trusted once" path.

### 3. Proxy — decrypt-in-memory reverse proxy (Rust)
The Rust proxy is the only place a key is ever in plaintext, and only for the duration of a single upstream request. On top of the security role it does the performance work: a **two-tier cache (memory + disk)** with **single-flight dedup** so identical calls collapse into one, landing Solana RPCs in a **50–80 ms** band.

---

## Delegation & revocation

This is the part built specifically for agents. A human issues a delegated token to an agent with a **strict subset** of their own permissions — narrower scopes, a spending cap, an expiry. The agent operates entirely through that token and never touches a raw key.

Revocation was designed to be boring and instant: because tokens are checked on every request, killing one takes effect on the *next* call — `401`, no stale-cache lag, and the parent credential is untouched.

---

## How the spec drove the build

The methodology, in order:

1. **Write `SPEC.md` first.** Protocol version, primitives, token format, invariants — all before implementation.
2. **Derive the architecture from the spec**, not the other way around. The six components exist because the spec needed a place to enforce each guarantee (encryption → browser, verification + caps → proxy, issuance → backend, ergonomics → SDK/extension/MCP).
3. **Implement each component against the spec.** Every surface — TS vault, Rust proxy, Python SDK, MCP server, on-chain program — traces a line back to a clause in `SPEC.md`.
4. **Verify on-chain.** The payment-streaming mechanism runs as a Solana devnet program with documented instructions and *verified transactions*, so the economic layer is auditable, not asserted.
5. **Keep the docs as living artifacts.** `SPEC.md`, `AGENTS.md`, `DEVELOPMENT.md`, `DEPLOY.md`, `docs/architecture/`, `docs/API.md`, and `CHANGELOG.md` evolve with the code rather than rotting behind it.

---

## The journey — balancing three languages

The honest version of this project: the hardest design decision wasn't the crypto, it was **deciding which language gets which job**. KeyShield ended up roughly a third TypeScript, a quarter Rust, a quarter Python — and that split wasn't an accident, it was the whole point.

My rule was simple: **put each language where it is strongest, and let the spec be the contract between them** so the seams don't leak.

- **TypeScript — the surfaces humans touch.** The vault UI, the control-plane backend, and the browser extension all live in TS. This is where iteration speed and the web ecosystem matter most: WebAuthn, wallet signatures, and the DOM all have first-class TS stories, and I wanted the front door to feel instant to build and change.
- **Rust — the one path that cannot be wrong.** The proxy is the only place a decrypted key exists in plaintext, and it's on the hot path for every single call. That is exactly where I wanted *no* garbage-collector pauses, *no* "it compiled but the type was wrong," and *no* surprise allocations. Rust's ownership model also means a decrypted key has a precise, visible lifetime — it's dropped the moment the upstream request ends, by construction.
- **Python — meet the users where they live.** Almost everyone wiring an AI agent or a script is in Python. So the SDK/CLI is Python (`pip install keyshield`) and there's an MCP server for agents. Adoption beats elegance here: the easiest thing in the world should be `from keyshield import ...`.

The thing I had to keep reminding myself: **the spec is what lets three languages cooperate.** As long as the token format, the encryption envelope, and the invariants are pinned in `SPEC.md`, it doesn't matter that the proxy is Rust and the SDK is Python — they're both implementing the *same* document.

---

## Rust vs Python: compilation & correctness

Working across both daily made the difference between them very concrete. They don't even "compile" in the same sense of the word.

| Dimension | **Rust** | **Python** |
|---|---|---|
| Build model | Ahead-of-time → **native machine code** (via LLVM) | Source → **bytecode** (`.pyc`) → run on the CPython VM (interpreted) |
| What "compile" checks | Types, ownership, lifetimes, exhaustiveness — the program **won't build** if they're wrong | Mostly **syntax**; bytecode generation doesn't verify types |
| Type checking | Static, compile-time, mandatory | Dynamic, run-time; type hints are optional and only checked by external tools (`mypy`) |
| Memory | Ownership + borrow checker, **no GC** | Reference counting + cycle collector (GC) |
| When bugs surface | **At compile time** — before it ships | **At run time** — when that exact line executes |
| Iteration speed | Slower builds, more upfront ceremony | Edit-and-run, great for prototyping |
| Runtime | Fast, predictable, no GC pauses | Slower, possible GC pauses |

### The accuracy comparison

When people say Rust is "more accurate," what they usually mean is **where the errors get caught**, and that's the part that actually changed how I worked:

- **Rust shifts correctness left.** A wrong type, a missing case, a use-after-free, an unhandled `None` — none of them compile. By the time the proxy *runs*, an entire class of bugs has already been ruled out. For code that handles plaintext keys and enforces spending caps, that compile-time guarantee is worth the slower build.
- **Python defers correctness to runtime.** The flexibility that makes the SDK pleasant to write is the same flexibility that lets a type mismatch sit quietly until the line executes in production. You buy that safety back with discipline — type hints, `mypy`, tests — but it's opt-in, not enforced by the compiler.

There's a nuance worth being honest about, because it cuts the other way on raw numeric accuracy:

- **Python has arbitrary-precision integers by default** — a big integer just keeps growing, exactly, with no overflow. For ad-hoc big-number math that's genuinely *more* forgiving than Rust.
- **Rust uses fixed-width integers** (`u64`, `i128`, …) and forces me to pick the width and decide what happens on overflow (checked in debug builds, explicit `checked_add` / `saturating_add` in release). That feels like more work — but on a financial hot path enforcing spending caps, *being forced to think about overflow* is the feature, not the friction.

So the trade I settled on: **Python where being wrong is cheap and iteration is king (the SDK); Rust where being wrong is expensive and the machine should refuse to let me be wrong (the proxy).** Spec-first development is what made that division safe — both sides answer to the same `SPEC.md`.

---

## What spec-first bought me

- **A trust boundary I can point at.** Security claims live in one reviewable document, not scattered across commits.
- **Six components that actually agree.** Each was implemented against the same contract, so the proxy, SDK, and extension share one mental model.
- **Cheap change.** When something needs to move, I edit the invariant or the primitive first and let the diff propagate — instead of discovering the disagreement in production.

---

## Try it / read more

- **Live:** <https://keyshield-sync-worker.vercel.app>
- **Code:** <https://github.com/lilaclilac09/keyshield>
- **Spec:** [`SPEC.md`](https://github.com/lilaclilac09/keyshield/blob/main/SPEC.md)
- **Python SDK:** `pip install keyshield`

*Spec first. Code second. Keys never.*
