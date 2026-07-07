#!/usr/bin/env python3
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / 'results'
OUT = ROOT / 'report.md'
TOPIC = 'Related work and positioning update for EPGSpeller: auditable lexicon-free EPG silent spelling benchmarks, protocol-specific generalization, and transfer-aware SSI evaluation'
FIELD_GROUPS = [
    ('Basic Info', ['paper_id','title','authors','year','venue','doi','primary_url','pdf_url','code_or_data_release','citation_key_suggestion','coverage_origin']),
    ('Task & Data', ['modality','device','task','output_unit','vocabulary_setting','datasets']),
    ('Protocol & Evaluation', ['evaluation_protocol','protocol_generalization','participant_generalization','metrics_reported','benchmark_or_audit_status','leakage_or_constraint_notes']),
    ('Methods', ['decoder','model_architecture','spatial_frontend','augmentation','language_model_or_postprocessing','transfer_or_adaptation_method']),
    ('Auditability', ['source_quality_notes','reproducibility_artifacts','evidence_retrieved_at']),
    ('Claims', ['key_contributions','limitations','reported_results_summary']),
    ('Relevance to EPGSpeller', ['relevance_to_epgspeller','takeaways_for_related_work_section','gap_or_relevance_to_current_epgspeller_manuscript']),
]

def slug(text: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return s or 'item'

def load_items():
    rows = []
    for p in sorted(RESULTS.glob('*.json')):
        d = json.loads(p.read_text(encoding='utf-8'))
        d['_source_file'] = p.name
        rows.append(d)
    return sorted(rows, key=lambda d: (str(d.get('coverage_origin','')), int(d.get('year') or 9999), d.get('paper_id','')))

def clean(value):
    if value is None or value == '':
        return 'N/A'
    if isinstance(value, list):
        if not value:
            return 'N/A'
        if all(isinstance(x, str) for x in value):
            if len(value) <= 4:
                return '; '.join(value)
            return '<br>'.join(f'- {x}' for x in value)
        return '<br>'.join(json.dumps(x, ensure_ascii=False) for x in value)
    if isinstance(value, dict):
        return '<br>'.join(f'**{k}**: {clean(v)}' for k, v in value.items())
    return str(value).replace('\n', ' ')

def main():
    items = load_items()
    seeded = [d for d in items if str(d.get('coverage_origin','')).startswith('seeded')]
    added = [d for d in items if str(d.get('coverage_origin','')).startswith('added')]
    lines = []
    lines.append('# Related Work and Positioning Update for EPGSpeller v2')
    lines.append('')
    lines.append(f'**Topic:** {TOPIC}')
    lines.append('')
    lines.append('## Summary')
    lines.append('')
    lines.append(f'- Total items: {len(items)}')
    lines.append(f'- Seeded from frozen 2026-02-17 survey: {len(seeded)}')
    lines.append(f'- Added or gap-closure items in 2026-06-27 v2: {len(added)}')
    lines.append('- This report distinguishes prior frozen EPG-centered coverage from v2 additions and does not treat non-EPG or LM-assisted systems as direct numeric baselines for EPGSpeller.')
    lines.append('')
    lines.append('## Gap / Relevance to Current EPGSpeller Manuscript')
    lines.append('')
    lines.append('The v2 update supports the current manuscript by sharpening three boundaries: protocol-specific generalization, sensor/modality-specific comparison, and decoder-assistance separation. The added LLM-conditioned and LLM-era items motivate keeping greedy CER, lexicon projection, and LM/LLM-assisted text entry as separate evaluation regimes. The added transfer and heterogeneous-sensor items support the manuscript emphasis that cross-participant and hardware/layout mismatch are first-class protocol issues. The electro-optical stomatography item closes a prior gap around EPG-adjacent cross-speaker recognition, while also reinforcing that command-word recognition is not directly comparable with lexicon-free silent spelling.')
    lines.append('')
    lines.append('## Table of Contents')
    lines.append('')
    for i, d in enumerate(items, 1):
        title = d.get('title') or d.get('paper_id')
        lines.append(f'{i}. [{title}](#{slug(d.get("paper_id", title))}) - {d.get("year", "N/A")} | {d.get("coverage_origin", "N/A")}')
    lines.append('')
    lines.append('## Added v2 Items')
    lines.append('')
    for d in added:
        lines.append(f'- **{d.get("title")}** ({d.get("year")}): {d.get("gap_or_relevance_to_current_epgspeller_manuscript")}')
    lines.append('')
    lines.append('## Detailed Items')
    lines.append('')
    for d in items:
        lines.append(f'<a id="{slug(d.get("paper_id", d.get("title", "item")))}"></a>')
        lines.append(f'### {d.get("title", d.get("paper_id"))}')
        lines.append('')
        for group, fields in FIELD_GROUPS:
            lines.append(f'#### {group}')
            lines.append('')
            for field in fields:
                value = clean(d.get(field))
                if '[uncertain]' in value:
                    continue
                lines.append(f'- **{field}**: {value}')
            lines.append('')
        lines.append('#### Sources')
        lines.append('')
        for s in d.get('sources', []):
            doi = f" DOI: {s.get('doi')}" if s.get('doi') else ''
            lines.append(f"- {s.get('title')} ({s.get('source_type')}, retrieved {s.get('retrieved_at')}). {s.get('url')}{doi}")
        lines.append('')
    text = '\n'.join(lines).rstrip() + '\n'
    OUT.write_text(text, encoding='utf-8')
    print(f'Wrote {OUT} with {len(items)} items')

if __name__ == '__main__':
    main()
