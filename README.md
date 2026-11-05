# Top Industrial AI Agents

> A curated list of LLM-agent projects, tools, benchmarks, and research applicable to industrial environments — SCADA, MES, historians, industrial protocols, predictive maintenance, computer vision on the shop floor, and industrial digital twins.

🇷🇺 **[Читать по-русски →](README.ru.md)**

---

## Why this list exists

The general agentic-AI ecosystem is huge and well-catalogued. Industrial applications are not. Most awesome-lists index chatbots, coding agents, and SaaS products — none of them tell you which projects are actually usable when the endpoint is an OPC UA server, a Modbus PLC, or a process historian, and when a wrong action can stop a furnace.

This list tries to answer a narrower question: **which agentic-AI projects survive contact with operational technology?**

**In scope:** LLM agents for SCADA/DCS/MES/historian, industrial-protocol connectors (OPC UA, Modbus, MQTT), OT-aware guardrails and policy layers, benchmarks and simulators for process control, predictive maintenance with LLMs, industrial computer vision, digital-twin-with-LLM hybrids.

**Out of scope:** general-purpose agentic frameworks (LangChain, AutoGen, CrewAI — see [awesome-ai-agents][kurilyak]), coding agents, sales/CRM agents, non-industrial predictive maintenance for pure SaaS.

**Curation stance:** "Top" in the name means opinionated. Projects included must (a) be reproducible or verifiably deployed, (b) address an industrial concern explicitly, (c) have public documentation. Marketing pages without code, demos, or peer-reviewed papers are rejected. A closed-source project may be listed if it has documented industrial deployments — it will be marked 🔒.

**Status:** v0.2 — early, fact-checked. Many categories are intentionally thin because the corresponding niche is genuinely empty. Empty categories are marked 🚧 and are open for contributions.

[kurilyak]: https://github.com/slavakurilyak/awesome-ai-agents

---

## Table of Contents

- [🔌 Industrial Protocol Bridges](#-industrial-protocol-bridges) — MCP/agent connectors for OPC UA, Modbus, MQTT, Historian
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

Legend: ⭐ stars · 🔒 closed-source · 🚧 category open for contributions · 🇷🇺 Russian-speaking ecosystem · 🇨🇳 Chinese ecosystem

---

## 🔌 Industrial Protocol Bridges

### [winccoa/winccoa-ae-js-mcpserver](https://github.com/winccoa/winccoa-ae-js-mcpserver) — Official Siemens MCP for WinCC OA
Official MCP server from Siemens for WinCC Open Architecture. JavaScript, extensive functionality: datapoints (read/write/create), OPC UA and MQTT connectivity, dashboards, alarms, archives, Pmon process management, PV range validation, 1400+ built-in icons. **Includes a built-in write-exclusion model**: administrators can disable entire tool categories (`datapoints/dp_set`, `dp_create`, `dp_type_create`) to prevent write operations to SCADA config and runtime data.
**Verdict:** first major-vendor MCP for industrial SCADA, and the most feature-complete industrial MCP available today. Signals mainstream adoption of MCP in OT. The write-exclusion model is a first step toward OT-aware access control, though not yet policy-driven at the semantic level.

### [vogler75/winccua-mcp-server](https://github.com/vogler75/winccua-mcp-server) — Third-party MCP for WinCC Unified
MCP server for **WinCC Unified** (a different Siemens SCADA product from WinCC OA), via its GraphQL API. Covers browsing objects, reading current tag values, historical logged values, active and logged alarms, tag writes, alarm resets. Community-maintained.
**Verdict:** useful counterpart for shops running WinCC Unified rather than OA. Not to be confused with the official OA server above.

### [kukapay/opcua-mcp](https://github.com/kukapay/opcua-mcp) — Minimal generic OPC UA MCP
Small reference MCP server for OPC UA. Five tools: read node, write node, browse namespace, read multiple, write multiple. No policy layer, no scoping, no auth model — write access is unrestricted.
**Verdict:** 6 stars, last activity May 2025 — this is an educational example, not a production tool. Included as the "naive baseline" that illustrates why OT-aware policy layers matter.

### [IndustriAgents/OPCUA-MCP](https://github.com/IndustriAgents/OPCUA-MCP) — Local OPC UA bridge for MCP clients
Browse OPC UA address spaces, read current and historical data, and monitor subscriptions, events and alarms. The default profile prevents writes and method calls.
**Verdict:** Runnable in Python or Node with a mock server for testing. It uses local stdio and connects to one OPC UA endpoint per process; real equipment requires a secured OPC UA channel.

### 🚧 Modbus MCP server — no production-quality entry yet
Several small experiments exist; nothing recommended in v0.2. Contributions welcome.

### 🚧 Historian MCP server — none identified
Reading historical time-series data through an agent (PI, Alpha.Historian, Aveva Historian, etc.) is a common industrial need with no publicly-released MCP implementation. Big gap.

---

## 🛡️ OT-Aware Guardrails & Policy Layers

### [meta-llama/PurpleLlama — LlamaFirewall](https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall)
Meta's open-source guardrail framework for LLM agents. Three primary scanners: **PromptGuard 2** (BERT-style jailbreak/injection detector), **AgentAlignmentCheck** (chain-of-thought auditor for goal-misalignment), **CodeShield** (static analysis for insecure code generation), plus customizable regex filters. Documented paper (arXiv 2505.03574) and website.
**Verdict:** the most mature open-source agent guardrail as of mid-2026. **Text-level only — does not understand process semantics** (rates of change, interlocks, physical constraints). Essential baseline for any industrial agent stack; insufficient on its own.

### [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)
NVIDIA's programmable guardrail toolkit. Five rail types: input, dialog, retrieval, execution, output. Integrates with Nemotron Content Safety, Topic Control, and Jailbreak Detect NIMs. Recently decoupled from LangChain (optional now). Active releases through 2026, including IORails milestone 2 (a new orchestration engine).
**Verdict:** the other major general-purpose guardrail platform. Same limitation as LlamaFirewall — general-purpose, no OT semantics — but a rich policy language (Colang) makes it plausibly extensible to industrial rules.

### Research frontier (2025–2026)

The academic and industrial community has produced a cluster of guardrail research in the last 12 months. None are production-grade in OT, but the direction is clear:

- **[AgentWall](https://arxiv.org/abs/2605.16265)** — OS-level runtime interception of shell commands, API calls, filesystem operations before execution. Preprint (May 2026), no public code yet. Closest in spirit to what OT needs.
- **AgentGuardian** (arXiv 2601.10440) — learned access-control policies for LLM agents
- **ToolSafe** (arXiv 2601.10156) — pre-execution safety detection at the tool-call step
- **OneShield** (arXiv 2507.21170) — "next-generation LLM guardrails" from IBM
- **[protectai/llm-guard](https://github.com/protectai/llm-guard)** — production-oriented security toolkit for LLM interactions

### 🚧 OT-aware policy layer — nothing production-ready yet
The gap: a guardrail that understands process context — that a write to `TIC-101` valid in absolute terms (40°C is in range) is still dangerous because current value is 22°C and the rate of change violates a safety envelope. The Siemens WinCC OA MCP has category-level exclusions; community projects like `uebelmar-oa-mcp` add plant-specific rules (forbidden tag patterns `*_SAFETY_*`, `*_ESD_*`, operational limits). But no standalone, vendor-neutral, semantics-aware OT guardrail exists. **This is one of the clearest open niches in industrial agentic AI.**

---

## 📊 Industrial Agent Benchmarks

### [amazon-science/SOP-Bench](https://github.com/amazon-science/SOP-Bench)
2000+ tasks across 12 domains testing agents on Standard Operating Procedures. Human expert-authored SOPs, executable interfaces with ground-truth outputs, evaluated on Environment Completion Rate (ECR), Task Success Rate (TSR), and Constraint-aware TSR. 11 frontier models already benchmarked; function-calling agents average ~64% task success. Paper: arXiv 2506.08119 (v2, Feb 2026, submitted to KDD 2026 Datasets Track).
**Verdict:** the most authoritative recent benchmark for procedural agent execution. Domains include Dangerous Goods, healthcare intake, logistics — industrially adjacent but **not process control**.

### [IBM/AssetOpsBench](https://github.com/IBM/AssetOpsBench)
IBM's flagship Industry 4.0 benchmark. **460+ scenarios**, 5 specialist agents (IoT, FMSR, TSFM, Work Order, plus orchestrator), multi-agent orchestration blueprints (MetaAgent, AgentHive) — **all built over MCP**. Grounded in ISO standards for platform-agnosticism (works across Oracle, IBM Maximo, others). Has a HuggingFace Space Playground and co-locates a challenge at IJCAI 2026. Active university extensions (Columbia, Binghamton, Albany). Paper: arXiv 2506.03828.
**Verdict:** the most active industrial agent benchmark community in 2026. Focus is asset lifecycle management — condition monitoring, maintenance planning, work-order generation — **not real-time process supervision**.

### [Leezekun/SOPBench](https://github.com/Leezekun/SOPBench)
Parallel SOP-following benchmark (note the different capitalization from Amazon's). Seven customer-service domains: bank, online market, DMV, healthcare, library, hotel, university. Different methodology, different constraint model — worth knowing as a comparison point.
**Verdict:** narrower domain than Amazon's SOP-Bench, but methodologically distinct and useful for triangulation.

### 🚧 Closed-loop process control benchmark — nothing exists
No open benchmark places an agent as supervisor of a running dynamic process, scored on safety-envelope violations, intervention count, and diagnostic quality on alarm floods. Candidates for a base simulator: Tennessee Eastman Process (see below), MODEX, custom batch processes. **Major open niche.**

---

## 🎛️ Process Simulators for Agent Evaluation

### Tennessee Eastman Process — a family of reference implementations
The classic Downs–Vogel–Braatz benchmark chemical process — reactor, separator, stripper, compressor, with configurable faults. Widely used in fault detection and process control research since 1993.

- **[ccreinartz11/pytep](https://github.com/ccreinartz11/pytep)** — pyTEP, high-level Python API for interactive simulation. Best entry point for agent supervision experiments. (Reinartz & Enevoldsen, SoftwareX 2022)
- **[jkitchin/tennessee-eastman-profbraatz](https://github.com/jkitchin/tennessee-eastman-profbraatz)** — original Fortran 77 codes plus Python backend via f2py (~5-10× faster).
- **[camaramm/tep2py](https://github.com/camaramm/tep2py)** — Python interface to the original Fortran TEP.
- **[usnistgov/tesim](https://github.com/usnistgov/tesim)** — NIST's version, optimized for wireless and cybersecurity research.
- **[ElsevierSoftwareX/SOFTX-D-24-00664](https://github.com/ElsevierSoftwareX/SOFTX-D-24-00664)** — COSTEP, complete open Simulink model of TEP.

**Verdict:** natural base for any process-control agent benchmark. pyTEP is the recommended starting point unless you need Fortran-level speed.

### 🚧 Batch-process simulators (concrete, hydroponics, food)
Discrete and batch industrial processes are underrepresented in openly available simulators. Contributions welcome, especially with realistic alarm patterns.

---

## 🤖 Operator Advisors & Copilots

Every credible operator advisor in industry today is proprietary and predates the current LLM wave. Listed here for landscape context, not as reproducible references.

### 🇷🇺 [Piklema Predictive](https://piklema.com/) 🔒
Helsinki-based, Russian-speaking team. Series A ($12.82M, July 2025). Flagship product **Driver Assistant** — real-time audio/visual advisor for open-pit dump truck operators, claimed effect **3-5% fuel savings**. Not process control; driver-behavior optimization. Additional products for tire, engine, and fatigue management.
**Verdict:** a working example of a pre-LLM digital advisor delivering measurable value in a narrow niche. Instructive for what "trust boundaries" and "operator UX" look like in production.

### 🇷🇺 [Zyfra (Цифра)](https://www.zyfra.com/) 🔒
Largest Russian-speaking industrial IIoT vendor. Not a single "advisor" product — a full stack: ZIIoT platform, Machine Data Collection (MDC Plus), Zyfra AI (process optimization via deep learning), Zyfra EYE (computer vision), plus vertical products for mining (Dispatcher, Overview 360, robotic drilling, autonomous haul truck), oil & gas, metallurgy, chemistry. All pre-LLM AI/ML.
**Verdict:** the reference "traditional industrial AI" stack in the Russian-speaking market. Included for landscape awareness of what LLM-based advisors will be measured against.

### 🇷🇺 SIPO (Rosatom, Novovoronezh NPP) 🔒
Nuclear operator support system, publicly documented as analysing ~360 systems, supporting ~200 procedures, with 30-minute forecasting horizon. No public implementation or SDK.
**Verdict:** referenced in Russian conference proceedings as the domestic reference for advisor systems at highest-criticality installations. Useful as a target for "what a mature advisor architecture looks like" without being available for reproduction.

### 🚧 Open-source LLM operator advisor — none identified
First open reference implementation is unclaimed.

---

## 🔧 Predictive Maintenance with LLMs

### 🚧 This category is thin
Predictive maintenance has a mature classical-ML ecosystem. LLM-augmented approaches (anomaly narration, RCA assistance, work-order drafting from sensor patterns) are emerging in research papers but rarely as open projects. IBM's AssetOpsBench (see Benchmarks) touches this space with its FMSR and Work Order agents. Contributions welcome.

---

## 👁️ Industrial Computer Vision Agents

### 🚧 Category placeholder
VLM-based agents for quality inspection, PPE detection, safety-zone monitoring exist as vendor products (Landing AI, Cognex, various startups) but rarely as open-source. Contributions welcome, especially where the VLM is used agentically (planning inspection routes, escalating findings) rather than as a simple classifier.

---

## 🌐 Digital Twin + LLM

### 🚧 Category placeholder
Research is active (Imperial College fault-tolerant control via LLM agents on digital twins, etc.) but reproducible open implementations are rare. Contributions welcome.

---

## 🏭 Vendor Platforms

Included for landscape awareness. None are open source.

- **Siemens Industrial Copilots + NVIDIA Industrial AI OS** 🔒 — nine copilots announced at CES 2026, tight coupling with Siemens hardware and software stack
- **Honeywell Forge** 🔒 — enterprise operations platform with AI modules
- **ABB Genix / ABB Ability** 🔒 — industrial analytics platform
- **Cognite Data Fusion + Atlas AI** 🔒 — industrial data platform with LLM layer
- **AspenTech / Aspen Hybrid Models** 🔒 — process optimization with hybrid ML
- **C3 AI Industrial Suite** 🔒
- 🇷🇺 **Atomiq Software / Alpha Platform** 🔒 — Russian SCADA vendor; no AI/LLM modules published as of v0.2 of this list

---

## 📚 Research & Standards

- **ASM Consortium** — [Abnormal Situation Management guidelines](https://www.asmconsortium.net/) — foundational human-factors work, decades of data. Key finding: 42% of process incidents have human factors in root cause.
- **Siemens True Cost of Downtime 2024** — most-cited industry study on unplanned downtime economics ($1.4T/year for Fortune Global 500, 11% of revenue).
- **MCP (Model Context Protocol)** — [spec](https://modelcontextprotocol.io/) — the standard now being adopted by industrial vendors (Siemens WinCC OA).
- **[GitHub MCP Registry](https://github.com/mcp)** — the emerging standard MCP catalog.
- **ISA-95 / ISA-88 / ISA-101 / ISA-18.2** — the industrial standards agents will need to respect. No public work yet on embedding these formally into agent guardrails.
- 🚧 Open-source implementations of ISA-18.2 alarm-management logic usable by agents — none identified.

---

## 🧰 Adjacent Tools Worth Knowing

General-purpose but genuinely useful when building industrial agent systems:

- **[AgentOps-AI/agentops](https://github.com/AgentOps-AI/agentops)** — Python SDK for agent monitoring, LLM cost tracking, session replay. Integrates with CrewAI, OpenAI Agents SDK, LangChain, AutoGen, AG2, CamelAI. TypeScript version at `AgentOps-AI/agentops-ts`. *Not to be confused with Microsoft's Azure/agentops, which is a separate product for Azure AI Foundry.*
- **[stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)** — ~35k stars, 5.9M+ monthly downloads. Compilable-prompt framework from Stanford NLP. Signatures, modules, optimizers (MIPROv2, GEPA). Relevant for evals-heavy industrial workflows where prompts need systematic tuning rather than hand-crafting.
- **[e2b-dev/E2B](https://github.com/e2b-dev/E2B)** — sandboxed code execution for agents. Conceptually related to shadow-mode for OT: run the agent's proposed actions in isolation before letting them touch reality.
- **[topoteretes/cognee](https://github.com/topoteretes/cognee)** — knowledge-graph layer for LLMs. Useful for grounding agent reasoning in regulations, SOPs, and P&IDs.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

Preferred contributions in v0.2:
1. **Filling 🚧 categories** — even a single credible entry per gap is high-value
2. **Corrections** — if a project I listed as "no policy layer" actually has one, tell me
3. **Removing hype** — if you find a project I included that doesn't meet the curation stance, PR the deletion
4. **Regional coverage** — Chinese ecosystem 🇨🇳 is underrepresented; contributions from readers with access to Baidu-space projects especially welcome

## Maintainer

Curated by [Ali](https://github.com/alikup-ai) — background in operating a manufacturing enterprise and pipeline-industry OT, currently building industrial AI-agent tooling. Reach out for corrections or collaboration.

## License

Content: [CC0-1.0](LICENSE) — public domain. Use freely.
