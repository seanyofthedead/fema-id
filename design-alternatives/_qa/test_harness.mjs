// Headless verification harness for the FEMA design-alternative HTML files.
// Usage: node test_harness.mjs <path-to-index.html>
//
// Checks:
//  1. HTML parses and all scripts execute with zero console errors / uncaught exceptions
//  2. Self-containment: no external http(s) resources, no fetch/XHR at runtime, no web storage use
//  3. Clicks every button / [role=button] / summary / .clickable and asserts no exception
//  4. Runs window.__SELFTEST__() if the file exposes one (each concept embeds its own smoke tests)
//  5. Static checks: @media queries present, SYNTHETIC watermark present, "simulated" labeling present
import { JSDOM, VirtualConsole } from "jsdom";
import fs from "node:fs";

const file = process.argv[2];
if (!file) { console.error("usage: node test_harness.mjs <index.html>"); process.exit(2); }
const html = fs.readFileSync(file, "utf-8");

const results = [];
const add = (name, pass, detail = "") => results.push({ name, pass, detail });

// ---- static checks -------------------------------------------------------
const externalRefs = [...html.matchAll(/(?:src|href)\s*=\s*["'](https?:\/\/[^"']+)["']/gi)]
  .map(m => m[1]);
add("no external src/href resources", externalRefs.length === 0, externalRefs.slice(0, 5).join(", "));
add("no fetch()/XHR in source", !/\bfetch\s*\(|XMLHttpRequest/.test(html));
add("no web storage in source", !/\b(localStorage|sessionStorage|indexedDB)\b/.test(html));
add("media queries present", /@media/.test(html));
add("SYNTHETIC watermark present", /SYNTHETIC/i.test(html));
add("simulated-capability labeling present", /simulat/i.test(html));

// ---- runtime -------------------------------------------------------------
const consoleErrors = [];
const vc = new VirtualConsole();
vc.on("jsdomError", e => consoleErrors.push("jsdomError: " + (e && e.message)));
vc.on("error", (...a) => consoleErrors.push("console.error: " + a.join(" ")));

let dom;
try {
  dom = new JSDOM(html, {
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
} catch (e) {
  add("HTML parses and scripts run", false, String(e).slice(0, 300));
  report();
}

await new Promise(r => setTimeout(r, 400)); // let load handlers / rAF settle
add("zero console errors on load", consoleErrors.length === 0, consoleErrors.slice(0, 5).join(" | "));

const { window } = dom;
const { document } = window;

// body has substantial rendered content
add("body has rendered content", (document.body?.textContent || "").trim().length > 500);

// ---- exercise every clickable control -------------------------------------
const clickables = [...document.querySelectorAll("button, [role=button], summary, [data-action], a[href^='#']")];
let clickErrors = [];
const onErr = e => { clickErrors.push(e.message || String(e.error)); e.preventDefault?.(); };
window.addEventListener("error", onErr);
for (const el of clickables) {
  try { el.click(); } catch (e) { clickErrors.push((el.tagName + " " + (el.textContent || "").trim().slice(0, 30)) + ": " + e.message); }
}
await new Promise(r => setTimeout(r, 300));
add(`clicking all ${clickables.length} controls throws no errors`, clickErrors.length === 0, clickErrors.slice(0, 5).join(" | "));

// change every select, input a value in text inputs
let inputErrors = [];
for (const sel of document.querySelectorAll("select")) {
  try {
    if (sel.options.length > 1) { sel.selectedIndex = (sel.selectedIndex + 1) % sel.options.length; sel.dispatchEvent(new window.Event("change", { bubbles: true })); }
  } catch (e) { inputErrors.push("select: " + e.message); }
}
for (const inp of document.querySelectorAll("input[type=text], input[type=search], input:not([type])")) {
  try { inp.value = "PA"; inp.dispatchEvent(new window.Event("input", { bubbles: true })); }
  catch (e) { inputErrors.push("input: " + e.message); }
}
for (const rng of document.querySelectorAll("input[type=range]")) {
  try { rng.value = rng.max || "30"; rng.dispatchEvent(new window.Event("input", { bubbles: true })); }
  catch (e) { inputErrors.push("range: " + e.message); }
}
await new Promise(r => setTimeout(r, 200));
add("exercising selects/inputs/sliders throws no errors", inputErrors.length === 0, inputErrors.slice(0, 5).join(" | "));

// ---- concept self-tests ----------------------------------------------------
if (typeof window.__SELFTEST__ === "function") {
  try {
    const st = await window.__SELFTEST__();
    for (const t of st) add("selftest: " + t.name, !!t.pass, t.detail || "");
  } catch (e) { add("selftest suite runs", false, String(e).slice(0, 300)); }
} else {
  add("window.__SELFTEST__ exposed", false, "concept must embed its own smoke tests");
}

report();

function report() {
  const failed = results.filter(r => !r.pass);
  for (const r of results) console.log((r.pass ? "PASS" : "FAIL") + "  " + r.name + (r.detail && !r.pass ? "  -- " + r.detail : ""));
  console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
  process.exit(failed.length ? 1 : 0);
}
