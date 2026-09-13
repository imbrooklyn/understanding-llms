# Part V acceptance evidence

`as_of: 2026-09-13`

These records describe actual local execution, separately from the assigned mechanism fixtures and measured candidate runs. Logs preserve the command output; the two workspace-specific absolute repository paths are replaced by `<book-root>` and `<main-root>`. No output lines or failures are converted into successful results. The successful final runs are retained here; earlier failures, corrections and the interrupted stale-cache run are described in [the validation record](../../../docs/part-v-validation.md).

`acceptance.json` records the commands, environment, final exit codes, log hashes, source-preservation check and composition check. Browser screenshots and the Playwright report are local generated files in `test-results/` and `playwright-report/`; they remain ignored. Re-running `pnpm test:browser` creates fresh screenshots for every Part V figure in both languages, themes and viewports, plus page openings, equations, wide-table edges and visible answers. The validation record distinguishes screenshot inspection from automated assertions.

These logs are historical evidence, not a claim that future machines must reproduce elapsed times. Re-run the documented commands to validate another environment. Original records and this explanation are CC BY-SA 4.0; dependency and tool names do not imply endorsement or a change to their licenses.
