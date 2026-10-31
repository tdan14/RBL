# Interpretation of BATCH01

DAI-v1 does not reduce measured miss rates in W1-W4 under the frozen layouts. Its improvement over direct mapping is confined to W5. This supports a placement-specific benefit rather than a general improvement for weighing-station streams.

W1 accesses eight four-byte words per line, producing 12.5% misses in every organization. Write-back traffic distinguishes writing from reading: 800,000 versus 400,000 measured bytes. W2's 1/4-KiB buffers remain resident after warmup; the 16-KiB scan exceeds capacity and produces 12.5% misses. Zero measured misses excludes warmup and does not imply absence of initial compulsory misses.

W3 reuses recent samples; all corresponding miss rates match across the four organizations. The 2,048-sample case exceeds the common data capacity, but its finite prefix covers only 53 complete sample cycles and part of another. These measurements do not establish steady-state behavior. W4's four contiguous buffers occupy exactly 4 KiB; all designs retain this layout after warmup, yielding zero measured misses for the round-robin case and every random seed. Seed variation does not represent variation across arbitrary layouts.

W5 intentionally causes conventional set conflicts through 4-KiB spacing. DAI-v1 disperses the declared group. D1 accommodates two competing blocks; D2 accommodates two or four; neither accommodates eight in a single conventional set. The favorable XOR structure was known from the workload specification. It is a mechanism check rather than evidence of general optimization.

The candidate's metadata estimate is 376 bytes, 24 more than D0 and equal to D1. Actual area, power, and lookup latency are unmeasured. Under equal assumed lookup times, equal miss rates yield equal estimated AMAT. A 0.5- or one-cycle candidate lookup increment worsens estimated AMAT in W1-W4. W5 remains favorable under the declared sensitivity assumptions, but no application speedup follows directly from that calculation.

The inputs are synthetic, the data capacity and line size are fixed, and coherence, prefetching, bypassing, instruction execution, and writeback stalls are omitted. Insufficient time and financial resources prevented hardware implementation and validation. The contribution is a reproducible controlled comparison with explicit negative results outside the stress family, rather than a universal optimality or energy-efficiency claim.
