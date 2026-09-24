# IndiBank Core Transaction & Ledger Engine - Structured Live Demonstration Script
> **Execution Playbook, Screen Actions, Talking Points, and Fail-Safe Commands**  
> Target System: **IndiBank Core Transaction & Immutable Ledger Engine**  
> Presenter: **Aldian Fazrihady** • Lead Platform & Distributed Systems Engineer  
> Total Demo Duration: **6 to 8 Minutes**

---

## 1. Pre-Demo Checklist (The 60-Second Preparation)

Before concluding your slide deck, prepare your workspace with these **4 browser tabs** and **1 terminal window**:

| Item | URL / Target | Purpose during Demo |
| :--- | :--- | :--- |
| **Tab 1 (Primary)** | `https://indibank.aldianapps.com` | Live Production Dashboard (Accounts, Form, Kafka Stream) |
| **Tab 2** | `https://indibank.aldianapps.com/swagger-ui.html` | OpenAPI 3.1 Interactive Specification & Schema Contracts |
| **Tab 3** | `https://indibank.aldianapps.com/actuator/prometheus` | Real-time Prometheus SRE Golden Signals & Micrometer Metrics |
| **Tab 4 (Optional)** | `https://test.indibank.aldianapps.com` | Ephemeral Preview Environment (Demonstrating Blue-Green / Preview isolation) |
| **Terminal** | `/mnt/projects/indivara` | Fail-safe CLI test runner (`./test-scenarios.sh https://indibank.aldianapps.com`) |

---

## 2. Quick Demo Progression Flow (Timeline)

```
00:00 - 01:00 | Act 1: The Transition & Production System Overview
01:00 - 02:30 | Act 2: Standard Interbank Transfer & Double-Entry Ledger Verification
02:30 - 04:00 | Act 3: Mobile Network Drop & Idempotent Replay Defense
04:00 - 05:30 | Act 4: High-Value AML Fraud Screening & Asynchronous Kafka Decoupling
05:30 - 07:00 | Act 5: Observability, SRE Golden Signals, & Contract Governance
07:00 - 08:00 | Conclusion & Transition to Discussion / Q&A
```

---

## 3. Step-by-Step Script & Actions

### Act 1: The Transition & Production System Overview (1 Minute)

#### 🎬 Screen Action:
1. Switch from your last slide to **Tab 1: `https://indibank.aldianapps.com`**.
2. Point out the three core visual zones:
   - **Top / Left:** Live Demo Accounts with balances fetched from Oracle DB 23c.
   - **Middle Left:** Interactive Transfer Console with auto-generated UUID Idempotency Key.
   - **Right:** Live Kafka KRaft Stream Terminal with the green `CONNECTED` status badge.

#### 🎙️ Speaker Script (English):
> *"Now that we have reviewed the architectural blueprint, let me transition directly to the running production system. What you see on screen is deployed live on Google Kubernetes Engine in the Jakarta region.*
> 
> *On the left, we have our active core banking accounts backed by Oracle Database 23c. Each transfer form loads with a cryptographically secure, unique UUID Idempotency Key.*
> 
> *On the right, we have our live terminal listening directly to our Apache Kafka broker running in KRaft mode. Notice the green CONNECTED indicator: it is currently awaiting real-time events published across our multi-pod GKE cluster."*

#### 🎙️ Speaker Script (Bahasa Indonesia):
> *"Setelah kita membahas arsitektur teknisnya, sekarang mari kita langsung melihat sistem yang berjalan secara live di Google Kubernetes Engine region Jakarta.*
> 
> *Di sebelah kiri, kita melihat rekening nasabah aktif yang terhubung langsung ke Oracle Database 23c. Setiap form transaksi secara otomatis dilengkapi dengan UUID Idempotency Key.*
> 
> *Di sebelah kanan, kita memiliki terminal stream real-time yang terhubung ke Apache Kafka mode KRaft. Status hijau CONNECTED menunjukkan bahwa terminal ini sedang mendengarkan event yang dipublikasikan secara terdistribusi di seluruh pod GKE kita."*

---

### Act 2: Standard Interbank Transfer & Double-Entry Ledger (1.5 Minutes)

#### 🎬 Screen Action:
1. Select **Source Account**: `1001002001 - PT Mega Pratama Logistik`.
2. Select **Destination Account**: `1001002002 - CV Berkah Sentosa Abadi`.
3. Click the **"5 Juta"** preset button (or type `5.000.000`). Point out the live `Rp 5.000.000,00` preview badge.
4. Click **"Settle Transfer"**.
5. Observe the result:
   - An emerald green alert appears: **"Settlement Succeeded!"** with Reference `TRX-20260924-...` and Journal GL ID (e.g., `#24`).
   - The Accounts table immediately updates both account balances.
   - The Kafka Event Terminal instantly captures and renders the `bank.transfers.settled` event card with topic, partition, offset, and timestamp.

#### 🎙️ Speaker Script (English):
> *"Let's execute a standard interbank transfer of 5 million Rupiah. When I click 'Settle Transfer', the engine executes an atomic ACID transaction within Oracle 23c.*
> 
> *Notice what happened in under 120 milliseconds:*
> 1. *Source account 2001 was debited, and destination account 2002 was credited by the exact same amount.*
> 2. *An immutable double-entry journal entry was created with General Ledger ID #24.*
> 3. *And on our right-hand terminal, Apache Kafka immediately received the `bank.transfers.settled` event, distributed across our Redis cache layer so that all 5 running GKE replicas stay synchronized.*
> 
> *Our account balance invariant holds: total system equity remains mathematically unchanged."*

#### 🎙️ Speaker Script (Bahasa Indonesia):
> *"Mari kita lakukan transfer antar-bank standar sebesar 5 juta Rupiah. Saat saya menekan 'Settle Transfer', engine mengeksekusi transaksi ACID di Oracle 23c.*
> 
> *Perhatikan apa yang terjadi dalam waktu kurang dari 120 milidetik:*
> 1. *Rekening pengirim 2001 didebit, dan rekening penerima 2002 dikredit dengan nominal yang sama persis.*
> 2. *Jurnal pembukuan ganda (double-entry ledger) dibuat dengan ID GL yang unik.*
> 3. *Di terminal kanan, Kafka secara instan menerima event `bank.transfers.settled` yang tersinkronisasi di seluruh pod GKE melalui Redis.*
> 
> *Invarian saldo bank tetap terjaga sempurna tanpa ada selisih."*

---

### Act 3: Mobile Network Drop & Idempotent Replay Defense (1.5 Minutes)

#### 🎬 Screen Action:
1. Without changing any form parameters, click **"Replay Same Request (Test Idempotency)"**.
2. Show the result immediately:
   - The alert displays: **"Idempotent Replay!"** with the exact same Reference Number and Journal GL ID.
   - Point to the Accounts table: **Account balances did NOT change at all.**
3. Optional Negative Test: Type `5000000000` (5 Billion Rupiah) and click **"Settle Transfer"**.
   - Show the red RFC 7807 error banner: `INSUFFICIENT_FUNDS: Source account does not have sufficient balance`.

#### 🎙️ Speaker Script (English):
> *"Now let's demonstrate the most critical test in digital banking: handling mobile network drops and client retries.*
> 
> *Imagine a user in a cellular dead zone: their mobile app sends a payment, the server settles it, but the cellular tower drops the connection before the confirmation receipt arrives. The mobile app automatically retries with the same `Idempotency-Key`.*
> 
> *I will now click 'Replay Same Request'.*
> 
> *Notice what happened: The engine detected the replay. Instead of re-executing the debit or throwing a database deadlock, it returned the original settlement receipt instantly. Look at the balances: not a single Rupiah was deducted twice.*
> 
> *Furthermore, if a client attempts to overdraw an account, our database check constraints and validation layer reject it with standardized RFC 7807 Problem Details."*

#### 🎙️ Speaker Script (Bahasa Indonesia):
> *"Sekarang mari kita uji skenario paling krusial dalam digital banking: gangguan jaringan seluler dan retry otomatis.*
> 
> *Bayangkan pengguna berada di area sinyal lemah: aplikasi mengirim transfer, server berhasil memprosesnya, namun koneksi putus sebelum bukti transfer sampai ke HP nasabah. Aplikasi akan otomatis melakukan retry dengan `Idempotency-Key` yang sama.*
> 
> *Sekarang saya klik 'Replay Same Request'.*
> 
> *Perhatikan: Engine langsung mendeteksi replay ini. Bukti transfer asli dikembalikan secara instan. Lihat tabel saldo: tidak ada saldo yang terpotong untuk kedua kalinya.*
> 
> *Jika pengguna mencoba mentransfer melebihi saldo, sistem langsung menolak dengan format standar RFC 7807 Problem Details."*

---

### Act 4: High-Value AML Fraud Screening & Asynchronous Decoupling (1.5 Minutes)

#### 🎬 Screen Action:
1. Click the red preset button: **"🚨 150 Juta (AML)"**.
2. Notice the description updates to `"High Value Corporate Settlement"`.
3. Click **"Settle Transfer"**.
4. Observe the results:
   - The transfer settles immediately (`HTTP 201`).
   - In the Kafka Event Terminal, **TWO events** appear in rapid succession:
     - `bank.transfers.settled` (settlement notification)
     - `bank.fraud.alerts` with a **red badge** showing `CRITICAL` severity and trigger reason: *"Transfer amount IDR 150000000.00 exceeds high-value reporting threshold of IDR 100000000"*.

#### 🎙️ Speaker Script (English):
> *"Now let's examine event-driven decoupling and compliance screening. In Indonesia, regulatory guidelines mandate real-time Anti-Money Laundering (AML) monitoring for high-value transactions.*
> 
> *I click our '150 Juta AML' preset, transferring 150 million Rupiah, which exceeds our AML threshold of 100 million.*
> 
> *Watch what happens when I click Settle:*
> *First, the client receives their settlement confirmation in under 150ms. The user experience is never degraded.*
> *Second, look at our Kafka terminal on the right: our event-driven consumer intercepted the transaction on the `bank.transfers.settled` topic, evaluated the AML risk rules, and asynchronously emitted a CRITICAL alert to `bank.fraud.alerts`.*
> 
> *This illustrates pure event-driven architecture: heavy compliance checks, fraud scoring, and regulatory reporting run asynchronously without blocking the low-latency payment pipeline."*

#### 🎙️ Speaker Script (Bahasa Indonesia):
> *"Sekarang kita beralih ke asynchronous decoupling dan kepatuhan regulasi AML (Anti-Money Laundering).*
> 
> *Sesuai ketentuan regulator perbankan, transaksi bernilai besar wajib dipantau untuk mendeteksi indikasi fraud atau pencucian uang. Di sini kita menetapkan threshold AML di 100 juta Rupiah.*
> 
> *Saya klik tombol '150 Juta AML' dan klik Settle:*
> *Pertama, nasabah tetap menerima konfirmasi sukses dalam waktu di bawah 150ms. Latensi transaksi tetap sangat cepat.*
> *Kedua, perhatikan terminal Kafka di sebelah kanan: consumer kita mendeteksi transfer bernilai tinggi, memproses aturan AML, dan langsung memublikasikan event CRITICAL ke topik `bank.fraud.alerts`.*
> 
> *Inilah keunggulan arsitektur event-driven: proses audit dan compliance yang berat berjalan secara asinkron tanpa membebani jalur transaksi utama."*

---

### Act 5: Observability, SRE Golden Signals, & Contract Governance (1 Minute)

#### 🎬 Screen Action:
1. Switch to **Tab 2: Swagger UI** (`https://indibank.aldianapps.com/swagger-ui.html`).
   - Scroll briefly through the endpoints: `/api/v1/transfers`, `/api/v1/accounts`, `/api/v1/events/recent`.
2. Switch to **Tab 3: Prometheus Actuator** (`https://indibank.aldianapps.com/actuator/prometheus`).
   - Use browser search (`Ctrl + F`) to highlight:
     - `http_server_requests_seconds_count` (Traffic rate)
     - `jvm_threads_live_threads` (Virtual threads)
     - `hikari` (Database connection pool health)

#### 🎙️ Speaker Script (English):
> *"To conclude our demonstration, let's view the platform engineering and governance tier.*
> 
> *In Tab 2, our OpenAPI 3.1 specification provides strict contract governance, schema validation, and interactive Swagger tooling for upstream API consumers.*
> 
> *In Tab 3, we expose full Prometheus telemetry. Our Grafana dashboards track the Four Golden Signals—Latency, Traffic, Errors, and Saturation. Notice how our JVM metrics reflect Java 21 Virtual Threads, enabling massive I/O concurrency with minimal memory overhead.*
> 
> *Every change deployed to this cluster passed our automated CI/CD pipeline, maintaining an enforced JaCoCo test coverage barrier above 95%, with zero-downtime Blue-Green cutover."*

#### 🎙️ Speaker Script (Bahasa Indonesia):
> *"Sebagai penutup demo, mari kita lihat sisi platform engineering dan tata kelola sistem.*
> 
> *Di Tab 2, spesifikasi OpenAPI 3.1 menjamin standardisasi kontrak API untuk integrasi antar-sistem.*
> 
> *Di Tab 3, telemetri Prometheus memonitor 'Four Golden Signals'—Latency, Traffic, Errors, dan Saturation. Metrik JVM menunjukkan efisiensi Java 21 Virtual Threads yang menangani I/O masif dengan konsumsi memori yang sangat rendah.*
> 
> *Seluruh sistem ini telah teruji dengan pipeline CI/CD otomatis, barrier coverage pengujian di atas 95%, dan deployment Blue-Green tanpa downtime."*

---

## 4. Fail-Safe CLI Mode (Backup Plan)

If screen sharing drops or browser connectivity stutters, execute this **single command** in your terminal:

```bash
./test-scenarios.sh https://indibank.aldianapps.com
```

### What this script displays on screen:
1. **Scenario 1:** Fetches live accounts from Oracle DB 23c.
2. **Scenario 2:** Executes an atomic transfer with auto-generated UUID Idempotency Key.
3. **Scenario 3:** Tests Idempotency replay with the identical key, verifying zero balance drift.
4. **Scenario 4:** Triggers the 150M IDR AML High-Value transfer and verifies event emission.
5. **Scenario 5:** Executes an overdraft attempt, demonstrating RFC 7807 `INSUFFICIENT_FUNDS` rejection.
6. **Scenario 6:** Polls recent Kafka KRaft stream events from Redis.
7. **Scenario 7:** Verifies Prometheus actuator metric counters on the live GKE cluster.

Every step prints formatted color output (`✓ PASSED`) with HTTP response payloads.

---

## 5. Anticipated Demo Questions & Quick Answers

| Question | Recommended 15-Second Answer |
| :--- | :--- |
| **"What happens if two users try to debit the same account at the exact same millisecond?"** | *"Redis acquires an account-level distributed lock with a 10-second TTL and token ownership check. The second request waits or receives a 409 Conflict. In the database, JPA `@Version` optimistic locking and Oracle row-level locks prevent dirty writes."* |
| **"Why does the Kafka stream work across 5 pods without WebSocket?"** | *"Recent Kafka events are persisted in a Redis rolling list (`indibank:events:recent`) capped at 50 items. Regardless of which pod the browser hits via GKE load balancing, all pods query the same Redis list in sub-millisecond time."* |
| **"How is zero-downtime achieved during deployments?"** | *"We use Kubernetes Service selector switching. The new version is deployed to the standby slot (`green` or `blue`), passes its health probes, and the Service selector is atomically updated. In-flight requests drain gracefully."* |
