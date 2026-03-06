# Claims (claims-first)

- generated_utc: 2026-03-04T11:22:19+00:00
- count: 4

Read this first for agent review. Each claim links to its block (supports) and to evidence excerpts.

## C1: [cl_table_main_has_header](blocks/cl_table_main_has_header.md)
- section: Logic Checks (logic_checks)
- kind: `paragraph` status: `supported` type_guess: `empirical`
- evidence_ids:
  - [ev_config_outline_yaml](evidence/ev_config_outline_yaml.md)
  - [ev_paper_layout_2026_03_03_table_main_compact_csv](evidence/ev_paper_layout_2026_03_03_table_main_compact_csv.md)
- positioning_status: `declared`
- closest_prior: `\\cite{kimura2022silentspeller}`
- known:
  - Silent speech interface surveys emphasize that evaluation comparisons are protocol-dependent.
- new:
  - This work exposes protocol tables as deterministic artifacts pinned by checksum.
- unverified:
  - External baseline systems are not evaluated in these tables.
- positioning_citations: `\\cite{denby2010silent,kimura2022silentspeller}`
- positioning_evidence: [ev_related_work_survey_epgspeller_2026-02-17_report_md](evidence/ev_related_work_survey_epgspeller_2026-02-17_report_md.md)
- verification_queries:
  - `a_table_main_header`: PASS (`protocol,n,cer,lex` == `protocol,n,cer,lex`) from [ev_paper_layout_2026_03_03_table_main_compact_csv](evidence/ev_paper_layout_2026_03_03_table_main_compact_csv.md)
- claim_text:
  - The baseline table includes protocol and aggregate metrics fields.

## C2: [cl_dataset_summary_has_header](blocks/cl_dataset_summary_has_header.md)
- section: Logic Checks (logic_checks)
- kind: `paragraph` status: `supported` type_guess: `empirical`
- evidence_ids:
  - [ev_paper_layout_2026_03_03_table_dataset_summary_csv](evidence/ev_paper_layout_2026_03_03_table_dataset_summary_csv.md)
- positioning_status: `declared`
- closest_prior: `\\cite{kimura2022silentspeller}`
- known:
  - Silent speech interface surveys emphasize that evaluation comparisons are protocol-dependent.
- new:
  - This work exposes protocol tables as deterministic artifacts pinned by checksum.
- unverified:
  - External baseline systems are not evaluated in these tables.
- positioning_citations: `\\cite{denby2010silent,kimura2022silentspeller}`
- positioning_evidence: [ev_related_work_survey_epgspeller_2026-02-17_report_md](evidence/ev_related_work_survey_epgspeller_2026-02-17_report_md.md)
- verification_queries:
  - `a_dataset_summary_header`: PASS (`id,N,V,Tmed,contact,zero` == `id,N,V,Tmed,contact,zero`) from [ev_paper_layout_2026_03_03_table_dataset_summary_csv](evidence/ev_paper_layout_2026_03_03_table_dataset_summary_csv.md)
- claim_text:
  - The dataset summary table includes id, N, V, Tmed, contact, and zero fields.

## C3: [cl_spatial_table_has_header](blocks/cl_spatial_table_has_header.md)
- section: Logic Checks (logic_checks)
- kind: `paragraph` status: `supported` type_guess: `empirical`
- evidence_ids:
  - [ev_paper_layout_2026_03_03_table_spatial_all_csv](evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- positioning_status: `declared`
- closest_prior: `\\cite{kimura2022silentspeller}`
- known:
  - Silent speech interface surveys emphasize that evaluation comparisons are protocol-dependent.
- new:
  - This work exposes protocol tables as deterministic artifacts pinned by checksum.
- unverified:
  - External baseline systems are not evaluated in these tables.
- positioning_citations: `\\cite{denby2010silent,kimura2022silentspeller}`
- positioning_evidence: [ev_related_work_survey_epgspeller_2026-02-17_report_md](evidence/ev_related_work_survey_epgspeller_2026-02-17_report_md.md)
- verification_queries:
  - `a_spatial_table_header`: PASS (`protocol,variant,cer,rtf` == `protocol,variant,cer,rtf`) from [ev_paper_layout_2026_03_03_table_spatial_all_csv](evidence/ev_paper_layout_2026_03_03_table_spatial_all_csv.md)
- claim_text:
  - The spatial modeling table includes protocol, variant, CER, and RTF fields.

## C4: [cl_k64_table_has_header](blocks/cl_k64_table_has_header.md)
- section: Logic Checks (logic_checks)
- kind: `paragraph` status: `supported` type_guess: `empirical`
- evidence_ids:
  - [ev_paper_layout_2026_03_03_table_k64_all_csv](evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- positioning_status: `declared`
- closest_prior: `\\cite{kimura2022silentspeller}`
- known:
  - Silent speech interface surveys emphasize that evaluation comparisons are protocol-dependent.
- new:
  - This work exposes protocol tables as deterministic artifacts pinned by checksum.
- unverified:
  - External baseline systems are not evaluated in these tables.
- positioning_citations: `\\cite{denby2010silent,kimura2022silentspeller}`
- positioning_evidence: [ev_related_work_survey_epgspeller_2026-02-17_report_md](evidence/ev_related_work_survey_epgspeller_2026-02-17_report_md.md)
- verification_queries:
  - `a_k64_table_header`: PASS (`protocol,method,cer,rtf` == `protocol,method,cer,rtf`) from [ev_paper_layout_2026_03_03_table_k64_all_csv](evidence/ev_paper_layout_2026_03_03_table_k64_all_csv.md)
- claim_text:
  - The electrode reduction table includes protocol, method, CER, and RTF fields.
