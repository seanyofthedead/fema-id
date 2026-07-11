#!/usr/bin/env python3
"""Build the single-file leave-behind demo (fema-demo.html).

Reads the Wave 1 synthetic dataset (data/synthetic/*.csv) and the generator
rule config (data/generator/rules.yaml), inlines them as JSON into
template.html, and writes fema-demo.html — one self-contained file, no
runtime network, no browser storage.

Deterministic: output is a pure function of the inputs (no timestamps, no
randomness), so re-runs on unchanged data are byte-identical.

Guardrails enforced here:
  * every embedded row must carry data_watermark == SYNTHETIC-DEMO
    (the constant column is then stripped to keep the file lean);
  * the validation-only answer key (answer_key.*) is never read and the
    string "answer_key" must not appear in the output;
  * the template must contain no runtime-fetched URLs (CDN scripts/styles,
    fetch/XHR) and no localStorage/sessionStorage.

Usage:  python build_demo_html.py          (stdlib only, Python 3.9+)
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "synthetic"
RULES_YAML = HERE.parent / "data" / "generator" / "rules.yaml"
TEMPLATE = HERE / "template.html"
OUT = HERE / "fema-demo.html"

WATERMARK = "SYNTHETIC-DEMO"
DATA_TOKEN = "/*__DATA__*/ null"

# The answer key is validation-only (DEC-22): never read, never embed.
FORBIDDEN_INPUTS = {"answer_key.csv", "answer_key.md"}


def read_table(name: str) -> list[dict]:
    """Read a synthetic CSV, verify the watermark on every row, strip it."""
    assert name not in FORBIDDEN_INPUTS, f"refusing to read validation-only file {name}"
    path = DATA / name
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for i, row in enumerate(rows):
        wm = row.pop("data_watermark", None)
        assert wm == WATERMARK, f"{name} row {i + 1}: watermark {wm!r} != {WATERMARK!r}"
    return rows


def num(s: str, cast=float):
    return None if s == "" else cast(s)


def parse_rules_yaml() -> dict:
    """Targeted, dependency-free parse of the config blocks the app needs.

    Only variance_trigger, confidence_routing and the cleansing pipeline are
    read — the planted taxonomy and exception plants stay out of the demo,
    which learns mappings from mapping_rule.csv / program_mapping.csv alone.
    """
    text = RULES_YAML.read_text(encoding="utf-8")

    def scalar(key: str, block: str | None = None):
        scope = text
        if block:
            m = re.search(rf"^{block}:\n((?:[ \t]+.*\n?)*)", text, re.M)
            assert m, f"rules.yaml: block {block} not found"
            scope = m.group(1)
        m = re.search(rf"^\s*{key}:\s*([^#\n]+)", scope, re.M)
        assert m, f"rules.yaml: key {key} not found"
        return m.group(1).strip()

    cleansing = re.search(r"^cleansing:\n((?:[ \t]+.*\n?)*)", text, re.M).group(1)
    normalize = re.findall(r"^\s+-\s+([a-z_]+)\s*(?:#.*)?$", cleansing, re.M)
    alias_block = re.search(r"alias_map:[^\n]*\n((?:\s+LEG-\d+:.*\n?)*)", cleansing).group(1)
    alias_map = dict(re.findall(r"(LEG-\d+):\s*(\S+)", alias_block))
    assert normalize and alias_map, "rules.yaml: cleansing pipeline not parsed"

    measures = [m.strip() for m in scalar("measures", "variance_trigger").strip("[]").split(",")]
    return {
        "threshold_pct": int(scalar("threshold_pct", "variance_trigger")),
        "direction": scalar("direction", "variance_trigger"),
        "min_prior_year_amount": int(scalar("min_prior_year_amount", "variance_trigger")),
        "min_prior_year_count": int(scalar("min_prior_year_count", "variance_trigger")),
        "measure": scalar("measure", "variance_trigger"),
        "measures": measures,                                   # REQ-031 dual-measure trigger
        "combine": scalar("combine", "variance_trigger"),
        "compare": scalar("compare", "variance_trigger"),
        "prefill_threshold": float(scalar("prefill_threshold", "confidence_routing")),
        "normalize": normalize,
        "alias_map": alias_map,
    }


# --------------------------------------------------------------------------
# Register content shown on screen 9. Text is condensed from the frozen
# canonical files — 03-assumptions-register.md (ASSUMP-01..15, SME links),
# 13-sme-validation-questions.md (SME-01..18, priorities) and
# 16-decision-log.md (ASSUMP-16..19 coined in the design pass). The files
# themselves are the authority; this is display copy for the demo screen.
# --------------------------------------------------------------------------
ASSUMPTIONS = [
    ("ASSUMP-01", "The financial system can export a flat, record-level file with program-relevant codes, amounts and dates.", "REQ-002, REQ-003", "SME-03"),
    ("ASSUMP-02", "Program ID assignment logic is deterministic and stable year over year, so historical inference can propose it.", "REQ-001, REQ-013", "SME-04"),
    ("ASSUMP-03", "The comprehensive-assessment trigger is a 20% YoY change in program spend, either direction, on the PRA's spend measure.", "REQ-010", "SME-01"),
    ("ASSUMP-04", "The PRA is a fixed 10-question instrument (~8 quantitative, ~2 qualitative); the real text is unavailable, so the demo's is an illustrative placeholder.", "REQ-007, REQ-008, REQ-009, REQ-011", "SME-05"),
    ("ASSUMP-05", "'Spend' means disbursement amounts recorded in the financial system for the FY — not obligations, budget authority or Treasury outlays.", "REQ-006, REQ-010, REQ-026", "SME-11"),
    ("ASSUMP-06", "The Program ID SOP will not be available before the demo; rules must be inferred, not transcribed. No SOP text is fabricated.", "REQ-001, REQ-015", "SME-02"),
    ("ASSUMP-07", "At least 3 consecutive prior fiscal years of extract data are retrievable in a mineable format.", "REQ-010, REQ-013, REQ-014", "SME-07"),
    ("ASSUMP-08", "Event-level tracking is expressed through the code structure itself (a code component identifies the disaster, analogous to public DR numbers).", "REQ-005", "SME-06"),
    ("ASSUMP-09", "The internal program set can be represented for demo purposes by FEMA's publicly named assistance programs, without claiming they are the real testing list.", "REQ-004, REQ-006", "SME-04, SME-13"),
    ("ASSUMP-10", "Synthetic data calibrated to verified public obligation data is acceptable for the demo, since actual spend is non-public.", "REQ-025, REQ-026", "SME-11"),
    ("ASSUMP-11", "A cloud-portable, laptop-runnable demo satisfies the environment constraint; no FedRAMP/on-prem requirement applies to the demo itself.", "REQ-020, REQ-025", "SME-09"),
    ("ASSUMP-12", "The pending financial-system migration does not change program-code semantics; a file-based source-agnostic design remains valid across it.", "REQ-019, REQ-023", "SME-10"),
    ("ASSUMP-13", "The annual FY-end snapshot is the correct processing unit for the demo scenario (single batch in, assessments out).", "REQ-017, REQ-022", "SME-08"),
    ("ASSUMP-15", "The 'macro based solution' recollection describes the legacy form factor, not a binding constraint; outputs stay Excel-compatible.", "REQ-021", "SME-03"),
    ("ASSUMP-16", "Below-confidence-threshold outputs route to the exception queue, never auto-classify (default threshold 0.85).", "design pass (files 05/06/09)", "SME-15"),
    ("ASSUMP-17", "Mandatory human review/sign-off before any PRA is finalized; overrides capture a reason.", "design pass (files 05/06/09)", "SME-16"),
    ("ASSUMP-18", "AI explanation grounding uses public guidance only for the demo (SRC-06/07/10); internal SOP text is excluded, never fabricated.", "design pass (files 06/09)", "SME-17"),
    ("ASSUMP-19", "Illustrative role model (analyst / reviewer / admin) stands in for the real, unconfirmed RBAC.", "design pass (file 06)", "SME-16"),
    ("ASSUMP-20", "WebFMIS is the source system carrying TAFS/fund-code and disbursement-type fields; realistically-formatted stand-ins appear until the real extract is seen.", "feedback review 2026-07-11 (REQ-028/029)", "SME-27"),
    ("ASSUMP-21", "The transaction-count trigger mirrors the dollar trigger's parameters (same ~20%, same directions) and a breach on either measure flags the program (team's 2024 change).", "feedback review 2026-07-11 (REQ-031)", "SME-28"),
    ("ASSUMP-22", "The financial system of record (source of the program-ID data pool) goes live ~October 1 this year; portability (file-in/file-out) hedges the migration timeline risk.", "feedback review 2026-07-11 (REQ-019)", "SME-10"),
    ("ASSUMP-23", "The five real public program names stand in for the client team's fuller 8-10 example list; sub-structures and the disaster/non-disaster designations follow the taxonomy provided after the feedback meeting.", "feedback review 2026-07-11 (REQ-027/030)", "SME-30"),
    ("ASSUMP-24", "Historical risk-assessment records (2018-19 onward) are client-owned and enter only at a pilot phase, powering trend views and pre-answered history questions.", "feedback review 2026-07-11 (REQ-033)", "SME-29"),
]

SME_QUESTIONS = [
    ("SME-01", "blocking", "Exact comprehensive-assessment trigger: precisely 20%? Which measure (disbursements/obligations/outlays)? Either direction? Codified where?", "REQ-010 · ASSUMP-03"),
    ("SME-02", "high", "Does the Program ID SOP actually exist, who owns it, and can we obtain it (or interview its author)?", "REQ-001 · REQ-015 · ASSUMP-06"),
    ("SME-03", "blocking", "What does the financial-system extract look like: system, format, grain, field list, which fields carry the codes? Is today's process genuinely macro-based?", "REQ-002 · REQ-003 · ASSUMP-01 · ASSUMP-15"),
    ("SME-04", "high", "Authoritative list of reporting programs and the code→sub-program→program rollup rules, incl. behind-the-scenes exceptions?", "REQ-001 · REQ-004 · REQ-013 · ASSUMP-02"),
    ("SME-05", "blocking", "The 10 PRA questions verbatim — which are quantitative vs qualitative, and what source data answers the ~8 automatable ones?", "REQ-006..009 · REQ-011 · ASSUMP-04"),
    ("SME-06", "roadmap", "How is event/disaster-level tracking encoded, and what rule decides when a program reports by event (Harvey/Irma/Maria)?", "REQ-005 · ASSUMP-08"),
    ("SME-07", "roadmap", "How many prior fiscal years of extracts are retrievable, in what formats, with consistent code semantics?", "REQ-013 · REQ-014 · ASSUMP-07"),
    ("SME-08", "roadmap", "The real reporting calendar: when does final actual-spend land, when are PRAs due, what date must 'accelerated' hit to matter?", "REQ-012 · REQ-017 · ASSUMP-13"),
    ("SME-09", "roadmap", "(Brett) Which cloud platforms/tools are actually available, and are there hosting constraints even for a demo?", "REQ-020 · ASSUMP-11"),
    ("SME-10", "roadmap", "Which financial system is FEMA migrating to, on what timeline, and is program-code continuity guaranteed?", "REQ-019 · REQ-023 · ASSUMP-12"),
    ("SME-11", "blocking", "Confirm the definition of 'spend' used in the PRA and trigger, and how no-year disaster money is handled in YoY comparisons.", "REQ-006 · REQ-010 · ASSUMP-05 · ASSUMP-10"),
    ("SME-12", "roadmap", "Who supplies the ~2 qualitative answers per program, and what does their sign-off workflow look like today?", "REQ-009"),
    ("SME-13", "roadmap", "Confirm assessment-cycle terminology and cadence against the PIIA / OMB A-123 App. C regime.", "REQ-018 · ASSUMP-09"),
    ("SME-14", "high", "Exact required reporting outputs and formats — fields per program; Excel workbook, PDF, dashboard or API?", "REQ-006 · REQ-021 · ASSUMP-15"),
    ("SME-15", "high", "What rationale/evidence must accompany each auto answer and inferred mapping for auditor acceptance, and what confidence threshold is acceptable?", "ASSUMP-16 · REQ-013 · REQ-016"),
    ("SME-16", "high", "Actual users and roles; what RBAC and sign-off authority govern finalizing a PRA?", "ASSUMP-17 · ASSUMP-19"),
    ("SME-17", "roadmap", "Which SOP/policy/guidance documents can be provided for retrieval-grounded explanation, and are they releasable?", "ASSUMP-18 · SME-02"),
    ("SME-18", "roadmap", "What audit-trail, record-retention and immutability requirements apply to generated assessments?", "SME-16"),
    ("SME-27", "high", "In the WebFMIS extract: actual field names/formats for TAFS / fund code and disbursement type, the disbursement-type value set, and where the disaster vs non-disaster distinction is carried?", "REQ-028 · REQ-029 · REQ-030 · ASSUMP-20"),
    ("SME-28", "high", "Exact post-2024 trigger rule: does ~20% apply to transaction count with the same directions as dollars, does either measure alone trigger, and what floors apply? Policy citation?", "REQ-031 · ASSUMP-21"),
    ("SME-29", "roadmap", "Confirm the 3-year comprehensive-assessment cycle rule, where the date of last comprehensive assessment is recorded, and the terms for the 2018-19+ historical risk-assessment records.", "REQ-033 · REQ-034"),
    ("SME-30", "high", "Confirm the program taxonomy: the team's 8-10 example public programs, each one's sub-structure (or by-disaster-number grouping), and disaster vs non-disaster designations.", "REQ-027 · ASSUMP-23"),
]


def build_payload() -> dict:
    cfg = parse_rules_yaml()

    fiscal_years = [
        {"fy": int(r["fiscal_year"]), "start": r["fy_start"], "end": r["fy_end"]}
        for r in read_table("fiscal_year.csv")
    ]
    events = [
        {"dr": int(r["disaster_number"]), "type": r["incident_type"], "state": r["state"],
         "fyDeclared": int(r["fy_declared"]), "title": r["declaration_title"]}
        for r in read_table("disaster_event.csv")
    ]
    programs = [
        {"id": r["program_id"], "name": r["program_name"], "listing": r["assistance_listing"],
         "isDisaster": r["is_disaster"] == "true", "tafs": r["tafs"]}
        for r in read_table("program.csv")
    ]
    sub_programs = [
        {"id": r["sub_program_id"], "progId": r["program_id"], "name": r["sub_program_name"]}
        for r in read_table("sub_program.csv")
    ]
    codes = [
        {"code": r["code"], "subId": r["sub_program_id"], "fund": r["fund_segment"],
         # non-disaster codes carry the ND event segment (REQ-030) -> null event
         "seg": r["program_segment"],
         "event": int(r["event_segment"]) if r["event_segment"].isdigit() else None,
         "tafs": r["tafs"]}
        for r in read_table("financial_code.csv")
    ]
    rules = [
        {"id": r["rule_id"], "type": r["rule_type"], "expr": r["expression"],
         "conf": float(r["confidence"]), "status": r["status"]}
        for r in read_table("mapping_rule.csv")
    ]
    mappings = [
        [r["code"], r["sub_program_id"], r["program_id"], int(r["fiscal_year"]),
         r["rule_id"], float(r["confidence"]), r["status"]]
        for r in read_table("program_mapping.csv")
    ]
    txns = [
        # disaster_number is empty for non-disaster spend (REQ-030) -> null
        [r["txn_id"], r["raw_code"], r["code"], num(r["disaster_number"], int),
         int(r["fiscal_year"]), float(r["disbursement_amount"]), r["disbursement_date"],
         r["disbursement_type"]]
        for r in read_table("transaction.csv")
    ]
    spend_summary = [
        [r["program_id"], int(r["fiscal_year"]), num(r["disaster_number"], int),
         float(r["total_disbursement"])]
        for r in read_table("spend_summary.csv")
    ]
    fy_summary = [
        [r["program_id"], int(r["fiscal_year"]), float(r["total_disbursement"]),
         num(r["prior_year_disbursement"]), num(r["yoy_pct_change"]),
         r["trigger_flag"] == "true", int(r["sub_program_count"]),
         int(r["financial_code_count"]), int(r["event_count"]),
         float(r["top_event_share_pct"]), int(r["exception_queue_count"]),
         # REQ-031 count dimension (indices 11..15)
         int(r["transaction_count"]), num(r["prior_year_transaction_count"], int),
         num(r["count_yoy_pct_change"]),
         r["dollar_trigger_flag"] == "true", r["count_trigger_flag"] == "true"]
        for r in read_table("fiscal_year_spend_summary.csv")
    ]
    questions = [
        {"id": r["question_id"], "text": r["text"], "qtype": r["qtype"],
         "auto": r["auto_populatable"] == "true", "binding": r["source_binding"]}
        for r in read_table("risk_question.csv")
    ]
    responses = [
        {"qid": r["question_id"], "progId": r["program_id"], "fy": int(r["fiscal_year"]),
         "value": r["answer_value"], "conf": num(r["confidence"]),
         "by": r["populated_by"], "status": r["review_status"]}
        for r in read_table("risk_response.csv")
    ]
    audit_events = [
        {"id": r["event_id"], "entity": r["entity"], "refs": r["input_refs"],
         "rule": r["rule_or_model"], "actor": r["actor"], "decision": r["decision"],
         "ts": r["ts"]}
        for r in read_table("audit_event.csv")
    ]
    sources = [
        {"id": r["src_id"], "title": r["title"], "url": r["url"],
         "verification": r["verification"], "date": r["access_date"]}
        for r in read_table("public_data_source.csv")
    ]

    return {
        "meta": {
            "watermark": WATERMARK,
            "seed": 20260708,
            "generated_from": "Wave 1 synthetic dataset (data/synthetic, seed 20260708)",
            "note": ("Conceptual demo, not production. Synthetic disbursements calibrated "
                     "to public FEMA obligation envelopes (SRC-03/SRC-04); obligations are "
                     "never presented as spend (ASSUMP-05, ASSUMP-10)."),
        },
        "config": cfg,
        "fiscalYears": fiscal_years,
        "events": events,
        "programs": programs,
        "subPrograms": sub_programs,
        "codes": codes,
        "rules": rules,
        "mappings": mappings,
        "txns": txns,
        "spendSummary": spend_summary,
        "fySummary": fy_summary,
        "questions": questions,
        "responses": responses,
        "auditEvents": audit_events,
        "sources": sources,
        "assumptions": [
            {"id": a, "text": t, "req": req, "sme": sme} for a, t, req, sme in ASSUMPTIONS
        ],
        "smeQuestions": [
            {"id": s, "priority": p, "text": t, "linked": l} for s, p, t, l in SME_QUESTIONS
        ],
    }


def self_check_template(tpl: str) -> None:
    """Static guardrails on the template before injection."""
    assert tpl.count(DATA_TOKEN) == 1, "template must contain exactly one data token"
    runtime_net = [
        r"<script[^>]+src=", r"<link[^>]+href=", r"@import\b", r"\burl\(\s*['\"]?https?:",
        r"\bfetch\s*\(", r"XMLHttpRequest", r"navigator\.sendBeacon", r"\bimport\s*\(",
        r"localStorage", r"sessionStorage", r"indexedDB", r"document\.cookie",
    ]
    for pat in runtime_net:
        hits = re.findall(pat, tpl, re.I)
        assert not hits, f"template violates offline/no-storage rule: {pat!r} -> {hits[:3]}"


def main() -> int:
    payload = build_payload()
    tpl = TEMPLATE.read_text(encoding="utf-8")
    self_check_template(tpl)

    blob = json.dumps(payload, separators=(",", ":"), ensure_ascii=True)
    blob = blob.replace("</", "<\\/")  # never allow an embedded </script>
    assert "answer_key" not in blob.lower(), "answer key must not be embedded (DEC-22)"

    out = tpl.replace(DATA_TOKEN, blob)
    assert "answer_key" not in out.lower()
    OUT.write_text(out, encoding="utf-8", newline="\n")

    n_rows = sum(len(payload[k]) for k in
                 ("txns", "mappings", "spendSummary", "fySummary", "codes", "rules"))
    print(f"wrote {OUT.name}: {OUT.stat().st_size:,} bytes "
          f"({len(payload['txns'])} txns, {n_rows} embedded rows total, "
          f"trigger {payload['config']['threshold_pct']}% {payload['config']['direction']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
