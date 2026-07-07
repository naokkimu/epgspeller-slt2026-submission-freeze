# Revision Changelog — iter_007 (format compression)

## Summary
Compressed LaTeX from 10 pages (9 content + refs) to 4 pages (3 content + 1 ref) while preserving all primary numeric results and iter_006 claim calibration.

## Section changes
- **01_introduction**: Removed repetitive AAC/fixed-vocab paragraphs; kept four research questions and three contributions with P1/P2/P3/$k$ CER values.
- **02_signal_task**: Merged signal + task tables into `tab:task_definition`; compact `tab:dataset_summary`; retained p3/p4 repetition-density semantics.
- **03_system**: Merged seven subsections into two; single `tab:recognizer_design`; kept hyperparameters and config path.
- **04_evaluation**: Removed five redundant setup tables; kept `tab:protocol_map`; bridge and deferred-baseline scope in prose.
- **05_results**: Converted `table*` to single-column tables; inlined SilentSpeller bridge CER; kept main/kshot/transfer numbers.
- **06_discussion**: Three subsections (findings, calibration/AAC, ethics/limitations/future); restored deferred baseline and ethics detail.
- **07_conclusion**: Shortened without dropping calibration-efficiency takeaway.

## Tables removed (content preserved in prose or merged)
tab:signal_summary, tab:decoding_metrics, tab:calibration_setup, tab:silentspeller_bridge_setup, tab:controls_scope, tab:main_vs_ablation, tab:silentspeller_lite, tab:engineering_summary

## Numeric preservation
All CER/LEX/RTF values from iter_006 main tables retained; n semantics stated in results text and table captions.
