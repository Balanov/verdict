import assert from 'node:assert/strict';
import fs from 'node:fs';
import { VerdictModel } from '../site/src/verdict.js';

const raw = fs.readFileSync(new URL('../weights/verdict-q8.bin', import.meta.url));
assert.equal(raw.subarray(0, 4).toString(), 'VRD1');
const headerSize = raw.readUInt32LE(4);
const config = JSON.parse(raw.subarray(8, 8 + headerSize).toString('utf8'));
const bytes = raw.subarray(8 + headerSize);
const coef = new Int8Array(bytes.buffer, bytes.byteOffset, bytes.byteLength);
const model = new VerdictModel(config, coef);

const fixtures = [
  ['mvn test', 0, '[INFO] BUILD SUCCESS\nTests run: 8, Failures: 0', '', 'success'],
  ['pytest', 0, 'no tests ran\ncollected 0 items', '', 'unknown'],
  ['kubectl get pods', 1, '', 'Error from server (Forbidden): permission denied', 'blocked'],
  ['npm test', 1, 'Tests: 2 failed, 4 passed', '', 'failure'],
];
for (const [command, code, stdout, stderr, expected] of fixtures) {
  const result = model.predict(command, code, stdout, stderr);
  assert.equal(result.label, expected);
  assert.ok(Math.abs(Object.values(result.probabilities).reduce((a, b) => a + b, 0) - 1) < 1e-10);
  console.log(expected, result.confidence.toFixed(6));
}
console.log('Browser model fixtures: OK');
