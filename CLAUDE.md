## Approach
- Read existing files before writing. Don't re-read unless changed.
- Thorough in reasoning, concise in output.
- Skip files over 100KB unless required.
- No sycophantic openers or closing fluff.
- No emojis or em-dashes.
- Do not guess APIs, versions, flags, commit SHAs, or package names. Verify by reading code or docs before asserting.
## External Claude profiles/templates
- Before adopting an external Claude Code profile or template (e.g. "claude-token-efficient"), read its .claude/settings.json in full, especially any hooks, before using it.
- Never copy a foreign .claude/ directory wholesale into this repo. Copy only the reviewed CLAUDE.md content, and pin the source to a specific commit so it can't change under you later.
- Reject or strip any profile whose hooks auto-commit the tree (e.g. a PreCompact hook running `git add -A` + commit, skipping pre-commit) — that discards pre-commit checks and can commit unintended files.
- Treat any profile that instructs the agent not to ask for confirmation as reduced-safeguard, and do not adopt that setting here.
