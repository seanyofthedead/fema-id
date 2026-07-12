"""Build a compact JSON data payload from the synthetic CSVs (answer key EXCLUDED).

Output: fema_data.json in this directory, shaped as an object whose top-level
key order and column conventions are documented in PAYLOAD-SCHEMA.md.
Transactions are arrays-of-arrays (documented column order) for size; all
other tables are arrays of objects.
"""
import csv, json, pathlib

HERE = pathlib.Path(__file__).parent
DATA = pathlib.Path(r"C:\dev\fema-id\solution-design\fema-program-id-risk-assessment\data\synthetic")

def rows(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def num(v):
    if v is None or v == "":
        return None
    try:
        f = float(v)
        return int(f) if f == int(f) and "." not in v else f
    except ValueError:
        return v

def boolv(v):
    return {"true": True, "false": False}.get(str(v).lower(), None)

payload = {}

payload["meta"] = {
    "watermark": "SYNTHETIC-DEMO",
    "note": "All spend data is synthetic, calibrated to public obligation envelopes. Program names and DR numbers are real public identifiers.",
    "fiscal_years": [2022, 2023, 2024, 2025, 2026],
    "trigger_default": {"threshold_pct": 20, "direction": "either",
                         "measures": ["disbursements", "transaction_count"], "combine": "any"},
    "confidence_routing_threshold": 0.85,
}

payload["programs"] = [
    {"id": r["program_id"], "name": r["program_name"], "listing": r["assistance_listing"] or None,
     "is_disaster": boolv(r["is_disaster"]), "tafs": r["tafs"]}
    for r in rows("program.csv")]

payload["sub_programs"] = [
    {"id": r["sub_program_id"], "program_id": r["program_id"], "name": r["sub_program_name"]}
    for r in rows("sub_program.csv")]

payload["disaster_events"] = [
    {"dr": int(r["disaster_number"]), "incident_type": r["incident_type"], "state": r["state"],
     "fy_declared": int(r["fy_declared"]), "title": r["declaration_title"]}
    for r in rows("disaster_event.csv")]

payload["financial_codes"] = [
    {"code": r["code"], "sub_program_id": r["sub_program_id"] or None,
     "fund_segment": r["fund_segment"], "program_segment": r["program_segment"],
     "event_segment": r["event_segment"], "tafs": r["tafs"] or None}
    for r in rows("financial_code.csv")]

payload["mapping_rules"] = [
    {"rule_id": r["rule_id"], "rule_type": r["rule_type"], "expression": r["expression"],
     "confidence": num(r["confidence"]), "status": r["status"]}
    for r in rows("mapping_rule.csv")]

# transactions: array-of-arrays, columns documented below
payload["transaction_columns"] = ["txn_id", "raw_code", "code", "disaster_number", "is_disaster",
                                    "fiscal_year", "amount", "disbursement_type", "date"]
payload["transactions"] = [
    [r["txn_id"], r["raw_code"], r["code"], num(r["disaster_number"]), boolv(r["is_disaster"]),
     int(r["fiscal_year"]), num(r["disbursement_amount"]), r["disbursement_type"], r["disbursement_date"]]
    for r in rows("transaction.csv")]

payload["program_mapping"] = [
    {"code": r["code"], "sub_program_id": r["sub_program_id"] or None,
     "program_id": r["program_id"] or None, "fy": int(r["fiscal_year"]),
     "rule_id": r["rule_id"] or None, "confidence": num(r["confidence"]), "status": r["status"]}
    for r in rows("program_mapping.csv")]

payload["fy_summary"] = [
    {k: v for k, v in {
        "program_id": r["program_id"], "fy": int(r["fiscal_year"]),
        "total": num(r["total_disbursement"]), "prior_total": num(r["prior_year_disbursement"]),
        "yoy_pct": num(r["yoy_pct_change"]),
        "txn_count": num(r["transaction_count"]), "prior_txn_count": num(r["prior_year_transaction_count"]),
        "count_yoy_pct": num(r["count_yoy_pct_change"]),
        "trigger_flag": boolv(r["trigger_flag"]),
        "dollar_trigger_flag": boolv(r["dollar_trigger_flag"]),
        "count_trigger_flag": boolv(r["count_trigger_flag"]),
        "sub_program_count": num(r["sub_program_count"]),
        "financial_code_count": num(r["financial_code_count"]),
        "event_count": num(r["event_count"]), "top_event_share_pct": num(r["top_event_share_pct"]),
        "exception_queue_count": num(r["exception_queue_count"]),
    }.items()}
    for r in rows("fiscal_year_spend_summary.csv")]

payload["event_summary"] = [
    {"program_id": r["program_id"], "fy": int(r["fiscal_year"]),
     "disaster_number": num(r["disaster_number"]),
     "total": num(r["total_disbursement"]), "prior_total": num(r["prior_year_disbursement"]),
     "yoy_pct": num(r["yoy_pct_change"]), "trigger_flag": boolv(r["trigger_flag"])}
    for r in rows("spend_summary.csv")]

payload["risk_questions"] = [
    {"id": r["question_id"], "text": r["text"], "qtype": r["qtype"],
     "auto_populatable": boolv(r["auto_populatable"]), "source_binding": r["source_binding"]}
    for r in rows("risk_question.csv")]

payload["risk_responses"] = [
    {"program_id": r["program_id"], "question_id": r["question_id"], "fy": int(r["fiscal_year"]),
     "answer_value": r["answer_value"] or None, "populated_by": r["populated_by"],
     "confidence": num(r["confidence"]), "review_status": r["review_status"]}
    for r in rows("risk_response.csv")]

out = HERE / "fema_data.json"
out.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size:,} bytes)")
for k, v in payload.items():
    if isinstance(v, list):
        print(f"  {k}: {len(v)} rows")
