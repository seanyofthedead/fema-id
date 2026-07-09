# 07 — Technology Stack

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-08
**Status:** Conceptual demo. Cloud stack is unconfirmed — Azure referenced for the client, delivery team on AWS; Brett to confirm (`REQ-020`, `ASSUMP-11`, `SME-09`). Both options below are deliberately cloud-portable (`A6` in file 06).
**Cross-references:** `REQ-` (02), `ASSUMP-` (03), `SME-` (13); architecture in file 06.

---

## 1. Two options at a glance

| Dimension | **Option A — Fast Demo** | **Option B — Enterprise-Aligned** |
|---|---|---|
| Goal | Ship the concept demo next week (`REQ-025`) | Show the production-shaped target |
| Front end | Streamlit (or minimal Next.js) | Next.js + React |
| Back end | In-process Python | FastAPI service (containerized) |
| Database | DuckDB (file-based) | PostgreSQL + warehouse (Databricks / Synapse) |
| Data processing | pandas / Polars + DuckDB SQL | Spark/Databricks or dbt + warehouse SQL |
| AI / LLM | Managed LLM API (explanations only) | Managed LLM via gateway + guardrails |
| RAG / search | In-memory vectors over public guidance | Managed vector store |
| Hosting | Laptop / single container | Cloud (AWS or Azure), client tenant if required |
| Auth | None (local) | OIDC SSO + RBAC |
| Build effort | Days | Weeks–months (pilot, not demo) |
| Recommended for | **The demo** | Post-demo pilot planning |

Both options implement the **same logical architecture** (file 06 §2); only the substrate changes. Rules-as-data (`REQ-001`, `REQ-015`) and file-in/file-out (`REQ-019`) are preserved in both.

---

## 2. Option A — Fast Demo stack (recommended for the demo)

| Layer | Choice | Why |
|---|---|---|
| Front end | **Streamlit** | Fastest path to a multi-screen, data-rich UI in Python; single language end-to-end; runs the whole storyboard (file 11) with minimal glue. Alternative: minimal Next.js if a more polished exec look is wanted. |
| Back end | **In-process Python** (no separate service) | The engine (ingest → rules → PRA) is a Python package the UI calls directly; nothing to deploy. |
| Database | **DuckDB** (+ SQLite for tiny config) | Embedded, zero-server, fast analytical SQL over the synthetic ledger; reads/writes Parquet/CSV; perfect for laptop-scale multi-FY data. |
| Data processing | **pandas / Polars + DuckDB SQL** | Cleansing, rollups, event splits, YoY variance in-memory; deterministic and seedable. |
| AI / LLM layer | **Managed LLM API** (Claude via API/gateway) for **explanations only** | Numbers stay deterministic (`A3`); LLM generates rationale text. Prefer a zero-retention endpoint; no real data anyway (synthetic). |
| RAG / search | **In-memory vector index** (e.g., FAISS/Chroma) over public guidance (`SRC-06`, `SRC-07`, `SRC-10`; `ASSUMP-18`) | Small corpus; no external service needed. |
| Rules store | **YAML/JSON config files** in-repo | Proves rules-as-data; editable live during the demo (`REQ-015`). |
| Hosting | **Laptop or single Docker container** | No cloud dependency in the critical path (`ASSUMP-11`). |
| Auth | **None / local** | Synthetic data, single presenter. Illustrative roles only (`ASSUMP-19`). |
| Export | **openpyxl (XLSX), CSV, PDF** | Excel-compatible outputs echo the legacy "macro" expectation (`ASSUMP-15`, `REQ-021`); format per `SME-14`. |

**Pros:** buildable in days; one language; trivially portable; no infra to provision; every rule change visible instantly.
**Cons:** not multi-user; no real auth/security; Streamlit ceiling on bespoke UX polish; not production-shaped.
**Recommended use:** the in-person concept demo (`REQ-025`) and iteration check-ins.

---

## 3. Option B — Enterprise-Aligned stack (post-demo pilot)

| Layer | Choice | Why |
|---|---|---|
| Front end | **Next.js + React** (App Router) | Production-grade UX, SSR, role-aware views, embeddable dashboards; matches a real analyst tool. |
| Back end | **FastAPI** (Python, containerized) | Keeps the demo's Python engine intact behind a typed HTTP API; async, OpenAPI docs, easy auth middleware. |
| Database | **PostgreSQL** (operational) + **warehouse** (Databricks Lakehouse or Azure Synapse) | Postgres for app/config/audit; warehouse for multi-year analytical spend at scale. |
| Data processing | **Databricks (Spark)** or **dbt + warehouse SQL** | Scales historical mining (`REQ-013`) and multi-FY aggregation; lineage-friendly. |
| AI / LLM layer | **Managed LLM through a gateway** with guardrails, logging, fallback | Centralized model access, observability, zero data retention; still explanation-only (`A3`). |
| RAG / search | **Managed vector store** (e.g., pgvector, Azure AI Search, or Databricks Vector Search) | Larger corpus incl. internal SOP once released (`SME-17`). |
| Rules store | **Config service / versioned rules repo** (DB-backed, UI-editable) | Rules-as-data with governance, versioning, approval (`REQ-015`). |
| Hosting | **AWS or Azure**, client tenant if mandated | Cloud-neutral; FedRAMP-authorized services in production (Wave 8). |
| Auth | **OIDC SSO** + **RBAC** (analyst / reviewer / admin) | Real identity + `ASSUMP-17` sign-off; confirm roles `SME-16`. |
| Reporting / BI | **Power BI** (or embedded dashboards) | Executive dashboard + distributable reports; format per `SME-14`. |

**Pros:** multi-user, secure, scalable; production-shaped; supports real governance and audit.
**Cons:** weeks–months to stand up; requires confirmed cloud/tenant and security posture; higher cost; overkill for a concept demo.
**Recommended use:** pilot after SME validation (files 12–13); never the vehicle for next week's demo.

---

## 4. Component decisions and rationale

| Decision | Chosen | Rejected alternative | Rationale | Traces to |
|---|---|---|---|---|
| Demo UI | Streamlit | React SPA | Speed over polish for concept demo | `REQ-025` |
| Demo DB | DuckDB | PostgreSQL | Zero-server, analytical, laptop-scale | `ASSUMP-11` |
| LLM role | Explanation/RAG only | LLM computes figures | Auditable determinism | `A3`, `SME-15` |
| Rules format | YAML config | Code branches | Swappable when SOP lands | `REQ-015`, `ASSUMP-06` |
| Data grain | Record-level synthetic | Aggregated only | Enables rollup + mining demos | `ASSUMP-01`, `REQ-013` |
| Warehouse (Opt B) | Databricks / Synapse | Bespoke ETL | Lineage + scale for many FYs | `REQ-014` |

---

## 5. Cloud portability matrix (Option B)

Cloud is unconfirmed; every Option-B component has an equivalent on both platforms so the choice can wait for `SME-09`.

| Capability | AWS | Azure | Portable/neutral |
|---|---|---|---|
| Object store | S3 | Blob Storage | MinIO / local FS |
| Warehouse | Redshift / Databricks on AWS | Synapse / Databricks on Azure | DuckDB (small), Postgres |
| Managed LLM | Bedrock | Azure OpenAI / AI Foundry | Gateway abstraction |
| Vector store | OpenSearch / pgvector | Azure AI Search / pgvector | Chroma / FAISS |
| Container hosting | ECS / EKS | Container Apps / AKS | Docker anywhere |
| Identity | Cognito / IAM + client IdP | Entra ID | OIDC standard |
| BI | QuickSight | Power BI | Embedded dashboard |

**Design rule:** no cloud-proprietary service sits in the critical path; swapping providers is configuration, not a rewrite (`ASSUMP-11`, `REQ-020`).

---

## 6. Recommendation

- **Build the demo on Option A.** It meets the fixed date (`REQ-025`), is fully portable (`ASSUMP-11`), and demonstrates every required capability.
- **Present Option B as the target** in the talk track (file 14) and roadmap (file 12), explicitly gated on `SME-09` (cloud/tenant), `SME-16` (roles), and security posture (file 15).
- Keep the **engine identical** across A and B: a Python package with a stable file-in/file-out contract, so the demo code carries forward into the pilot rather than being thrown away.

> No production readiness is implied. Option B is a *direction*, hardened only after SME validation and a security assessment (Wave 8).
