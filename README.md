<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/hero-dark.svg">
  <img src=".github/assets/hero-light.svg" alt="$ ./katsuba --serve — Igor Katsuba, a system exposed over a few transports. status: 200 OK" width="100%">
</picture>

```jsonc
// manifest
// I build software whose users are increasingly not people.
// Agents call it, other systems depend on it, and it has to
// keep working when nobody's watching.
```

### `GET /about` — `200 OK · text/plain`

I'm a senior engineer working out of Valencia. For the last while I've been living at the seam between AI agents and backend infrastructure — the unglamorous layer that decides whether the clever stuff on top actually holds.

The framing on this page isn't a gimmick. It's genuinely how I think about building: define a capability once, expose it through whatever transport the caller speaks — HTTP, MCP, a CLI. Same idea applies to a person. This is me, exposed over the transports below.

```rust
fn building()  // Durable execution, agent orchestration, developer tooling,
               // the glue between systems. Happiest one layer below the product,
               // where reliability is the whole job.

fn writing()   // A Telegram channel on Angular and frontend, a blog with 20+
               // articles. Explaining things is how I understand them.

fn speaking()  // Talks on monorepos, build tooling, and pipeline acceleration.
               // The recordings age; the problems they solve mostly don't.
```

### `GET /tools` — `200 OK · 7 items · application/json`

| # | tool | description |
|---|------|-------------|
| `01` | [`ng.guide`](https://ng.guide) | An Angular course an agent takes itself. Delivered over MCP, built for the world where the student isn't always human. |
| `02` | [`roost`](https://github.com/IKatsuba/roost) | A native macOS workspace for Claude Code sessions — projects, tabs, a tree of terminal panes, and an attention queue that tells you which agent is stuck. |
| `03` | [`nx-cache-server`](https://github.com/IKatsuba/nx-cache-server) | Self-hosted remote cache for Nx. S3, Docker, Helm — bring your own infra, keep your build times. |
| `04` | [`mutates`](https://github.com/IKatsuba/mutates) | AST mutation toolkit — mutate the AST, not your brain. Hands for an agent that needs to rewrite code and be sure it did. |
| `05` | [`ng-http`](https://github.com/IKatsuba/ng-http) | Experimental declarative HTTP server written with Angular. What if your backend spoke the framework your frontend already does? |
| `06` | [`deno-mastra`](https://github.com/IKatsuba/deno-mastra) | AI agents built with Deno and the Mastra framework — the runtime and the orchestration, end to end. |
| `07` | [`serverless-redis`](https://github.com/IKatsuba/serverless-redis) | HTTP → Redis server, Upstash-compatible. Hono + Deno, one click to deploy on Railway. |

### `GET /speaking` — `200 OK · 3 talks · video`

- [**Repository evolution: from simple to complex**](https://www.youtube.com/watch?v=pqV863ysMRQ) — Frontend Conf 2021
- [**Extreme Pipeline Acceleration**](https://youtu.be/j0OhmZeAoKQ) — CodeFest Russia 2022
- [**It's all about Nx**](https://www.youtube.com/watch?v=D-JwmfQKfIE) — Podlodka 2022

### `GET /experience` — `200 OK · 4 roles · résumé`

| company | role | period |
|---------|------|--------|
| **Plata Card** | Principal Engineer | `2022–2025` |
| **Tinkoff** | Staff Engineer | `2020–2022` |
| **Fix Group** | Senior Frontend Developer | `2018–2020` |
| **RTLabs** | Frontend Developer | `2014–2018` |

### `POST /contact` — `accepting connections`

If you want to talk infrastructure, agents, or the tooling underneath both — or just argue about durable execution — open a connection.

**→** [`github`](https://github.com/IKatsuba) &nbsp; **→** [`x`](https://x.com/katsuba_igor) &nbsp; **→** [`instagram`](https://www.instagram.com/igor.katsuba/) &nbsp; **→** [`telegram`](https://t.me/Katsuba) &nbsp; **→** [`email`](mailto:igor@katsuba.dev)

---

<p align="center"><sub><a href="https://katsuba.dev"><code>katsuba.dev</code></a> · connection closed · <code>200</code></sub></p>
