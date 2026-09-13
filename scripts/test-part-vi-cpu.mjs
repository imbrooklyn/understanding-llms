// SPDX-License-Identifier: Apache-2.0
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const result = spawnSync(process.env.BOOK_PYTHON ?? 'python3', ['-m', 'unittest', 'discover', '-s', 'code/part-vi', '-p', 'test_*.py', '-v'], { cwd: fileURLToPath(new URL('../', import.meta.url)), stdio: 'inherit' });
if (result.error) console.error(result.error.message);
process.exit(result.status ?? 1);

