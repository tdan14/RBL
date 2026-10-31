# Analysis Table Definitions

The original CSV files retain their collected bytes. This dictionary clarifies units and signs.

| Field | Definition |
|---|---|
| `accesses` | Measured demand accesses; 100,000 per run |
| `hits`, `misses` | Measured events; their sum equals accesses |
| `read_misses`, `write_misses` | Misses classified by demand operation |
| `evictions` | Replacements of valid lines during measurement |
| `dirty_writebacks` | Evicted dirty lines transferred during measurement |
| `line_fills` | Complete-line fills; equal to misses without prefetch or bypass |
| `miss_rate` | Misses divided by measured accesses, stored as a fraction |
| `memory_traffic_bytes` | 32 times fills plus dirty writebacks; no final flush |
| `miss_rate_delta_pp` | 100 times (D0 miss rate minus this design's rate); positive means fewer misses than D0 |
| `relative_miss_reduction_pct` | 100 times (D0 rate minus this rate) divided by D0 rate; blank when D0 has zero misses |
| `n` | One for deterministic scenarios; ten for W4-random seed summaries |
| `miss_rate_mean` | Arithmetic mean of the group's fractional miss rates |
| `miss_rate_sample_stddev` | Sample standard deviation with denominator n-1; blank for n=1 |
| `traffic_bytes_mean` | Arithmetic mean measured traffic across the scenario's runs |
| `estimated_amat_cycles` | Assumed lookup cycles plus miss rate times additional miss penalty |
| `estimated_amat_reduction_pct` | Relative reduction of estimated AMAT against the same-trace D0 estimate |

The report's miss-rate table multiplies fractional rates by 100 and displays three decimals. Percentages and percentage-point differences are distinct. Deterministic runs are not replicated independent samples. Different cache designs on one trace form a matched comparison; a replay is not a new sample.
