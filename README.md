# Top Industrial AI Agents

> A curated list of LLM-agent projects, tools, benchmarks, and research applicable to industrial environments — SCADA, MES, historians, industrial protocols, predictive maintenance, computer vision on the shop floor, and industrial digital twins.

🇷🇺 **[Читать по-русски →](README.ru.md)**

---

## Why this list exists

The general agentic-AI ecosystem is huge and well-catalogued. Industrial applications are not. Most awesome-lists index chatbots, coding agents, and SaaS products — none of them tell you which projects are actually usable when the endpoint is an OPC UA server, a Modbus PLC, or a process historian, and when a wrong action can stop a furnace.

This list tries to answer a narrower question: **which agentic-AI projects survive contact with operational technology?**

**In scope:** LLM agents for SCADA/DCS/MES/historian, industrial-protocol connectors (OPC UA, Modbus, MQTT, S7), OT-aware guardrails and policy layers, agents that work inside PLC engineering tools, benchmarks and simulators for process control, predictive maintenance with LLMs, industrial computer vision, digital-twin-with-LLM hybrids.

**Out of scope:** general-purpose agentic frameworks (LangChain, AutoGen, CrewAI — see [awesome-ai-agents][kurilyak]), coding agents, sales/CRM agents, non-industrial predictive maintenance for pure SaaS. Also out of scope: "digital twin of a person" projects, which dominate a naive `digital twin` search and have nothing to do with industry.

**Curation stance:** "Top" in the name means opinionated. Projects included must (a) be reproducible or verifiably deployed, (b) address an industrial concern explicitly, (c) have public documentation. Marketing pages without code, demos, or peer-reviewed papers are rejected. A closed-source project may be listed if it has documented industrial deployments — it will be marked 🔒. Star counts are a weak signal in this niche and are **not** a criterion: several of the most on-target projects here have single-digit stars.

**Status:** v0.3.1 — **all entries, links, star counts, licenses and arXiv IDs re-verified 2026-11-07.** Four categories that v0.2 declared empty have since been filled; see [What changed in v0.3](#what-changed-in-v03). Remaining genuinely-empty niches are marked 🚧.

[kurilyak]: https://github.com/slavakurilyak/awesome-ai-agents

---

## Table of Contents

- [🔌 Industrial Protocol Bridges](#-industrial-protocol-bridges) — MCP/agent connectors for OPC UA, Modbus, MQTT, S7, Historian
- [🏗️ PLC & Engineering-Tool Agents](#️-plc--engineering-tool-agents) — agents inside TIA Portal, GX Works, Ignition Designer
- [🛡️ OT-Aware Guardrails & Policy Layers](#️-ot-aware-guardrails--policy-layers) — safety envelopes for agents acting on physical processes
- [📊 Industrial Agent Benchmarks](#-industrial-agent-benchmarks) — evaluation frameworks for agents in operations, maintenance, control
- [🎛️ Process Simulators for Agent Evaluation](#️-process-simulators-for-agent-evaluation) — open simulators usable as agent training/evaluation environments
- [🤖 Operator Advisors & Copilots](#-operator-advisors--copilots) — advisory systems for control-room operators (mostly pre-LLM)
- [🔧 Predictive Maintenance with LLMs](#-predictive-maintenance-with-llms) — asset-ops agents, anomaly narration, RCA assistants
- [👁️ Industrial Computer Vision Agents](#️-industrial-computer-vision-agents) — VLM-based quality inspection, safety monitoring
- [🌐 Digital Twin + LLM](#-digital-twin--llm) — hybrid systems combining physics-based twins with language models
- [🏭 Vendor Platforms](#-vendor-platforms) — industrial-AI offerings from major automation vendors
- [📚 Research & Standards](#-research--standards) — key papers, standards, consortium reports
- [🧰 Adjacent Tools Worth Knowing](#-adjacent-tools-worth-knowing) — general-purpose but genuinely useful in OT context
- [🇨🇳 Chinese Ecosystem](#-chinese-ecosystem) — projects published primarily in Chinese
- [What changed in v0.3.1](#what-changed-in-v031)
- [What changed in v0.3](#what-changed-in-v03)

Legend: ⭐ stars · 🔒 closed-source · 🚧 category open for contributions · 📦 archived/unmaintained · 🇷🇺 Russian-speaking ecosystem · 🇨🇳 Chinese ecosystem

All metrics below were measured 2026-11-07. Run `python update_stars.py` to refresh them.

---

## 🔌 Industrial Protocol Bridges

### OPC UA

#### [IndustriAgents/OPCUA-MCP](https://github.com/IndustriAgents/OPCUA-MCP) — the recommended general-purpose OPC UA MCP ⭐31
Python **and** Node implementations behind one tool contract, published to both PyPI and npm, with CI, a `.mcpb` one-file Claude Desktop bundle, and an entry in the official MCP registry. Covers the full operator toolkit: read, browse, history and aggregates, subscriptions, events and alarms, writes and method calls. A simulated plant ships in the repository, so you can evaluate it without touching a real endpoint.

**Read-only by default.** Writes and method calls require an explicit control profile *and* an authenticated server (pinned certificate or CA trust store). The `operator` profile additionally requires allowlisted targets, and every control call is audited. Remote MCP and shared multi-client operation are deliberately gated behind an [identity-and-isolation RFC](https://github.com/IndustriAgents/OPCUA-MCP/blob/main/docs/rfc/0001-remote-identity-isolation.md) rather than shipped half-done.

**Verdict:** as of v0.3 this is the default recommendation for connecting an agent to an OPC UA endpoint. The profile model is the closest thing in the open-source world to OT-appropriate access control at the bridge layer. MIT.

#### [kukapay/opcua-mcp](https://github.com/kukapay/opcua-mcp) — minimal generic OPC UA MCP ⭐31
Small reference MCP server for OPC UA. Five tools: read node, write node, browse namespace, read multiple, write multiple. No policy layer, no scoping, no auth model — write access is unrestricted. Last activity October 2025.

**Verdict:** an educational example, not a production tool. Still worth reading as the "naive baseline" that shows why bridge-level profiles and policy layers matter — compare its five unrestricted tools against the profile model above. MIT.

#### Other OPC UA bridges worth knowing
- **[shriramkv/opcua-mcp](https://github.com/shriramkv/opcua-mcp)** ⭐25 — exposes OPC UA sources as "safe, permissioned" tools. No explicit license file.
- **[mwieczorkiewicz/opcua-mcp](https://github.com/mwieczorkiewicz/opcua-mcp)** ⭐5 — Go implementation, aimed at robots and PLCs. MIT.
- **[AndreasHeine/i3x2ua](https://github.com/AndreasHeine/i3x2ua)** ⭐19 — turns any OPC UA server into an i3X-compliant REST **and** MCP API. From a known OPC UA community contributor. AGPL-3.0.
- **[node-opcua/node-opcua-modeler-mcp-server](https://github.com/node-opcua/node-opcua-modeler-mcp-server)** ⭐2 — from the `node-opcua` project itself: MCP for OPC UA **information modeling** and companion-spec discovery. Addresses a different problem from data access — building the address space. Apache-2.0.
- **[marcschier/opcuakb-mcp](https://github.com/marcschier/opcuakb-mcp)** ⭐2 — OPC UA knowledge-base MCP, C#. MIT.
- **[AddisonTech/Hermes](https://github.com/AddisonTech/Hermes)** ⭐2 — Rust OPC UA bridge and MCP server for plant-floor access. MIT.

### Modbus — *gap closed since v0.2*

v0.2 said "no production-quality entry yet". That was already inaccurate at publication, and three credible options now exist:

- **[kukapay/modbus-mcp](https://github.com/kukapay/modbus-mcp)** ⭐26 — standardizes and contextualizes Modbus data for agents. Predates this list (May 2025) and was missed in v0.2. Same caveat as its OPC UA sibling: no policy layer. MIT.
- **[industrial-aiops/industrial-aiops](https://github.com/industrial-aiops/industrial-aiops)** ⭐10 — Modbus TCP/RTU as one of 15 protocols, read-first with a governance engine (see Guardrails below). MIT.
- **[IndustriAgents/IndustriConnect](https://github.com/IndustriAgents/IndustriConnect)** ⭐10 — multi-protocol device-to-agent connector, TypeScript. MIT.

### Historian — *gap closed since v0.2*

v0.2 said "none identified". Two routes now exist:

- **[chewcw/aveva-historian-mcpserver](https://github.com/chewcw/aveva-historian-mcpserver)** ⭐0 — MCP server for **AVEVA Historian**, time-series retrieval for agents. Go. Zero stars and no license file, but it is the first public implementation of exactly the gap v0.2 described, and worth watching.
- **[industrial-aiops/industrial-aiops](https://github.com/industrial-aiops/industrial-aiops)** ⭐10 — OPC UA **Historical Access** with tag auto-discovery, plus a `historian_push` egress tool. The more production-shaped of the two.

PI System and Ignition's historian still have no dedicated public MCP. Narrower gap than v0.2 described, but not closed.

### MQTT / Sparkplug B
- **[ezhuk/mqtt-mcp](https://github.com/ezhuk/mqtt-mcp)** ⭐25 — generic MQTT MCP server, Python. MIT.
- **[Benniu/emqx-mcp-server](https://github.com/Benniu/emqx-mcp-server)** ⭐27 — MCP for the EMQX broker: cluster, client and topic operations. Apache-2.0.
- **[emqx/uns-demo](https://github.com/emqx/uns-demo)** ⭐9 — EMQX's own demo of exploring IIoT **Sparkplug B** data in natural language over MCP. A demo, not a product, but a clean reference for Unified Namespace + agent.
- **[AddisonTech/Iris](https://github.com/AddisonTech/Iris)** ⭐1 — MQTT/Sparkplug bridge exposing REST + MCP.

### Vendor-native SCADA and DCS
- **[winccoa/winccoa-ae-js-mcpserver](https://github.com/winccoa/winccoa-ae-js-mcpserver)** ⭐27 — **official Siemens MCP for WinCC OA.** JavaScript; datapoints (read/write/create), OPC UA and MQTT connectivity, dashboards, alarms, archives, Pmon process management, PV range validation, 1400+ built-in icons. Includes a **write-exclusion model**: administrators can disable whole tool categories (`datapoints/dp_set`, `dp_create`, `dp_type_create`). Still the only MCP published by a top-tier automation vendor.
- **[vogler75/winccua-mcp-server](https://github.com/vogler75/winccua-mcp-server)** ⭐15 — third-party MCP for **WinCC Unified** via its GraphQL API: browse objects, current tag values, historical logged values, active and logged alarms, tag writes, alarm resets. GPL-3.0.
- **[vogler75/winccv8-mcp-server](https://github.com/vogler75/winccv8-mcp-server)** ⭐13 — same author, for **WinCC V8**. Missed in v0.2. GPL-3.0.
- **[Nodeblue-AI/ignition-mcp-server](https://github.com/Nodeblue-AI/ignition-mcp-server)** ⭐12 — MCP for **Ignition** SCADA, positioned as a development tool for Ignition projects. MIT.
- **[Nodeblue-AI/bridge-mcp-server](https://github.com/Nodeblue-AI/bridge-mcp-server)** ⭐10 — correlates Ignition tags with other sources. MIT.
- **[smithaldon1/deltav-mcp](https://github.com/smithaldon1/deltav-mcp)** ⭐2 — **Emerson DeltaV** via Edge API and OPC UA. First public MCP touching a major DCS. GPL-3.0.
- **[zavora-ai/mcp-scada](https://github.com/zavora-ai/mcp-scada)** ⭐3 — self-described critical-risk industrial-control MCP for energy. Rust. Treat the framing with caution; included for completeness.

### Multi-protocol taps
- **[industrial-aiops/industrial-aiops](https://github.com/industrial-aiops/industrial-aiops)** ⭐10 — **15 field protocols** from one read-first tap: OPC UA (+ Historical Access), Modbus TCP/RTU, S7comm, Mitsubishi MC, Omron FINS, MTConnect, MQTT/Sparkplug B, EtherNet/IP, EtherCAT, PROFINET, SECS/GEM, HART-IP, BACnet/IP, IO-Link, serial ASCII instruments — plus read-only REST layers for Metasys/Niagara and Ignition Gateway. Substation telecontrol (IEC 60870-5-104, DNP3, IEC 61850) ships separately as [`industrial-aiops-energy`](https://github.com/industrial-aiops/industrial-aiops-energy) ⭐2. Cosign-signed non-root container, air-gapped deployment profile, deterministic analysis engine that needs no GPU or model API (the LLM only *phrases* the verdict). MIT.
- **[lwsinclair/IoT-Edge-MCP-Server](https://github.com/lwsinclair/IoT-Edge-MCP-Server)** ⭐5 — unifies MQTT sensors with SCADA/PLC sources. MIT.
- **[cadugrillo/s7-mcp-bridge](https://github.com/cadugrillo/s7-mcp-bridge)** ⭐28 — direct **Siemens S7** bridge, bypassing OPC UA entirely. TypeScript, MIT. Notable as the most-starred single-protocol bridge after the OPC UA pair.

---

## 🏗️ PLC & Engineering-Tool Agents

**New category in v0.3.** A distinct 2026 development that v0.2 did not anticipate: agents that operate inside vendor *engineering* tools — generating and compiling PLC logic, exporting nodesets, archiving projects — rather than reading live process data. The risk profile is completely different from a runtime bridge: the blast radius is the project file and the download to the controller, not a live setpoint.

- **[Arienax/gxworks-agent](https://github.com/Arienax/gxworks-agent)** ⭐24 — MCP server and AI workbench for **Mitsubishi** PLC programming via GX Works2/3. Apache-2.0. Documentation primarily in Chinese.
- **[agimx-ai/seedagent-tia-programming](https://github.com/agimx-ai/seedagent-tia-programming)** ⭐13 — agent for **Siemens TIA Portal V16–V21**: automatic SCL generation for S7-1200/1500, compile diagnostics, project archiving to `.zap`. No license file — check before use. Documentation in Chinese.
- **[gangsterke/Tia-Portal-MCP-server](https://github.com/gangsterke/Tia-Portal-MCP-server)** ⭐10 — narrower: exports OPC UA nodeset files from a TIA Portal PLC project. C#. No license file.

**Research:** "Vendor-Aware Industrial Agents: RAG-Enhanced LLMs for Secure On-Premise PLC Code Generation" ([arXiv 2511.09122](https://arxiv.org/abs/2511.09122)) is the reference paper for this category and argues the on-premise case explicitly.

**Verdict:** the most commercially active industrial-agent niche right now, and the least governed. None of the three has a review-and-approve gate before code reaches a controller. If you adopt one, keep it on the engineering workstation and keep the download step human.

---

## 🛡️ OT-Aware Guardrails & Policy Layers

### [meta-llama/PurpleLlama — LlamaFirewall](https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall) ⭐4466
Meta's open-source guardrail framework for LLM agents. Three primary scanners: **PromptGuard 2** (BERT-style jailbreak/injection detector), **AgentAlignmentCheck** (chain-of-thought auditor for goal-misalignment), **CodeShield** (static analysis for insecure code generation), plus customizable regex filters. Paper: [arXiv 2505.03574](https://arxiv.org/abs/2505.03574).

**Verdict:** still one of the two most mature open-source agent guardrails. **Text-level only — does not understand process semantics** (rates of change, interlocks, physical constraints). Essential baseline for any industrial agent stack; insufficient on its own.

### [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) ⭐7445
NVIDIA's programmable guardrail toolkit. Five rail types: input, dialog, retrieval, execution, output. Integrates with Nemotron Content Safety, Topic Control, and Jailbreak Detect NIMs. Decoupled from LangChain (optional now). Actively released through 2026.

**Verdict:** the other major general-purpose guardrail platform. Same limitation as LlamaFirewall — general-purpose, no OT semantics — but the Colang policy language makes it plausibly extensible to industrial rules. *Note: the repository moved from `NVIDIA/NeMo-Guardrails` to `NVIDIA-NeMo/Guardrails`; the old path still redirects.*

### [industrial-aiops/industrial-aiops](https://github.com/industrial-aiops/industrial-aiops) — the first OT-shaped governance engine ⭐10
Listed above as a protocol tap, but its governance layer belongs here and is the reason v0.2's headline gap has to be rewritten. Four controls applied on **every** call, from both MCP and CLI, through one engine: **audit · budget · risk-tier · undo**. Read-first by design. Egress is explicit: exactly six tools can send data off-box, and `IAIOPS_NO_EGRESS=1` withholds all six for an air-gapped posture. Ships ISA-18.2 alarm-flood analysis, downtime root-cause with cited evidence, dataflow-break and data-trustworthiness checks, OEE, and a legacy PLC program explainer for ST/AWL/L5X.

**Verdict:** not yet the semantics-aware envelope described in the gap below — risk-tiering is per-tool, not per-process-variable, and there is no rate-of-change or interlock model. But it is the first open project to treat governance as the product rather than an afterthought, and the `undo` and `budget` primitives are ones no general-purpose guardrail offers. MIT.

### [sint-ai/sint-protocol](https://github.com/sint-ai/sint-protocol) ⭐15
Runtime security and governance for AI agents, MCP tools and robots. TypeScript, Apache-2.0, actively developed.

**Verdict:** adjacent rather than industrial — robots and MCP tools generally, not process semantics — but the only other open project framing itself as runtime governance rather than text filtering. Worth tracking.

### [shadowhunter-92/wafertrust — WaferTrust](https://github.com/shadowhunter-92/wafertrust) — fab-first agent-governance prototype
Python gateway demo at the MCP tool-call boundary for simulated semiconductor equipment and
maintenance workflows. Uses AgentBridge's governance kernel: reads are logged; sensitive writes
require human approval and sufficient budget. Fixed per-tool costs express illustrative
wafer-dollar exposure, with a cumulative budget and per-call cap. The full in-process audit
is hash-chained. Apache-2.0.

**Verdict:** runnable simulator-based alpha, with no field deployment or live SECS/GEM connection.
Governs tool access, not process physics: no live interlocks, rate-of-change, cross-tag, or
mode-dependent envelope. Audit entries are unsigned; registered Ed25519 identities do not
provide caller-signature verification in this demo. Committed JSONL files are partial summaries,
not self-contained independently verifiable logs. Useful for evaluating a fab-first audit/approval
workflow and illustrative wafer-dollar accounting, not production safety or SEMI compliance.
The agentAudit extension is simulated, not a native E191 field. Overlaps industrial-aiops'
SECS/GEM governance; does not claim to replace it or fill the process-semantics gap.

### 📦 [protectai/llm-guard](https://github.com/protectai/llm-guard) — archived ⭐3219
Production-oriented security toolkit for LLM interactions. **The repository was archived (read-only) and receives no further development.** Listed in v0.2 without that caveat.

**Verdict:** do not start new work on it. Mentioned here only so readers who find it via search know its status.

### Research frontier (2025–2026)

- **[AgentWall](https://arxiv.org/abs/2605.16265)** — OS-level runtime interception of shell commands, API calls and filesystem operations before execution. Preprint **first submitted March 2026** (v0.2 said May), revised as recently as November 2026; still no public code. Scoped to local developer machines rather than OT, but architecturally the closest published design to what an OT action-gate needs.
- **[Evidence-Governed Deployment Readiness for Networked Agents on Industrial OT Infrastructure](https://arxiv.org/abs/2610.18426)** (Oct 2026) — **the most on-topic paper published since v0.2.** Frames OT agent deployment as an evidence-and-readiness problem rather than a filtering problem.
- **[Securing AI Agents: Implementing Role-Based Access Control for Industrial Applications](https://arxiv.org/abs/2509.11431)** — RBAC applied specifically to industrial agents. The nearest thing to a formal access-control model for this domain.
- **[AgentGuardian](https://arxiv.org/abs/2601.10440)** — learned access-control policies for LLM agents.
- **[ToolSafe](https://arxiv.org/abs/2601.10156)** — pre-execution safety detection at the tool-call step.
- **[OneShield](https://arxiv.org/abs/2507.21170)** — "next-generation LLM guardrails" from IBM.

### [alikup-ai/otgate](https://github.com/alikup-ai/otgate) — the only open process-aware policy layer ⭐0
> **Disclosure: this is the maintainer's own project.** It is listed because v0.3 of this list declared its niche empty, which was wrong. Weigh the verdict below accordingly, and PR a deletion if you think it does not meet the curation stance.

An authorization gateway that sits between an agent and an OPC UA server, and is itself an MCP server: the agent connects to it as if it were an ordinary OPC UA MCP, and every call is intercepted. Policy is per tag, deny-by-default, and expressed in process terms — `value_range`, `max_rate` over `rate_interval`, `interlocks` that read live guard tags, `cumulative_range` over a window so a forbidden move cannot be sliced into legal steps, and `max_calls` against call storms. Writes can require **human approval on a physically separate authenticated channel**, so the agent cannot even see the `approve` tool; approval re-checks policy against current process state before executing, because an interlock may have tripped while the request waited. Shadow mode executes nothing and records what the agent *would* have done. Unverifiable safety conditions **fail closed**. Apache-2.0, Python, 142 tests including an integration suite against a live `opc.tcp://` server.

**Verdict:** this is the category the gap below describes, and the only open implementation of it — but judge it as alpha. Zero stars, no forks, no field deployment, one author. It went unmaintained from July to November 2026, during which a major `mcp` release broke its install outright; that, and two baseline defects in its own core checks (rate and drift were measured against the gateway's own memory rather than the live process, so a 144-unit jump passed a 5-per-60s policy), were fixed in November. The honest reading: the *design* is the right shape for OT and nothing else open has it; the *implementation* has had one careful pass and no adversarial contact with a real plant. Its [threat model](https://github.com/alikup-ai/otgate/blob/main/docs/threat-model.md) is explicit about what it does not cover.

### 🚧 Process-semantics-aware safety envelope — one alpha implementation, problem not solved
**Corrected in v0.3.1.** v0.3 said "nothing open understands the process". That was wrong — `otgate` above does, and it existed when v0.3 was written. The gap is narrower than stated, and still real.

The problem itself is unchanged. A write of 40 °C to `TIC-101` can be inside the absolute range, inside the operator's allowlist, within budget, fully audited and still dangerous — because the current value is 22 °C, the ramp violates a thermal-shock limit, and an interlock three tags away is bypassed. Everything else in this section governs *the agent* (profiles, risk tiers, audit, undo); governing *the physics* takes a different kind of policy.

What is genuinely still missing:

- **Field validation.** One alpha project with zero stars and no deployment is not a solved category. Until an envelope like this has been run against a real plant by someone other than its author, the category is unproven rather than filled.
- **Cross-tag constraints.** Envelopes and budgets are per tag everywhere, `otgate` included. An agent that spreads its effect across several tags, each inside its own allowance, is detected by nothing open.
- **Mode-dependent envelopes.** Safe limits differ between startup, steady state, shutdown and maintenance. No open project expresses "this range applies only in these process modes".
- **Trend awareness.** A tag's live value tells you *where* the process is, not *how* it got there. Nothing open consults the historian trend before judging a write.
- **A vendor-neutral way to express any of it.** Text guardrails have Colang, OPA and Cedar. Process envelopes have one project's YAML dialect. ISA-88 modes and ISA-18.2 alarm states are the obvious vocabularies, and nobody has mapped them onto agent policy.

**Still the clearest open niche in industrial agentic AI** — not because it is empty, but because what exists is a single unproven implementation and four of the five hard parts are untouched.

---

## 📊 Industrial Agent Benchmarks

### [IBM/AssetOpsBench](https://github.com/IBM/AssetOpsBench) ⭐2411
IBM's flagship Industry 4.0 benchmark, and by far the most-starred project in this list's core categories. **460+ scenarios**, 5 specialist agents (IoT, FMSR, TSFM, Work Order, plus orchestrator), multi-agent orchestration blueprints (MetaAgent, AgentHive) — **all built over MCP**. Grounded in ISO standards for platform-agnosticism. HuggingFace Space playground, a challenge co-located at IJCAI 2026, active university extensions. Paper: [arXiv 2506.03828](https://arxiv.org/abs/2506.03828).

**Verdict:** the most active industrial agent benchmark community in 2026. Focus is asset lifecycle — condition monitoring, maintenance planning, work-order generation — **not real-time process supervision.**

### [amazon-science/SOP-Bench](https://github.com/amazon-science/SOP-Bench) ⭐46
2000+ tasks across 12 domains testing agents on Standard Operating Procedures. Human expert-authored SOPs, executable interfaces with ground-truth outputs, evaluated on Environment Completion Rate, Task Success Rate and Constraint-aware TSR. 11 frontier models benchmarked; function-calling agents average ~64% task success. Paper: [arXiv 2506.08119](https://arxiv.org/abs/2506.08119).

**Verdict:** the most authoritative recent benchmark for procedural agent execution. Domains include Dangerous Goods, healthcare intake and logistics — industrially adjacent but **not process control**.

### [Leezekun/SOPBench](https://github.com/Leezekun/SOPBench) ⭐26
Parallel SOP-following benchmark (note the different capitalization from Amazon's). Seven customer-service domains: bank, online market, DMV, healthcare, library, hotel, university. Different methodology, different constraint model.

**Verdict:** narrower domain than Amazon's, but methodologically distinct and useful for triangulation.

### Benchmark methodology research
- **[Synthetic Scenario Generation for Evaluation of Industry 4.0 Agents](https://arxiv.org/abs/2607.22563)** — addresses the scarcity of industrial evaluation scenarios by generating them. Relevant to anyone attempting the closed-loop gap below.
- **[Beyond Static Leaderboards: Predictive Validity for the Evaluation of LLM Agents](https://arxiv.org/abs/2606.19704)** — on whether agent leaderboards predict deployed behaviour at all. Worth reading before trusting any number above.

### 🚧 Closed-loop process control benchmark — still nothing
No open benchmark places an agent as supervisor of a running dynamic process, scored on safety-envelope violations, intervention count, and diagnostic quality under alarm floods. Candidate base simulators are listed below. **Major open niche, unchanged since v0.2.**

---

## 🎛️ Process Simulators for Agent Evaluation

### Tennessee Eastman Process — a family of reference implementations
The classic Downs–Vogel–Braatz benchmark chemical process — reactor, separator, stripper, compressor, with configurable faults. Standard in fault detection and process control research since 1993.

- **[ccreinartz11/pytep](https://github.com/ccreinartz11/pytep)** ⭐45 — pyTEP, high-level Python API for interactive simulation. Best entry point for agent supervision experiments. (Reinartz & Enevoldsen, *SoftwareX* 2022)
- **[camaramm/tennessee-eastman-profBraatz](https://github.com/camaramm/tennessee-eastman-profBraatz)** ⭐191 — the most-starred mirror of the original Fortran codes.
- **[jkitchin/tennessee-eastman-profbraatz](https://github.com/jkitchin/tennessee-eastman-profbraatz)** ⭐32 — original Fortran 77 plus a Python backend via f2py (~5–10× faster).
- **[camaramm/tep2py](https://github.com/camaramm/tep2py)** ⭐16 — Python interface to the original Fortran TEP.
- **[usnistgov/tesim](https://github.com/usnistgov/tesim)** ⭐3 — NIST's version, optimized for wireless and cybersecurity research. Last touched 2018.
- **[ElsevierSoftwareX/SOFTX-D-24-00664](https://github.com/ElsevierSoftwareX/SOFTX-D-24-00664)** ⭐5 — COSTEP, complete open Simulink model of TEP.

**Verdict:** natural base for any process-control agent benchmark. pyTEP remains the recommended starting point unless you need Fortran-level speed. Note that none of these has seen meaningful activity since 2025 — they are stable references, not living projects.

### 🚧 Batch-process simulators (concrete, hydroponics, food) — still nothing suitable
Searched again for v0.3 across batch, fermentation, bioreactor and wastewater keywords: the open results are student projects and single-author experiments with no fault models and no alarm behaviour. Discrete and batch industrial processes remain badly underrepresented. **Contributions especially welcome here** — a batch process with realistic alarm patterns would unlock the closed-loop benchmark gap above.

Adjacent and worth knowing: **[YuchenXia/LLMDrivenSimulation](https://github.com/YuchenXia/LLMDrivenSimulation)** ⭐33 (CC-BY-4.0) — an LLM system interacting with simulation models in digital twins; the closest published work to "agent drives a simulator" even though the simulator is not a batch plant.

---

## 🤖 Operator Advisors & Copilots

Every credible operator advisor in industry today is proprietary and predates the current LLM wave. Listed for landscape context, not as reproducible references.

### 🇷🇺 [Piklema Predictive](https://piklema.com/) 🔒
Helsinki-based, Russian-speaking team. Series A ($12.82M, July 2025). Flagship **Driver Assistant** — real-time audio/visual advisor for open-pit dump truck operators, claimed effect 3–5% fuel savings. Not process control; driver-behaviour optimization. Additional products for tyre, engine and fatigue management.

**Verdict:** a working example of a pre-LLM digital advisor delivering measurable value in a narrow niche. Instructive for what trust boundaries and operator UX look like in production.

### 🇷🇺 [Zyfra (Цифра)](https://www.zyfra.com/) 🔒
Largest Russian-speaking industrial IIoT vendor. Not a single advisor product but a full stack: ZIIoT platform, Machine Data Collection (MDC Plus), Zyfra AI, Zyfra EYE (computer vision), plus verticals for mining, oil & gas, metallurgy, chemistry. All pre-LLM AI/ML.

**Verdict:** the reference "traditional industrial AI" stack in the Russian-speaking market — the baseline LLM-based advisors will be measured against.

### 🇷🇺 SIPO (Rosatom, Novovoronezh NPP) 🔒
Nuclear operator support system, publicly documented as analysing ~360 systems, supporting ~200 procedures, with a 30-minute forecasting horizon. No public implementation or SDK.

**Verdict:** the domestic reference for advisor systems at highest-criticality installations. Useful as an architecture target, not available for reproduction.

### 🚧 Open-source LLM operator advisor — still none
First open reference implementation remains unclaimed. Nearest adjacent work: **[Beyond touch-based human-machine interface: Control your machines in natural language](https://arxiv.org/abs/2510.11300)** and **[LLM-Driven Multi-Agent Control for Skill-Based Smart Manufacturing](https://arxiv.org/abs/2610.01364)**.

---

## 🔧 Predictive Maintenance with LLMs

*v0.2 called this category thin. It is not thin any more.*

### [LGDiMaggio/predictive-maintenance-mcp](https://github.com/LGDiMaggio/predictive-maintenance-mcp) ⭐109
An MCP server that turns an LLM into a condition-monitoring assistant for reliability engineers: **43 endpoints** (40 tools and 3 prompts) for vibration diagnostics — envelope-spectrum analysis, bearing fault-frequency matching, severity assessment, anomaly detection trained on the user's own healthy baselines, and interactive HTML diagnostic reports. Ships 20 real bearing measurements from the MathWorks rolling-element dataset so the whole pipeline is reproducible from a clone. Also packaged as a Claude Code plugin with 9 diagnostic skills.

Its core design rule is the one this list has been asking for all along: **the server refuses to guess.** No diagnosis is inferred from filenames or summary statistics — a fault indication requires matching spectral evidence. Every severity claim cites **ISO 20816-3**, and the evaluative wording in reports is authored by the server, not improvised by the model. The LLM orchestrates and presents; the judgement stays with the engineer. Signals never leave local infrastructure.

Has tests in CI, Codecov coverage, and a citable DOI ([10.5281/zenodo.17611542](https://doi.org/10.5281/zenodo.17611542)). MIT.

**Verdict:** the single best-engineered project in this list by the criteria stated at the top — reproducible, standards-cited, honest about its own limits, and architecturally resistant to the failure mode that makes LLMs dangerous in diagnostics. **Recommended starting point for anyone building agentic condition monitoring.**

### Also in this space
- **[industrial-aiops/industrial-aiops](https://github.com/industrial-aiops/industrial-aiops)** ⭐10 — downtime root-cause copilot with cited evidence, deterministic engine.
- **[IBM/AssetOpsBench](https://github.com/IBM/AssetOpsBench)** ⭐2411 — FMSR and Work Order agents cover maintenance planning (see Benchmarks).
- **[arcspots/FactoryMindAI](https://github.com/arcspots/FactoryMindAI)** ⭐5 — predictive and prescriptive maintenance platform. Early, no license file.
- **Research:** [Cleaning Maintenance Logs with LLM Agents for Improved Predictive Maintenance](https://arxiv.org/abs/2511.05311) — the unglamorous but highest-value LLM application in maintenance: making historical work-order text usable at all.

---

## 👁️ Industrial Computer Vision Agents

### 🚧 Category still empty
Re-searched for v0.3 across VLM defect detection, visual inspection and PPE monitoring: nothing open-source qualifies. VLM-based agents for quality inspection, PPE detection and safety-zone monitoring exist as vendor products (Landing AI, Cognex, Zyfra EYE, numerous startups) but not as reproducible projects. Contributions welcome, **especially where the VLM is used agentically** — planning inspection routes, escalating findings, deciding what to re-inspect — rather than as a classifier behind an API.

---

## 🌐 Digital Twin + LLM

Research is active; reproducible open implementations remain rare. Note that a naive search for "digital twin" in this space is dominated by "digital twin of a *person*" projects, which are out of scope here.

- **[YuchenXia/LLMDrivenSimulation](https://github.com/YuchenXia/LLMDrivenSimulation)** ⭐33 — LLM system interacting with simulation models in digital twins. CC-BY-4.0. The most credible open entry.
- **[j03rul4nd/digital-twin-water](https://github.com/j03rul4nd/digital-twin-water)** ⭐10 — runnable water-treatment digital twin, Three.js, deliberately scoped to "working in 30 minutes". No license file.
- **Research:** [Semantic Graph Unification for Industrial Digital Threads](https://arxiv.org/abs/2608.24918) (bridging 11 heterogeneous manufacturing sources) and [Autonomous Structural Discovery of Bioprocess Dynamics and Kinetics via LLM-Driven Agents](https://arxiv.org/abs/2610.35391).

### 🚧 Still thin
A reproducible physics-based twin with an agent in the loop, scored on anything, does not exist openly.

---

## 🏭 Vendor Platforms

Included for landscape awareness. None are open source; all claims are vendor-stated and not independently verified here.

- **Siemens Industrial Copilots + NVIDIA Industrial AI OS** 🔒 — copilots across the Siemens software and hardware stack
- **Honeywell Forge** 🔒 — enterprise operations platform with AI modules
- **ABB Genix / ABB Ability** 🔒 — industrial analytics platform
- **Cognite Data Fusion + Atlas AI** 🔒 — industrial data platform with LLM layer
- **AspenTech / Aspen Hybrid Models** 🔒 — process optimization with hybrid ML
- **C3 AI Industrial Suite** 🔒
- 🇷🇺 **Atomiq Software / Alpha Platform** 🔒 — Russian SCADA vendor; no AI/LLM modules published as of v0.3

Worth noting against this list: the only vendor to have published an actual open MCP server is Siemens (WinCC OA, above). Everyone else's AI story remains inside their own platform.

---

## 📚 Research & Standards

### Standards and consortium work
- **ASM Consortium** — [Abnormal Situation Management guidelines](https://www.asmconsortium.net/) — foundational human-factors work, decades of data. Key finding: 42% of process incidents have human factors in the root cause.
- **MCP (Model Context Protocol)** — [spec](https://modelcontextprotocol.io/) — now adopted by an industrial vendor (Siemens WinCC OA) and carrying an [official registry](https://registry.modelcontextprotocol.io/).
- **[GitHub MCP Registry](https://github.com/mcp)** — the emerging community catalog.
- **ISA-95 / ISA-88 / ISA-101 / ISA-18.2** — the standards agents will need to respect.
- **Siemens True Cost of Downtime 2024** — widely cited study on unplanned downtime economics. Vendor-published; treat the headline figures as marketing-adjacent.

### ISA-18.2 in code — *gap closed since v0.2*
v0.2 said no open implementation of ISA-18.2 alarm logic existed.

- **[cbvance/AlarmsByTheNumbers](https://github.com/cbvance/AlarmsByTheNumbers)** ⭐0 — `almetrics` reconstructs alarm episodes from an Ignition `alarm_events` journal and computes the benchmark metrics used in **ISA-18.2 and EEMUA 191** work: floods, chattering, fleeting, stale and standing alarms, bad-actor ranking, a master-alarm-database workbook for rationalization meetings, and a before-and-after proof report. Companion code to *Alarm Rationalization by the Numbers* (Charles Vance, LearnSCADA, 2026). Python, MIT, zero stars — and exactly the thing v0.2 said did not exist.
- **[industrial-aiops](https://github.com/industrial-aiops/industrial-aiops)** ⭐10 — ships ISA-18.2 alarm-flood analysis as one of its advisory checks.

### Papers published since v0.2
- **[Industrial Agentic AI: LLM-Driven New-Generation Agents for Smart Manufacturing](https://arxiv.org/abs/2610.26941)** (Oct 2026) — the survey to read first if you are new to the field.
- **[Evidence-Governed Deployment Readiness for Networked Agents on Industrial OT Infrastructure](https://arxiv.org/abs/2610.18426)** (Oct 2026) — OT-specific deployment governance.
- **[LLM-Driven Multi-Agent Control for Skill-Based Smart Manufacturing](https://arxiv.org/abs/2610.01364)** (Oct 2026).
- **[Semantic Graph Unification for Industrial Digital Threads](https://arxiv.org/abs/2608.24918)** (Aug 2026).
- **[Synthetic Scenario Generation for Evaluation of Industry 4.0 Agents](https://arxiv.org/abs/2607.22563)**.
- **[Vendor-Aware Industrial Agents: RAG-Enhanced LLMs for Secure On-Premise PLC Code Generation](https://arxiv.org/abs/2511.09122)**.
- **[Securing AI Agents: Implementing Role-Based Access Control for Industrial Applications](https://arxiv.org/abs/2509.11431)**.
- OT security with LLMs: **[LLMs as Explainable Cyberattack Detectors for Energy Industrial Control](https://arxiv.org/abs/2604.26079)** and **[HydroJEV](https://arxiv.org/abs/2610.02048)** (training-free cyber-attack and fault attribution in water systems).

---

## 🧰 Adjacent Tools Worth Knowing

General-purpose but genuinely useful when building industrial agent systems:

- **[stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)** ⭐38964 — compilable-prompt framework from Stanford NLP. Signatures, modules, optimizers (MIPROv2, GEPA). Relevant for evals-heavy industrial workflows where prompts need systematic tuning rather than hand-crafting.
- **[topoteretes/cognee](https://github.com/topoteretes/cognee)** ⭐33119 — knowledge-graph layer for LLMs. Useful for grounding agent reasoning in regulations, SOPs and P&IDs.
- **[e2b-dev/E2B](https://github.com/e2b-dev/E2B)** ⭐14756 — sandboxed code execution for agents. Conceptually related to shadow-mode for OT: run proposed actions in isolation before letting them touch reality.
- **[AgentOps-AI/agentops](https://github.com/AgentOps-AI/agentops)** ⭐5949 — Python SDK for agent monitoring, LLM cost tracking, session replay. Integrates with CrewAI, OpenAI Agents SDK, LangChain, AutoGen, AG2, CamelAI. TypeScript version at `AgentOps-AI/agentops-ts`. *Not to be confused with Microsoft's Azure/agentops.* Last repository activity June 2026 — check before depending on it.
- **[pnoker/iot-dc3](https://github.com/pnoker/iot-dc3)** ⭐1266 — open-source IIoT platform, Java, explicitly repositioned around connecting physical devices to AI. The largest industrial-adjacent codebase in this list.
- **[anviod/edgeCore](https://github.com/anviod/edgeCore)** ⭐135 — industrial edge runtime, Go. Deployed at field sites; documentation partly Chinese.
- **[slalaure/korelate](https://github.com/slalaure/korelate)** ⭐27 — AI-powered **Unified Namespace** operations center. Apache-2.0. The UNS layer is where most agent-era industrial data architecture is heading.
- **[TobiasLante/node-red-contrib-mcp](https://github.com/TobiasLante/node-red-contrib-mcp)** ⭐15 — MCP nodes for **Node-RED**. Low-friction way to put an agent next to existing plant integrations. Apache-2.0.
- **[akya-dev/AyMON](https://github.com/akya-dev/AyMON)** ⭐12 — SCADA/IIoT monitoring and automation engine, actively developed.

---

## 🇨🇳 Chinese Ecosystem

**New section in v0.3**, responding to v0.2's own request. These projects are substantial but documented primarily in Chinese, which is why English-language awesome-lists miss them.

- **[iduyuhe/zhiyan-evolviq](https://github.com/iduyuhe/zhiyan-evolviq)** ⭐13 — 智衍 EvolvIQ, self-described as the first open AI-native industrial agent platform: 25 industrial agents across production line, management and supply chain. Apache-2.0.
- **[Arienax/gxworks-agent](https://github.com/Arienax/gxworks-agent)** ⭐24 — Mitsubishi GX Works programming agent (see PLC agents).
- **[agimx-ai/seedagent-tia-programming](https://github.com/agimx-ai/seedagent-tia-programming)** ⭐13 — Siemens TIA Portal SCL generation (see PLC agents).
- **[hanshiyingbing/chemon](https://github.com/hanshiyingbing/chemon)** ⭐6 — CHEMON, multi-agent orchestration for chemical processes. MIT.
- **[ESEAI-Lab/LLM-MCP-OPCUA-Agent](https://github.com/ESEAI-Lab/LLM-MCP-OPCUA-Agent)** ⭐2 — natural-language control of industrial robots over OPC UA via MCP: single-arm, dual-arm coordination. MIT.

---

## What changed in v0.3.1

A correction, not a sweep. v0.3 declared the process-semantics safety-envelope niche empty. It was not: [`alikup-ai/otgate`](https://github.com/alikup-ai/otgate) implements exactly that category and had existed since July 2026. It is now listed under Guardrails with a disclosure that it is this list's maintainer's own project, and the gap is rewritten to say what is actually still missing — field validation, cross-tag constraints, mode-dependent envelopes, trend awareness, and a vendor-neutral vocabulary — instead of claiming nothing exists.

The lesson is the one this list keeps relearning. A "nothing exists here" claim is the most perishable thing in a curated list and the hardest to notice going stale, because nobody opens a PR to tell you a gap has stopped being a gap.

## What changed in v0.3

Re-verified every entry on **2026-11-07** against the GitHub and arXiv APIs. v0.2 was published 2026-07-22 and not updated since.

**Corrections to v0.2:**
1. `kukapay/opcua-mcp` was described as "6 stars, last activity May 2025". Actual: **31 stars, last activity October 2025.**
2. `stanfordnlp/dspy` was "~35k stars". Actual: **38,964.**
3. `protectai/llm-guard` is **archived** and was listed without that caveat.
4. `NVIDIA/NeMo-Guardrails` **moved** to `NVIDIA-NeMo/Guardrails`; `data.yaml` still had the old path.
5. AgentWall was dated "May 2026". The preprint was **first submitted March 2026.**
6. `data.yaml` claimed to be the source of truth but was a v0.1 file describing fewer projects than the v0.2 README, and listed Siemens by marketing URL instead of its actual repository. It is now regenerated from the README and carries verified metrics.
7. `update_stars.py` had never been run (no `stars` field existed anywhere) and could not run: it resolved `data.yaml` one directory above the repository root. **Fixed**, and now scheduled.

**Gaps v0.2 declared empty that are now filled:**
- **Modbus MCP** — `kukapay/modbus-mcp` already existed in May 2025 and was missed; `industrial-aiops` and `IndustriConnect` have since added credible coverage.
- **Historian MCP** — `chewcw/aveva-historian-mcpserver`, plus OPC UA Historical Access in `industrial-aiops`.
- **Predictive maintenance with LLMs** — `LGDiMaggio/predictive-maintenance-mcp`, 109 stars, DOI, ISO 20816-3 citations. The category was "thin"; it now has a clear recommendation.
- **ISA-18.2 alarm logic in code** — `cbvance/AlarmsByTheNumbers`.

**New in v0.3:**
- Category: **PLC & Engineering-Tool Agents** — the fastest-moving and least-governed industrial agent niche.
- Section: **Chinese ecosystem**, which v0.2 asked for by name.
- Protocol coverage expanded from 3 bridges to 25, including S7, MQTT/Sparkplug, EtherNet/IP, BACnet, SECS/GEM, DeltaV, Ignition and WinCC V8.
- 12 papers published since v0.2.
- Weekly automated metric refresh via GitHub Actions, so this list cannot silently rot again.

**Gaps that did not move, and are the real open niches:**
1. **Process-semantics-aware safety envelope** — governing the physics, not the agent. *(Corrected in v0.3.1: one alpha implementation exists, `otgate`. Field validation, cross-tag constraints, mode-dependent envelopes, trend awareness and a vendor-neutral policy vocabulary are all still missing.)*
2. **Closed-loop process control benchmark.**
3. **Batch-process simulators** with fault and alarm behaviour.
4. **Open-source LLM operator advisor.**
5. **Agentic industrial computer vision.**

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

Preferred contributions in v0.3:
1. **Filling the five remaining 🚧 gaps** — even a single credible entry is high-value
2. **Corrections** — if a project is mischaracterized here, say so; v0.3 exists because v0.2 had errors
3. **Removing hype** — if an included project does not meet the curation stance, PR the deletion
4. **Non-English ecosystems** — the Chinese section is a start; Japanese, Korean and German industrial projects are still missing

## Maintainer

Curated by [Ali](https://github.com/alikup-ai) — background in operating a manufacturing enterprise and pipeline-industry OT, currently building industrial AI-agent tooling. Reach out for corrections or collaboration.

## License

Content: [CC0-1.0](LICENSE) — public domain. Use freely.
