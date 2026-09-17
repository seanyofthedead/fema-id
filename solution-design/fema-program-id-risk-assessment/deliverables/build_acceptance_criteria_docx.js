const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  PageOrientation, LevelFormat, Footer, PageNumber, TabStopType,
} = require('docx');

const NAVY = '1F3A5F';
const SLATE = '44546A';
const RULE = 'BFC9D4';
const ALT = 'F4F6F9';
const BODY = 21;   // 10.5pt
const TBL = 18;    // 9pt
const FONT = 'Calibri';

// ---------- inline parsing: **bold** and `code` ----------
function parseInline(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ ...base, text: text.slice(last, m.index) }));
    const tok = m[0];
    if (tok.startsWith('**')) {
      out.push(new TextRun({ ...base, text: tok.slice(2, -2), bold: true }));
    } else {
      out.push(new TextRun({ ...base, text: tok.slice(1, -1), font: 'Consolas', size: (base.size || BODY) - 2 }));
    }
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ ...base, text: text.slice(last) }));
  return out.length ? out : [new TextRun({ ...base, text: '' })];
}

function p(text, opts = {}) {
  const { size = BODY, spacing = { after: 140, line: 264 }, ...rest } = opts;
  return new Paragraph({ spacing, children: parseInline(text, { size, font: FONT }), ...rest });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 160 },
    children: [new TextRun({ text, bold: true, size: 26, color: NAVY, font: FONT })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, bold: true, size: 22, color: SLATE, font: FONT })],
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: 'bullets', level },
    spacing: { after: 100, line: 264 },
    children: parseInline(text, { size: BODY, font: FONT }),
  });
}

function numbered(text) {
  return new Paragraph({
    numbering: { reference: 'steps', level: 0 },
    spacing: { after: 100, line: 264 },
    children: parseInline(text, { size: BODY, font: FONT }),
  });
}

// ---------- table helpers ----------
const noBorders = {
  top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
  left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
};

function hCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' },
    margins: { top: 90, bottom: 90, left: 120, right: 120 },
    children: [new Paragraph({
      spacing: { after: 0 },
      children: [new TextRun({ text, bold: true, size: TBL, color: 'FFFFFF', font: FONT })],
    })],
  });
}

function bCell(text, width, shaded) {
  const shading = shaded
    ? { type: ShadingType.CLEAR, fill: ALT, color: 'auto' }
    : undefined;
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading,
    margins: { top: 90, bottom: 90, left: 120, right: 120 },
    children: [new Paragraph({
      spacing: { after: 0, line: 252 },
      children: parseInline(text, { size: TBL, font: FONT }),
    })],
  });
}

function table(widths, headers, rows) {
  const trs = [new TableRow({
    tableHeader: true,
    children: headers.map((t, i) => hCell(t, widths[i])),
  })];
  rows.forEach((r, ri) => {
    trs.push(new TableRow({
      children: r.map((t, i) => bCell(t, widths[i], ri % 2 === 1)),
    }));
  });
  return new Table({
    columnWidths: widths,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      left: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      right: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: RULE },
      insideVertical: { style: BorderStyle.SINGLE, size: 4, color: RULE },
    },
    rows: trs,
  });
}

function spacer(after = 200) {
  return new Paragraph({ spacing: { after }, children: [new TextRun({ text: '', size: 8 })] });
}

// ---------- cover block ----------
function metaRow(label, value) {
  return new TableRow({
    children: [
      new TableCell({
        width: { size: 2400, type: WidthType.DXA }, borders: noBorders,
        margins: { top: 50, bottom: 50, left: 0, right: 160 },
        children: [new Paragraph({
          spacing: { after: 0 },
          children: [new TextRun({ text: label, bold: true, size: 19, color: SLATE, font: FONT })],
        })],
      }),
      new TableCell({
        width: { size: 6960, type: WidthType.DXA }, borders: noBorders,
        margins: { top: 50, bottom: 50, left: 0, right: 0 },
        children: [new Paragraph({
          spacing: { after: 0, line: 252 },
          children: parseInline(value, { size: 19, font: FONT }),
        })],
      }),
    ],
  });
}

const PORTRAIT = { size: { width: 12240, height: 15840 }, margin: { top: 1300, right: 1440, bottom: 1300, left: 1440 } };
const LANDSCAPE = { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1150, right: 1150, bottom: 1150, left: 1150 } };
const W_P = 9360;    // portrait content width
const W_L = 13540;   // landscape content width

function footer() {
  return {
    default: new Footer({
      children: [new Paragraph({
        tabStops: [{ type: TabStopType.RIGHT, position: W_P }],
        spacing: { before: 120 },
        children: [
          new TextRun({ text: 'DRAFT — internal review. Not yet sent to FEMA.', size: 16, color: SLATE, font: FONT, italics: true }),
          new TextRun({ text: '\t', size: 16 }),
          new TextRun({ text: 'Page ', size: 16, color: SLATE, font: FONT }),
          new TextRun({ children: [PageNumber.CURRENT], size: 16, color: SLATE, font: FONT }),
          new TextRun({ text: ' of ', size: 16, color: SLATE, font: FONT }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: SLATE, font: FONT }),
        ],
      })],
    }),
  };
}

// =====================================================================
// SECTION 1 — portrait: cover, §1–§5
// =====================================================================
const s1 = [];

s1.push(new Paragraph({
  spacing: { after: 60 },
  children: [new TextRun({ text: 'DRAFT FOR INTERNAL REVIEW — NOT YET SENT TO FEMA', bold: true, size: 18, color: 'B03A2E', font: FONT })],
}));

s1.push(new Paragraph({
  spacing: { after: 60 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 8 } },
  children: [new TextRun({ text: 'Proposed Acceptance Criteria', bold: true, size: 40, color: NAVY, font: FONT })],
}));

s1.push(new Paragraph({
  spacing: { before: 140, after: 260 },
  children: [new TextRun({ text: 'FEMA PIIA Proof of Concept — Program Identification and Preliminary Risk Assessment Automation', size: 24, color: SLATE, font: FONT })],
}));

s1.push(new Table({
  columnWidths: [2400, 6960],
  width: { size: W_P, type: WidthType.DXA },
  borders: noBorders,
  rows: [
    metaRow('Deliverable', 'Acceptance criteria proposed by Guidehouse within ten business days of the period-of-performance start (FFP pricing template, Assumptions #2).'),
    metaRow('Contract', 'Task order 70FA3126F00000042 under GS00F045DA, modification P00001, CLIN 0010 — Additional In-Scope Work.'),
    metaRow('Period of performance', '2026-09-18 – 2027-02-18'),
    metaRow('Scope hook', 'PWS 5.8.2 / 5.8.3 / 5.8.4. Which paragraph carries PIIA is not stated in the modification; 5.8.4 Analytics Reporting Services is the expected fit and is on the confirmation list in section 2.'),
    metaRow('Due', '2026-10-01 or 2026-10-02, depending on how the ten business days are counted from a Friday start — see section 2, item 6.'),
    metaRow('Solution', 'Program Identification and Preliminary Risk Assessment (PIIA) automation, delivered as a proof of concept inside FEMADex.'),
  ],
}));

s1.push(spacer(260));

s1.push(h1('1.  Purpose and how to read this document'));
s1.push(p('This document proposes what "done" means for the PIIA proof of concept, so that acceptance at the end of the period of performance is a check against agreed statements rather than a negotiation.'));
s1.push(p('Each criterion below is written to be **demonstrable**: it names the artifact, query or on-screen action that shows it is met, and a pass condition that two people looking at the same evidence would score the same way. Criteria that could only be settled by opinion have been rewritten or moved to section 5.'));
s1.push(p('Three things this document deliberately does **not** do:'));
s1.push(bullet('It does not promise an accuracy percentage for automated mapping or for AI-proposed rules on data we have not yet seen. Section 5 explains what is measured and reported instead, and why that is the more useful commitment.'));
s1.push(bullet('It does not accept criteria that depend on FEMA-provided inputs arriving, without also stating what happens if they do not. Section 3 covers that.'));
s1.push(bullet('It does not extend the proof of concept toward production. Section 4 lists what is outside acceptance.'));

s1.push(h1('2.  Basis — points to confirm before this is signed'));
s1.push(p('These criteria are written against the pricing template’s Assumptions tab. **Modification P00001 does not restate those assumptions**, and its three pages reference the PWS rather than the consolidated SOW. We therefore ask FEMA to confirm the following, so that both parties are measuring against the same scope:'));
s1.push(table([620, 4100, 4640],
  ['#', 'To confirm', 'Why it matters here'],
  [
    ['1', 'Which document governs PIIA scope: the PWS paragraph, the consolidated SOW, or the quote’s Assumptions tab', 'Determines whether the SOW’s "Phase 2 Full Implementation" is in or out of this modification. Every criterion below assumes **proof of concept only**'],
    ['2', 'That production deployment remains excluded', 'Assumptions tab states it; the modification does not repeat it'],
    ['3', 'Planning quantities: **20 programs, FY2024–FY2026**', 'AC-06, AC-08 and AC-13 are scoped by these numbers'],
    ['4', 'That FIMS extracts are due **2026-12-15**, with a WebIFMIS-only delivery if they do not arrive', 'AC-01 and AC-11 change shape if FIMS is mandatory'],
    ['5', 'The trigger measure — obligations or **disbursements**', 'Named as a dependency in the funding documents; AC-05 is configuration either way, but the reported figures differ entirely'],
    ['6', 'How the ten-business-day dependency windows are counted from a Friday start', 'Ten business days from Fri 2026-09-18 is **Thu 2026-10-01** if the start day counts, **Fri 2026-10-02** if not'],
    ['7', 'Acceptance response window', 'The SOW refers to a 15-business-day acceptance clause; section 8 assumes it. To be confirmed against the executed documents'],
  ]));

s1.push(h1('3.  FEMA-provided dependencies, and what happens if one is late'));
s1.push(p('Per Assumptions #3 and #4, FEMA provides the following within ten business days of the start — that is, by **2026-10-01/02**:'));
s1.push(table([4700, 4660],
  ['Dependency', 'Criteria that depend on it'],
  [
    ['Sample WebIFMIS extracts, FY2024–FY2026, in the as-is layout', 'AC-01, AC-02, AC-03, AC-06, AC-08, AC-11'],
    ['FEMADex workspace access, catalog creation rights, bundle deployment permission', 'All criteria requiring a run on the platform'],
    ['An approved LLM endpoint in FEMADex', 'AC-10 only'],
    ['A named product owner', 'AC-06, AC-07, AC-09 (adjudication and review sessions)'],
    ['FEMA’s actual preliminary risk assessment instrument', 'AC-07, AC-08'],
    ['The taxonomy for the 20 programs, and last-comprehensive-assessment dates if the three-year cycle is in scope', 'AC-06, AC-08'],
  ]));
s1.push(spacer(160));
s1.push(p('**Proposed rule for a late dependency.** Where a criterion cannot be demonstrated because a dependency above was not available, that criterion is recorded as **deferred, with the date the dependency arrived**, and is not scored as a failure. Where a documented fallback exists, the fallback is demonstrated instead and is sufficient for acceptance:'));
s1.push(bullet('**No LLM endpoint by the deadline** → AC-10 is demonstrated against deterministic, clearly-labelled template rationale, and the endpoint is swapped in without code change when it arrives. The guardrail that AI never computes a reportable number holds in both cases.'));
s1.push(bullet('**No FIMS extracts by 2026-12-15** → the tool is delivered against WebIFMIS only, and we provide a written determination to the Contracting Officer instead of the FIMS comparison.'));
s1.push(bullet('**No real PRA instrument** → AC-07 and AC-08 are demonstrated against the illustrative ten-question instrument already built, explicitly labelled as a placeholder, with the binding mechanism proven so that swapping the real instrument is a configuration change.'));
s1.push(p('We request that late dependencies and their impact be noted in the weekly status so that this is never a surprise at acceptance.'));

s1.push(h1('4.  Explicitly outside acceptance'));
s1.push(p('Stated so that neither party expects them in February:'));
[
  'Production deployment, production data, or operation in a production environment.',
  'Authority to operate, FedRAMP assessment, or any security accreditation activity.',
  'Organisation-wide RBAC rollout beyond the dev/test role model used to demonstrate sign-off.',
  'Migration of, or changes to, WebIFMIS, FIMS or any system of record.',
  'Ongoing maintenance of the WebIFMIS-to-FIMS code bridge after the period of performance.',
  'Training programmes and change management beyond the handover walkthrough in AC-12.',
  'Any guarantee of a specific automated-mapping accuracy rate (see section 5).',
  'Processing of live or production CUI outside the agreed dev/test catalogs.',
].forEach(t => s1.push(bullet(t)));

s1.push(h1('5.  Measured and reported, not guaranteed'));
s1.push(p('Two things will be quantified during the pilot, reported honestly, and used as inputs to the go/no-go decision. We are **not** proposing them as pass/fail thresholds, and we would advise FEMA against accepting a vendor who offers a number here before seeing the data:'));
s1.push(numbered('**Automated mapping agreement rate.** Measured against the SME-adjudicated validation sample of prior-year mapping decisions (AC-06). The rate depends on how consistent the historical groupings actually are — which is precisely what is unknown today, and is the reason the pilot exists.'));
s1.push(numbered('**AI-proposed rule quality and rationale usefulness.** Evaluated against the same adjudicated sample under the evaluation protocol agreed with FEMA (Assumptions #3), tracked in MLflow.'));
s1.push(p('What **is** committed is the **method**: the sample is adjudicated by FEMA SMEs, the measurement is reproducible, the result is reported whatever it says, and every figure carries the lineage to reproduce it. A pilot that returns a low agreement rate with clear evidence of why is a successful pilot — it answers the question the proof of concept was funded to answer.'));
s1.push(p('Batch runtime and data volumes will likewise be measured and reported. No throughput figure is proposed as a criterion, because extract volumes at 20 programs are not yet known.'));

// =====================================================================
// SECTION 2 — landscape: §6
// =====================================================================
const s2 = [];
s2.push(h1('6.  Acceptance criteria'));
s2.push(p('Legend — **When** refers to the demonstration milestone in section 7.', { spacing: { after: 180 } }));
s2.push(table([1000, 2340, 4600, 4180, 1420],
  ['ID', 'Criterion', 'Pass condition', 'Evidence', 'When'],
  [
    ['**AC-01**', 'Extracts are ingested through configuration, not code',
      'The agreed WebIFMIS extracts for FY2024–FY2026 load end to end with the source-to-canonical mapping expressed entirely in `config.schema_map`; no engine code change is made to accommodate a layout',
      '`config.schema_map` rows; one successful job run per fiscal year; row and checksum counts recorded in `silver.mapping_run`', 'M2'],
    ['**AC-02**', 'The deterministic core is reproducible',
      'Two runs of the same job over the same extract and the same configuration version produce byte-identical `silver` and `gold` outputs',
      'Table hashes compared across two `mapping_run_id` values, demonstrated live', 'M1, re-shown M4'],
    ['**AC-03**', 'No dollar is silently dropped',
      'For every run, sum(bronze disbursements) = sum(mapped) + sum(exception queue) exactly, and every transaction is in exactly one of those two states',
      'Reconciliation query executed on screen; exception-queue total shown as an explicit figure', 'M2'],
    ['**AC-04**', 'Machine-proposed mappings cannot reach a report unreviewed',
      'Any mapping rule with status `inferred` carries a confidence and contributes to no reportable figure until an approval row exists in `review.decision`',
      'Rule status lifecycle demonstrated in the app; query showing inferred-but-unapproved rules excluded from `gold`', 'M3'],
    ['**AC-05**', 'The comprehensive-assessment trigger is configuration',
      'Measures, threshold, direction and floors are edited in configuration; re-running re-flags programs with no code change and no redeploy',
      'Before/after `gold.trigger_evaluation` for the same fiscal year across two configuration versions', 'M2'],
    ['**AC-06**', 'Mapping decisions are validated against FEMA judgement',
      'For the agreed 20 programs, a validation sample of prior-year mapping decisions is adjudicated with FEMA SMEs, and the agreement rate is computed and reported. **No minimum rate is guaranteed** (section 5)',
      'Adjudication workbook; `review.decision` rows; agreement rate in the summary deliverable', 'M3'],
    ['**AC-07**', 'FEMA’s instrument drives the assessment',
      'FEMA’s actual PRA instrument is loaded into `config.risk_question`, and every question is classified auto-populated, conditional or human-answered with its named data binding recorded',
      '`config.risk_question` contents shown against the source instrument', 'M3'],
    ['**AC-08**', 'Draft responses carry lineage to the ledger',
      'Draft PRA responses exist for all 20 programs for FY2026 with prior-year comparison, and any auto-populated figure can be traced on screen to the contributing transaction identifiers',
      '`gold.risk_response` plus a live lineage query from a single answer down to `txn_id`', 'M4'],
    ['**AC-09**', 'A human signs off, and the record proves it',
      'A reviewer authenticated through FEMA identity can approve, override with a mandatory reason, and finalize; nothing reaches final status without sign-off; every action appears in `review.audit_event` with the acting identity',
      'Live walkthrough by a FEMA reviewer; audit query over that session', 'M4'],
    ['**AC-10**', 'AI explains, never computes',
      'Rationale text is generated only via the FEMA-approved endpoint, is labelled as AI-generated, and any numeral appearing in generated text is validated against the source figure — a mismatch quarantines the row rather than publishing it',
      '`explain` task logs showing a deliberately induced mismatch being quarantined; MLflow evaluation record', 'M4'],
    ['**AC-11**', 'Downstream teams can consume the output',
      'Spend summary and PRA package exports are produced to a Volume in the agreed formats and reconcile exactly to `gold.*`',
      'Export files plus a diff against the source tables', 'M4'],
    ['**AC-12**', 'FEMA owns what was built',
      'Documented repeatable methodology, summary deliverable (approach, confidence levels, validated codes, items needing further validation), results briefing and scaled-deployment outline are delivered; all code and configuration are in the FEMA-owned repository and deployable bundle; secrets rotated at handover',
      'Documents; repository and bundle transfer; handover walkthrough', 'M5'],
    ['**AC-13**', 'The engine is provably correct before it touches real data',
      'The engine reproduces a committed reference dataset **exactly** — every value of the mapping, spend summary, fiscal-year summary and risk-response tables — from the transaction ledger and the rules alone, as an automated test that runs on every change',
      'Test suite executed live against the reference dataset; value count reported', '**M1**'],
  ]));
s2.push(spacer(180));
s2.push(p('**A note on AC-13.** This one is already met and can be demonstrated at kickoff. The engine reproduces **4,014 committed values** across four tables from the transaction ledger plus the rules in force, on both the off-platform and Spark execution paths, and re-checks them after a Delta round trip. We propose it as a criterion because it is the cheapest possible early proof that the deterministic core is sound, and because it gives FEMA a concrete acceptance event in the first weeks rather than only in February.'));

// =====================================================================
// SECTION 3 — portrait: §7–§9
// =====================================================================
const s3 = [];
s3.push(h1('7.  Demonstration milestones'));
s3.push(p('We propose acceptance be demonstrated in stages rather than once at the end. Each stage is a working session with the product owner; criteria accepted at a stage are not reopened unless the underlying code or configuration changes.'));
s3.push(table([700, 2900, 2200, 3560],
  ['', 'Milestone', 'Indicative timing', 'Criteria demonstrated'],
  [
    ['**M1**', 'Platform and engine proof — on synthetic reference data, before real extracts exist', 'Early October', 'AC-13, AC-02'],
    ['**M2**', 'Real extract through the pipeline', 'Late October / early November', 'AC-01, AC-03, AC-05'],
    ['**M3**', 'Mapping validated; instrument loaded', 'Late November', 'AC-04, AC-06, AC-07'],
    ['**M4**', 'Full run, review and sign-off', 'Late January', 'AC-08, AC-09, AC-10, AC-11, and AC-02 re-shown on real data'],
    ['**M5**', 'Handover', 'February, before 2027-02-18', 'AC-12'],
  ]));
s3.push(spacer(160));
s3.push(p('Indicative timings follow the delivery plan and move with the dependency dates in section 3.'));

s3.push(h1('8.  Acceptance process'));
[
  'Guidehouse demonstrates the criteria for a milestone and provides the evidence named in section 6.',
  'FEMA responds in writing within the agreed acceptance window (section 2, item 7) with acceptance, or with specific criteria not met and the reason.',
  'Where a criterion is not met, Guidehouse proposes a remediation and a date; the criterion is re-demonstrated at the next milestone or in a dedicated session.',
  'Where a criterion is **deferred** under section 3, the record states which dependency was outstanding and from when.',
  'Acceptance of the proof of concept overall is the acceptance of AC-01 through AC-13, each either accepted or formally deferred, at M5.',
].forEach(t => s3.push(numbered(t)));
s3.push(p('A criterion is never accepted or rejected on the basis of a figure this document has stated will be measured rather than guaranteed (section 5).'));

s3.push(h1('9.  Traceability'));
s3.push(table([900, 3800, 4660],
  ['AC', 'SOW Phase 1 item', 'Design reference'],
  [
    ['AC-01', 'Ingestion via schema-mapping adapter', 'File 06 A2; `REQ-001`, `ASSUMP-12`, `DEC-14`'],
    ['AC-02', 'Deterministic cleansing, crosswalk, rollup', 'File 09 §1; `DEC-05`, `PLT-13`'],
    ['AC-03', 'Confidence-based exception routing', 'File 09 §2; `REQ-003`, `ASSUMP-16`, `DEC-07`'],
    ['AC-04', 'AI proposes only where rules are thin', 'File 09 §§2, 11; `REQ-013`, `DEC-05`'],
    ['AC-05', 'Variance triggers never hard coded', 'File 10 §5; `REQ-010`, `REQ-031`, `ASSUMP-03`, `DEC-08`'],
    ['AC-06', 'Validation sample of prior-year decisions', 'File 09 §7; `SME-04`, `SME-07`'],
    ['AC-07', 'Instrument incorporation', 'File 10 §2; `SME-05`, `DEC-03`'],
    ['AC-08', 'PRA responses with lineage', 'File 10 §4; `REQ-008`, `PLT-02`'],
    ['AC-09', 'Review, approval, sign-off', 'File 06 §5; `ASSUMP-17`, `DEC-06`, `PLT-06`, `PLT-11`'],
    ['AC-10', 'AI-use approvals and guardrails', 'File 09 §11 G1/G3; `PLT-08`'],
    ['AC-11', 'Data support for downstream assessment', 'File 10 §6; `ASSUMP-15`, `SME-14`, `PLT-12`'],
    ['AC-12', 'Methodology, briefing, go/no-go, handover', 'File 18 §5; Assumptions #6'],
    ['AC-13', 'Underpins every criterion above', '`PLT-13`, `PLT-14`, `DEC-27`, `DEC-33`'],
  ]));

s3.push(spacer(300));
s3.push(new Paragraph({
  spacing: { before: 200 },
  border: { top: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 10 } },
  children: [new TextRun({
    text: 'Prepared by Guidehouse for FEMA Financial Systems Modernization. Figures describing the reference dataset refer to a synthetic, watermarked dataset built for development and regression testing; it contains no FEMA data.',
    size: 17, italics: true, color: SLATE, font: FONT,
  })],
}));

// =====================================================================
const doc = new Document({
  creator: 'Guidehouse',
  title: 'Proposed Acceptance Criteria — FEMA PIIA Proof of Concept',
  description: 'Draft acceptance criteria for the PIIA proof of concept under task order 70FA3126F00000042, modification P00001.',
  numbering: {
    config: [
      {
        reference: 'bullets',
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 460, hanging: 240 } } } },
          { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 920, hanging: 240 } } } },
        ],
      },
      {
        reference: 'steps',
        levels: [
          { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 460, hanging: 280 } } } },
        ],
      },
    ],
  },
  sections: [
    { properties: { page: PORTRAIT }, footers: footer(), children: s1 },
    { properties: { page: LANDSCAPE }, footers: footer(), children: s2 },
    { properties: { page: PORTRAIT }, footers: footer(), children: s3 },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(process.argv[2], buf);
  console.log('wrote', process.argv[2], buf.length, 'bytes');
});
