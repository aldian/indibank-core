# Panduan Presentasi Teknis Arsitektur IndiBank Core Engine (Bahasa Indonesia)
> **Panduan Lengkap Presentasi Eksekutif, Skrip Presenter, dan Skenario Tanya Jawab Teknis**  
> Sistem Target: **IndiBank Core Transaction & Immutable Ledger Engine**  
> Presenter: **Aldian Fazrihady** • Lead Platform & Distributed Systems Engineer

---

## 1. Daftar Aset Presentasi

| Aset | Format | Lokasi | Kegunaan |
| :--- | :--- | :--- | :--- |
| **Slide PowerPoint (ID)** | `.pptx` (16:9 Widescreen) | [`docs/presentation/IndiBank_Core_Architecture_Presentation_ID.pptx`](./IndiBank_Core_Architecture_Presentation_ID.pptx) | Slide deck berbahasa Indonesia dengan catatan presenter (speaker notes) lengkap di setiap slide. Siap diunggah ke Google Slides. |
| **Slide PowerPoint (EN)** | `.pptx` (16:9 Widescreen) | [`docs/presentation/IndiBank_Core_Architecture_Presentation_EN.pptx`](./IndiBank_Core_Architecture_Presentation_EN.pptx) | Slide deck berbahasa Inggris dengan speaker notes lengkap di setiap slide. |
| **Web Slides Interaktif (Bilingual)** | `.html` (Standalone) | [`docs/presentation/slides.html`](./slides.html) | Presentasi web interaktif dengan tombol toggle instan bahasa [EN / ID], navigasi keyboard panah, dan panel catatan presenter (`S`). |
| **Generator Skrip Python** | Python (`python-pptx`) | [`docs/presentation/build_deck.py`](./build_deck.py) | Generator otomatis untuk membuild slide presentasi dalam kedua bahasa secara serempak. |

### 🚀 Cara Membuka di Google Slides
1. Buka browser dan kunjungi **[Google Slides](https://slides.google.com)**.
2. Klik ikon folder (**Buka pemilih file** / *Open file picker*) di kanan atas $\to$ pilih tab **Upload** (Unggah).
3. Pilih atau drag-and-drop file:
   ```text
   /mnt/projects/indivara/docs/presentation/IndiBank_Core_Architecture_Presentation_ID.pptx
   ```
4. Google Slides akan secara otomatis mengonversinya menjadi presentasi Google Slides native dengan seluruh format tata letak, palet warna, dan **catatan presenter** tetap utuh!

---

## 2. Struktur Presentasi & Alokasi Waktu (Total 18–20 Menit)

```
00:00 - 01:30 | Slide 0: Pengantar Eksekutif & Misi Arsitektur Core Banking
01:30 - 03:30 | Slide 1: Konteks Bisnis & Dilema Konsistensi Core Banking
03:30 - 05:30 | Slide 2: Blueprint Arsitektur Enterprise (Tinjauan C4 Container)
05:30 - 07:30 | Slide 3: Defensive Concurrency & Jaminan Saldo Zero-Loss
07:30 - 09:00 | Slide 4: Event Streaming Kafka & Skrining AML Real-Time
09:00 - 10:30 | Slide 5: Spec-Driven Development (SDD) & Tata Kelola Kontrak
10:30 - 12:30 | Slide 6: Rekayasa Kualitas 3-Tingkat & Barrier JaCoCo (99.27%)
12:30 - 14:30 | Slide 7: Site Reliability Engineering (SRE), SLO, & Telemetri
14:30 - 16:30 | Slide 8: Deployment Rilis Blue-Green Zero-Downtime & Domain Preview
16:30 - 18:00 | Slide 9: Portabilitas Multi-Platform Cloud (GCP, AWS, Azure, OpenShift)
18:00 - 20:00 | Slide 10: Demonstrasi Produksi Langsung, Rangkuman, & Tanya Jawab
```

---

## 3. Rincian Skrip Presenter, Poin Penting, & Antisipasi Tanya Jawab

### Slide 0: Pengantar Eksekutif
* **Visual:** Latar belakang navy gelap, lencana hijau "ARSITEKTUR CORE BANKING ENTERPRISE", judul tegas, badge teknologi, dan tautan URL produksi live.
* **Waktu:** 1.5 menit.
* **Skrip Presenter:**
  > *"Selamat pagi/siang bapak, ibu, dan rekan-rekan sekalian. Hari ini saya mempresentasikan IndiBank Core Transaction and Ledger Engine. Sistem ini merupakan platform transaksi perbankan inti dan buku besar umum (general ledger) terdistribusi yang dirancang dari prinsip dasar untuk kebutuhan perbankan digital kritis berkecepatan tinggi, seperti BI-FAST, kliring antarbank instan, dan transfer intrabank. Sistem ini mengintegrasikan Java 21 dengan Virtual Threads, Apache Kafka mode KRaft, Redis 7 sebagai penjaga konkurensi terdistribusi, dan Oracle Database 23c sebagai system of record pembukuan berpasangan ACID, yang aktif berjalan secara langsung di Google Kubernetes Engine dengan pipeline rilis Blue-Green tanpa downtime."*
* **Poin Penting:**
  - Ruang lingkup perbankan skala besar (BI-FAST / RTGS / Buku Besar Inti).
  - Integrasi nyata: Java 21, Kafka, Redis, Oracle DB 23c, Kubernetes.
  - Sudah aktif berjalan di domain produksi publik.

---

### Slide 1: Dilema Core Banking: Real-Time vs Konsistensi ACID
* **Visual:** 3 kartu risiko: Pengulangan Jaringan (Network Retry), Race Condition Konkurensi, dan Drift Saldo Buku Besar.
* **Waktu:** 2.0 menit.
* **Skrip Presenter:**
  > *"Di dunia perbankan enterprise, ketersediaan sistem tidak boleh mengorbankan integritas data. Pada aplikasi e-commerce, pengulangan request mungkin hanya menambah pesanan ganda yang bisa dibatalkan secara manual. Namun di core banking, pendebetan ganda sebesar Rp 50.000.000 adalah pelanggaran regulasi fatal dan kerugian finansial langsung. Kami memetakan 3 tantangan eksistensial: Pertama, putusnya sinyal seluler nasabah yang memicu pengulangan transfer agresif. Kedua, transaksi paralel simultan pada satu rekening yang memicu race condition saldo minus. Dan ketiga, manipulasi saldo langsung yang menghilangkan jejak audit keuangan. Filosofi arsitektur kami jelas: Konsistensi > Latensi > Throughput. Kami tidak pernah mengorbankan invariansi saldo."*
* **Antisipasi Tanya Jawab:**
  - **T:** *Bagaimana sistem menangani network timeout saat transfer?*
  - **J:** *Transaksi selesai dengan aman di database dan resi di-cache di Redis dengan TTL 24 jam. Ketika nasabah retry dengan Idempotency-Key yang sama, resi asli langsung dikembalikan tanpa pemotongan saldo ulang.*

---

### Slide 2: Arsitektur Multi-Tier Enterprise & Alur Data (C4 Container)
* **Visual:** 4 kolom arsitektur: Ingress & Mesin Utama, Konkurensi & Cache, System of Record, dan Streaming & Operasional.
* **Waktu:** 2.0 menit.
* **Skrip Presenter:**
  > *"Mari kita telusuri blueprint arsitektur multi-tier ini. Pada lapisan terluar, Caddy menangani TLS dan membagi lalu lintas secara cerdas antara domain produksi dan domain preview pengujian. Mesin inti dibangun dengan Java 21 dan Spring Boot 3.3, memanfaatkan Virtual Threads sehingga thread transaksi dapat menunggu operasi I/O tanpa menghabiskan platform threads sistem operasi. Di depan database, Redis 7 bertindak sebagai perisai konkurensi defensif. Redis memeriksa Idempotency-Key dan mengamankan lock terdistribusi pada rekening pengirim. Oracle Database 23c adalah sumber kebenaran tunggal (System of Record). Setiap transfer dieksekusi dalam batasan ACID yang mencatat jurnal ganda yang tidak dapat diubah (immutable). Terakhir, Apache Kafka dalam mode KRaft menangani streaming event secara asinkron, termasuk pemindaian AML fraud secara langsung untuk transaksi di atas 100 juta Rupiah."*
* **Antisipasi Tanya Jawab:**
  - **T:** *Mengapa memilih Oracle 23c dibanding PostgreSQL?*
  - **J:** *Oracle adalah standar de facto perbankan tier-1 global karena keandalan mesin transaksi ACID, auditabilitas tinggi, check constraint ketat, dan dukungan enterprise.*

---

### Slide 3: Defensive Concurrency & Jaminan Buku Besar Zero-Loss
* **Visual:** Grid 2x2: State Machine Idempotensi Redis, Mutex Terdistribusi & Rilis Atomik Lua, Pembukuan Berpasangan Ketat, dan Constraint Database.
* **Waktu:** 2.0 menit.
* **Skrip Presenter:**
  > *"Di slide ini kita melihat implementasi teknis dari jaminan konsistensi kami. Pertama, state machine idempotensi Redis: saat request transfer masuk, kami mengeksekusi SETNX atomik. Jika ada request duplikat saat transaksi pertama masih berjalan, request tersebut langsung direspon 409 Conflict. Setelah transaksi settled, kami menyimpan respon 201 selama 24 jam. Saat aplikasi mobile nasabah retry karena sinyal drop, nasabah menerima resi resmi yang sama tanpa pemotongan saldo sepeser pun. Kedua, penguncian terdistribusi: kami mengunci rekening pengirim dengan token berdurasi 10 detik dan merilisnya menggunakan script Lua atomik yang memverifikasi kepemilikan token. Ketiga, mesin double-entry kami: saldo tidak pernah diubah secara sepihak. Setiap transfer menghasilkan baris DEBIT dan KREDIT seimbang. Dan terakhir, Oracle menerapkan CHECK constraint level database bahwa saldo harus >= 0, didukung optimistic locking @Version."*
* **Antisipasi Tanya Jawab:**
  - **T:** *Mengapa script Lua diperlukan untuk melepaskan distributed lock?*
  - **J:** *Jika transaksi mengalami jeda jaringan melebihi TTL 10 detik, Redis akan menghapus lock secara otomatis dan transaksi lain mengambilnya. Tanpa script Lua yang memverifikasi kecocokan token sebelum menghapus, proses A akan secara tidak sengaja menghapus lock milik proses B, memicu potensi double-spending.*

---

### Slide 4: Apache Kafka KRaft: Asynchronous Decoupling & AML Real-Time
* **Visual:** 2 kartu: Arsitektur Event Kafka KRaft dan Mesin Kepatuhan AML Real-Time.
* **Waktu:** 1.5 menit.
* **Skrip Presenter:**
  > *"Sekarang mari kita lihat lapisan event streaming kami. Kami menggunakan Apache Kafka dalam mode KRaft, yang meniadakan ketergantungan pada Zookeeper. Ketika transfer antarbank committed di Oracle, event langsung dipublikasikan ke topic `bank.transfers.settled`. Berjalan secara paralel, modul Anti-Money Laundering (AML) kami melakukan pemindaian real-time. Setiap transfer dengan nilai sama dengan atau melebihi 100 juta Rupiah secara otomatis memicu event peringatan ke `bank.fraud.alerts` dengan status CRITICAL. Penting untuk dicatat bahwa pemrosesan kepatuhan ini terpisah secara asinkron dari API HTTP. Nasabah menerima resi 201 dalam waktu di bawah 150 milidetik. Kami juga mengekspos ticker stream memori di `/api/v1/events/recent` yang divisualisasikan langsung pada dashboard kami."*
* **Antisipasi Tanya Jawab:**
  - **T:** *Bagaimana mencegah hilangnya event jika Kafka broker down saat transaksi database commit?*
  - **J:** *Kami menerapkan pola Transactional Outbox: event disimpan di tabel OUTBOX_EVENTS dalam transaksi database ACID yang sama. Pekerja outbox menjamin pengiriman at-least-once ke Kafka saat broker kembali online.*

---

### Slide 5: Spec-Driven Development (SDD) & Tata Kelola Kontrak
* **Visual:** 3 kartu: Kontrak REST & Asinkron, Spesifikasi Database & Cache, dan Standarisasi Error RFC 7807.
* **Waktu:** 1.5 menit.
* **Skrip Presenter:**
  > *"Metodologi pengembangan kami berpegang teguh pada Spec-Driven Development (SDD). Sebelum menulis baris kode Java pertama, kami merumuskan spesifikasi secara formal: Pertama, spesifikasi OpenAPI 3.1 untuk semua endpoint REST yang secara otomatis menghasilkan dokumentasi Swagger interaktif. Kedua, spesifikasi AsyncAPI 3.0 untuk event Kafka. Ketiga, DDL Oracle 23c dengan integritas relasional penuh dan data benih. Dan keempat, spesifikasi konkurensi Redis yang menetapkan konvensi penamaan kunci, masa TTL, dan script Lua. Selain itu, semua respon error mengikuti format standar RFC 7807 Problem Details, memudahkan integrasi sistem pihak ketiga."*

---

### Slide 6: Piramida Pengujian 3-Tingkat & Barrier Cakupan JaCoCo
* **Visual:** 3 kartu tingkat pengujian dan banner hijau hasil cakupan terverifikasi 99.27%.
* **Waktu:** 2.0 menit.
* **Skrip Presenter:**
  > *"Beralih ke aspek rekayasa kualitas. Kami menerapkan piramida pengujian 3 tingkat yang sangat disiplin: Pada Tingkat 1, unit test mengisolasi logika bisnis domain, menguji akuisisi lock, transisi idempotensi, dan berbagai kasus batas. Pada Tingkat 2, pengujian integrasi WebMvc menggunakan MockMvc untuk memastikan keandalan validasi Bean Validation, header HTTP, dan kode status RFC 7807. Pada Tingkat 3, skrip otomatisasi bash `test-scenarios.sh` mengeksekusi 7 skenario perbankan nyata terhadap cluster GKE aktif. Yang paling penting, pipeline CI/CD kami menerapkan barrier cakupan JaCoCo minimal 95%: pull request dengan cakupan di bawah 95% akan langsung ditolak otomatis. Hasil pengujian kami saat ini mencapai 99.27% Line Coverage dan 99.04% Instruction Coverage dengan 70 tes yang semuanya berstatus lulus."*

---

### Slide 7: Framework SRE Produksi, SLO, & Telemetri Real-Time
* **Visual:** 3 kartu: SLO & Error Budget, Empat Sinyal Emas, dan Alerting & Autoscaling.
* **Waktu:** 2.0 menit.
* **Skrip Presenter:**
  > *"Mari kita tinjau aspek Site Reliability Engineering (SRE). Pada core banking, SRE bertujuan memastikan prediktabilitas dan pembatasan dampak kegagalan (blast radius). Kami menetapkan SLO yang ketat: ketersediaan 99.99% dengan batas error budget 4.3 menit per bulan. Target latensi adalah sub-150ms untuk p95 dan sub-500ms untuk p99. Dan invariansi saldo buku besar memiliki toleransi nol: jika ada drift sepeser pun, sistem akan menghentikan transaksi secara aman. Kami memantau Empat Sinyal Emas via metrik Prometheus di `/actuator/prometheus`. Sangat penting: kami membedakan error 4xx validasi bisnis nasabah, seperti saldo kurang, dari error 5xx server, sehingga kesalahan input nasabah tidak menghanguskan error budget ketersediaan sistem. Kami juga memasang Kubernetes Horizontal Pod Autoscaler (HPA) untuk autoscaling 1 sampai 5 pod, serta menyusun runbook SOP penanganan insiden."*

---

### Slide 8: Deployment Blue-Green Zero-Downtime & Domain Preview
* **Visual:** 3 kartu: Proteksi Branch Utama, Domain Preview Ephemeral, dan Blue-Green Produksi.
* **Waktu:** 2.0 menit.
* **Skrip Presenter:**
  > *"Pipeline rilis kami menjamin zero-downtime dan pengendalian radius dampak (blast radius) secara aman. Pertama, push langsung ke branch `main` diblokir total melalui GitHub Branch Protection dengan penegakan level admin. Setiap perubahan wajib melalui branch fitur dan PR. Kedua, setiap kali branch fitur di-push, pipeline CI/CD kami mendeploy kontainer preview ke `https://test.indibank.aldianapps.com`. Hal ini memungkinkan developer dan stakeholder memverifikasi fungsionalitas secara langsung di domain aktif sebelum digabungkan. Ketiga, ketika PR di-merge ke `main`, pipeline Blue-Green kami secara otomatis mendeploy image baru ke slot standby (misal green), menunggu pod siap sempurna, dan mem-patch selector Service Kubernetes secara atomik. Pengalihan trafik terjadi secara instan tanpa ada request yang terputus. Jika terdeteksi masalah, kami dapat melakukan rollback dalam waktu kurang dari satu detik."*

---

### Slide 9: Portabilitas Lintas GCP, AWS, Azure, OpenShift, & Lokal
* **Visual:** 2 kartu: Matriks Portabilitas Cloud & On-Premise dan Helm Chart Produksi & Pengerasan Kontainer.
* **Waktu:** 1.5 menit.
* **Skrip Presenter:**
  > *"Meskipun demonstrasi live kami berjalan di Google Kubernetes Engine region Jakarta, seluruh platform ini dirancang dengan portabilitas multi-cloud dan on-premise. Banyak institusi perbankan yang mengoperasikan arsitektur hybrid atau menggunakan AWS, Azure, maupun on-premise Red Hat OpenShift. Kami telah menyusun Helm chart produksi di `helm/indibank/` yang memungkinkan deployment ke cluster Kubernetes standar mana pun, termasuk Minikube lokal untuk pengembangan offline. Arsitektur deployment ini dijelaskan secara mendalam di `docs/deployment/MULTI_PLATFORM.md`. Selain itu, kontainer kami mematuhi standar keamanan enterprise: berjalan sebagai user non-root dan memiliki kuota resource CPU serta memori yang terkelola."*

---

### Slide 10: Verifikasi Produksi Langsung & Rangkuman Eksekutif
* **Visual:** 3 kartu: Endpoint Produksi Aktif, Hasil Verifikasi (7/7 Lulus), dan Rangkuman Eksekutif.
* **Waktu:** 2.0 menit.
* **Skrip Presenter:**
  > *"Sebagai penutup, IndiBank Core Engine bukan sekadar prototipe di atas kertas—ini adalah sistem transaksi perbankan inti aktif yang sedang berjalan di Google Cloud saat ini. Bapak dan ibu dapat membuka `https://indibank.aldianapps.com` melalui browser laptop atau ponsel untuk mengeksekusi transfer antarbank langsung, memeriksa buku besar umum, dan melihat ticker event Kafka bergerak secara real-time. Rangkaian pengujian otomatis kami telah memvalidasi seluruh 7 skenario perbankan inti terhadap lingkungan produksi aktif, dan semuanya berhasil lulus dengan sempurna. Sebagai rangkuman apa yang telah kita bangun: Pertama, konsistensi finansial absolut berbasis akuntansi berpasangan di Oracle 23c. Kedua, konkurensi defensif dengan idempotensi Redis dan distributed locking yang mencegah pendebetan ganda. Ketiga, streaming event throughput tinggi dengan Kafka KRaft. Dan keempat, operasi rilis Blue-Green zero-downtime dengan barrier pengujian 95% dan observabilitas SRE lengkap. Terima kasih banyak atas waktu dan perhatiannya, dan saya siap menjawab pertanyaan teknis dari bapak/ibu sekalian."*

---

## 4. Perintah Verifikasi Cepat

```bash
# Jalankan pengujian 7 skenario live terhadap server produksi
./test-scenarios.sh https://indibank.aldianapps.com

# Periksa telemetri Prometheus secara langsung
curl -s https://indibank.aldianapps.com/actuator/prometheus | grep http_server_requests_seconds_count
```
