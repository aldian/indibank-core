# IndiBank Core Transaction & Ledger Engine - Technical Presentation Guide
> **Executive Architecture Presentation, Speaker Notes, and Demonstration Guide**  
> Target System: **IndiBank Core Transaction & Immutable Ledger Engine**  
> Presenter: **Aldian Fazrihady** • Lead Platform & Distributed Systems Engineer

---

## 1. Quick Presentation Assets (Bilingual: EN & ID)

| Asset | Language | Format | Location | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **PowerPoint / Google Slides (EN)** | English | `.pptx` (16:9 Widescreen) | [`docs/presentation/IndiBank_Core_Architecture_Presentation_EN.pptx`](./IndiBank_Core_Architecture_Presentation_EN.pptx) | English slide deck with embedded speaker notes on every slide. Ready to upload to Google Slides. |
| **PowerPoint / Google Slides (ID)** | Bahasa Indonesia | `.pptx` (16:9 Widescreen) | [`docs/presentation/IndiBank_Core_Architecture_Presentation_ID.pptx`](./IndiBank_Core_Architecture_Presentation_ID.pptx) | Indonesian slide deck with embedded speaker notes on every slide. Ready to upload to Google Slides. |
| **Interactive Web Slides** | Bilingual (Toggle) | `.html` (Standalone) | [`docs/presentation/slides.html`](./slides.html) | Browser-based interactive presentation with instant `[EN \| ID]` toggle, keyboard navigation, and speaker notes panel (`S` key). |
| **Indonesian Guide & Script** | Bahasa Indonesia | Markdown | [`docs/presentation/PRESENTATION_DECK_ID.md`](./PRESENTATION_DECK_ID.md) | Dedicated Indonesian presentation guide, talking script, and Q&A prep. |
| **Slide Generator Script** | Python (`python-pptx`) | Python | [`docs/presentation/build_deck.py`](./build_deck.py) | Automated generator that builds both English and Indonesian decks simultaneously. |

### 🚀 How to Open in Google Slides
1. Open your browser and navigate to **[Google Slides](https://slides.google.com)**.
2. Click **Blank presentation** (or click the folder icon **"Open file picker"**).
3. Select the **Upload** tab.
4. Drag and drop or browse to either:
   - **English Version:** `/mnt/projects/indivara/docs/presentation/IndiBank_Core_Architecture_Presentation_EN.pptx`
   - **Indonesian Version:** `/mnt/projects/indivara/docs/presentation/IndiBank_Core_Architecture_Presentation_ID.pptx`
5. Google Slides automatically converts the presentation into native Google Slides format with all layouts, color palettes, and **presenter notes** preserved!

---

## 2. Presentation Structure & Pitch Timing (18-20 Minutes Total)

```
00:00 - 01:30 | Slide 0: Executive Introduction & Core Mission
01:30 - 03:30 | Slide 1: Business Context & The Core Banking Challenge
03:30 - 05:30 | Slide 2: Enterprise Architectural Blueprint (C4 Container View)
05:30 - 07:30 | Slide 3: Defensive Concurrency & Zero-Loss Financial Consistency
07:30 - 09:00 | Slide 4: Event-Driven Settlement & Real-Time AML Fraud Screening
09:00 - 10:30 | Slide 5: Spec-Driven Development (SDD) & Contract Governance
10:30 - 12:30 | Slide 6: 3-Tier Quality Engineering & JaCoCo Coverage Barrier (99.27%)
12:30 - 14:30 | Slide 7: Site Reliability Engineering (SRE), SLOs, & Prometheus Telemetry
14:30 - 16:30 | Slide 8: Zero-Downtime Blue-Green Release Engineering & Blast Radius Control
16:30 - 18:00 | Slide 9: Multi-Platform Cloud Portability (GCP, AWS, Azure, OpenShift)
18:00 - 20:00 | Slide 10: Live Production Verification, Demonstration, & Q&A
```

---

## 3. Detailed Slide-by-Slide Script, Talking Points, & Anticipated Q&A

### Slide 0: Title Slide
* **Visual:** Deep navy background, bold title, green "ENTERPRISE CORE BANKING PLATFORM" badge, technology stack pills, live domain URLs.
* **Timing:** 1.5 minutes.
* **Speaker Script:**
  > *"Good morning/afternoon everyone. Today I am presenting the IndiBank Core Transaction and Ledger Engine. This system represents an enterprise core banking transaction and immutable general ledger platform designed from first principles for mission-critical digital banking—specifically payment rails like BI-FAST, instant interbank clearing, and intra-bank transfers. It integrates Java 21 with virtual threads, Apache Kafka in KRaft mode, Redis 7 for distributed concurrency guarding, and Oracle Database 23c as the ACID double-entry system of record, deployed live on Google Kubernetes Engine with zero-downtime Blue-Green pipelines."*
* **Key Highlights:**
  - Real-world enterprise banking scope (BI-FAST / RTGS / Core General Ledger).
  - Concrete technology stack: Java 21, Kafka, Redis, Oracle DB 23c, Kubernetes.
  - Live and running on public production domains.

---

### Slide 1: The Core Banking Conundrum: Real-Time vs ACID Consistency
* **Visual:** 3 dark cards highlighting Network Retries, Concurrency Race Conditions, and Ledger Drift.
* **Timing:** 2 minutes.
* **Speaker Script:**
  > *"In consumer tech, availability is often prioritized over strict consistency. If an e-commerce cart retries a request, an extra item might appear. In core banking, consistency is absolute: a duplicate debit of Rp 50,000,000 is an immediate regulatory violation and monetary loss. We identified three existential challenges in high-throughput banking: First, mobile network drops causing aggressive client retries. Second, concurrent payment requests draining the same account simultaneously, risking overdrafts. And third, ledger drift where balances are mutated in-place without immutable audit trails. Our architectural rule is clear: Consistency > Latency > Throughput. We never compromise balance invariance."*
* **Anticipated Q&A:**
  - **Q:** *How do you handle client network drops where the client disconnects before receiving the HTTP response?*
  - **A:** *The transaction completes safely in the database and caches its receipt in Redis with a 24-hour TTL. When the client retries with the same `Idempotency-Key`, they receive the exact cached settled receipt instantaneously with zero duplicate deduction.*

---

### Slide 2: Enterprise Multi-Tier Architecture & Data Flow
* **Visual:** 4 container columns representing Ingress & Engine, Concurrency & Cache, System of Record, and Streaming & Operations.
* **Timing:** 2 minutes.
* **Speaker Script:**
  > *"Here is the multi-tier architectural blueprint. At the edge, Caddy handles automated TLS and routes traffic between our production domain and test preview domain. The core engine is built on Java 21 and Spring Boot 3.3, leveraging Virtual Threads so that each transaction thread can block on I/O without exhausting OS platform threads. Ahead of our database, Redis 7 serves as our defensive concurrency guard. It verifies the client Idempotency-Key and acquires an account-level distributed lock. Oracle Database 23c acts as the single source of truth. Every transfer executes inside an ACID boundary that creates immutable double-entry journal records. Finally, Apache Kafka running in KRaft mode handles asynchronous event streaming, including real-time AML fraud detection for transactions over 100 million Rupiah, and dead-letter queues."*
* **Anticipated Q&A:**
  - **Q:** *Why did you choose Oracle 23c instead of PostgreSQL?*
  - **A:** *Oracle remains the gold standard in tier-1 banking institutions due to its battle-tested ACID engine, robust PL/SQL auditing, fine-grained check constraints, and enterprise backup/recovery tooling.*

---

### Slide 3: Defensive Concurrency & Zero-Loss Ledger Guarantees
* **Visual:** 2x2 grid covering Redis Idempotency State Machine, Distributed Mutex with Lua release, Strict Double-Entry Bookkeeping, and Database Constraints.
* **Timing:** 2 minutes.
* **Speaker Script:**
  > *"Here we examine the technical implementation of our consistency guarantees. First, our Redis Idempotency state machine: when a transfer request arrives, we execute an atomic SETNX. If a duplicate request arrives while the first is in-flight, it receives an immediate 409 Conflict. Once settled, we cache the 201 response for 24 hours. When the user's mobile app retries after a network drop, it receives the exact cached receipt without deducting a single Rupiah. Second, distributed locking: we lock the sender's account using an auto-expiring 10-second token and release it with an atomic Lua script that verifies token ownership. Third, our double-entry engine: balances are never updated in isolation. Every transfer creates equal DEBIT and CREDIT lines. And finally, Oracle enforces a hardware-level CHECK constraint that balance must remain >= 0, backed by JPA @Version optimistic locking."*
* **Anticipated Q&A:**
  - **Q:** *Why is an atomic Lua script required to release the Redis lock?*
  - **A:** *If a transaction experiences an unexpected network delay that exceeds the 10-second TTL, Redis auto-expires the lock and another transaction acquires it. Without an atomic Lua script comparing the lock token before deleting, process A would accidentally delete process B's active lock, exposing the account to race conditions.*

---

### Slide 4: Apache Kafka KRaft: Asynchronous Decoupling & Real-Time AML
* **Visual:** Two side-by-side cards: Kafka KRaft Event Architecture and Real-Time AML Compliance Engine.
* **Timing:** 1.5 minutes.
* **Speaker Script:**
  > *"Now let's examine our event-driven tier. We use Apache Kafka in KRaft mode, eliminating Zookeeper dependencies. When an interbank transfer settles in Oracle, an event is published to `bank.transfers.settled`. Running in parallel is our real-time Anti-Money Laundering (AML) fraud detector. Any transfer equal to or exceeding 100 million Rupiah automatically triggers an alert event to `bank.fraud.alerts` with severity CRITICAL. Notice that this heavy compliance processing is completely decoupled from the HTTP transfer endpoint. The client gets their HTTP 201 settlement receipt in under 150ms. Furthermore, we expose an in-memory stream ticker at `/api/v1/events/recent`, which our dashboard uses to show Kafka events ticking in real-time."*
* **Anticipated Q&A:**
  - **Q:** *How do you prevent event loss if the Kafka broker is temporarily unreachable during database commit?*
  - **A:** *We implemented the Transactional Outbox Pattern: the event is stored in an OUTBOX_EVENTS table within the same ACID database transaction as the ledger lines. An outbox publisher guarantees at-least-once delivery to Kafka.*

---

### Slide 5: Spec-Driven Development (SDD) & Contract Governance
* **Visual:** 3 cards: REST & Async Contracts, Database & Cache Specs, and Standardized RFC 7807 Errors.
* **Timing:** 1.5 minutes.
* **Speaker Script:**
  > *"Our development methodology followed Spec-Driven Development (SDD). Before writing Java code, we formalized our specifications: First, an OpenAPI 3.1 specification for all REST endpoints, which generates our interactive Swagger documentation. Second, an AsyncAPI 3.0 specification for Kafka event payloads. Third, an Oracle 23c DDL specification with strict relational constraints and seed data. And fourth, a Redis Concurrency specification defining key naming conventions, TTL policies, and Lua scripts. In addition, all error responses strictly follow RFC 7807 Problem Details, giving API consumers machine-readable error codes such as VALIDATION_ERROR or INSUFFICIENT_FUNDS."*

---

### Slide 6: 3-Tier Testing Pyramid & JaCoCo Coverage Barrier
* **Visual:** 3 vertical cards (Tier 1 Unit, Tier 2 WebMvc, Tier 3 Live E2E) and an emerald green bottom banner highlighting verified 99.27% coverage.
* **Timing:** 2 minutes.
* **Speaker Script:**
  > *"Let's turn to quality engineering. We implemented a rigorous 3-tier testing pyramid: At Tier 1, our unit tests isolate all core domain logic, testing distributed lock acquisition, idempotency states, and edge cases. At Tier 2, WebMvc integration tests use MockMvc to verify HTTP headers, Bean Validation constraints, and RFC 7807 error status codes. At Tier 3, our automated bash test suite `test-scenarios.sh` executes 7 live banking journeys against the running GKE cluster. Crucially, our CI/CD pipeline enforces a strict JaCoCo quality barrier: any pull request with less than 95% line or instruction coverage is automatically rejected. Our current test suite achieves 99.27% Line Coverage and 99.04% Instruction Coverage with 70 passing tests."*
* **Anticipated Q&A:**
  - **Q:** *How do you prevent slow E2E tests from blocking developers?*
  - **A:** *Unit and WebMvc integration tests run in under 45 seconds in the CI build step. The live E2E test suite runs against the deployed preview domain asynchronously before final production merge.*

---

### Slide 7: Production SRE Framework, SLOs, & Real-Time Telemetry
* **Visual:** 3 cards: SLOs & Error Budgets, Four Golden Signals, and Alerting & Autoscaling.
* **Timing:** 2 minutes.
* **Speaker Script:**
  > *"Let's look at Site Reliability Engineering. In core banking, SRE is about predictability and blast-radius control. We defined clear SLOs: 99.99% availability, which allows just 4.3 minutes of downtime per month. Our latency targets are sub-150ms for p95 and sub-500ms for p99. And our ledger invariance SLO has zero tolerance: mathematical drift is an immediate hard system stop. We monitor the Four Golden Signals via Prometheus metrics exposed at `/actuator/prometheus`. Importantly, we distinguish 4xx client errors, like an insufficient balance, from 5xx system errors, ensuring user validation failures don't consume our reliability error budget. We also implemented Kubernetes Horizontal Pod Autoscaling (HPA) to scale between 1 and 5 replicas based on CPU and memory thresholds, and provided SOP runbooks for incident response."*
* **Anticipated Q&A:**
  - **Q:** *How do you handle database connection pool saturation under spike load?*
  - **A:** *Our Prometheus alert triggers if HikariCP pending threads exist for more than 30 seconds. In parallel, our Kubernetes HPA scales application replicas, and Redis rate limiters protect the database from query storms.*

---

### Slide 8: Zero-Downtime Blue-Green Deployment & Preview Domains
* **Visual:** 3 cards: Branch Protection Gate, Feature Preview Domain, and Blue-Green Production Deploy.
* **Timing:** 2 minutes.
* **Speaker Script:**
  > *"Our release pipeline guarantees zero-downtime deployments and safe blast-radius containment. First, direct pushes to `main` are strictly blocked via GitHub Branch Protection with admin enforcement. Every change requires a feature branch and pull request. Second, when a feature branch is pushed, our CI/CD pipeline deploys a preview container to `https://test.indibank.aldianapps.com`. This allows engineers and testers to verify changes on a live domain before merging. Third, when the PR merges to `main`, our Blue-Green deployment pipeline automatically deploys the new image to the standby slot, waits for pod readiness, and atomically patches the Kubernetes Service selector. Traffic cutover happens instantaneously with zero dropped requests. If a regression is detected post-deployment, we can roll back in under one second by flipping the selector back."*

---

### Slide 9: Multi-Platform Cloud Architecture & Portability
* **Visual:** 2 cards: Cloud & On-Premise Portability Matrix and Production Helm Chart & Container Hardening.
* **Timing:** 1.5 minutes.
* **Speaker Script:**
  > *"While our live demonstration runs on Google Kubernetes Engine in the Jakarta region, the entire platform is designed for multi-cloud and on-premise portability. Many financial institutions operate hybrid environments or deploy across AWS, Azure, or on-premise Red Hat OpenShift. We built a comprehensive Helm chart in `helm/indibank/` that allows deploying IndiBank Core to any CNCF-conformant Kubernetes cluster, including local Minikube or Kind for offline development. The deployment architecture is fully documented in `docs/deployment/MULTI_PLATFORM.md`. Furthermore, our containers adhere to strict enterprise security standards: they run as unprivileged non-root users with strict CPU and memory resource quotas."*

---

### Slide 10: Live Demonstration & Executive Summary
* **Visual:** 3 cards: Live Production Endpoints, Verification Results (7/7 passing), and Executive Summary.
* **Timing:** 2 minutes.
* **Speaker Script:**
  > *"To conclude, IndiBank Core Engine is not a theoretical prototype—it is a live, production-grade core banking engine running in Google Cloud right now. You can open `https://indibank.aldianapps.com` on your browser or phone to execute live interbank transfers, inspect the double-entry general ledger, and watch the real-time Kafka event ticker. Our automated verification suite tested all 7 key banking scenarios against live production, and every single scenario passed. To summarize what we've built: First, absolute financial consistency backed by double-entry accounting in Oracle 23c. Second, defensive concurrency with Redis idempotency and distributed locking preventing double debits. Third, high-throughput asynchronous event streaming with Kafka KRaft. And fourth, zero-downtime Blue-Green deployments backed by an enforced 95% test coverage barrier and full SRE observability. Thank you, and I look forward to taking your questions."*

---

## 4. Live System Verification Proof

```bash
# Execute the live 7-scenario E2E test against production
./test-scenarios.sh https://indibank.aldianapps.com

# Verify live Prometheus metrics
curl -s https://indibank.aldianapps.com/actuator/prometheus | grep http_server_requests_seconds_count
```
