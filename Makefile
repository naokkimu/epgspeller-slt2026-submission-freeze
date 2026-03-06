SHELL := /bin/bash

.PHONY: paper exp_report manuscript_check verify_interspeech exp_report_check

PYTHON := .venv/bin/python
PAPERJSON := $(PYTHON) ~/.codex/skills/paperjson/scripts/paperjson.py
PAPERJSON_TO_SUBMISSION := $(PYTHON) ~/.codex/skills/paperjson-to-submission/scripts/paper_json_to_submission.py
INTERSPEECH_AUDIT := $(PYTHON) ~/.codex/skills/interspeech-submission-audit/scripts/audit_interspeech_submission.py

paper:
	$(PAPERJSON) all --root . --expected-version 1.0.0
	$(PAPERJSON_TO_SUBMISSION) --root . --overwrite
	cp -f paper/submission/interspeech2026_review.pdf paper/main.pdf

exp_report:
	mkdir -p reports/interspeech/exp_report
	test -f docs/report/multi_subject_extended_results_2026-02-24.md
	test -f sweeps/msx20260224/results/msx_all_metrics.csv
	test -d docs/report/figures/msx20260224
	tar -czf reports/interspeech/exp_report/exp_report_msx20260224.tar.gz \
		docs/report/multi_subject_extended_results_2026-02-24.md \
		docs/report/figures/msx20260224 \
		sweeps/msx20260224/results/msx_all_metrics.csv \
		paper/paper.json

manuscript_check:
	$(PAPERJSON) gate --root . --expected-version 1.0.0
	$(PAPERJSON) manuscript --root . --expected-version 1.0.0

verify_interspeech:
	PATH="$(PWD)/.venv/bin:/usr/bin:/bin:$$PATH" $(INTERSPEECH_AUDIT) \
		--pdf paper/submission/interspeech2026_review.pdf \
		--tex paper/submission/interspeech2026_review.tex \
		--paper-kit Interspeech2026-Paper-Kit.zip \
		--out reviews/curated/interspeech_submission_audit.json \
		--root . \
		--stage review \
		--paper-type regular \
		--ai-tools-used true

exp_report_check:
	test -f reports/interspeech/exp_report/exp_report_msx20260224.tar.gz
	test -f paper/main.pdf
	test -f reviews/curated/interspeech_submission_audit.json
	$(PYTHON) -c "import json; d=json.load(open('reviews/curated/interspeech_submission_audit.json')); print('audit_overall_status=', d.get('overall_status', 'UNKNOWN'))"
