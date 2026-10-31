// AI self-check of design arithmetic and toy expected results, not the research
// simulator, official benchmark, or an independent review. Run from ai/:
// node verification/check_q10_spec.mjs
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const checks = [];
function check(name, fn) { fn(); checks.push({ name, status: 'PASS' }); }
const index = (b, k) => (b ^ (b >>> k)) & (2 ** k - 1);
const recover = (s, t, k) => (t * 2 ** k) + (s ^ (t & (2 ** k - 1)));
const names = ['accesses', 'hits', 'misses', 'read_misses', 'write_misses',
  'evictions', 'dirty_writebacks', 'line_fills'];

// The toy oracle stores full block IDs and LRU-to-MRU lists, rather than the
// compressed tags and single LRU bit of the proposed implementation.
class ToyOracle {
  constructor(mode = 'DAI') {
    this.mode = mode;
    this.nsets = mode === 'D0' ? 128 : 64;
    this.ways = mode === 'D0' ? 1 : 2;
    this.sets = Array.from({ length: this.nsets }, () => []);
    this.begin();
  }
  begin() { this.c = Object.fromEntries(names.map(n => [n, 0])); this.wb = []; }
  access(op, a, size = 4) {
    if (!['R', 'W'].includes(op) || !Number.isInteger(a) || size !== 4 ||
        a < 0 || a > 0xFFFFFFFC || a % 4 !== 0) throw new Error('invalid input');
    const b = Math.floor(a / 32);
    const s = this.mode === 'DAI' ? index(b, 6) : b % this.nsets;
    const lines = this.sets[s];
    const pos = lines.findIndex(x => x.b === b);
    this.c.accesses++;
    if (pos >= 0) {
      const [line] = lines.splice(pos, 1);
      if (op === 'W') line.dirty = true;
      lines.push(line);
      this.c.hits++;
      return 'H';
    }
    this.c.misses++;
    this.c[op === 'R' ? 'read_misses' : 'write_misses']++;
    if (lines.length === this.ways) {
      const victim = lines.shift();
      this.c.evictions++;
      if (victim.dirty) { this.c.dirty_writebacks++; this.wb.push(victim.b * 32); }
    }
    lines.push({ b, dirty: op === 'W' });
    this.c.line_fills++;
    return 'M';
  }
}
function toy(trace, expected, counters = {}, mode = 'DAI', warmup = []) {
  const cache = new ToyOracle(mode);
  for (const [op, a] of warmup) cache.access(op, a);
  cache.begin();
  assert.equal(trace.map(([op, a]) => cache.access(op, a)).join(''), expected);
  for (const [name, value] of Object.entries(counters)) assert.equal(cache.c[name], value, name);
  assert.equal(cache.c.hits + cache.c.misses, cache.c.accesses);
  assert.equal(cache.c.read_misses + cache.c.write_misses, cache.c.misses);
  assert.equal(cache.c.line_fills, cache.c.misses);
  assert(cache.c.dirty_writebacks <= cache.c.evictions && cache.c.evictions <= cache.c.misses);
  return cache;
}
const R = (...addresses) => addresses.map(a => ['R', a]);

check('A/B: round-trip over 262144 low blocks and upper-bound probes', () => {
  for (const k of [6, 7]) {
    for (let b = 0; b < 262144; b++) assert.equal(recover(index(b, k), b >>> k, k), b);
    for (const b of [2 ** 26, 2 ** 27 - 128, 2 ** 27 - 1])
      assert.equal(recover(index(b, k), b >>> k, k), b);
  }
});
check('A/B: victim writeback addresses require inverse hash', () => {
  assert.equal(recover(1, 1, 7) * 32, 4096);
  assert.equal(recover(1, 1, 6) * 32, 2048);
});
check('A/B/C: conflict examples in R001/R002', () => {
  assert.equal(index(0, 7), index(129, 7));
  assert.notEqual(index(0, 7), index(128, 7));
  assert.deepEqual([0, 65, 130].map(b => index(b, 6)), [0, 0, 0]);
  assert.deepEqual([0, 4096, 8192].map(b => [b & 63, index(b, 6)]), [[0, 0], [0, 0], [0, 0]]);
  assert.deepEqual([2, 67, 128].map(b => index(b, 6)), [2, 2, 2]);
});
check('T01: repeat', () => toy(R(0, 0), 'MH', { hits: 1, misses: 1, evictions: 0 }));
check('T02: DAI/D0/D1', () => {
  for (const [mode, expected] of [['DAI', 'MMHH'], ['D0', 'MMMM'], ['D1', 'MMHH']])
    toy(R(0, 4096, 0, 4096), expected, {}, mode);
});
check('T03: exact recency expected trace', () =>
  toy(R(0, 2080, 0, 4160, 2080), 'MMHMM', { misses: 4, evictions: 2, dirty_writebacks: 0 }));
check('T04: dirty read hit preserves dirty; correct writeback base and traffic', () => {
  const cache = toy([['W', 2048], ...R(2048, 32, 4192)], 'MHMM',
    { misses: 3, evictions: 1, dirty_writebacks: 1, read_misses: 2, write_misses: 1 });
  assert.deepEqual(cache.wb, [2048]);
  assert.equal((cache.c.line_fills + cache.c.dirty_writebacks) * 32, 128);
});
check('T04: clean eviction traffic', () => {
  const cache = toy(R(2048, 2048, 32, 4192), 'MHMM', { dirty_writebacks: 0, evictions: 1 });
  assert.equal((cache.c.line_fills + cache.c.dirty_writebacks) * 32, 96);
});
check('T05: line boundary', () => toy(R(28, 32, 28), 'MMH', { line_fills: 2 }));
check('T06: debug circular generator arithmetic', () => {
  const addresses = Array.from({ length: 257 }, (_, i) => (i * 4) % 1024);
  assert.equal(addresses.at(-1), 0);
  const cache = new ToyOracle();
  for (const a of addresses) cache.access('R', a);
  assert.deepEqual([cache.c.accesses, cache.c.misses, cache.c.hits, cache.c.evictions], [257, 32, 225, 0]);
});
check('X01-X03: distinct tags, high bit and maximum address', () => {
  toy(R(0, 2080, 0), 'MMH');
  toy(R(0, 0x80000000, 0, 0x80000000), 'MMHH');
  toy(R(0xFFFFFFFC, 0xFFFFFFFC), 'MH');
  const b = Math.floor(0xFFFFFFFC / 32);
  assert.deepEqual([b, index(b, 6), b >>> 6, 0xFFFFFFFC % 32], [0x7FFFFFF, 0, 0x1FFFFF, 28]);
});
check('X04: warmup contents, recency and dirty survive counter reset', () => {
  const cache = toy(R(4160, 0), 'MH', { accesses: 2, misses: 1, hits: 1, evictions: 1,
    dirty_writebacks: 0 }, 'DAI', [['W', 0], ...R(2080, 0)]);
  assert(cache.sets[0].some(x => x.b === 0 && x.dirty));
});
check('X05: candidate loses against D0/D1 on toy counterexample', () => {
  toy(R(0, 2080, 4160, 0, 2080, 4160), 'MMMMMM', { evictions: 4 });
  for (const mode of ['D0', 'D1']) toy(R(0, 2080, 4160, 0, 2080, 4160), 'MMMHHH', {}, mode);
});
check('X06: invalid inputs reject without state mutation', () => {
  const cache = new ToyOracle(); cache.access('W', 0);
  for (const args of [['X', 0, 4], ['R', 0, 8], ['R', 2, 4], ['R', -4, 4], ['R', 2 ** 32, 4]]) {
    const before = JSON.stringify(cache);
    assert.throws(() => cache.access(...args), /invalid input/);
    assert.equal(JSON.stringify(cache), before);
  }
});
check('Metadata arithmetic: D0/D1/D2/DAI', () => {
  assert.deepEqual([128 * 22 / 8, (128 * 23 + 64) / 8, (128 * 24 + 256) / 8], [352, 376, 416]);
  assert.equal((128 * (27 + 2 + 64) + 64) / 8, 1496);
});
check('Original input/prompt evidence remains unchanged', () => {
  const originals = {
    'inputs/experiment_protocol.md': 'EDC53F5FCA930A031076279A1EA4A8280FAE1ABC768D630F60544A21CADFD0A6',
    'inputs/Tong_hop_9_bai_bao_tham_khao_Q10.md': 'D812B2FA879BAF05F5FE8C167785BC1FD3C59BE05CC4280454776DA504672F6D',
    'prompts/P001.md': '1733BFB4320CD901CDD537E04A305A38BE229BBDC0649BC758FCD18D40DCEFF2',
    'prompts/P002.md': '7678D037D95AADF760522693908756B83ABFBEF3ED7681058186136168ECD660',
    'prompts/P003.md': '18F3F6E9BCCD3C619538E2E4F9C5C3838C8FAA02D11D9B64A0BC1F2C5F264A7D'
  };
  for (const [path, expected] of Object.entries(originals))
    assert.equal(createHash('sha256').update(readFileSync(path)).digest('hex').toUpperCase(), expected, path);
});

console.log(JSON.stringify({ scope: 'AI self-check only; no official trace or independent review',
  checks_passed: checks.length, checks }, null, 2));
