# Detex Proofread Report

## Summary
- body_lines: 141
- reference_entries: 19
- body_findings: 1
- reference_findings: 0

## Body Findings
- L125 R004: Double space or tab detected :: The dominant and most stable signal is the protocol gap: P3 CER is 0.691±0.133, versus 0.180±0.084 for P1 and 0.145±0.063 for P2. This ordering persists under front-end swaps, channel reduction, and low-shot settings, so cross-participant mismatch remains the primary error source in this audited setup.  Layout-aware bias alone is insufficient. Rowcol remains close to vec across P1-P3, while grid variants often increase CER and RTF; patch pooling narrows some gaps but does not create a consistent winner. Spatial encoders therefore need protocol-specific validation against explicit latency constraints.  Source aggregation helps at the p4 aggregate level (CER 0.686 to 0.582), but direction-level outcomes remain heterogeneous. Together with k-shot behavior (vec and rowcol improve from k1 to k2 while grid variants worsen), this indicates that transfer benefit depends on source-target compatibility and model family.  Our practical rule is protocol-specific selection under matched audited splits and manifests. We limit all claims to these datasets, this normalization pipeline, and these protocol definitions, and we do not extrapolate to unaudited populations or sensing setups.

## References Findings
- None
