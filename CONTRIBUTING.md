# Contributing to Top Industrial AI Agents

Thank you for helping curate this list. Because the value of a curated list is inversely proportional to noise, contributions are held to a specific bar.

## Curation stance

A project is included only if it meets **all three** criteria:

1. **Reproducible or verifiably deployed.** Open-source with runnable code, or closed-source with documented industrial deployments (case study, press release with client name, or peer-reviewed paper).
2. **Explicitly addresses an industrial concern.** Not just "usable in industry in principle." The project must be designed for, or documented against, industrial protocols (OPC UA, Modbus, IEC 61850, etc.), industrial systems (SCADA/DCS/MES/historian), or industrial workflows (operator advisories, work-order generation from sensor data, alarm-flood analysis, etc.).
3. **Public documentation.** README, paper, or vendor product page with enough detail to evaluate what it actually does. Landing pages with only "AI-powered" marketing prose are rejected.

## What we intentionally exclude

- General-purpose agentic frameworks (LangChain, AutoGen, CrewAI, etc.) — see [awesome-ai-agents](https://github.com/slavakurilyak/awesome-ai-agents)
- Coding agents, sales/CRM agents, personal assistants
- Chatbots without agentic tool use
- Consumer-facing products
- Whitepapers without implementations

## How to submit

1. Fork this repo
2. Add your entry to the appropriate section in **both** `README.md` and `README.ru.md`
3. Use the entry template below
4. Open a PR with the following in the description:
   - Which of the three criteria the project meets, with evidence
   - If closed-source, link to at least one documented industrial deployment
   - If it duplicates or replaces an existing entry, explain why

## Entry template

```markdown
### [Project Name](link) — one-line description
Brief factual summary of what it does. Focus on what makes it industrial. Include which protocols, systems, or workflows it targets.
**Verdict:** honest assessment of maturity, gaps, and where it fits. Avoid marketing language.
```

Add badges after the name where relevant:
- 🔒 closed-source
- 🇷🇺 🇨🇳 country of origin (only for ecosystem-relevant regional projects)
- 🚧 category placeholder (open for contributions)

## Style rules

- **Honest assessment beats promotion.** The whole point of the list is the "Verdict" line — if a project has known limitations, name them.
- **No emoji in project descriptions** (badges only).
- **No affiliate links, no tracking parameters.**
- **English README is primary; Russian mirror must be updated in the same PR.** If you don't speak Russian, add the entry to `README.md` only and note in the PR description that translation is needed — a maintainer will handle it.
- **One PR per project or per category cleanup** — don't mix additions with structural changes.

## What we especially want in v0.1

Priority contributions:

1. **Filling 🚧 categories** — the empty categories are marked because the corresponding niche is genuinely underserved. Even one credible entry per gap is high-value.
2. **Chinese-ecosystem coverage** 🇨🇳 — the Chinese industrial agent space is active (Huawei's industrial AI stack, Alibaba Cloud IoT + LLM, various OPC UA MCP experiments) and severely underrepresented in English-language lists.
3. **Corrections** — if a project I listed as "no policy layer" actually has one, or a category I marked as empty has a real project, file an issue or PR.
4. **Removing hype** — if you find a project that shouldn't be here by the curation stance, PR the deletion with justification.

## What we don't want

- Adding a project you contributed to without disclosing that in the PR
- Blanket additions ("here are 50 projects from another list")
- Marketing rewrites of existing entries
- Reorganization proposals without discussing in an issue first

## Questions

Open an issue with the `question` label. Substantive category or scope questions are welcome — this list is v0.1 and the shape of it will evolve.
