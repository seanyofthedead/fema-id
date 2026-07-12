// Structural critic probe for the six FEMA design alternatives.
// Usage: node critic_probe.mjs <index.html> [<index.html> ...]
// Emits per-file: heading outline, landmarks, view/workspace inventory, control census,
// accessibility posture, policy scans (requirement IDs, synthetic/simulated labeling),
// and a primary-navigation exercise (click nav candidates, diff visible views).
import { JSDOM, VirtualConsole } from "jsdom";
import fs from "node:fs";

let files = process.argv.slice(2);
const REVERIFY = files[0] === "--reverify";
if (REVERIFY) files = files.slice(1);
if (!files.length) { console.error("usage: node critic_probe.mjs [--reverify] <index.html>..."); process.exit(2); }

const trunc = (s, n = 90) => { s = (s || "").replace(/\s+/g, " ").trim(); return s.length > n ? s.slice(0, n) + "…" : s; };

function accName(el) {
  return trunc(el.getAttribute?.("aria-label") || el.getAttribute?.("title") || el.textContent, 60);
}

async function probe(file) {
  const html = fs.readFileSync(file, "utf-8");
  const consoleErrors = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", e => consoleErrors.push("jsdomError: " + (e && e.message)));
  vc.on("error", (...a) => consoleErrors.push("console.error: " + a.join(" ")));

  const dom = new JSDOM(html, {
    runScripts: "dangerously",
    pretendToBeVisual: true,
    url: "file:///" + file.replace(/\\/g, "/"),
    virtualConsole: vc,
    beforeParse(window) {
      window.matchMedia = window.matchMedia || (q => ({
        matches: false, media: q, addListener() {}, removeListener() {},
        addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; },
      }));
      window.HTMLElement.prototype.scrollIntoView = window.HTMLElement.prototype.scrollIntoView || function () {};
      window.HTMLElement.prototype.scrollTo = window.HTMLElement.prototype.scrollTo || function () {};
      window.scrollTo = () => {};
      if (window.SVGElement && !window.SVGElement.prototype.getBBox) {
        window.SVGElement.prototype.getBBox = () => ({ x: 0, y: 0, width: 100, height: 20 });
      }
      window.requestAnimationFrame = cb => setTimeout(() => cb(0), 0);
    },
  });
  await new Promise(r => setTimeout(r, 500));
  const { window } = dom;
  const { document } = window;

  const hiddenCache = new Map();
  function isHidden(el) {
    if (!el || el === document.body || el === document.documentElement) return false;
    if (hiddenCache.has(el)) return hiddenCache.get(el);
    let h = false;
    try {
      if (el.hidden || el.getAttribute?.("aria-hidden") === "true") h = true;
      else {
        const cs = window.getComputedStyle(el);
        if (cs.display === "none" || cs.visibility === "hidden") h = true;
        else h = isHidden(el.parentElement);
      }
    } catch { h = isHidden(el.parentElement); }
    hiddenCache.set(el, h);
    return h;
  }
  const clearVis = () => hiddenCache.clear();

  const out = { file, consoleErrors: consoleErrors.slice(0, 3) };
  out.title = document.title;

  // ---- heading outline (visible + hidden counts) ----
  const heads = [...document.querySelectorAll("h1,h2,h3")];
  out.headingCounts = { total: heads.length, visible: heads.filter(h => !isHidden(h)).length };
  out.outlineVisible = heads.filter(h => !isHidden(h)).slice(0, 60)
    .map(h => h.tagName.toLowerCase() + ": " + trunc(h.textContent, 80));
  out.outlineHiddenSample = heads.filter(h => isHidden(h)).slice(0, 25)
    .map(h => h.tagName.toLowerCase() + ": " + trunc(h.textContent, 60));

  // ---- landmarks ----
  out.landmarks = [...document.querySelectorAll("header,nav,main,aside,footer,[role=navigation],[role=main],[role=banner],[role=complementary],[role=dialog],[role=tablist],[role=region],[role=search],[role=log],[role=toolbar]")]
    .slice(0, 40).map(el => `${el.tagName.toLowerCase()}${el.getAttribute("role") ? "[role=" + el.getAttribute("role") + "]" : ""}${el.getAttribute("aria-label") ? " '" + trunc(el.getAttribute("aria-label"), 50) + "'" : ""}${isHidden(el) ? " (hidden)" : ""}`);

  // ---- named views / workspaces / sections ----
  const viewSel = "[data-view],[data-screen],[data-workspace],[data-panel],section[id],main > section, .view,.workspace,.screen,.panel[id]";
  const views = [...document.querySelectorAll(viewSel)];
  out.views = views.slice(0, 40).map(v => {
    const label = v.getAttribute("aria-label") || v.getAttribute("data-view") || v.getAttribute("data-screen") || v.getAttribute("data-workspace") || v.id || trunc(v.querySelector("h1,h2,h3")?.textContent, 50);
    return `${v.tagName.toLowerCase()}#${v.id || "-"} '${trunc(label, 55)}'${isHidden(v) ? " (hidden)" : ""}`;
  });

  // ---- control census ----
  const btns = [...document.querySelectorAll("button,[role=button]")];
  const selects = [...document.querySelectorAll("select")];
  const ranges = [...document.querySelectorAll("input[type=range]")];
  const texts = [...document.querySelectorAll("input[type=text],input[type=search],input:not([type]),textarea")];
  const checks = [...document.querySelectorAll("input[type=checkbox],input[type=radio]")];
  out.controls = {
    buttons: btns.length, buttonsVisible: btns.filter(b => !isHidden(b)).length,
    selects: selects.length, ranges: ranges.length, textInputs: texts.length, checksRadios: checks.length,
    detailsSummary: document.querySelectorAll("summary").length,
    tables: document.querySelectorAll("table").length,
    svgs: document.querySelectorAll("svg").length,
  };
  out.buttonNameSample = btns.filter(b => !isHidden(b)).slice(0, 45).map(accName);
  out.rangeLabels = ranges.map(r => {
    const id = r.id; let lab = r.getAttribute("aria-label");
    if (!lab && id) lab = document.querySelector(`label[for="${id}"]`)?.textContent;
    return trunc(lab || "(unlabeled)", 60);
  });
  out.selectLabels = selects.map(s => {
    const id = s.id; let lab = s.getAttribute("aria-label");
    if (!lab && id) lab = document.querySelector(`label[for="${id}"]`)?.textContent;
    return trunc(lab || "(unlabeled)", 60);
  });

  // ---- accessibility posture ----
  const unlabeledButtons = btns.filter(b => !isHidden(b) && !(b.getAttribute("aria-label") || "").trim() && !(b.textContent || "").trim() && !(b.getAttribute("title") || "").trim());
  const inputsNeedingLabel = [...texts, ...selects, ...ranges, ...checks].filter(i => {
    if (i.getAttribute("aria-label") || i.getAttribute("aria-labelledby")) return false;
    if (i.id && document.querySelector(`label[for="${i.id}"]`)) return false;
    if (i.closest("label")) return false;
    return true;
  });
  out.a11y = {
    unlabeledVisibleButtons: unlabeledButtons.length,
    unlabeledFormControls: inputsNeedingLabel.length,
    unlabeledFormControlSample: inputsNeedingLabel.slice(0, 8).map(i => i.tagName.toLowerCase() + "[" + (i.type || "") + "]#" + (i.id || i.className || "?")),
    ariaLive: document.querySelectorAll("[aria-live],[role=status],[role=alert],[role=log]").length,
    ariaExpanded: document.querySelectorAll("[aria-expanded]").length,
    ariaCurrentOrSelected: document.querySelectorAll("[aria-current],[aria-selected=true],[aria-pressed=true]").length,
    skipLink: !!document.querySelector("a[href^='#']:first-child, .skip-link, [class*=skip]"),
    positiveTabindex: document.querySelectorAll("[tabindex]:not([tabindex='0']):not([tabindex='-1'])").length,
    dialogs: [...document.querySelectorAll("[role=dialog],dialog")].map(d => `${d.tagName.toLowerCase()} aria-modal=${d.getAttribute("aria-modal")} labelled=${!!(d.getAttribute("aria-label") || d.getAttribute("aria-labelledby"))}`).slice(0, 8),
    tablesWithScope: document.querySelectorAll("th[scope]").length,
    thTotal: document.querySelectorAll("th").length,
  };

  // ---- policy scans on rendered (non-script) text ----
  const bodyClone = document.body.cloneNode(true);
  for (const s of bodyClone.querySelectorAll("script,style,noscript,template")) s.remove();
  const bodyText = bodyClone.textContent || "";
  const reqIds = [...bodyText.matchAll(/\b(?:REQ|ASSUMP|SRC|GAP|DEC|FLOW|RL|UX|CH)-\d+\b|\bSME-\d+\b/g)].map(m => m[0]);
  out.policy = {
    requirementIdBadges: [...new Set(reqIds)].slice(0, 10),
    syntheticMentions: (bodyText.match(/SYNTHETIC/gi) || []).length,
    simulatedMentions: (bodyText.match(/simulat/gi) || []).length,
    illustrativeMentions: (bodyText.match(/illustrativ/gi) || []).length,
    glossary: {
      PRA_glossed: /Preliminary Risk Assessment/i.test(bodyText),
      PIIA_glossed: /Payment Integrity Information Act|improper.payment/i.test(bodyText),
      YoY_glossed: /year.over.year/i.test(bodyText),
      TAFS_glossed: /Treasury Appropriation Fund Symbol|TAFS \(|account symbol/i.test(bodyText),
    },
    bannerText: trunc(document.querySelector("header, [role=banner], .banner, [class*=banner]")?.textContent, 220),
  };

  // ---- primary navigation exercise ----
  const navCandidates = [...new Set([
    ...document.querySelectorAll("[role=tab]"),
    ...document.querySelectorAll("nav button, nav a"),
    ...document.querySelectorAll("header button"),
    ...document.querySelectorAll("[data-nav],[data-view-btn],[data-target-view],[aria-controls]"),
  ])].filter(el => !isHidden(el)).slice(0, 16);

  function visState() {
    clearVis();
    const vh = heads.filter(h => !isHidden(h)).map(h => trunc(h.textContent, 40));
    return vh.join(" | ");
  }
  out.navExercise = [];
  const before0 = visState();
  for (const el of navCandidates) {
    const before = visState();
    try { el.click(); } catch (e) { out.navExercise.push({ ctrl: accName(el), error: e.message }); continue; }
    await new Promise(r => setTimeout(r, 60));
    const after = visState();
    out.navExercise.push({
      ctrl: accName(el) || el.tagName,
      changedVisibleHeadings: before !== after,
      visibleHeadingsAfter: before !== after ? trunc(after, 220) : undefined,
    });
    // press Escape to close any overlay it opened
    try { document.dispatchEvent(new window.KeyboardEvent("keydown", { key: "Escape", bubbles: true })); } catch {}
    await new Promise(r => setTimeout(r, 30));
  }
  out.initialVisibleHeadings = trunc(before0, 300);

  // ---- deep dive: open primary work objects and census what appears ----
  out.deepDive = [];
  const deepPatterns = [/CASE-2026-IA/i, /open case/i, /4 of 5 programs/i, /codes I can.t map|can.t you verify/i, /why is|why did|show me why/i, /preset|investigat/i, /^inbox|^review$|^registry/i, /flag|breach|flare/i, /rule|code card/i];
  const seen = new Set();
  for (const pat of deepPatterns) {
    clearVis();
    const cand = [...document.querySelectorAll("button,[role=button],[role=tab],a[href^='#']")]
      .find(el => !isHidden(el) && pat.test(accName(el)) && !seen.has(accName(el)));
    if (!cand) continue;
    seen.add(accName(cand));
    try { cand.click(); } catch (e) { out.deepDive.push({ clicked: accName(cand), error: e.message }); continue; }
    await new Promise(r => setTimeout(r, 300));
    clearVis();
    const vh = [...document.querySelectorAll("h1,h2,h3,h4")].filter(h => !isHidden(h)).slice(0, 22).map(h => trunc(h.textContent, 55));
    const vb = [...document.querySelectorAll("button,[role=button]")].filter(b => !isHidden(b));
    out.deepDive.push({
      clicked: accName(cand),
      visibleHeadings: vh,
      visibleButtonCount: vb.length,
      newButtonNames: vb.slice(0, 28).map(accName),
    });
    try { document.dispatchEvent(new window.KeyboardEvent("keydown", { key: "Escape", bubbles: true })); } catch {}
    await new Promise(r => setTimeout(r, 40));
  }

  try { window.close(); } catch {}
  return out;
}

// ===================== RE-VERIFICATION MODE =====================
async function makeDom(file) {
  const html = fs.readFileSync(file, "utf-8");
  const errors = [];
  const vc = new VirtualConsole();
  vc.on("jsdomError", e => errors.push("jsdomError: " + (e && e.message)));
  vc.on("error", (...a) => errors.push("console.error: " + a.join(" ")));
  const dom = new JSDOM(html, {
    runScripts: "dangerously", pretendToBeVisual: true,
    url: "file:///" + file.replace(/\\/g, "/"), virtualConsole: vc,
    beforeParse(window) {
      window.matchMedia = window.matchMedia || (q => ({ matches: false, media: q, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; } }));
      window.HTMLElement.prototype.scrollIntoView = window.HTMLElement.prototype.scrollIntoView || function () {};
      window.HTMLElement.prototype.scrollTo = window.HTMLElement.prototype.scrollTo || function () {};
      window.scrollTo = () => {};
      if (window.SVGElement && !window.SVGElement.prototype.getBBox) window.SVGElement.prototype.getBBox = () => ({ x: 0, y: 0, width: 100, height: 20 });
      window.requestAnimationFrame = cb => setTimeout(() => cb(0), 0);
    },
  });
  await new Promise(r => setTimeout(r, 500));
  return { dom, errors };
}
const settle = (ms = 300) => new Promise(r => setTimeout(r, ms));

async function reverify(file) {
  const { dom, errors } = await makeDom(file);
  const { window } = dom; const { document } = window;
  const out = [];
  const chk = (name, pass, detail = "") => out.push((pass ? "PASS  " : "FAIL  ") + name + (detail ? "  -- " + trunc(String(detail), 240) : ""));
  const btns = () => [...document.querySelectorAll("button,[role=button]")];
  const byName = re => btns().find(b => re.test((b.getAttribute("aria-label") || "") + " " + (b.textContent || "")));
  const renderedText = () => { const c = document.body.cloneNode(true); for (const s of c.querySelectorAll("script,style,noscript,template")) s.remove(); return c.textContent || ""; };

  // universal regressions
  chk("zero console errors on load", errors.length === 0, errors.slice(0, 3).join(" | "));
  const ids = [...renderedText().matchAll(/\b(?:REQ|ASSUMP|SRC|GAP|DEC|FLOW|RL|UX|CH)-\d+\b|\bSME-\d+\b/g)].map(m => m[0]);
  chk("no rendered requirement-ID badges", ids.length === 0, ids.slice(0, 5).join(","));

  if (/01-executive/.test(file)) {
    const h3s = [...document.querySelectorAll("#cards h3")];
    const labeled = h3s.filter(h => (h.getAttribute("aria-label") || "").trim());
    chk("finding h3s carry aria-labels", labeled.length >= 5, labeled.length + "/" + h3s.length + " labeled; sample: " + (labeled[0]?.getAttribute("aria-label") || ""));
    const concise = labeled.filter(h => h.getAttribute("aria-label").length < (h.textContent || "").length);
    chk("aria-labels are concise (shorter than sentence)", concise.length === labeled.length, concise.length + "/" + labeled.length);
    const findCard = re => { const h = h3s.find(x => re.test(x.textContent)); if (!h) return null; let c = h.parentElement; while (c && c.id !== "cards" && !c.querySelector("button")) c = c.parentElement; return c && c.id !== "cards" ? c : null; };
    const usr = findCard(/Urban Search/i);
    if (usr) {
      const names = [...usr.querySelectorAll("button")].map(accName);
      const hasAck = !!usr.querySelector('[data-action="acknowledge"]') || names.some(n => /noted|acknowledg/i.test(n));
      const hasFull = names.some(n => /^concur$|send back|^assign/i.test(n));
      chk("US&R (unflagged) card is acknowledge-only", hasAck && !hasFull, "buttons: " + names.join(" | "));
    } else chk("US&R card located", false);
    const ia = findCard(/Individual Assistance/i);
    if (ia) {
      const names = [...ia.querySelectorAll("button")].map(accName);
      chk("flagged IA card keeps full decision set", names.some(n => /^concur/i.test(n)) && names.some(n => /send back/i.test(n)) && names.some(n => /assign/i.test(n)), names.join(" | "));
    } else chk("IA card located", false);
    // PRA card: expand then inspect
    const praBtn = byName(/review the program drafts|show the draft answers/i);
    if (praBtn) { praBtn.click(); await settle(); }
    // re-query after click: concept 01 re-renders #cards on every state change
    const praH = [...document.querySelectorAll("#cards h3")].find(x => /Preliminary Risk Assessment/i.test(x.textContent));
    let praCard = praH || null; while (praCard && praCard.parentElement && praCard.parentElement.id !== "cards") praCard = praCard.parentElement;
    if (praCard) {
      const names = [...praCard.querySelectorAll("button")].map(accName);
      chk("PRA card has no per-answer editing (no Override)", !names.some(n => /override/i.test(n)), names.filter(n => /override/i.test(n)).join(" | ") || "no override buttons");
      chk("PRA card offers concur / send-back per program", names.some(n => /concur/i.test(n)) && names.some(n => /send back|send-back/i.test(n)), "buttons: " + names.slice(0, 14).join(" | "));
    } else chk("PRA card located", false);
    // regression: unfold
    const why = byName(/show me why/i);
    if (why) { why.click(); await settle(); chk("regression: 'Show me why' unfold reveals lineage path", !!byName(/underlying transactions/i), byName(/underlying transactions/i) ? accName(byName(/underlying transactions/i)) : "lineage button not found"); }
    else chk("'Show me why' present", false);
  }

  if (/02-risk/.test(file)) {
    const kpis = [...document.querySelectorAll("#view-board .kpi")];
    const subs = [...document.querySelectorAll("#view-board .kpi .k-sub")].map(e => trunc(e.textContent, 40));
    chk("queue KPI stat row with sublines", kpis.length >= 3 && subs.length >= 3, kpis.length + " KPIs; sublines: " + subs.join(" · "));
    const lanes = [...document.querySelectorAll("#view-board .lane-sum")].map(e => trunc(e.textContent, 40));
    chk("per-lane posture summaries", lanes.length === 5, lanes.length + " lane summaries: " + lanes.join(" / "));
    const open = byName(/CASE-2026-IA/);
    if (open) {
      open.click(); await settle();
      const h1 = document.querySelector("#view-case h1") || document.querySelector("h1");
      const t = (h1?.textContent || "").replace(/\s+/g, " ").trim();
      chk("case h1 contains only the program name", t === "Individual Assistance", "h1='" + t + "'");
      const chipNear = h1?.parentElement ? trunc(h1.parentElement.textContent, 120) : "";
      chk("status chips render outside the h1 (context)", /Auto-populated|Disaster|Comprehensive/i.test(chipNear), chipNear);
    } else chk("IA case opens", false);
  }

  if (/03-data/.test(file)) {
    const live = document.getElementById("live");
    chk("polite live region exists", !!live && live.getAttribute("aria-live") === "polite", live ? live.outerHTML.slice(0, 80) : "missing");
    const skip = [...document.querySelectorAll("a[href^='#']")].find(a => /skip/i.test(a.textContent));
    chk("skip link present", !!skip, skip ? skip.outerHTML.slice(0, 90) : "");
    const th = document.querySelectorAll("th").length, thS = document.querySelectorAll("th[scope]").length;
    chk("all th scoped", th > 0 && th === thS, thS + "/" + th);
    chk("aria-expanded present on expandables", document.querySelectorAll("[aria-expanded]").length > 0, document.querySelectorAll("[aria-expanded]").length + " elements");
    const emojiRe = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2190}-\u{21FF}\u{25A0}-\u{25FF}\u{2B00}-\u{2BFF}]/u;
    const dirty = btns().filter(b => emojiRe.test(b.getAttribute("aria-label") || (b.getAttribute("aria-label") === null ? b.textContent : "")));
    // accessible name = aria-label if present, else textContent
    const globalEmojiRe = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2190}-\u{21FF}\u{25A0}-\u{25FF}\u{2B00}-\u{2BFF}]/gu;
    const dirtyNames = btns().map(b => {
      const name = b.getAttribute("aria-label") || b.textContent || "";
      const hits = name.match(globalEmojiRe);
      return hits ? "[" + hits.map(c => "U+" + c.codePointAt(0).toString(16).toUpperCase()).join(",") + "] " + trunc(name, 70) : null;
    }).filter(Boolean);
    chk("no emoji in accessible button names", dirtyNames.length === 0, dirtyNames.slice(0, 8).join(" | "));
    const inspH2 = document.querySelector("#inspector h2, aside h2");
    chk("inspector h2 not concatenated", !!inspH2 && !/synthetic data$/i.test(inspH2.textContent.trim()), "h2='" + trunc(inspH2?.textContent, 70) + "'");
    const noOverride = !btns().some(b => /override/i.test(accName(b)));
    chk("PRA: no in-place completion (no Override buttons)", noOverride, btns().filter(b => /override/i.test(accName(b))).map(accName).join(" | ") || "none");
    const hand = byName(/send findings to assessment owner/i);
    chk("PRA hand-off affordance present", !!hand, hand ? accName(hand) : "not found");
    if (hand) {
      hand.click(); await settle();
      chk("hand-off is reason-gated (note field appears)", !!document.getElementById("handoff-note"), document.getElementById("handoff-note")?.outerHTML.slice(0, 90) || "no #handoff-note");
    }
    // live announcement + trail regression on scope change
    const trailBefore = btns().filter(b => /return to (this )?step/i.test(accName(b))).length;
    const progSel = [...document.querySelectorAll("select")].find(s => {
      let lab = s.getAttribute("aria-label") || "";
      if (!lab && s.id) lab = document.querySelector(`label[for="${s.id}"]`)?.textContent || "";
      if (!lab) lab = s.closest("label")?.textContent || "";
      return /program/i.test(lab) && !/sub-program|baseline|comparison/i.test(lab);
    });
    if (progSel && progSel.options.length > 1) {
      progSel.selectedIndex = (progSel.selectedIndex + 1) % progSel.options.length;
      progSel.dispatchEvent(new window.Event("change", { bubbles: true })); await settle();
      chk("live region announces scope change", !!(live && live.textContent.trim()), "'" + trunc(live?.textContent, 120) + "'");
      const trailAfter = btns().filter(b => /return to (this )?step/i.test(accName(b))).length;
      chk("regression: investigation trail still records pivots", trailAfter > trailBefore, trailBefore + " -> " + trailAfter + " steps");
    } else chk("program facet select found", false);
  }

  if (/04-ai-native/.test(file)) {
    const rail = [...document.querySelectorAll(".inq-item")];
    const withLabel = rail.filter(b => (b.getAttribute("aria-label") || "").trim());
    chk("rail items have aria-labels", rail.length > 0 && withLabel.length === rail.length, withLabel.length + "/" + rail.length + "; sample: '" + (withLabel[0]?.getAttribute("aria-label") || "") + "'");
    const garbled = rail.map(b => b.getAttribute("aria-label") || b.textContent).filter(n => /examineropen|examinerdone|youaskedopen/i.test(n.replace(/\s+/g, "")));
    const separated = withLabel.every(b => /[·—,;:]|\. /.test(b.getAttribute("aria-label")));
    chk("rail aria-labels use separators, no concatenation", garbled.length === 0 && separated, garbled.slice(0, 3).join(" | ") || (withLabel[1]?.getAttribute("aria-label") || ""));
    const second = rail[1];
    if (second) {
      second.click(); await settle();
      const h2 = document.querySelector("#threadPane h2");
      chk("active thread question is the pane's h2", !!h2, "h2='" + trunc(h2?.textContent, 90) + "'");
    }
    const skip = document.querySelector("a.skip-link, a[href='#threadPane']");
    chk("skip link present", !!skip && /skip/i.test(skip.textContent), skip ? skip.outerHTML.slice(0, 90) : "");
  }

  if (/05-radical/.test(file)) {
    const cv = document.getElementById("chronology");
    const zero = cv ? [...cv.querySelectorAll('[tabindex="0"]')] : [];
    const neg = cv ? [...cv.querySelectorAll('[tabindex="-1"]')] : [];
    chk("canvas roving tabindex: exactly one tab stop", zero.length === 1 && neg.length > 50, zero.length + " zero-stops, " + neg.length + " minus-one; current: '" + trunc(zero[0]?.getAttribute("aria-label"), 70) + "'");
    const ann = document.getElementById("navAnnounce");
    chk("canvas aria-live announcer exists", !!ann && ann.getAttribute("aria-live") === "polite", ann ? ann.outerHTML.slice(0, 90) : "missing");
    if (zero[0]) {
      const beforeLbl = zero[0].getAttribute("aria-label");
      zero[0].dispatchEvent(new window.KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true })); await settle();
      const nowZero = [...cv.querySelectorAll('[tabindex="0"]')];
      const moved = nowZero.length === 1 && nowZero[0].getAttribute("aria-label") !== beforeLbl;
      chk("ArrowRight moves roving focus and announces", moved && !!ann?.textContent.trim(), "moved=" + moved + "; announce='" + trunc(ann?.textContent, 110) + "'");
    }
    const th = document.querySelectorAll("th").length, thS = document.querySelectorAll("th[scope]").length;
    chk("all th scoped", th > 0 && th === thS, thS + "/" + th);
    const thr = document.getElementById("thRange");
    chk("threshold slider label meaningful", !!thr && /year-over-year|threshold.*percent/i.test(thr.getAttribute("aria-label") || "") && thr.getAttribute("aria-label") !== "Threshold slider", "'" + thr?.getAttribute("aria-label") + "'");
    const flare = cv?.querySelector('[data-act="flare"]');
    if (flare) {
      flare.dispatchEvent(new window.Event("click", { bubbles: true })); await settle();
      const heads = [...document.querySelectorAll("h1,h2,h3,h4")].map(h => h.textContent);
      chk("regression: flare -> trigger evidence + underlying records", heads.some(t => /Trigger evidence/i.test(t)) && heads.some(t => /Underlying records/i.test(t)), heads.filter(t => /Trigger evidence|Underlying records/i.test(t)).map(t => trunc(t, 50)).join(" | "));
    } else chk("flare element present", false);
  }

  if (/06-additional/.test(file)) {
    const badge = document.getElementById("badge-review");
    chk("Review badge shows 1 pending", (badge?.textContent || "").trim() === "1", "badge='" + badge?.textContent.trim() + "'");
    const live = document.getElementById("live-region");
    chk("polite live region exists", !!live && live.getAttribute("aria-live") === "polite", live ? live.outerHTML.slice(0, 80) : "missing");
    const tpBefore = (document.getElementById("tp-governed")?.textContent || "").trim();
    const tab = byName(/^review/i) || document.getElementById("tab-review");
    if (tab) {
      tab.click(); await settle();
      const card = document.querySelector(".change-card");
      chk("seeded staged change card present", !!card, trunc(card?.querySelector(".change-h")?.textContent, 160));
      chk("seeded change labeled illustrative/simulated", !!card && /illustrativ|simulat/i.test(card.textContent), "");
      const discard = card ? [...card.querySelectorAll("button")].find(b => /discard/i.test(accName(b))) : null;
      chk("seeded change is discardable", !!discard, discard ? accName(discard) : [...(card?.querySelectorAll("button") || [])].map(accName).join(" | "));
      const tpMid = (document.getElementById("tp-governed")?.textContent || "").trim();
      chk("totals unchanged while pending", tpMid === tpBefore, tpBefore + " -> " + tpMid);
      if (discard) {
        discard.click(); await settle();
        const tpAfter = (document.getElementById("tp-governed")?.textContent || "").trim();
        const badgeAfter = (document.getElementById("badge-review")?.textContent || "").trim();
        chk("discard leaves totals unchanged, badge -> 0", tpAfter === tpBefore && (badgeAfter === "0" || badgeAfter === ""), "tp " + tpBefore + " -> " + tpAfter + "; badge='" + badgeAfter + "'; announce='" + trunc(live?.textContent, 90) + "'");
      }
    } else chk("Review tab found", false);
  }

  try { window.close(); } catch {}
  return out;
}

if (REVERIFY) {
  for (const f of files) {
    console.log("\n========== REVERIFY " + f + " ==========");
    try { (await reverify(f)).forEach(l => console.log(l)); }
    catch (e) { console.log("REVERIFY FAILED: " + (e && e.stack || e)); }
  }
} else {
  for (const f of files) {
    try {
      const r = await probe(f);
      console.log("\n========== " + f + " ==========");
      console.log(JSON.stringify(r, null, 1));
    } catch (e) {
      console.log("\n========== " + f + " ==========\nPROBE FAILED: " + (e && e.stack || e));
    }
  }
}
