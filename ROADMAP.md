# agentic-config Roadmap

This roadmap tracks the evolution of this fork into a **prompt-based installer/distribution** for AI coding configurations.

Core goals:
- Keep using the **existing profile system** (`registry.json`)
- Keep `install.sh` as the **single installer engine**
- Support installing into **project** (`./.opencode`) and **global** (`~/.config/opencode`) targets
- Continue shipping and improving agents, commands, system builder, tools, and plugins

---

## 🎯 Now (Current Focus)

**Priority items for the next 4–6 weeks:**

- [ ] README/docs alignment for this fork (fix repo URLs, targets, examples)
- [ ] Define and document install targets clearly (project vs global)
- [ ] Expand/curate profiles for personal use cases (e.g. `esp32`, `linux-admin`, etc.)
- [ ] Remove or quarantine unused files over time (without breaking installer profiles)
- [ ] Document upstream syncing workflow (merge/rebase + conflict strategy)

---

## 🔜 Next (Coming Soon)

**Planned for the following 6–10 weeks:**

- [ ] Add `.env` handling per install target (copy/merge/skip) via `install.sh`
- [ ] Add MCP server selection per install target (format + prompts TBD)
- [ ] Improve installer UX for non-interactive installs (flags + output)
- [ ] Add more example profiles/workflows to validate real-world installs

---

## 🔭 Later (Exploration / TBD)

- [ ] Claude Code support alongside OpenCode (details TBD; avoid guessing formats)
- [ ] Better “update” story for customized installs (guided upgrade strategies)
- [ ] Additional tooling integrations as needed

---

## 📝 How to Use This Roadmap

- Track work via GitHub issues in this repo: https://github.com/fcimeson/agentic-config/issues
- Label suggestions with `idea` where appropriate

**Last Updated:** December 15, 2025
