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
2. Add your entry to the appropriate section in **both** `README.md` and `README.ru.md`, and to `data.yaml`
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
- **`data.yaml` mirrors the READMEs.** Add the project to all three in the same PR. v0.2 drifted because `data.yaml` was left behind at v0.1 while the README moved on, and the file that called itself the source of truth became the least accurate one.
- **Never hand-edit `stars`, `pushed` or `archived`.** Those are written by `python update_stars.py` and refreshed weekly by CI. Set them to `0`/`null` in a new entry and let the script fill them in.
- **Star counts are not a criterion.** Several of the most on-target projects in this list have zero or single-digit stars. Do not argue for inclusion on popularity, and do not argue for exclusion on obscurity.

## What we especially want in v0.3

Five niches are marked 🚧 because they are genuinely empty, re-checked on 2026-11-07. One credible entry in any of them is worth more than ten additions elsewhere:

1. **Process-semantics-aware safety envelope** — a guardrail that understands rate-of-change limits, interlocks, mode-dependent envelopes and cross-tag constraints. Everything that exists governs the *agent*; nothing governs the *physics*. This is the clearest open niche in the field.
2. **Closed-loop process control benchmark** — an agent supervising a running dynamic process, scored on safety-envelope violations, intervention count and diagnostic quality under alarm floods.
3. **Batch-process simulators** (concrete, hydroponics, food) with fault models and realistic alarm behaviour. Closing this unlocks #2.
4. **Open-source LLM operator advisor** — no open reference implementation exists.
5. **Agentic industrial computer vision** — where the VLM plans inspection routes and escalates findings, not a classifier behind an API.

Also wanted:

6. **Corrections.** v0.3 exists because v0.2 contained wrong star counts, a stale repository path, an archived project listed as live, a misdated preprint, and four "nothing exists here" claims that were already false. If something here is wrong, say so — that is the most valuable contribution to this list.
7. **Non-English ecosystems.** The 🇨🇳 Chinese section was added in v0.3 and is still thin. Japanese, Korean and German industrial projects are entirely absent.
8. **Removing hype** — if a project doesn't meet the curation stance, PR the deletion with justification.

## What we don't want

- Adding a project you contributed to without disclosing that in the PR
- Blanket additions ("here are 50 projects from another list")
- Marketing rewrites of existing entries
- Reorganization proposals without discussing in an issue first

## Questions

Open an issue with the `question` label. Substantive category or scope questions are welcome — this list is v0.3 and the shape of it will evolve.
