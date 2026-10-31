# BATCH01 Results Summary

The collected matrix contains 24 synthetic traces evaluated under four designs: 96 successful runs and zero failures. Each run has 10,000 warmup and 100,000 measured accesses. Total measured accesses are 9,600,000. The runs form 24 matched trace groups, not 96 independent application samples.

The table reports miss counts out of 100,000 measured accesses. W4-random reports the mean over all ten seeds; each seed has zero misses for every design. All other rows are single deterministic cases.

| Scenario | D0 misses | D1 misses | D2 misses | DAI-v1 misses | D0 / DAI traffic (bytes) |
|---|---:|---:|---:|---:|---:|
| W1-read | 12,500 | 12,500 | 12,500 | 12,500 | 400,000 / 400,000 |
| W1-write | 12,500 | 12,500 | 12,500 | 12,500 | 800,000 / 800,000 |
| W2-1024 | 0 | 0 | 0 | 0 | 0 / 0 |
| W2-4096 | 0 | 0 | 0 | 0 | 0 / 0 |
| W2-16384 | 12,500 | 12,500 | 12,500 | 12,500 | 400,000 / 400,000 |
| W3-N8 | 1,389 | 1,389 | 1,389 | 1,389 | 88,896 / 88,896 |
| W3-N32 | 379 | 379 | 379 | 379 | 21,376 / 21,376 |
| W3-N128 | 97 | 97 | 97 | 97 | 3,104 / 3,104 |
| W3-N512 | 24 | 24 | 24 | 24 | 768 / 768 |
| W3-N2048 | 12,537 | 12,537 | 12,537 | 12,537 | 402,752 / 402,752 |
| W4-even | 0 | 0 | 0 | 0 | 0 / 0 |
| W4-random | 0 | 0 | 0 | 0 | 0 / 0 |
| W5-K2 | 100,000 | 0 | 0 | 0 | 3,200,000 / 0 |
| W5-K4 | 100,000 | 100,000 | 0 | 0 | 3,200,000 / 0 |
| W5-K8 | 100,000 | 100,000 | 100,000 | 0 | 3,200,000 / 0 |

DAI-v1 matches the conventional designs in W1-W4 and improves over D0 only in the declared W5 conflict stress. D1 also removes W5 misses for two competing blocks; D2 does so for two and four. W5 benefits depend on the chosen placement pattern.

Memory traffic counts 32-byte fills and dirty writebacks in measurement, without a final flush. AMAT values in the separate sensitivity table use assumed lookup and extra miss-penalty cycles; they are not hardware measurements. Insufficient time and financial resources prevented hardware implementation and validation.

The original CSV tables are retained unchanged. This submission summary is a regenerated presentation of those tables; the historical release is preserved separately in the original evidence archive.
