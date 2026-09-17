"""Pipeline task 8 — ``bind_pra``: draft ``gold.risk_response``.

Port of the leave-behind's ``praAnswers()``. One row per program × question ×
FY, each quantitative answer **bound to a named column of
``gold.fiscal_year_spend_summary``** rather than composed in prose — the binding
is in ``config.risk_question.source_binding`` and the value is copied, never
recomputed here.

Guardrail G1 (file 09 §11) lives at this seam: ``bind_pra`` writes every
reportable number, and task 9 (``explain``) may afterwards write only the
``rationale_*`` columns. The qualitative questions (Q9/Q10, REQ-009) are left
deliberately empty for the program office; nothing fills them in.
"""

from __future__ import annotations

from .config import EngineConfig

__all__ = ["pra_answers", "build_risk_response", "DRAFT", "AUTO", "HUMAN"]

DRAFT = "draft"
AUTO = "auto"
HUMAN = "human"

#: Q8 reads the prior cycle's outcome, which is a recomputation rather than a
#: direct measurement, so it carries a lower stated confidence.
_Q8_CONFIDENCE = "0.90"


def pra_answers(program_id: str, fiscal_year: int,
                summary_by_program_fy: dict[tuple[str, int], dict]) -> dict[str, str]:
    """The auto-populatable answers (Q1–Q8) for one program × FY.

    Every value comes from the program's ``fiscal_year_spend_summary`` row for
    this FY, except Q8 which reads the prior year's row.
    """
    current = summary_by_program_fy[(program_id, fiscal_year)]
    prior = summary_by_program_fy.get((program_id, fiscal_year - 1))
    pct = current["yoy_pct_change"]
    prior_flagged = bool(prior) and prior["trigger_flag"] == "true"
    return {
        "Q1": current["total_disbursement"],
        "Q2": "" if pct == "" else f"{float(pct):+.1f}%",
        "Q3": "yes" if current["trigger_flag"] == "true" else "no",
        "Q4": f"{current['sub_program_count']} sub-programs; "
              f"{current['financial_code_count']} financial codes",
        "Q5": str(current["event_count"]),
        "Q6": f"{current['top_event_share_pct']}%",
        "Q7": str(current["exception_queue_count"]),
        "Q8": (f"FY{fiscal_year - 1}: comprehensive assessment triggered" if prior_flagged
               else f"FY{fiscal_year - 1}: began and closed with the preliminary, no trigger"),
    }


def build_risk_response(fiscal_year_spend_summary: list[dict], config: EngineConfig,
                        pra_fiscal_year: int | None = None,
                        watermark: str = "") -> list[dict]:
    """Draft ``gold.risk_response`` for the assessment year.

    Defaults to the latest FY in the batch — the year the PRA is being prepared
    for. Rows land as ``draft``; nothing is final until a reviewer signs it off
    (DEC-06, ASSUMP-17).
    """
    summary = {(row["program_id"], row["fiscal_year"]): row
               for row in fiscal_year_spend_summary}
    if pra_fiscal_year is None:
        pra_fiscal_year = max(fy for _, fy in summary)

    rows: list[dict] = []
    for program in config.programs:
        pid = program.program_id
        if (pid, pra_fiscal_year) not in summary:
            continue
        answers = pra_answers(pid, pra_fiscal_year, summary)
        for question in config.risk_questions:
            auto = question.qtype == "quantitative"
            rows.append({
                "response_id": f"RSP-{pid}-{pra_fiscal_year}-{question.question_id}",
                "question_id": question.question_id,
                "program_id": pid,
                "fiscal_year": pra_fiscal_year,
                "answer_value": answers.get(question.question_id, "") if auto else "",
                "confidence": (_Q8_CONFIDENCE if question.question_id == "Q8" else "1.00")
                              if auto else "",
                "populated_by": AUTO if auto else HUMAN,
                "review_status": DRAFT,
                "data_watermark": watermark,
            })
    return rows
