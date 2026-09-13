// SPDX-License-Identifier: Apache-2.0
import { test } from 'node:test';
import { checkPartVNumbers } from '../scripts/part-v-evidence.mjs';
test('Part V independent calculations, complete paired records and evidence provenance', () => { checkPartVNumbers(); });
