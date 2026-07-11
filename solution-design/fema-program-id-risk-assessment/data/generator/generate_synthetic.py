#!/usr/bin/env python3
"""Wave 1 synthetic dataset generator — FEMA Program ID & PRA Automation (demo).

Generates the synthetic DISBURSEMENT ledger and reference tables defined in
08-data-model.md, planted with the demo scenarios and calibrated so that
cumulative synthetic disbursements per disaster stay inside the real public
OBLIGATION envelopes pulled from OpenFEMA (SRC-03 Public Assistance 97.036,
SRC-04 Hazard Mitigation 97.039) for the verified SRC-02 disaster set.

Correctness constraint (file 04 §3, file 08): public dollars are OBLIGATIONS;
this ledger models DISBURSEMENTS, which are non-public. Nothing here is real
FEMA spend. Every output row is watermarked SYNTHETIC-DEMO.

Determinism: a single fixed seed (rules.yaml `seed`, 20260708) drives all
randomness; the script builds the dataset twice and asserts the two runs are
byte-identical before writing (self-check 10).

Usage:
    python generate_synthetic.py                 # regenerate from cached anchors
    python generate_synthetic.py --refresh-anchors   # re-pull OpenFEMA anchors first

No network access is required unless --refresh-anchors is passed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "synthetic"
RULES_PATH = HERE / "rules.yaml"
ANCHORS_PATH = HERE / "anchors.json"

# Fixed timestamp for audit rows — wall-clock time would break byte-identical re-runs.
GEN_TS = "2026-07-08T00:00:00Z"
ACCESS_DATE = "2026-07-08"

CALIBRATION_BASIS = (
    "Synthetic disbursement magnitudes calibrated to real public OBLIGATION "
    "envelopes: per-disaster sum of federalShareObligated from SRC-03 "
    "(PublicAssistanceFundedProjectsDetails v2, listing 97.036) and SRC-04 "
    "(HazardMitigationAssistanceProjects v4, listing 97.039), pulled live "
    f"{ACCESS_DATE} and cached in anchors.json. Obligations are NOT presented "
    "as disbursements; synthetic disbursements draw down against (and stay "
    "below) the obligation envelopes (ASSUMP-05, ASSUMP-10)."
)

# ---------------------------------------------------------------------------
# Anchor refresh (optional; network only when explicitly requested)
# ---------------------------------------------------------------------------

def refresh_anchors() -> None:
    import urllib.parse
    import urllib.request

    endpoints = {
        "SRC-03": ("https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails",
                   "PublicAssistanceFundedProjectsDetails", "pa"),
        "SRC-04": ("https://www.fema.gov/api/open/v4/HazardMitigationAssistanceProjects",
                   "HazardMitigationAssistanceProjects", "hma"),
    }
    anchors = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))
    drs = sorted(anchors["disasters"].keys())

    def get_json(url: str) -> dict:
        req = urllib.request.Request(url, headers={"User-Agent": "fema-demo-calibration/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))

    for dr in drs:
        row: dict = {}
        for _src, (base, entity, prefix) in endpoints.items():
            total, n, skip = 0.0, 0, 0
            while True:
                qs = urllib.parse.urlencode({
                    "$filter": f"disasterNumber eq {dr}",
                    "$select": "federalShareObligated",
                    "$top": 10000, "$skip": skip,
                })
                rows = get_json(f"{base}?{qs}")[entity]
                for rec in rows:
                    v = rec.get("federalShareObligated")
                    if v is not None:
                        total += float(v)
                        n += 1
                if len(rows) < 10000:
                    break
                skip += 10000
            row[f"{prefix}_federal_share_obligated"] = round(total, 2)
            row[f"{prefix}_project_count"] = n
        anchors["disasters"][dr] = row
        print(f"  refreshed DR-{dr}: PA ${row['pa_federal_share_obligated']:,.0f} | "
              f"HMA ${row['hma_federal_share_obligated']:,.0f}")
    ANCHORS_PATH.write_text(json.dumps(anchors, indent=2) + "\n", encoding="utf-8")
    print(f"anchors.json refreshed ({ACCESS_DATE=})")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def cents(x: float) -> int:
    return int(round(x * 100))


def money(c: int) -> str:
    sign = "-" if c < 0 else ""
    c = abs(c)
    return f"{sign}{c // 100}.{c % 100:02d}"


def largest_remainder(total: int, weights: list[float]) -> list[int]:
    """Split integer `total` by weights; parts sum exactly to total."""
    s = sum(weights)
    raw = [total * w / s for w in weights]
    parts = [int(r) for r in raw]
    short = total - sum(parts)
    order = sorted(range(len(raw)), key=lambda i: (raw[i] - parts[i], -i), reverse=True)
    for i in range(short):
        parts[order[i % len(order)]] += 1
    return parts


def fy_window(fy: int) -> tuple[date, date]:
    return date(fy - 1, 10, 1), date(fy, 9, 30)


class Table:
    def __init__(self, name: str, columns: list[str]):
        self.name = name
        self.columns = columns
        self.rows: list[list] = []

    def add(self, **kv) -> None:
        assert set(kv) == set(self.columns), f"{self.name}: {set(kv) ^ set(self.columns)}"
        self.rows.append([kv[c] for c in self.columns])

    def to_csv_bytes(self) -> bytes:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(self.columns)
        w.writerows(self.rows)
        return buf.getvalue().encode("utf-8")

    def col(self, name: str) -> list:
        i = self.columns.index(name)
        return [r[i] for r in self.rows]


# ---------------------------------------------------------------------------
# Dataset build (pure function of config + anchors + seed)
# ---------------------------------------------------------------------------

def build_dataset(cfg: dict, anchors: dict) -> tuple[dict[str, bytes], dict]:
    rng = random.Random(cfg["seed"])
    wm = cfg["watermark"]
    fys: list[int] = cfg["fiscal_years"]
    trig = cfg["variance_trigger"]
    threshold = float(trig["threshold_pct"])
    direction = trig["direction"]
    min_prior = cents(float(trig["min_prior_year_amount"]))
    min_prior_count = int(trig.get("min_prior_year_count", 0))
    measures = list(trig.get("measures", [trig.get("measure", "disbursements")]))
    combine_mode = trig.get("combine", "any")
    max_util = float(cfg["calibration"]["max_envelope_utilization"])

    envelope = {int(dr): d["pa_federal_share_obligated"] + d["hma_federal_share_obligated"]
                for dr, d in anchors["disasters"].items()}

    def dir_fires(yoy_pct: float) -> bool:
        if direction == "increase_only":
            return yoy_pct >= threshold
        if direction == "decrease_only":
            return yoy_pct <= -threshold
        return abs(yoy_pct) >= threshold

    def fires(yoy_pct: float | None, prior: int) -> bool:
        """Dollar measure (prior in cents)."""
        if yoy_pct is None or prior < min_prior or prior <= 0:
            return False
        return dir_fires(yoy_pct)

    def fires_count(yoy_pct: float | None, prior_n: int) -> bool:
        """Transaction-count measure (REQ-031, 2024 change; ASSUMP-21/SME-28)."""
        if yoy_pct is None or prior_n < min_prior_count or prior_n <= 0:
            return False
        return dir_fires(yoy_pct)

    def combined_flag(dollar_flag: bool, count_flag: bool) -> bool:
        flags = []
        if "disbursements" in measures:
            flags.append(dollar_flag)
        if "transaction_count" in measures:
            flags.append(count_flag)
        if not flags:
            flags = [dollar_flag]
        return all(flags) if combine_mode == "all" else any(flags)

    # --- taxonomy ---------------------------------------------------------
    programs = cfg["programs"]
    codes: list[dict] = []          # canonical codes with planted truth
    rules: list[dict] = []
    rule_by_sub: dict[str, str] = {}
    rid = 0

    def next_rule(rule_type: str, expression: str, confidence: float, status: str) -> str:
        nonlocal rid
        rid += 1
        r = {"rule_id": f"BR-{rid:03d}", "rule_type": rule_type, "expression": expression,
             "confidence": confidence, "status": status}
        rules.append(r)
        return r["rule_id"]

    next_rule("event_split", "event_segment -> disaster_number (SRC-02)", 1.0, "sme_confirmed")
    next_rule("cleansing", "normalize: strip_whitespace, uppercase, separators_to_hyphen", 1.0, "sme_confirmed")
    for alias, target in cfg["cleansing"]["alias_map"].items():
        next_rule("cleansing", f"alias {alias} -> {target} (legacy code retired after FY2023)",
                  0.97, "sme_confirmed")

    inferred_subs = {"SUB-IA-MC", "SUB-HS-OPSG", "SUB-PA-4341"}   # texture: still 'inferred'
    ND_SEG = "ND"   # event-segment token for non-disaster codes (REQ-030)
    for prog in programs:
        fund = prog["fund_segment"]
        for sub in prog["sub_programs"]:
            sid = sub["sub_program_id"]
            if prog["mapping_style"] == "event_driven":
                sub_segments = prog["program_segments"]
                expr = (f"fund_segment == '{fund}' and program_segment in {sub_segments} "
                        f"and event_segment in {sub['events']} -> {sid}")
            else:
                sub_segments = sub["segments"]
                expr = (f"fund_segment == '{fund}' and program_segment in {sub_segments} "
                        f"-> {sid}")
            status = "inferred" if sid in inferred_subs else "sme_confirmed"
            conf = 0.88 if status == "inferred" else 0.98
            rule_by_sub[sid] = next_rule("code_to_subprogram", expr, conf, status)
            events = sub["events"] or [None]   # non-disaster: single ND pseudo-event
            for seg in sub_segments:
                for ev in events:
                    codes.append({
                        "code": f"{fund}-{seg}-{ev if ev is not None else ND_SEG}",
                        "fund_segment": fund, "program_segment": seg, "event": ev,
                        "sub_program_id": sid, "sub_program_name": sub["sub_program_name"],
                        "program_id": prog["program_id"], "program_name": prog["program_name"],
                        "rule_id": rule_by_sub[sid],
                    })
        sub_ids = [s["sub_program_id"] for s in prog["sub_programs"]]
        rollup_rule = next_rule("rollup", f"{sub_ids} -> {prog['program_id']}", 0.98, "sme_confirmed")
        prog["_rollup_rule"] = rollup_rule

    dup = {c["code"] for c in codes}
    assert len(dup) == len(codes), "duplicate canonical codes in taxonomy"

    # --- planned totals (cents), before any envelope scaling ---------------
    prog_fy_total: dict[tuple[str, int], int] = {}
    for prog in programs:
        total = float(prog["base_annual_disbursement"])
        for fy in fys:
            if fy != fys[0]:
                total *= 1.0 + float(prog["growth"][fy])
            prog_fy_total[(prog["program_id"], fy)] = cents(total)

    # allocate program-FY totals to codes: sub weight and event weight follow
    # the real obligation envelope of each event, so tiny DRs get tiny dollars
    prog_codes = {p["program_id"]: [c for c in codes if c["program_id"] == p["program_id"]]
                  for p in programs}
    code_fy: dict[tuple[str, int], int] = {}
    for prog in programs:
        pid = prog["program_id"]
        clist = prog_codes[pid]
        # disaster codes weight by the real DR obligation envelope; non-disaster
        # codes (no envelope exists) split evenly (DATA_DICTIONARY note)
        weights = [envelope[c["event"]] if c["event"] is not None else 1.0 for c in clist]
        for fy in fys:
            parts = largest_remainder(prog_fy_total[(pid, fy)], weights)
            for c, part in zip(clist, parts):
                code_fy[(c["code"], fy)] = part

    # --- envelope check + optional global scale (calibration, ASSUMP-10) ---
    exc = cfg["exception_codes"]
    dr_total: dict[int, int] = {dr: 0 for dr in envelope}
    for c in codes:
        if c["event"] is None:      # non-disaster spend has no DR envelope (REQ-030)
            continue
        for fy in fys:
            dr_total[c["event"]] += code_fy[(c["code"], fy)]
    for e in exc:
        dr_total[e["event"]] += cents(float(e["total_amount"]))
    scale = 1.0
    for dr, tot in dr_total.items():
        cap = max_util * envelope[dr] * 100
        if tot > cap:
            scale = min(scale, cap / tot)
    if scale < 1.0:
        for k in code_fy:
            code_fy[k] = int(code_fy[k] * scale)
        for e in exc:
            e["total_amount"] = float(e["total_amount"]) * scale
        for k in prog_fy_total:
            prog_fy_total[k] = sum(code_fy[(c["code"], k[1])] for c in prog_codes[k[0]])
        dr_total = {dr: 0 for dr in envelope}
        for c in codes:
            if c["event"] is None:
                continue
            for fy in fys:
                dr_total[c["event"]] += code_fy[(c["code"], fy)]
        for e in exc:
            dr_total[e["event"]] += cents(float(e["total_amount"]))
    utilization = {dr: dr_total[dr] / (envelope[dr] * 100) for dr in sorted(envelope)}

    # --- tables -------------------------------------------------------------
    t_fy = Table("fiscal_year", ["fiscal_year", "fy_start", "fy_end", "data_watermark"])
    for fy in fys:
        s, e = fy_window(fy)
        t_fy.add(fiscal_year=fy, fy_start=s.isoformat(), fy_end=e.isoformat(), data_watermark=wm)

    t_dr = Table("disaster_event", ["disaster_number", "incident_type", "state", "fy_declared",
                                    "declaration_title", "data_watermark"])
    for d in cfg["disaster_events"]:
        t_dr.add(disaster_number=d["disaster_number"], incident_type=d["incident_type"],
                 state=d["state"], fy_declared=d["fy_declared"],
                 declaration_title=d["declaration_title"], data_watermark=wm)

    t_prog = Table("program", ["program_id", "program_name", "assistance_listing", "is_disaster",
                               "tafs", "data_watermark"])
    t_sub = Table("sub_program", ["sub_program_id", "program_id", "sub_program_name", "data_watermark"])
    for prog in programs:
        t_prog.add(program_id=prog["program_id"], program_name=prog["program_name"],
                   assistance_listing=prog["assistance_listing"],
                   is_disaster=str(bool(prog["is_disaster"])).lower(),
                   tafs=prog["tafs"], data_watermark=wm)
        for sub in prog["sub_programs"]:
            t_sub.add(sub_program_id=sub["sub_program_id"], program_id=prog["program_id"],
                      sub_program_name=sub["sub_program_name"], data_watermark=wm)

    # financial_code: canonical codes; sub_program_id left EMPTY for exception
    # codes (dimension unresolved as-landed; truth lives in the answer key only)
    tafs_by_prog = {p["program_id"]: p["tafs"] for p in programs}
    t_code = Table("financial_code", ["code", "sub_program_id", "fund_segment", "program_segment",
                                      "event_segment", "tafs", "data_watermark"])
    for c in codes:
        t_code.add(code=c["code"], sub_program_id=c["sub_program_id"], fund_segment=c["fund_segment"],
                   program_segment=c["program_segment"],
                   event_segment=c["event"] if c["event"] is not None else ND_SEG,
                   tafs=tafs_by_prog[c["program_id"]], data_watermark=wm)
    for e in exc:   # exception codes: fund symbol unresolved as-landed (like the dimension)
        t_code.add(code=e["code"], sub_program_id="", fund_segment=e["fund_segment"],
                   program_segment=e["program_segment"], event_segment=e["event"],
                   tafs="", data_watermark=wm)

    t_rule = Table("mapping_rule", ["rule_id", "rule_type", "expression", "confidence", "status",
                                    "data_watermark"])
    for r in rules:
        t_rule.add(rule_id=r["rule_id"], rule_type=r["rule_type"], expression=r["expression"],
                   confidence=f"{r['confidence']:.2f}", status=r["status"], data_watermark=wm)

    # --- transactions --------------------------------------------------------
    alias_rev: dict[str, str] = {v: k for k, v in cfg["cleansing"]["alias_map"].items()}
    dirty_share = float(cfg["cleansing"]["dirty_raw_share"])
    dtype_names = [d["name"] for d in cfg["disbursement_types"]]
    dtype_weights = [float(d["weight"]) for d in cfg["disbursement_types"]]
    t_txn = Table("transaction", ["txn_id", "raw_code", "code", "disaster_number", "is_disaster",
                                  "fiscal_year", "disbursement_amount", "disbursement_type",
                                  "disbursement_date", "data_watermark"])
    txn_no = 0
    n_dirty = 0
    n_alias = 0

    def dirty_variant(code: str) -> str:
        pick = rng.randrange(3)
        if pick == 0:
            return code.lower()
        if pick == 1:
            return code.replace("-", "/")
        return code.replace("-", " ")

    def emit_txns(code: str, event: int | None, fy: int, total: int, n: int, alias_ok: bool,
                  is_dis: bool) -> None:
        nonlocal txn_no, n_dirty, n_alias
        if total <= 0 or n <= 0:
            return
        weights = [rng.uniform(0.6, 1.6) for _ in range(n)]
        parts = largest_remainder(total, weights)
        s, e = fy_window(fy)
        span = (e - s).days + 1
        for part in parts:
            txn_no += 1
            d = s + timedelta(days=rng.randrange(span))
            raw = code
            if alias_ok and fy <= 2023 and rng.random() < 0.5:
                raw = alias_rev[code]
                n_alias += 1
            elif rng.random() < dirty_share:
                raw = dirty_variant(code)
                n_dirty += 1
            t_txn.add(txn_id=f"TXN-{txn_no:06d}", raw_code=raw, code=code,
                      disaster_number=event if event is not None else "",
                      is_disaster=str(is_dis).lower(), fiscal_year=fy,
                      disbursement_amount=money(part),
                      disbursement_type=rng.choices(dtype_names, weights=dtype_weights)[0],
                      disbursement_date=d.isoformat(), data_watermark=wm)

    for prog in programs:
        pid = prog["program_id"]
        clist = prog_codes[pid]
        count_plan = prog.get("txn_count_plan")
        for fy in fys:
            prog_total = prog_fy_total[(pid, fy)]
            # transaction-count dimension (REQ-031): an explicit txn_count_plan
            # plants exact per-FY counts (the count-only-breach scenario needs
            # them exact); otherwise counts follow dollar magnitude.
            if count_plan:
                n_prog = int(count_plan[fy])
            else:
                n_prog = max(6, min(200, prog_total // cents(6_000_000) + 6))
            shares = [float(max(code_fy[(c["code"], fy)], 1)) for c in clist]
            parts_n = largest_remainder(n_prog, shares)
            for i, c in enumerate(clist):   # every funded code gets >= 1 transaction
                if code_fy[(c["code"], fy)] > 0 and parts_n[i] == 0:
                    j = max(range(len(parts_n)), key=lambda k: parts_n[k])
                    if parts_n[j] > 1:
                        parts_n[j] -= 1
                        parts_n[i] += 1
            for c, n in zip(clist, parts_n):
                amt = code_fy[(c["code"], fy)]
                emit_txns(c["code"], c["event"], fy, amt, n, alias_ok=c["code"] in alias_rev,
                          is_dis=bool(prog["is_disaster"]))

    for e in exc:   # FY2026-only unmapped codes (REQ-003 plants); all carry DR events
        emit_txns(e["code"], e["event"], 2026, cents(float(e["total_amount"])), int(e["txn_count"]),
                  alias_ok=False, is_dis=True)

    # actual per-program-FY transaction counts (mapped codes only, mirroring the
    # dollar rule: exception-queue spend and counts never roll up — file 09 §2)
    code_pid = {c["code"]: c["program_id"] for c in codes}
    txn_count: dict[tuple[str, int], int] = {}
    for row in t_txn.rows:
        rec = dict(zip(t_txn.columns, row))
        pid = code_pid.get(rec["code"])
        if pid is None:
            continue
        txn_count[(pid, rec["fiscal_year"])] = txn_count.get((pid, rec["fiscal_year"]), 0) + 1

    # --- program_mapping ------------------------------------------------------
    t_map = Table("program_mapping", ["mapping_id", "code", "sub_program_id", "program_id",
                                      "fiscal_year", "rule_id", "confidence", "status",
                                      "data_watermark"])
    rule_conf = {r["rule_id"]: r["confidence"] for r in rules}
    for c in codes:
        for fy in fys:
            t_map.add(mapping_id=f"MAP-{c['code']}-{fy}", code=c["code"],
                      sub_program_id=c["sub_program_id"], program_id=c["program_id"],
                      fiscal_year=fy, rule_id=c["rule_id"],
                      confidence=f"{rule_conf[c['rule_id']]:.2f}", status="auto", data_watermark=wm)
    for e in exc:   # similarity SUGGESTION only — below prefill threshold, queued
        t_map.add(mapping_id=f"MAP-{e['code']}-2026", code=e["code"],
                  sub_program_id=e["suggested_sub_program"], program_id=e["suggested_program"],
                  fiscal_year=2026, rule_id="",
                  confidence=f"{float(e['suggested_confidence']):.2f}",
                  status="exception_queue", data_watermark=wm)

    # --- summaries (mapped spend only; exception-queue rows excluded) ----------
    pe_total: dict[tuple[str, int, int], int] = {}
    for c in codes:
        for fy in fys:
            key = (c["program_id"], fy, c["event"])
            pe_total[key] = pe_total.get(key, 0) + code_fy[(c["code"], fy)]

    t_ss = Table("spend_summary", ["summary_id", "program_id", "fiscal_year", "disaster_number",
                                   "total_disbursement", "prior_year_disbursement", "yoy_pct_change",
                                   "trigger_flag", "data_watermark"])
    for prog in programs:
        pid = prog["program_id"]
        events = sorted({c["event"] for c in prog_codes[pid]},
                        key=lambda e: -1 if e is None else e)
        for fy in fys:
            for ev in events:
                cur = pe_total.get((pid, fy, ev), 0)
                prior = pe_total.get((pid, fy - 1, ev), 0) if fy != fys[0] else 0
                yoy = round((cur - prior) / prior * 100, 1) if prior > 0 else None
                t_ss.add(summary_id=f"SS-{pid}-{fy}-{ev if ev is not None else 'ND'}",
                         program_id=pid, fiscal_year=fy,
                         disaster_number=ev if ev is not None else "",
                         total_disbursement=money(cur),
                         prior_year_disbursement=money(prior) if fy != fys[0] else "",
                         yoy_pct_change="" if yoy is None else f"{yoy:.1f}",
                         trigger_flag=str(fires(yoy, prior)).lower(), data_watermark=wm)

    exc_count = {p["program_id"]: 0 for p in programs}
    for e in exc:
        exc_count[e["suggested_program"]] += 1

    t_fss = Table("fiscal_year_spend_summary",
                  ["summary_id", "program_id", "fiscal_year", "total_disbursement",
                   "prior_year_disbursement", "yoy_pct_change", "transaction_count",
                   "prior_year_transaction_count", "count_yoy_pct_change", "trigger_flag",
                   "dollar_trigger_flag", "count_trigger_flag",
                   "sub_program_count", "financial_code_count", "event_count",
                   "top_event_share_pct", "exception_queue_count", "data_watermark"])
    fss_lookup: dict[tuple[str, int], dict] = {}
    for prog in programs:
        pid = prog["program_id"]
        for fy in fys:
            cur = prog_fy_total[(pid, fy)]
            prior = prog_fy_total.get((pid, fy - 1), 0) if fy != fys[0] else 0
            yoy = round((cur - prior) / prior * 100, 1) if prior > 0 else None
            n_cur = txn_count.get((pid, fy), 0)
            n_prior = txn_count.get((pid, fy - 1), 0) if fy != fys[0] else 0
            cyoy = round((n_cur - n_prior) / n_prior * 100, 1) if n_prior > 0 else None
            dflag = fires(yoy, prior)
            cflag = fires_count(cyoy, n_prior)
            ev_totals = [pe_total.get((pid, fy, ev), 0)
                         for ev in {c["event"] for c in prog_codes[pid]} if ev is not None]
            ev_present = [v for v in ev_totals if v > 0]
            top_share = round(max(ev_present) / cur * 100, 1) if cur > 0 and ev_present else 0.0
            rec = {
                "summary_id": f"FSS-{pid}-{fy}", "program_id": pid, "fiscal_year": fy,
                "total_disbursement": money(cur),
                "prior_year_disbursement": money(prior) if fy != fys[0] else "",
                "yoy_pct_change": "" if yoy is None else f"{yoy:.1f}",
                "transaction_count": n_cur,
                "prior_year_transaction_count": n_prior if fy != fys[0] else "",
                "count_yoy_pct_change": "" if cyoy is None else f"{cyoy:.1f}",
                "trigger_flag": str(combined_flag(dflag, cflag)).lower(),
                "dollar_trigger_flag": str(dflag).lower(),
                "count_trigger_flag": str(cflag).lower(),
                "sub_program_count": len(prog["sub_programs"]),
                "financial_code_count": len(prog_codes[pid]),
                "event_count": len(ev_present),
                "top_event_share_pct": f"{top_share:.1f}",
                "exception_queue_count": exc_count[pid] if fy == 2026 else 0,
                "data_watermark": wm,
            }
            t_fss.add(**rec)
            fss_lookup[(pid, fy)] = {**rec, "_yoy": yoy, "_cur": cur, "_prior": prior,
                                     "_cyoy": cyoy, "_ncur": n_cur, "_nprior": n_prior,
                                     "_dflag": dflag, "_cflag": cflag}

    # --- PRA template + responses (file 10 §2; ASSUMP-04 placeholder) ----------
    q_rows = [
        ("Q1", "Total program disbursements this FY (illustrative placeholder, ASSUMP-04)",
         "quantitative", "true", "fiscal_year_spend_summary.total_disbursement"),
        ("Q2", "Year-over-year change in program spend, percent (illustrative placeholder, ASSUMP-04)",
         "quantitative", "true", "fiscal_year_spend_summary.yoy_pct_change"),
        ("Q3", "Does YoY change breach the comprehensive-assessment threshold on dollars or transaction volume? (illustrative placeholder, ASSUMP-04)",
         "quantitative", "true", "fiscal_year_spend_summary.trigger_flag (dollar or transaction-count measure, REQ-031)"),
        ("Q4", "Number of sub-programs / financial codes rolled into this program (illustrative placeholder, ASSUMP-04)",
         "quantitative", "true", "fiscal_year_spend_summary.sub_program_count,financial_code_count"),
        ("Q5", "Number of disaster events contributing to spend (illustrative placeholder, ASSUMP-04)",
         "quantitative", "true", "fiscal_year_spend_summary.event_count"),
        ("Q6", "Share of spend concentrated in the top event, percent (illustrative placeholder, ASSUMP-04)",
         "quantitative", "true", "fiscal_year_spend_summary.top_event_share_pct"),
        ("Q7", "Count of exception-queue / unmapped records for this program (illustrative placeholder, ASSUMP-04)",
         "quantitative", "true", "fiscal_year_spend_summary.exception_queue_count"),
        ("Q8", "Prior-year comprehensive-assessment status / recency (illustrative placeholder, ASSUMP-04)",
         "quantitative", "true", "prior fiscal_year_spend_summary.trigger_flag"),
        ("Q9", "Were there significant changes to program rules or regulation this FY? (illustrative placeholder, ASSUMP-04)",
         "qualitative", "false", "program-office input (REQ-009)"),
        ("Q10", "Were there significant staffing / process changes affecting controls? (illustrative placeholder, ASSUMP-04)",
         "qualitative", "false", "program-office input (REQ-009)"),
    ]
    t_q = Table("risk_question", ["question_id", "text", "qtype", "auto_populatable",
                                  "source_binding", "data_watermark"])
    for q in q_rows:
        t_q.add(question_id=q[0], text=q[1], qtype=q[2], auto_populatable=q[3],
                source_binding=q[4], data_watermark=wm)

    pra_fy = fys[-1]
    t_resp = Table("risk_response", ["response_id", "question_id", "program_id", "fiscal_year",
                                     "answer_value", "confidence", "populated_by", "review_status",
                                     "data_watermark"])
    for prog in programs:
        pid = prog["program_id"]
        cur = fss_lookup[(pid, pra_fy)]
        prior = fss_lookup[(pid, pra_fy - 1)]
        yoy = cur["_yoy"]
        answers = {
            "Q1": money(cur["_cur"]),
            "Q2": "" if yoy is None else f"{yoy:+.1f}%",
            "Q3": "yes" if cur["trigger_flag"] == "true" else "no",
            "Q4": f"{cur['sub_program_count']} sub-programs; {cur['financial_code_count']} financial codes",
            "Q5": str(cur["event_count"]),
            "Q6": f"{cur['top_event_share_pct']}%",
            "Q7": str(cur["exception_queue_count"]),
            "Q8": (f"FY{pra_fy - 1}: comprehensive assessment triggered"
                   if prior["trigger_flag"] == "true"
                   else f"FY{pra_fy - 1}: began and closed with the preliminary, no trigger"),
        }
        for qid, _text, qtype, _auto, _bind in q_rows:
            if qtype == "quantitative":
                conf = "0.90" if qid == "Q8" else "1.00"
                t_resp.add(response_id=f"RSP-{pid}-{pra_fy}-{qid}", question_id=qid, program_id=pid,
                           fiscal_year=pra_fy, answer_value=answers[qid], confidence=conf,
                           populated_by="auto", review_status="draft", data_watermark=wm)
            else:   # Q9/Q10 intentionally blank for SME input (REQ-009)
                t_resp.add(response_id=f"RSP-{pid}-{pra_fy}-{qid}", question_id=qid, program_id=pid,
                           fiscal_year=pra_fy, answer_value="", confidence="",
                           populated_by="human", review_status="draft", data_watermark=wm)

    # --- provenance -------------------------------------------------------------
    t_src = Table("public_data_source", ["src_id", "title", "url", "verification", "access_date",
                                         "data_watermark"])
    for src in [
        ("SRC-01", "OpenFEMA API (platform + dataset metadata endpoints)",
         "https://www.fema.gov/api/open", "API"),
        ("SRC-02", "OpenFEMA Disaster Declarations Summaries v2",
         "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries", "API"),
        ("SRC-03", "OpenFEMA Public Assistance Funded Projects Details v2",
         "https://www.fema.gov/api/open/v2/PublicAssistanceFundedProjectsDetails", "API"),
        ("SRC-04", "OpenFEMA Hazard Mitigation Assistance Projects v4",
         "https://www.fema.gov/api/open/v4/HazardMitigationAssistanceProjects", "API"),
        ("SRC-12", "SAM.gov Assistance Listings (97.036 PA, 97.039 HMGP)",
         "https://sam.gov/assistance-listings", "Search"),
    ]:
        t_src.add(src_id=src[0], title=src[1], url=src[2], verification=src[3],
                  access_date=ACCESS_DATE, data_watermark=wm)

    t_audit = Table("audit_event", ["event_id", "entity", "input_refs", "rule_or_model", "actor",
                                    "decision", "ts", "data_watermark"])
    t_audit.add(event_id="EVT-0001", entity="calibration",
                input_refs="SRC-03;SRC-04;anchors.json",
                rule_or_model="per-DR sum of federalShareObligated",
                actor="generate_synthetic.py",
                decision=CALIBRATION_BASIS, ts=GEN_TS, data_watermark=wm)
    t_audit.add(event_id="EVT-0002", entity="generation",
                input_refs="rules.yaml;anchors.json",
                rule_or_model=f"seed={cfg['seed']}",
                actor="generate_synthetic.py",
                decision=f"deterministic synthetic build; envelope scale factor={scale:.6f}",
                ts=GEN_TS, data_watermark=wm)
    t_audit.add(event_id="EVT-0003", entity="calibration",
                input_refs="anchors.json",
                rule_or_model=f"max_envelope_utilization={max_util}",
                actor="generate_synthetic.py",
                decision="per-DR utilization: " + "; ".join(
                    f"DR-{dr}={utilization[dr]:.4f}" for dr in sorted(utilization)),
                ts=GEN_TS, data_watermark=wm)

    # --- answer key (VALIDATION ONLY) --------------------------------------------
    ak_cols = ["record_type", "raw_or_alias_code", "canonical_code", "fund_segment",
               "program_segment", "event_segment", "disaster_number", "sub_program_id",
               "sub_program_name", "program_id", "program_name", "rule_id", "scenario_tags",
               "note", "data_watermark"]
    t_ak = Table("answer_key", ak_cols)
    prog_scenario = {p["program_id"]: p.get("scenario", "") for p in programs}
    for c in codes:
        t_ak.add(record_type="code_mapping", raw_or_alias_code="", canonical_code=c["code"],
                 fund_segment=c["fund_segment"], program_segment=c["program_segment"],
                 event_segment=c["event"] if c["event"] is not None else ND_SEG,
                 disaster_number=c["event"] if c["event"] is not None else "",
                 sub_program_id=c["sub_program_id"], sub_program_name=c["sub_program_name"],
                 program_id=c["program_id"], program_name=c["program_name"], rule_id=c["rule_id"],
                 scenario_tags=prog_scenario[c["program_id"]], note="", data_watermark=wm)
    for alias, target in cfg["cleansing"]["alias_map"].items():
        c = next(x for x in codes if x["code"] == target)
        t_ak.add(record_type="alias", raw_or_alias_code=alias, canonical_code=target,
                 fund_segment=c["fund_segment"], program_segment=c["program_segment"],
                 event_segment=c["event"] if c["event"] is not None else ND_SEG,
                 disaster_number=c["event"] if c["event"] is not None else "",
                 sub_program_id=c["sub_program_id"], sub_program_name=c["sub_program_name"],
                 program_id=c["program_id"], program_name=c["program_name"], rule_id="",
                 scenario_tags="cleansing_adjustment (REQ-003)",
                 note="legacy code appearing in raw_code for FY2022-FY2023 rows",
                 data_watermark=wm)
    for e in exc:
        t_ak.add(record_type="exception_truth", raw_or_alias_code="", canonical_code=e["code"],
                 fund_segment=e["fund_segment"], program_segment=e["program_segment"],
                 event_segment=e["event"], disaster_number=e["event"],
                 sub_program_id=e["suggested_sub_program"], sub_program_name="",
                 program_id=e["suggested_program"], program_name="", rule_id="",
                 scenario_tags="exception_queue_plant (REQ-003)",
                 note=f"FY2026-only code, no rule; similarity suggestion confidence "
                      f"{float(e['suggested_confidence']):.2f} (< prefill threshold)",
                 data_watermark=wm)
    for prog in programs:
        growth = "; ".join(f"FY{fy}: {prog['growth'][fy]:+.0%}" for fy in fys[1:])
        t_ak.add(record_type="variance_plan", raw_or_alias_code="", canonical_code="",
                 fund_segment=prog["fund_segment"], program_segment="", event_segment="",
                 disaster_number="", sub_program_id="", sub_program_name="",
                 program_id=prog["program_id"], program_name=prog["program_name"], rule_id="",
                 scenario_tags=prog_scenario[prog["program_id"]],
                 note=f"base FY{fys[0]} ${prog['base_annual_disbursement']:,}; planted growth {growth}",
                 data_watermark=wm)

    tables = [t_fy, t_dr, t_prog, t_sub, t_code, t_rule, t_txn, t_map, t_ss, t_fss, t_q, t_resp,
              t_src, t_audit]

    stats = {
        "tables": tables, "answer_key": t_ak, "codes": codes, "programs": programs,
        "utilization": utilization, "scale": scale, "n_dirty": n_dirty, "n_alias": n_alias,
        "fss_lookup": fss_lookup, "threshold": threshold, "exc": exc, "envelope": envelope,
        "prog_codes": prog_codes, "fys": fys, "wm": wm,
    }

    files: dict[str, bytes] = {t.name + ".csv": t.to_csv_bytes() for t in tables}
    files["answer_key.csv"] = t_ak.to_csv_bytes()
    files["answer_key.md"] = build_answer_key_md(cfg, stats).encode("utf-8")
    return files, stats


def build_answer_key_md(cfg: dict, stats: dict) -> str:
    fys = stats["fys"]
    lines = [
        "# Answer Key — Planted Ground Truth (VALIDATION ONLY)",
        "",
        "> **VALIDATION ONLY.** This file records the ground truth used to PLANT the",
        "> synthetic dataset: raw code → sub-program → parent program, event groupings,",
        "> cleansing aliases, exception plants, and the variance plan. The Wave 4",
        "> historical-mining crawler (REQ-013) must rediscover these groupings from the",
        "> transaction history alone. **No inference-path code may read this file or",
        "> `answer_key.csv`**; they exist solely to score the crawler's output later.",
        "> All content is synthetic (SYNTHETIC-DEMO). Machine-readable version:",
        "> `answer_key.csv`.",
        "",
        "## 1. Code → sub-grouping → program mapping (planted truth)",
        "",
        "See `answer_key.csv` rows with `record_type = code_mapping` (one per canonical",
        "code, with the rule ID that plants it). The five parent programs carry REAL,",
        "public FEMA program names (CH-01/REQ-027); every segment, code, TAFS value and",
        "dollar beneath them is fictional. Structural notes:",
        "",
        "- `PROG-PA` (Public Assistance) and `PROG-HM` (HMGP) are **event-driven**: the",
        "  event segment decides the sub-grouping. PA's sub-groupings ARE the disaster",
        "  numbers (`PA-97036-4332 → SUB-PA-4332`, etc. — per-DR grouping, no named",
        "  sub-programs); HMGP has no sub-programs at all, so every HM code maps to the",
        "  single pass-through grouping `SUB-HM-ALL`.",
        "- `PROG-IA` (Individual Assistance) and `PROG-HS` (HSGP) are **segment-driven**:",
        "  each sub-program owns one or two 5-digit program segments; several codes",
        "  (segment × event) map to one sub-program, and several sub-programs roll up to",
        "  one parent — no code maps 1:1 to a program (REQ-002/003). `PROG-UR` (US&R)",
        "  is segment-driven with a single pass-through grouping (no sub-programs).",
        "- **Non-disaster programs** (`PROG-HS`, `PROG-UR` — REQ-030): codes carry the",
        "  `ND` event segment and their transactions carry no disaster number.",
        "- **Shared-segment trap:** program segment `55501` exists under BOTH `IA`",
        "  (→ SUB-IA-DCM, PROG-IA) and `HS` (→ SUB-HS-OPSG, PROG-HS). A correct mapping",
        "  rule needs fund segment + program segment together.",
        "",
        "## 2. Sub-program rollup plant (REQ-004)",
        "",
        "`PROG-IA` has **exactly 3 sub-programs** (IHP / Mass Care / Disaster Case",
        "Management) rolling up to one reporting program; `PROG-HS` mirrors it",
        "(SHSP / UASI / Operation Stonegarden).",
        "",
        "## 3. Disaster/event split plant (REQ-005, SRC-02)",
        "",
        "| Program | Events (real DR numbers) |",
        "|---|---|",
    ]
    for prog in stats["programs"]:
        evs = sorted({c["event"] for c in stats["prog_codes"][prog["program_id"]]
                      if c["event"] is not None})
        label = ", ".join("DR-" + str(e) for e in evs) or "non-disaster — no DR events (REQ-030)"
        lines.append(f"| {prog['program_id']} | {label} |")
    lines += [
        "",
        "`PROG-PA` spend splits across all seven verified DRs (Harvey/Irma/Maria",
        "multi-event pattern) — and its sub-groupings ARE the disaster numbers, per the",
        "client taxonomy. Within a sub-grouping, spend splits across its events in",
        "proportion to each DR's real obligation envelope, so small-envelope DRs",
        "(4338, 4341, 4346) carry proportionally small synthetic dollars. Non-disaster",
        "programs have no envelope; their synthetic bases are fixed in rules.yaml.",
        "",
        "## 4. Cleansing / adjustment plants (REQ-003)",
        "",
        "| Legacy alias (raw_code) | Canonical code | Appears in |",
        "|---|---|---|",
    ]
    for alias, target in cfg["cleansing"]["alias_map"].items():
        lines.append(f"| {alias} | {target} | FY2022–FY2023 rows (~50%) |")
    lines += [
        "",
        f"Additionally ~{int(float(cfg['cleansing']['dirty_raw_share']) * 100)}% of all rows carry a",
        "format-dirty `raw_code` (lowercase, `/` or space separators) that normalizes to",
        "the canonical code via the cleansing rules in `rules.yaml`.",
        "",
        "## 5. Exception-queue plants (REQ-003; new FY2026 codes, no rule)",
        "",
        "| Code | True (suggested) sub-program | True (suggested) program | Similarity confidence |",
        "|---|---|---|---|",
    ]
    for e in stats["exc"]:
        lines.append(f"| {e['code']} | {e['suggested_sub_program']} | {e['suggested_program']} | "
                     f"{float(e['suggested_confidence']):.2f} |")
    lines += [
        "",
        "These appear only in FY2026 transactions, have no mapping rule, and sit in",
        "`program_mapping` with `status = exception_queue`. Their spend is **excluded**",
        "from `spend_summary` / `fiscal_year_spend_summary` (unconfirmed mappings never",
        "roll up — file 09 §2).",
        "",
        "## 6. Variance plan (REQ-010; threshold 20%, direction either, measure disbursements)",
        "",
        f"FY{fys[-1]} planted YoY outcomes (see `answer_key.csv` `record_type = variance_plan`",
        "for every program):",
        "",
        "| Outcome | Programs |",
        "|---|---|",
    ]
    ups, downs, within = [], [], []
    for prog in stats["programs"]:
        y = stats["fss_lookup"][(prog["program_id"], fys[-1])]["_yoy"]
        if y is None:
            continue
        (ups if y >= stats["threshold"] else downs if y <= -stats["threshold"] else within).append(
            f"{prog['program_id']} ({y:+.1f}%)")
    count_only = [f"{p['program_id']} (count {stats['fss_lookup'][(p['program_id'], fys[-1])]['_cyoy']:+.1f}%, "
                  f"dollars {stats['fss_lookup'][(p['program_id'], fys[-1])]['_yoy']:+.1f}%)"
                  for p in stats["programs"]
                  if stats["fss_lookup"][(p["program_id"], fys[-1])]["_cflag"]
                  and not stats["fss_lookup"][(p["program_id"], fys[-1])]["_dflag"]]
    lines += [
        f"| crosses +{stats['threshold']:.0f}% dollars (trigger) | {', '.join(ups)} |",
        f"| crosses −{stats['threshold']:.0f}% dollars (trigger) | {', '.join(downs)} |",
        f"| within ±{stats['threshold']:.0f}% dollars (no dollar trigger) | {', '.join(within)} |",
        f"| **count-only breach** (REQ-031: transaction volume crosses, dollars do not) | {', '.join(count_only) or '—'} |",
        "",
        "The trigger is dual-measure (REQ-031, the team's 2024 change): a breach on",
        "EITHER dollars or transaction count flags the program. Earlier-FY texture",
        "crossings (so the trigger history is not flat) are recorded in the",
        "`scenario_tags` column.",
        "",
        "---",
        f"*Generated deterministically by `generator/generate_synthetic.py` (seed {cfg['seed']}).*",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Self-checks (the run must report pass/fail; failures abort before writing)
# ---------------------------------------------------------------------------

def run_self_checks(files: dict[str, bytes], files2: dict[str, bytes], stats: dict,
                    cfg: dict) -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    tables: list[Table] = stats["tables"]
    ak: Table = stats["answer_key"]
    fys = stats["fys"]
    threshold = stats["threshold"]
    wm = stats["wm"]

    # 1. watermark on every row of every output table (incl. answer key)
    bad = [t.name for t in tables + [ak]
           if "data_watermark" not in t.columns or any(v != wm for v in t.col("data_watermark"))]
    results.append(("1 watermark on every row", not bad, f"violations: {bad or 'none'}"))

    # 2. >=1 parent with exactly 3 sub-programs
    subs = next(t for t in tables if t.name == "sub_program")
    per_parent: dict[str, int] = {}
    for pid in subs.col("program_id"):
        per_parent[pid] = per_parent.get(pid, 0) + 1
    exactly3 = sorted(p for p, n in per_parent.items() if n == 3)
    results.append(("2 parent with exactly 3 sub-programs (REQ-004)", "PROG-IA" in exactly3,
                    f"exactly-3 parents: {exactly3}"))

    # 3. >=1 program splits across >=2 real DRs (REQ-005, SRC-02)
    src02 = {4332, 4337, 4338, 4339, 4340, 4341, 4346}
    pa_events = {c["event"] for c in stats["prog_codes"]["PROG-PA"]}
    ok3 = len(pa_events & src02) >= 2
    results.append(("3 multi-event split across SRC-02 DRs (REQ-005)", ok3,
                    f"PROG-PA events: {sorted(pa_events)}"))

    # 4. >=4 consecutive fiscal years
    ok4 = len(fys) >= 4 and fys == list(range(fys[0], fys[0] + len(fys)))
    txn = next(t for t in tables if t.name == "transaction")
    txn_fys = sorted(set(txn.col("fiscal_year")))
    results.append(("4 >=4 consecutive FYs", ok4 and txn_fys == fys, f"FYs: {txn_fys}"))

    # 5. variance coverage at configured threshold (REQ-010, ASSUMP-03) — both
    # measures: dollars AND a count-only breach (REQ-031)
    ups = downs = within = count_only = 0
    for prog in stats["programs"]:
        rec = stats["fss_lookup"][(prog["program_id"], fys[-1])]
        y = rec["_yoy"]
        if y is None:
            continue
        if y >= threshold:
            ups += 1
        elif y <= -threshold:
            downs += 1
        else:
            within += 1
        if rec["_cflag"] and not rec["_dflag"]:
            count_only += 1
    ok5 = ups >= 2 and downs >= 1 and within >= 2 and count_only >= 1
    results.append((f"5 variance coverage at ±{threshold:.0f}% (dollars + count-only, REQ-031)", ok5,
                    f"+crossers={ups}, -crossers={downs}, within={within}, count_only={count_only}"))

    # 6. no 1:1 code→program; adjustment cases exist
    per_prog_codes = {p["program_id"]: len(stats["prog_codes"][p["program_id"]])
                      for p in stats["programs"]}
    min_codes = min(per_prog_codes.values())
    pm = next(t for t in tables if t.name == "program_mapping")
    n_exc = sum(1 for s in pm.col("status") if s == "exception_queue")
    ok6 = min_codes >= 2 and stats["n_dirty"] > 0 and stats["n_alias"] > 0 and n_exc > 0
    results.append(("6 non-1:1 codes + adjustment cases (REQ-002/003)", ok6,
                    f"min codes/program={min_codes}, dirty raw={stats['n_dirty']}, "
                    f"alias rows={stats['n_alias']}, exception rows={n_exc}"))

    # 7. PRA fields: Q1–Q8 populated, Q9–Q10 intentionally blank (file 10)
    resp = next(t for t in tables if t.name == "risk_response")
    by_q: dict[str, list[str]] = {}
    for row in resp.rows:
        rec = dict(zip(resp.columns, row))
        by_q.setdefault(rec["question_id"], []).append(rec["answer_value"])
    n_prog = len(stats["programs"])
    ok7 = all(len(by_q.get(f"Q{i}", [])) == n_prog for i in range(1, 11))
    ok7 = ok7 and all(all(v != "" for v in by_q[f"Q{i}"]) for i in range(1, 9))
    ok7 = ok7 and all(all(v == "" for v in by_q[f"Q{i}"]) for i in (9, 10))
    results.append(("7 PRA fields populated (quant) / blank (qual)", ok7,
                    f"{n_prog} programs x 10 questions; Q1-Q8 filled, Q9-Q10 blank"))

    # 8. magnitudes within plausible band of SRC-03/04 obligation anchors —
    # disaster programs only; non-disaster programs have no envelope (REQ-030)
    util = stats["utilization"]
    max_u = float(cfg["calibration"]["max_envelope_utilization"])
    total_syn = sum(stats["fss_lookup"][(p["program_id"], fy)]["_cur"]
                    for p in stats["programs"] if p["is_disaster"] for fy in fys)
    total_env = sum(stats["envelope"].values()) * 100
    overall = total_syn / total_env
    ok8 = all(u <= max_u for u in util.values()) and 0.02 <= overall <= max_u
    results.append(("8 magnitudes within obligation-anchor band (ASSUMP-10; disaster programs)", ok8,
                    f"overall utilization={overall:.1%}; per-DR max="
                    f"{max(util.values()):.1%} (cap {max_u:.0%})"))

    # 9. answer key present, labeled validation-only, not referenced by inference code
    md = files["answer_key.md"].decode("utf-8")
    repo_root = HERE.parents[3]
    # build_demo_html.py may NAME answer_key: its guard asserts the key is
    # neither read nor embedded (DEC-22/DEC-28) — that mention is the guard
    # itself, not a use. Every other .py referencing the key is an offender.
    guard_files = {"build_demo_html.py"}
    offenders = []
    for py in repo_root.rglob("*.py"):
        if py.resolve() == Path(__file__).resolve() or ".git" in py.parts:
            continue
        if py.name in guard_files:
            continue
        if "answer_key" in py.read_text(encoding="utf-8", errors="ignore"):
            offenders.append(str(py))
    ok9 = "VALIDATION ONLY" in md and "answer_key.csv" in files and not offenders
    results.append(("9 answer key labeled validation-only, unreferenced", ok9,
                    f"offending files: {offenders or 'none'}"))

    # 10. deterministic re-run byte-identical
    ok10 = set(files) == set(files2) and all(files[k] == files2[k] for k in files)
    results.append(("10 re-run byte-identical (seed fixed)", ok10,
                    f"{len(files)} files compared"))
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh-anchors", action="store_true",
                    help="re-pull obligation anchors from OpenFEMA before generating")
    args = ap.parse_args()

    if args.refresh_anchors:
        print("Refreshing calibration anchors from OpenFEMA (SRC-03/SRC-04)...")
        refresh_anchors()

    cfg = yaml.safe_load(RULES_PATH.read_text(encoding="utf-8"))
    anchors = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))

    print(f"Building dataset (seed={cfg['seed']}) ... run 1")
    files, stats = build_dataset(cfg, anchors)
    print("Building dataset ... run 2 (determinism check)")
    files2, _ = build_dataset(yaml.safe_load(RULES_PATH.read_text(encoding="utf-8")), anchors)

    results = run_self_checks(files, files2, stats, cfg)

    print("\n=== SELF-CHECK REPORT ===")
    all_ok = True
    for name, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {detail}")
        all_ok = all_ok and ok
    if not all_ok:
        print("\nSelf-checks FAILED — nothing written.")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_lines = []
    for fname in sorted(files):
        (OUT_DIR / fname).write_bytes(files[fname])
        manifest_lines.append(f"{hashlib.sha256(files[fname]).hexdigest()}  {fname}")
    (OUT_DIR / "MANIFEST.sha256").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    print("\n=== DATASET SUMMARY ===")
    print(f"  seed: {cfg['seed']}   watermark: {cfg['watermark']}")
    print(f"  calibration: {CALIBRATION_BASIS}")
    print(f"  envelope scale factor: {stats['scale']:.6f}")
    print(f"  per-DR envelope utilization: " + ", ".join(
        f"DR-{dr}={u:.1%}" for dr, u in stats["utilization"].items()))
    print("  rows written:")
    for t in stats["tables"]:
        print(f"    {t.name + '.csv':32s} {len(t.rows):6d}")
    print(f"    {'answer_key.csv':32s} {len(stats['answer_key'].rows):6d}   (VALIDATION ONLY)")
    print(f"\n  output dir: {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
