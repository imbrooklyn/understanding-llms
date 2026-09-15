// SPDX-License-Identifier: Apache-2.0
import { spawnSync } from 'node:child_process';
const result = spawnSync(process.env.BOOK_PYTHON ?? 'python3', ['code/part-ix/run_notebooks.py'], { cwd: new URL('../', import.meta.url), stdio: 'inherit' });
if (result.error) console.error(result.error.message);
process.exit(result.status ?? 1);
