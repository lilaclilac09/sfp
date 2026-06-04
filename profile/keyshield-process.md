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
