#!/usr/bin/env python3
"""
IndiBank Core Transaction & Ledger Engine - Slide Deck Generator (Bilingual: EN & ID)
Generates widescreen (16:9) executive presentations (.pptx)
in both English and Bahasa Indonesia with dark enterprise banking styling,
structured layouts, and comprehensive speaker notes.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==========================================
# DESIGN CONSTANTS (Enterprise Dark Banking)
# ==========================================
BG_COLOR = RGBColor(11, 19, 41)       # #0B1329 Deep Navy Slate
CARD_BG = RGBColor(26, 38, 57)        # #1A2639 Slate Card
CARD_BORDER = RGBColor(46, 64, 87)    # #2E4057 Card Border
TEXT_MAIN = RGBColor(248, 250, 252)   # #F8FAFC Crisp White
TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8 Slate Gray
TEXT_DIM = RGBColor(100, 116, 139)    # #64748B Dim Gray
ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981 Emerald Green
ACCENT_BLUE = RGBColor(14, 165, 233)  # #0EA5E9 Sky Blue
ACCENT_AMBER = RGBColor(245, 158, 11) # #F59E0B Amber
ACCENT_PURPLE = RGBColor(139, 92, 246)# #8B5CF6 Purple

FONT_HEADING = "Calibri"
FONT_BODY = "Calibri"

def apply_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, category, title):
    apply_background(slide)
    
    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.name = FONT_HEADING
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = ACCENT_GREEN
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_MAIN

def add_card(slide, left, top, width, height, title, items, accent=ACCENT_BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = CARD_BORDER
    shape.line.width = Pt(1)
    
    header_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.45))
    tf_h = header_box.text_frame
    tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]
    p_h.text = title
    p_h.font.name = FONT_HEADING
    p_h.font.size = Pt(14)
    p_h.font.bold = True
    p_h.font.color.rgb = accent
    
    body_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.6), width - Inches(0.4), height - Inches(0.75))
    tf_b = body_box.text_frame
    tf_b.word_wrap = True
    
    for i, item in enumerate(items):
        p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
        p.space_after = Pt(6)
        
        if isinstance(item, tuple):
            label, desc = item
            run_lbl = p.add_run()
            run_lbl.text = "• " + label + ": "
            run_lbl.font.name = FONT_BODY
            run_lbl.font.size = Pt(11)
            run_lbl.font.bold = True
            run_lbl.font.color.rgb = TEXT_MAIN
            
            run_desc = p.add_run()
            run_desc.text = desc
            run_desc.font.name = FONT_BODY
            run_desc.font.size = Pt(11)
            run_desc.font.color.rgb = TEXT_MUTED
        else:
            run = p.add_run()
            run.text = "• " + str(item)
            run.font.name = FONT_BODY
            run.font.size = Pt(11)
            run.font.color.rgb = TEXT_MUTED

def set_speaker_notes(slide, timing, script, key_points, anticipated_qa, lang="en"):
    notes_tf = slide.notes_slide.notes_text_frame
    if lang == "id":
        notes_tf.text = f"⏱ ESTIMASI WAKTU: {timing}\n\n"
        notes_tf.text += f"🎙 SKRIP PRESENTASI:\n{script}\n\n"
        notes_tf.text += "📌 POIN UTAMA UNTUK DITEKANKAN:\n"
        for kp in key_points:
            notes_tf.text += f"- {kp}\n"
        notes_tf.text += "\n💡 ANTISIPASI PERTANYAAN TEKNIS & JAWABAN:\n"
        for q, a in anticipated_qa:
            notes_tf.text += f"T: {q}\nJ: {a}\n\n"
    else:
        notes_tf.text = f"⏱ ESTIMATED TIMING: {timing}\n\n"
        notes_tf.text += f"🎙 TALKING SCRIPT:\n{script}\n\n"
        notes_tf.text += "📌 KEY HIGHLIGHTS TO EMPHASIZE:\n"
        for kp in key_points:
            notes_tf.text += f"- {kp}\n"
        notes_tf.text += "\n💡 ANTICIPATED TECHNICAL Q&A:\n"
        for q, a in anticipated_qa:
            notes_tf.text += f"Q: {q}\nA: {a}\n\n"

# ==========================================
# PRESENTATION BUILDER FUNCTION
# ==========================================
def build_deck(lang="en", output_path=None):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    is_id = (lang == "id")
    
    # -------------------------------------------------------------
    # SLIDE 0: TITLE SLIDE
    # -------------------------------------------------------------
    s0 = prs.slides.add_slide(blank_layout)
    apply_background(s0)
    
    t_box = s0.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(0.5))
    tf = t_box.text_frame
    p = tf.paragraphs[0]
    p.text = "ARSITEKTUR CORE BANKING ENTERPRISE" if is_id else "ENTERPRISE CORE BANKING ARCHITECTURE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    
    t_box2 = s0.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.5))
    tf2 = t_box2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "IndiBank Core Transaction & Ledger Engine"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(38)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN
    
    p2_sub = tf2.add_paragraph()
    p2_sub.text = (
        "Arsitektur Produksi, Defensive Concurrency, & Integritas Finansial Zero-Loss"
        if is_id else
        "Production Architecture, Defensive Concurrency, & Zero-Loss Financial Integrity"
    )
    p2_sub.font.name = FONT_HEADING
    p2_sub.font.size = Pt(18)
    p2_sub.font.color.rgb = ACCENT_BLUE
    p2_sub.space_before = Pt(8)
    
    banner = s0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.333), Inches(1.4))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = CARD_BORDER
    
    b_tf = banner.text_frame
    b_tf.word_wrap = True
    bp1 = b_tf.paragraphs[0]
    bp1.text = "TEKNOLOGI & PLATFORM CLOUD PRODUKSI" if is_id else "TECHNOLOGY STACK & CLOUD PLATFORM"
    bp1.font.name = FONT_HEADING
    bp1.font.size = Pt(11)
    bp1.font.bold = True
    bp1.font.color.rgb = ACCENT_AMBER
    
    bp2 = b_tf.add_paragraph()
    bp2.text = "Java 21 (Virtual Threads) • Spring Boot 3.3 • Apache Kafka 3.7 (KRaft) • Redis 7 • Oracle DB 23c • GKE • Terraform"
    bp2.font.name = FONT_BODY
    bp2.font.size = Pt(13)
    bp2.font.bold = True
    bp2.font.color.rgb = TEXT_MAIN
    bp2.space_before = Pt(4)
    
    bp3 = b_tf.add_paragraph()
    bp3.text = "Live URLs: https://indibank.aldianapps.com • https://test.indibank.aldianapps.com"
    bp3.font.name = FONT_BODY
    bp3.font.size = Pt(11)
    bp3.font.color.rgb = ACCENT_GREEN
    bp3.space_before = Pt(4)
    
    auth_box = s0.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.3), Inches(1.0))
    a_tf = auth_box.text_frame
    ap1 = a_tf.paragraphs[0]
    ap1.text = "Presenter: Aldian Fazrihady"
    ap1.font.name = FONT_HEADING
    ap1.font.size = Pt(14)
    ap1.font.bold = True
    ap1.font.color.rgb = TEXT_MAIN
    
    ap2 = a_tf.add_paragraph()
    ap2.text = (
        "Lead Platform & Distributed Systems Engineer | Spec-Driven Development Showcase"
        if is_id else
        "Lead Platform & Distributed Systems Engineer | Spec-Driven Development Showcase"
    )
    ap2.font.name = FONT_BODY
    ap2.font.size = Pt(12)
    ap2.font.color.rgb = TEXT_MUTED
    
    if is_id:
        set_speaker_notes(
            s0, "1.5 menit",
            "Selamat pagi/siang rekan-rekan dan bapak/ibu sekalian. Hari ini saya mempresentasikan IndiBank Core Transaction and Ledger Engine. "
            "Sistem ini merupakan platform transaksi core banking dan buku besar umum (general ledger) terdistribusi yang dirancang dari prinsip dasar "
            "untuk perbankan digital kritis berkecepatan tinggi, seperti BI-FAST, kliring transfer antarbank instan, dan transfer intrabank. "
            "Sistem ini mengintegrasikan Java 21 dengan Virtual Threads (Project Loom), Apache Kafka mode KRaft, Redis 7 sebagai penjaga konkurensi terdistribusi, "
            "dan Oracle Database 23c sebagai system of record pembukuan berpasangan ACID, yang dideploy secara langsung di Google Kubernetes Engine (GKE) dengan pipeline Blue-Green zero-downtime.",
            [
                "Fokus core banking enterprise (BI-FAST / RTGS / Buku Besar Inti)",
                "Integrasi komprehensif Java 21, Kafka, Redis, dan Oracle DB 23c",
                "Aktif secara live di cloud publik dengan portabilitas multi-cloud"
            ],
            [
                ("Mengapa Anda membangun sistem ini?", "Untuk mendemonstrasikan bagaimana arsitektur terdistribusi modern menyelesaikan masalah klasik perbankan seperti pendebetan ganda, pengulangan jaringan, dan inkonsistensi saldo tanpa mengorbankan latensi sub-150ms.")
            ],
            lang="id"
        )
    else:
        set_speaker_notes(
            s0, "1.5 minutes",
            "Good morning/afternoon everyone. Today I am presenting the IndiBank Core Transaction and Ledger Engine. "
            "This system represents an enterprise-grade core banking transaction and immutable general ledger platform designed from "
            "first principles for mission-critical digital banking, such as BI-FAST, instant interbank clearing, and intra-bank transfers. "
            "It integrates Java 21 with virtual threads, Apache Kafka in KRaft mode, Redis 7 for distributed concurrency guarding, "
            "and Oracle Database 23c as the ACID double-entry system of record, deployed live on Google Kubernetes Engine with zero-downtime Blue-Green pipelines.",
            [
                "Enterprise banking focus (BI-FAST / RTGS / Core Ledger)",
                "Strict integration of Java 21, Kafka, Redis, and Oracle DB 23c",
                "Deployed live to public production with multi-cloud portability"
            ],
            [
                ("Why did you build this system?", "To demonstrate how modern distributed architecture patterns solve the classic core banking challenges of double-spending, network retries, and ledger drift while maintaining sub-150ms settlement latency.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 1: BUSINESS CONTEXT & CHALLENGES
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s1, "Masalah Bisnis & Kebutuhan Sistem", "Dilema Core Banking: Real-Time vs Konsistensi ACID")
        add_card(s1, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. Retry Jaringan & Replay Request", [
            ("Risiko", "Koneksi seluler yang tidak stabil membuat aplikasi mobile nasabah mengirim pengulangan transfer berkali-kali."),
            ("Malapetaka", "Tanpa idempotensi deterministik, pengulangan request memicu pendebetan saldo ganda (double debit)."),
            ("Solusi IndiBank", "Redis SETNX dengan cache resi 24 jam mengembalikan bukti transaksi asli secara instan tanpa mendebet ulang.")
        ], ACCENT_BLUE)
        add_card(s1, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. Konkurensi & Race Conditions", [
            ("Risiko", "Transaksi bersamaan menyasar rekening sumber yang sama (misal: penggajian massal/payroll atau auto-debet)."),
            ("Malapetaka", "Kondisi balapan read-modify-write menyebabkan overdraft dan saldo nasabah menjadi negatif."),
            ("Solusi IndiBank", "Mutex terdistribusi dengan auto-expiry 10 detik dan rilis atomik Lua menjamin eksekusi satu arah (single-flight).")
        ], ACCENT_AMBER)
        add_card(s1, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. Drift Buku Besar & Auditabilitas", [
            ("Risiko", "Pembaruan saldo langsung di tempat (in-place update) menghilangkan jejak audit historis."),
            ("Malapetaka", "Uang berpindah tanpa adanya ayat jurnal penyeimbang, menyebabkan pelanggaran regulasi BI/OJK."),
            ("Solusi IndiBank", "Pembukuan Berpasangan (Double-Entry) ketat di Oracle 23c memastikan total debit selalu setara total kredit.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s1, "2 menit",
            "Di industri perbankan enterprise, ketersediaan sistem tidak boleh mengorbankan integritas data. Pada aplikasi e-commerce, pengulangan request mungkin hanya menambah pesanan ganda yang bisa dibatalkan. "
            "Namun di core banking, pendebetan ganda sebesar Rp 50.000.000 adalah pelanggaran regulasi fatal dan kerugian finansial langsung. "
            "Kami memetakan 3 tantangan eksistensial: Pertama, putusnya sinyal seluler nasabah yang memicu pengulangan transfer agresif. "
            "Kedua, transaksi paralel simultan pada satu rekening yang memicu race condition saldo minus. "
            "Dan ketiga, manipulasi saldo langsung yang menghilangkan jejak audit keuangan. "
            "Filosofi arsitektur kami jelas: Konsistensi > Latensi > Throughput. Kami tidak pernah mengorbankan invariansi saldo.",
            [
                "Perbedaan krusial antara konsistensi e-commerce vs core banking",
                "Toleransi nol (zero tolerance) untuk pendebetan ganda dan saldo negatif",
                "Kewajiban regulasi pembukuan berpasangan (double-entry bookkeeping)"
            ],
            [
                ("Bagaimana sistem menangani network timeout saat transfer?", "Transaksi selesai dengan aman di database dan resi di-cache di Redis. Ketika nasabah retry dengan Idempotency-Key yang sama, resi asli langsung dikembalikan tanpa pemotongan saldo ulang.")
            ],
            lang="id"
        )
    else:
        add_header(s1, "Business Problem & Requirements", "The Core Banking Conundrum: Real-Time vs ACID Consistency")
        add_card(s1, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. Network Retries & Replays", [
            ("The Risk", "Unreliable mobile data networks cause clients to retry transfers multiple times."),
            ("The Catastrophe", "Without deterministic idempotency, retries cause duplicate debit deductions."),
            ("IndiBank Solution", "Redis SETNX 24-hour cached receipt returns identical payload on replays without re-debiting.")
        ], ACCENT_BLUE)
        add_card(s1, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. Concurrency & Race Conditions", [
            ("The Risk", "Concurrent API requests targeting the same sender (e.g. automated payroll or debit sweep)."),
            ("The Catastrophe", "Read-modify-write race conditions lead to overdraft and negative balances."),
            ("IndiBank Solution", "Distributed mutex with 10s auto-expiry and atomic Lua verification guarantees single-flight execution.")
        ], ACCENT_AMBER)
        add_card(s1, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. Ledger Drift & Auditability", [
            ("The Risk", "In-place balance updates lose historical context and violate financial audit regulations."),
            ("The Catastrophe", "Money vanishes or appears without a balancing journal line, failing bank audit."),
            ("IndiBank Solution", "Strict Double-Entry Bookkeeping in Oracle 23c ensures total debits always equal total credits.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s1, "2 minutes",
            "In enterprise banking, availability cannot come at the expense of data integrity. In an e-commerce cart, an occasional retry might add a duplicate item. "
            "In core banking, a duplicate debit of Rp 50,000,000 is an immediate regulatory breach and financial loss. "
            "We identified three existential challenges: First, mobile network drops causing aggressive user retries. "
            "Second, concurrent payment requests draining the same account simultaneously, risking double spending. "
            "Third, ledger drift where balances are modified in-place without immutable audit trails. "
            "Our design enforces the core banking invariant: Consistency > Latency > Throughput. We never compromise balance invariance.",
            [
                "Highlight the difference between general e-commerce and banking consistency",
                "Zero tolerance for duplicate deductions or negative balances",
                "Explain the non-negotiable nature of double-entry bookkeeping"
            ],
            [
                ("How do you handle network timeouts where the client disconnects before receiving the response?", 
                 "The transaction completes safely in the database and caches its receipt in Redis. When the client retries with the same Idempotency-Key, they receive the exact cached settled receipt instantaneously.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 2: ARCHITECTURE BLUEPRINT
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s2, "Arsitektur Sistem & Tinjauan C4", "Arsitektur Multi-Tier Enterprise & Alur Data")
        add_card(s2, Inches(0.8), Inches(1.6), Inches(2.8), Inches(5.2), "Ingress & Mesin Utama", [
            ("Caddy Ingress", "Routing TLS multi-domain, sertifikat otomatis Let's Encrypt, terminasi SSL di edge."),
            ("Java 21 LTS", "Virtual Threads (Project Loom) menangani konkurensi tinggi tanpa kehabisan OS thread."),
            ("Spring Boot 3.3", "Arsitektur Heksagonal, Spring Data JPA, Spring Kafka, Spring Data Redis."),
            ("OpenAPI / Swagger", "Dokumentasi interaktif live di /swagger-ui.html.")
        ], ACCENT_BLUE)
        add_card(s2, Inches(3.8), Inches(1.6), Inches(2.8), Inches(5.2), "Konkurensi & Cache", [
            ("Redis 7 Store", "Penyimpanan in-memory performa tinggi di depan database relasional."),
            ("Mesin Idempotensi", "State machine SETNX dengan penyimpanan respon 24 jam."),
            ("Distributed Lock", "Mutex tingkat rekening dengan auto-expiry 10 detik."),
            ("Fast Balance Cache", "Pembacaan saldo sub-milidetik dengan pembatalan cache otomatis.")
        ], ACCENT_AMBER)
        add_card(s2, Inches(6.8), Inches(1.6), Inches(2.8), Inches(5.2), "System of Record", [
            ("Oracle DB 23c", "Buku besar transaksi finansial ACID dan status rekening master."),
            ("Double-Entry Book", "Jurnal baris berpasangan: DEBIT rekening sumber, KREDIT rekening tujuan."),
            ("Pengecekan Integritas", "CHECK (balance >= 0) dan optimistic locking (@Version)."),
            ("Tabel Outbox", "Transactional outbox menjamin publikasi event Kafka tanpa kehilangan data.")
        ], ACCENT_GREEN)
        add_card(s2, Inches(9.8), Inches(1.6), Inches(2.8), Inches(5.2), "Streaming & Operasional", [
            ("Apache Kafka KRaft", "Streaming event throughput tinggi terpisah dari thread pool HTTP."),
            ("Mesin Fraud AML", "Skrining kepemilikan real-time mendeteksi transaksi >= Rp 100 Juta."),
            ("Dead-Letter Queue", "Isolasi event gagal ke bank.transfers.dlq dengan kebijakan retry."),
            ("Telemetri Prometheus", "Empat Sinyal Emas diekspos secara live di /actuator/prometheus.")
        ], ACCENT_PURPLE)
        set_speaker_notes(
            s2, "2 menit",
            "Mari kita telusuri blueprint arsitektur multi-tier ini. Pada lapisan terluar, Caddy menangani TLS dan membagi lalu lintas secara cerdas antara domain produksi dan domain preview pengujian. "
            "Mesin inti dibangun dengan Java 21 dan Spring Boot 3.3, memanfaatkan Virtual Threads sehingga thread transaksi dapat menunggu operasi I/O tanpa menghabiskan platform threads sistem operasi. "
            "Di depan database, Redis 7 bertindak sebagai perisai konkurensi defensif. Redis memeriksa Idempotency-Key dan mengamankan lock terdistribusi pada rekening pengirim. "
            "Oracle Database 23c adalah sumber kebenaran tunggal (System of Record). Setiap transfer dieksekusi dalam batasan ACID yang mencatat jurnal ganda yang tidak dapat diubah (immutable). "
            "Terakhir, Apache Kafka dalam mode KRaft menangani streaming event secara asinkron, termasuk pemindaian AML fraud secara langsung untuk transaksi di atas 100 juta Rupiah.",
            [
                "Pemisahan tanggung jawab (separation of concerns) yang bersih pada 4 lapisan",
                "Virtual threads menghilangkan bottleneck thread pool pada operasi I/O",
                "Kafka memisahkan proses kepatuhan berat dari jalur penyelesaian transaksi (settlement)"
            ],
            [
                ("Mengapa memilih Oracle 23c dibanding PostgreSQL?", "Oracle adalah standar de facto perbankan tier-1 global karena keandalan mesin transaksi ACID, auditabilitas tinggi, check constraint ketat, dan dukungan enterprise.")
            ],
            lang="id"
        )
    else:
        add_header(s2, "System Architecture & C4 View", "Enterprise Multi-Tier Architecture & Data Flow")
        add_card(s2, Inches(0.8), Inches(1.6), Inches(2.8), Inches(5.2), "Ingress & Engine", [
            ("Caddy Ingress", "Multi-domain TLS routing, rate limiting, and SSL termination at the edge."),
            ("Java 21 LTS", "High-throughput execution with Virtual Threads (Project Loom) handling high concurrency."),
            ("Spring Boot 3.3", "Clean Hexagonal architecture, Spring Data JPA, Spring Kafka, Spring Data Redis."),
            ("OpenAPI / Swagger", "Interactive documentation exposed live at /swagger-ui.html.")
        ], ACCENT_BLUE)
        add_card(s2, Inches(3.8), Inches(1.6), Inches(2.8), Inches(5.2), "Concurrency & Cache", [
            ("Redis 7 Store", "In-memory guard operating ahead of the relational database."),
            ("Idempotency Engine", "SETNX state machine with 24-hour cached responses."),
            ("Distributed Lock", "Account-level mutex with 10s auto-expiry TTL."),
            ("Fast Balance Cache", "Sub-millisecond balance reads with automated write-invalidation.")
        ], ACCENT_AMBER)
        add_card(s2, Inches(6.8), Inches(1.6), Inches(2.8), Inches(5.2), "System of Record", [
            ("Oracle DB 23c", "ACID financial transaction ledger and master account state."),
            ("Double-Entry Book", "Immutable journal lines: DEBIT source, CREDIT destination."),
            ("Integrity Checks", "CHECK (balance >= 0) and optimistic locking (@Version)."),
            ("Outbox Table", "Transactional outbox for guaranteed event dispatch.")
        ], ACCENT_GREEN)
        add_card(s2, Inches(9.8), Inches(1.6), Inches(2.8), Inches(5.2), "Streaming & Ops", [
            ("Apache Kafka KRaft", "High-throughput event streaming decoupled from HTTP thread pool."),
            ("AML Fraud Engine", "Automated compliance screening flagging transactions >= Rp 100M."),
            ("Dead-Letter Queue", "Dead-lettering to bank.transfers.dlq with retry policies."),
            ("Prometheus Telemetry", "Four Golden Signals exposed live at /actuator/prometheus.")
        ], ACCENT_PURPLE)
        set_speaker_notes(
            s2, "2 minutes",
            "Let's examine the multi-tier architectural blueprint. At the edge, Caddy handles TLS and routes traffic between our production domain and test preview domain. "
            "The core engine is built on Java 21 and Spring Boot 3.3, leveraging Virtual Threads so that each transaction thread can block on I/O without exhausting OS platform threads. "
            "Ahead of our database, Redis 7 serves as our defensive concurrency guard. It verifies the client Idempotency-Key and acquires an account-level distributed lock. "
            "Oracle Database 23c acts as the single source of truth. Every transfer executes inside an ACID boundary that creates immutable double-entry journal records. "
            "Finally, Apache Kafka running in KRaft mode handles asynchronous event streaming, including real-time AML fraud detection for transactions over 100 million Rupiah, and dead-letter queues.",
            [
                "Clear separation of concerns across the 4 architectural layers",
                "Virtual threads eliminate thread starvation during database and Redis I/O",
                "Kafka decouples heavy notifications and compliance checks from the critical settlement path"
            ],
            [
                ("Why did you choose Oracle 23c instead of Postgres?", "Oracle is the industry standard in tier-1 banking institutions due to its battle-tested ACID engine, robust PL/SQL auditing, fine-grained check constraints, and enterprise backup/recovery tooling.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 3: DEFENSIVE CONCURRENCY
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s3, "Konsistensi Finansial & Keamanan", "Defensive Concurrency & Jaminan Buku Besar Zero-Loss")
        add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(2.5), "1. State Machine Idempotensi Redis", [
            ("Akuisisi Kunci Atomik", "SETNX indibank:idempotency:{key} IN_PROGRESS dengan masa kunci 60 detik."),
            ("Deduplikasi In-Flight", "Permintaan bersamaan dengan kunci sama langsung mendapat HTTP 409 Conflict."),
            ("Cache Resi 24 Jam", "Saat settlement berhasil, payload respon disimpan selama 86.400 detik (24 jam)."),
            ("Pelepasan Kunci Aman", "Jika validasi bisnis gagal, kunci dihapus agar nasabah bisa mengulang transfer.")
        ], ACCENT_BLUE)
        add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.5), "2. Mutex Terdistribusi & Rilis Atomik Lua", [
            ("Lock Rekening Sumber", "SET indibank:lock:account:{acc} {UUID} NX PX 10000 menjamin eksekusi satu arah."),
            ("Auto-Expiry TTL 10 Detik", "Mencegah terjadinya deadlock permanen jika kontainer crash di tengah jalan."),
            ("Script Lua Verifikasi Token", "Memverifikasi kepemilikan token sebelum menghapus kunci, mencegah pembajakan lock."),
            ("Manajemen Antrean Padat", "Jika lock tidak berhasil diperoleh dalam batas waktu, respon 409 Conflict dikembalikan.")
        ], ACCENT_AMBER)
        add_card(s3, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.6), "3. Pembukuan Berpasangan Ketat (Double-Entry)", [
            ("Keseimbangan Matematis", "Setiap transaksi menghasilkan pasangan baris jurnal DEBIT dan KREDIT yang setara."),
            ("Zero Ledger Drift", "Invariansi terjamin: |Debit - Kredit| == 0.00 IDR di seluruh transaksi tanpa pengecualian."),
            ("Buku Besar Append-Only", "Baris jurnal bersifat permanen; data historis tidak pernah diubah atau dihapus."),
            ("API Rekening Koran Audit", "Pemeriksaan mutasi historis riil secara real-time via /api/v1/accounts/{acc}/statement.")
        ], ACCENT_GREEN)
        add_card(s3, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.6), "4. Constraint Database & Optimistic Locking", [
            ("Saldo Non-Negatif", "Constraint fisik Oracle CHECK (BALANCE >= 0) memblokir terjadinya saldo minus."),
            ("Optimistic Locking", "Kolom @Version pada entitas rekening mencegah overwrite transaksi yang tumpang tindih."),
            ("Rollback Terisolasi", "Anotasi @Transactional mengembalikan saldo dan merilis kunci jika terjadi kegagalan."),
            ("Tabel Outbox Transaksional", "Menjamin konsistensi pengiriman event Kafka sejalan dengan commit database.")
        ], ACCENT_PURPLE)
        set_speaker_notes(
            s3, "2 menit",
            "Di slide ini kita melihat implementasi teknis dari jaminan konsistensi kami. "
            "Pertama, state machine idempotensi Redis: saat request transfer masuk, kami mengeksekusi SETNX atomik. Jika ada request duplikat saat transaksi pertama masih berjalan, request tersebut langsung direspon 409 Conflict. "
            "Setelah transaksi settled, kami menyimpan respon 201 selama 24 jam. Saat aplikasi mobile nasabah retry karena sinyal drop, nasabah menerima resi resmi yang sama tanpa pemotongan saldo sepeser pun. "
            "Kedua, penguncian terdistribusi: kami mengunci rekening pengirim dengan token berdurasi 10 detik dan merilisnya menggunakan script Lua atomik yang memverifikasi kepemilikan token. "
            "Ketiga, mesin double-entry kami: saldo tidak pernah diubah secara sepihak. Setiap transfer menghasilkan baris DEBIT dan KREDIT seimbang. "
            "Dan terakhir, Oracle menerapkan CHECK constraint level database bahwa saldo harus >= 0, didukung optimistic locking @Version.",
            [
                "Alasan krusial script Lua pada distributed lock (mencegah penghapusan lock milik proses lain)",
                "Jaminan zero mathematical drift dari prinsip akuntansi double-entry",
                "Pertahanan berlapis (defense-in-depth) dengan check constraint database"
            ],
            [
                ("Apa yang terjadi jika server Redis down di tengah transfer?", "Sistem memiliki jalur degradasi anggun (graceful degradation): jika Redis tidak dapat diakses, sistem langsung beralih ke row-level lock Oracle (SELECT FOR UPDATE) untuk menjaga integritas saldo.")
            ],
            lang="id"
        )
    else:
        add_header(s3, "Financial Consistency & Safety", "Defensive Concurrency & Zero-Loss Ledger Guarantees")
        add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(2.5), "1. Redis Idempotency State Machine", [
            ("Atomic Key Acquisition", "SETNX indibank:idempotency:{key} IN_PROGRESS with 60s lock window."),
            ("In-Flight Deduplication", "Concurrent requests with the same key receive HTTP 409 Conflict immediately."),
            ("24-Hour Replay Cache", "On settlement, complete HTTP response payload is cached for 86,400s."),
            ("Safe Retries", "On validation error, key is released to allow corrected resubmissions.")
        ], ACCENT_BLUE)
        add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.5), "2. Distributed Mutex & Lua Release", [
            ("Source Account Lock", "SET indibank:lock:account:{acc} {UUID} NX PX 10000 ensures single-flight execution."),
            ("Auto-Expiry TTL", "10-second TTL prevents deadlocks if a container crashes mid-flight."),
            ("Atomic Lua Release", "Validates lock token ownership in Redis before deleting, preventing lock hijacking."),
            ("Graceful Contention", "If lock cannot be acquired within timeout, returns 409 Conflict.")
        ], ACCENT_AMBER)
        add_card(s3, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.6), "3. Strict Double-Entry Bookkeeping", [
            ("Mathematical Balance", "Every transfer generates matching DEBIT and CREDIT journal lines."),
            ("Zero Ledger Drift", "Invariance guaranteed: |Debit - Credit| == 0.00 IDR across all transactions."),
            ("Immutable Ledger", "Journal entries are append-only; historical entries are never updated or deleted."),
            ("Audit Statement API", "Real-time historical account statement query via /api/v1/accounts/{acc}/statement.")
        ], ACCENT_GREEN)
        add_card(s3, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.6), "4. Database Constraints & Optimistic Locking", [
            ("Non-Negative Balance", "Oracle CHECK constraint (BALANCE >= 0) physically prevents overdrafts."),
            ("Optimistic Locking", "@Version column on ACCOUNTS prevents concurrent dirty read modifications."),
            ("Isolated Rollback", "Spring @Transactional rolls back debit/credit and releases Redis locks on failure."),
            ("Transactional Outbox", "Outbox table persists Kafka events inside the same Oracle transaction.")
        ], ACCENT_PURPLE)
        set_speaker_notes(
            s3, "2 minutes",
            "Here we see the technical implementation of our consistency guarantees. "
            "First, our Redis Idempotency state machine: when a transfer request arrives, we execute an atomic SETNX. If a duplicate request arrives while the first is in-flight, it gets an immediate 409 Conflict. "
            "Once settled, we cache the 201 response for 24 hours. When the user's mobile app retries after a network drop, it receives the exact cached receipt without deducting a single Rupiah. "
            "Second, distributed locking: we lock the sender's account using an auto-expiring 10-second token and release it with an atomic Lua script that verifies token ownership. "
            "Third, our double-entry engine: balances are never updated in isolation. Every transfer creates equal DEBIT and CREDIT lines. "
            "And finally, Oracle enforces a hardware-level CHECK constraint that balance must remain >= 0, backed by JPA @Version optimistic locking.",
            [
                "Explain why Lua script is essential for distributed lock release (preventing releasing someone else's expired lock)",
                "Emphasize that double-entry guarantees zero mathematical ledger drift",
                "Point out that the database check constraint provides defense-in-depth"
            ],
            [
                ("What happens if the Redis server goes down during the transfer?", 
                 "We designed a graceful degradation path: if Redis is unavailable, the system falls back directly to Oracle DB row-level locking (SELECT FOR UPDATE) to ensure transaction safety, while logging a critical operational warning to Prometheus.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 4: EVENT STREAMING & AML
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s4, "Event Streaming & Kepatuhan Regulasi", "Apache Kafka KRaft: Asynchronous Decoupling & AML Real-Time")
        add_card(s4, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Arsitektur Event Kafka KRaft", [
            ("Arsitektur Tanpa Zookeeper", "Apache Kafka 3.7+ mode KRaft untuk latensi lebih rendah, pemilihan leader lebih cepat, dan efisiensi memori."),
            ("Topic 1: bank.transfers.settled", "Dipublikasikan segera setelah commit ACID Oracle berhasil. Payload memuat nomor referensi, rekening sumber/tujuan, nilai transfer, dan timestamp."),
            ("Topic 2: bank.fraud.alerts", "Dipublikasikan oleh pekerja AML real-time saat transaksi berisiko tinggi atau mencurigakan terdeteksi."),
            ("Topic 3: bank.transfers.dlq", "Dead-letter queue yang menangkap pesan gagal setelah 3 kali retry dengan exponential backoff."),
            ("Pemisahan Asinkron (Decoupling)", "Nasabah menerima respon HTTP 201 Created secara instan; notifikasi dan kepatuhan diproses asinkron di belakang layar.")
        ], ACCENT_PURPLE)
        add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Mesin Kepatuhan AML Real-Time", [
            ("Aturan Transaksi Bernilai Tinggi", "Secara otomatis mendeteksi dan menandai transfer tunggal >= Rp 100.000.000 sebagai risiko CRITICAL AML."),
            ("Consumer Group Independen", "Consumer group 'indibank-fraud-detector' membaca dari topic bank.transfers.settled secara paralel tanpa membebani thread transfer."),
            ("Payload Peringatan Terstruktur", "Menghasilkan pesan alert lengkap dengan level keparahan, alasan risiko, dan kode regulasi."),
            ("Ticker Stream In-Memory Live", "RecentEventsTracker mengelola ring buffer memori yang dapat diakses publik di /api/v1/events/recent."),
            ("Demonstrasi Dashboard Interaktif", "Evaluator dan auditor dapat melihat event Kafka mengalir secara live detik demi detik di dashboard perbankan kami.")
        ], ACCENT_AMBER)
        set_speaker_notes(
            s4, "1.5 menit",
            "Sekarang mari kita lihat lapisan event streaming kami. Kami menggunakan Apache Kafka dalam mode KRaft, yang meniadakan ketergantungan pada Zookeeper. "
            "Ketika transfer antarbank committed di Oracle, event langsung dipublikasikan ke topic `bank.transfers.settled`. "
            "Berjalan secara paralel, modul Anti-Money Laundering (AML) kami melakukan pemindaian real-time. "
            "Setiap transfer dengan nilai sama dengan atau melebihi 100 juta Rupiah secara otomatis memicu event peringatan ke `bank.fraud.alerts` dengan status CRITICAL. "
            "Penting untuk dicatat bahwa pemrosesan kepatuhan ini terpisah secara asinkron dari API HTTP. Nasabah menerima resi 201 dalam waktu di bawah 150 milidetik. "
            "Kami juga mengekspos ticker stream memori di `/api/v1/events/recent` yang divisualisasikan langsung pada dashboard kami.",
            [
                "Keunggulan mode KRaft (metadata lebih bersih, failover instan)",
                "Pemisahan settlement sinkron dari pemrosesan kepatuhan asinkron",
                "Dead-letter queue memastikan pesan bermasalah tidak menghalangi antrean transaksi"
            ],
            [
                ("Bagaimana mencegah event hilang jika Kafka broker down saat commit database?", "Kami menerapkan pola Transactional Outbox: event disimpan di tabel OUTBOX_EVENTS dalam transaksi database ACID yang sama. Pekerja outbox menjamin pengiriman at-least-once ke Kafka.")
            ],
            lang="id"
        )
    else:
        add_header(s4, "Event Streaming & Compliance", "Apache Kafka KRaft: Asynchronous Decoupling & Real-Time AML")
        add_card(s4, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Kafka KRaft Event Architecture", [
            ("Zookeeper-Less Architecture", "Apache Kafka 3.7+ running in KRaft mode for lower latency, faster failover, and simplified ops."),
            ("Topic 1: bank.transfers.settled", "Emitted immediately after Oracle ACID commit. Payload includes transfer reference, accounts, amount, and timestamp."),
            ("Topic 2: bank.fraud.alerts", "Emitted by real-time AML worker whenever suspicious or high-value activity is detected."),
            ("Topic 3: bank.transfers.dlq", "Dead-letter queue capturing failed messages after 3 retry attempts with exponential backoff."),
            ("Async Decoupling", "User receives 201 Created immediately; downstream notifications and analytics process asynchronously.")
        ], ACCENT_PURPLE)
        add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Real-Time AML Compliance Engine", [
            ("High-Value Detection Rule", "Automatically flags any single transfer >= Rp 100,000,000 as CRITICAL AML risk."),
            ("Independent Consumer Group", "Consumer group 'indibank-fraud-detector' consumes from bank.transfers.settled in parallel."),
            ("Compliance Alert Payload", "Generates structured alert event with severity, risk reason, and compliance reference."),
            ("In-Memory Live Stream Ticker", "RecentEventsTracker maintains an in-memory ring buffer exposed at /api/v1/events/recent."),
            ("Interactive UI Demonstration", "Auditors and evaluators can watch the live Kafka event ticker update in real-time on our dashboard.")
        ], ACCENT_AMBER)
        set_speaker_notes(
            s4, "1.5 minutes",
            "Now let's examine our event-driven tier. We use Apache Kafka in KRaft mode, eliminating Zookeeper dependencies. "
            "When an interbank transfer settles in Oracle, an event is published to `bank.transfers.settled`. "
            "Running in parallel is our real-time Anti-Money Laundering (AML) fraud detector. "
            "Any transfer equal to or exceeding 100 million Rupiah automatically triggers an alert event to `bank.fraud.alerts` with severity CRITICAL. "
            "Notice that this heavy compliance processing is completely decoupled from the HTTP transfer endpoint. The client gets their HTTP 201 settlement receipt in under 150ms. "
            "Furthermore, we expose an in-memory stream ticker at `/api/v1/events/recent`, which our dashboard uses to show Kafka events ticking in real-time.",
            [
                "KRaft mode advantages (cleaner metadata management, instant failovers)",
                "Decoupling of synchronous settlement from asynchronous compliance processing",
                "Dead-letter queues ensure poisoned messages do not block consumer partitions"
            ],
            [
                ("How do you prevent event loss if the Kafka broker is temporarily unreachable during commit?", 
                 "We implemented the Transactional Outbox Pattern: the event is stored in an OUTBOX_EVENTS table within the same ACID database transaction as the ledger lines. An outbox publisher guarantees at-least-once delivery to Kafka.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 5: SPEC-DRIVEN DEVELOPMENT
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s5, "Metodologi Rekayasa Perangkat Lunak", "Spec-Driven Development (SDD) & Tata Kelola Kontrak")
        add_card(s5, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "Kontrak REST & Asinkron", [
            ("Spesifikasi OpenAPI 3.1", "spec/openapi.yaml mendefinisikan seluruh endpoint, parameter, struktur request/response, dan skema validasi."),
            ("Swagger UI Interaktif", "Dokumentasi interaktif live di /swagger-ui.html dengan kemampuan 'Try It Out' langsung."),
            ("Spesifikasi AsyncAPI 3.0", "spec/asyncapi.yaml mendefinisikan kontrak streaming Kafka, skema payload pesan, dan channel bindings."),
            ("Multi-Lingkungan", "Kontrak mendefinisikan URL produksi GKE, lingkungan pengujian preview, dan lokal dev.")
        ], ACCENT_BLUE)
        add_card(s5, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Spesifikasi Database & Cache", [
            ("DDL Relasional Oracle 23c", "spec/database-schema.sql mendefinisikan tabel, kolom identity, foreign key, dan CHECK constraints."),
            ("Skema Buku Besar Dobel", "Tabel JOURNAL_ENTRIES dengan ENUM DEBIT/CREDIT yang ketat dan verifikasi saldo non-negatif."),
            ("Spesifikasi Konkurensi Redis", "spec/redis-spec.md mendefinisikan konvensi namespace kunci, masa kedaluwarsa TTL, dan script penguncian Lua."),
            ("Data Awal Demo", "5 rekening perbankan terdaftar: korporasi, ritel tabungan, payroll, dan kliring nasional.")
        ], ACCENT_AMBER)
        add_card(s5, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Format Error Standar RFC 7807", [
            ("RFC 7807 Problem Details", "Seluruh respon error mengikuti standar perbankan yang seragam melalui ApiErrorDto."),
            ("HTTP 400 Bad Request", "Header wajib tidak ada, format nomor rekening bukan 10 digit, atau skema JSON tidak valid."),
            ("HTTP 409 Conflict", "Transaksi duplikat sedang berjalan atau terjadi perebutan lock rekening pengirim."),
            ("HTTP 422 Unprocessable", "Pelanggaran aturan domain bisnis: saldo tidak cukup, rekening tidak aktif, atau transfer ke diri sendiri.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s5, "1.5 menit",
            "Metodologi pengembangan kami berpegang teguh pada Spec-Driven Development (SDD). Sebelum menulis baris kode Java pertama, kami merumuskan spesifikasi secara formal: "
            "Pertama, spesifikasi OpenAPI 3.1 untuk semua endpoint REST yang secara otomatis menghasilkan dokumentasi Swagger interaktif. "
            "Kedua, spesifikasi AsyncAPI 3.0 untuk event Kafka. "
            "Ketiga, DDL Oracle 23c dengan integritas relasional penuh dan data benih. "
            "Dan keempat, spesifikasi konkurensi Redis yang menetapkan konvensi penamaan kunci, masa TTL, dan script Lua. "
            "Selain itu, semua respon error mengikuti format standar RFC 7807 Problem Details, memudahkan integrasi sistem pihak ketiga.",
            [
                "Spesifikasi menjadi satu-satunya sumber kebenaran (source of truth) di folder /spec",
                "OpenAPI 3.1 dan AsyncAPI 3.0 menyelaraskan tim frontend, backend, dan auditor",
                "Standarisasi RFC 7807 menghadirkan pengalaman developer kelas enterprise"
            ],
            [
                ("Bagaimana memastikan kode tidak menyimpang dari spesifikasi OpenAPI?", "Kami menggunakan anotasi SpringDoc OpenAPI langsung pada DTO dan controller, serta memanfaatkan integration test untuk memvalidasi skema payload terhadap kontrak.")
            ],
            lang="id"
        )
    else:
        add_header(s5, "Engineering Methodology", "Spec-Driven Development (SDD) & Contract Governance")
        add_card(s5, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "REST & Async Contracts", [
            ("OpenAPI 3.1 Spec", "spec/openapi.yaml defines all endpoints, parameters, request/response bodies, and validation schemas."),
            ("Live Swagger UI", "Auto-generated from OpenAPI 3.1, available live at /swagger-ui.html with full 'Try It Out' capability."),
            ("AsyncAPI 3.0 Spec", "spec/asyncapi.yaml defines Kafka event streaming contracts, message schemas, and channel bindings."),
            ("Multi-Environment", "Contracts specify production GKE, test preview, and local dev environments.")
        ], ACCENT_BLUE)
        add_card(s5, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Database & Cache Specs", [
            ("Oracle 23c Relational DDL", "spec/database-schema.sql defines tables, identity columns, foreign keys, and CHECK constraints."),
            ("Double-Entry Ledger Schema", "JOURNAL_ENTRIES table with strict DEBIT/CREDIT ENUM and non-negative balance checks."),
            ("Redis Concurrency Spec", "spec/redis-spec.md defines key namespaces, TTL expiry policies, and Lua locking scripts."),
            ("Seed Data & Baseline", "5 pre-seeded banking accounts for corporate, retail, payroll, and interbank clearing.")
        ], ACCENT_AMBER)
        add_card(s5, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Standardized RFC 7807 Errors", [
            ("RFC 7807 Problem Details", "All error responses conform to the standard banking error contract (ApiErrorDto)."),
            ("HTTP 400 Bad Request", "Missing headers, invalid 10-digit account formatting, or payload schema violations."),
            ("HTTP 409 Conflict", "Duplicate transfer in-flight or distributed account lock contention."),
            ("HTTP 422 Unprocessable", "Domain rule violations: insufficient funds, inactive accounts, or negative amounts.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s5, "1.5 minutes",
            "Our development methodology followed Spec-Driven Development (SDD). Before writing Java code, we formalized our specifications: "
            "First, an OpenAPI 3.1 specification for all REST endpoints, which generates our interactive Swagger documentation. "
            "Second, an AsyncAPI 3.0 specification for Kafka event payloads. "
            "Third, an Oracle 23c DDL specification with strict relational constraints and seed data. "
            "And fourth, a Redis Concurrency specification defining key naming conventions, TTL policies, and Lua scripts. "
            "In addition, all error responses strictly follow RFC 7807 Problem Details, giving API consumers machine-readable error codes such as VALIDATION_ERROR or INSUFFICIENT_FUNDS.",
            [
                "Specs exist as source-of-truth contracts in the repository under /spec",
                "OpenAPI 3.1 and AsyncAPI 3.0 ensure complete full-stack alignment",
                "RFC 7807 standard error formatting provides enterprise-grade developer experience"
            ],
            [
                ("How do you ensure code doesn't drift from the OpenAPI spec?", 
                 "We use SpringDoc OpenAPI annotations in our controllers and DTOs to generate the live OpenAPI JSON directly from code, and our integration tests validate request/response payload schemas against the contract.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 6: QUALITY ENGINEERING & TEST PYRAMID
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s6, "Jaminan Kualitas & Barrier Cakupan", "Piramida Pengujian 3-Tingkat & Barrier Cakupan JaCoCo")
        add_card(s6, Inches(0.8), Inches(1.6), Inches(3.7), Inches(4.3), "Tingkat 1: Pengujian Unit", [
            ("Logika Bisnis & Domain", "Pengujian unit mendalam pada TransferService, AccountService, dan IdempotencyService."),
            ("Mocking Terisolasi", "Verifikasi Mockito pada lock Redis, rilis Lua, dan rollback transaksi database."),
            ("Kasus Negatif & Ekstrem", "Uji tuntas untuk saldo nol, transfer ke rekening sendiri, dan ketidakcocokan mata uang."),
            ("Komponen Kafka", "Verifikasi publikasi event, pemicu aturan AML, dan pengiriman ke antrean DLQ.")
        ], ACCENT_BLUE)
        add_card(s6, Inches(4.8), Inches(1.6), Inches(3.7), Inches(4.3), "Tingkat 2: Integrasi WebMvc", [
            ("Uji Slice HTTP MockMvc", "@WebMvcTest menguji TransferController dan AccountController pada web slice terisolasi."),
            ("Validasi Header & DTO", "Memvalidasi kewajiban header Idempotency-Key, regex 10-digit, dan batas @DecimalMax."),
            ("Pemetaan Exception Global", "Memastikan mapping otomatis ke format RFC 7807 HTTP 400, 404, 409, dan 422."),
            ("Serialisasi JSON DTO", "Memastikan presisi BigDecimal mata uang dan timestamp ISO-8601 tanpa pembulatan.")
        ], ACCENT_AMBER)
        add_card(s6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(4.3), "Tingkat 3: End-to-End (E2E) Live", [
            ("Eksekusi Cluster GKE Aktif", "test-scenarios.sh menjalankan 7 skenario perbankan nyata terhadap domain produksi dan preview."),
            ("Skenario 1: Query Akun", "Mengambil saldo awal langsung dari database Oracle 23c aktif."),
            ("Skenario 2 & 3: Idempotensi", "Melakukan transfer, lalu mengulang kunci yang sama persis untuk memverifikasi resi identik."),
            ("Skenario 4 & 5: AML Kafka", "Transfer Rp 150 Juta dan verifikasi event alert pada ticker stream Kafka live."),
            ("Skenario 6 & 7: Audit Saldo", "Verifikasi saldo mutasi jurnal debit/kredit dan penolakan 422 saat saldo kurang.")
        ], ACCENT_GREEN)
        
        j_banner = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.9))
        j_banner.fill.solid()
        j_banner.fill.fore_color.rgb = CARD_BG
        j_banner.line.color.rgb = ACCENT_GREEN
        j_tf = j_banner.text_frame
        jp = j_tf.paragraphs[0]
        jp.text = "🏆 STANDAR KUALITAS WAJIB: CAKUPAN >= 95% DIENFORCE DALAM CI/CD"
        jp.font.name = FONT_HEADING
        jp.font.size = Pt(11)
        jp.font.bold = True
        jp.font.color.rgb = ACCENT_GREEN
        jp2 = j_tf.add_paragraph()
        jp2.text = "Hasil Terverifikasi: 70 Tes Berhasil • 99.27% Line Coverage (410/413) • 99.04% Instruction Coverage (1,652/1,668)"
        jp2.font.name = FONT_BODY
        jp2.font.size = Pt(12)
        jp2.font.bold = True
        jp2.font.color.rgb = TEXT_MAIN
        
        set_speaker_notes(
            s6, "2 menit",
            "Beralih ke aspek rekayasa kualitas. Kami menerapkan piramida pengujian 3 tingkat yang sangat disiplin: "
            "Pada Tingkat 1, unit test mengisolasi logika bisnis domain, menguji akuisisi lock, transisi idempotensi, dan berbagai kasus batas. "
            "Pada Tingkat 2, pengujian integrasi WebMvc menggunakan MockMvc untuk memastikan keandalan validasi Bean Validation, header HTTP, dan kode status RFC 7807. "
            "Pada Tingkat 3, skrip otomatisasi bash `test-scenarios.sh` mengeksekusi 7 skenario perbankan nyata terhadap cluster GKE aktif. "
            "Yang paling penting, pipeline CI/CD kami menerapkan barrier cakupan JaCoCo minimal 95%: pull request dengan cakupan di bawah 95% akan langsung ditolak otomatis. "
            "Hasil pengujian kami saat ini mencapai 99.27% Line Coverage dan 99.04% Instruction Coverage dengan 70 tes yang semuanya berstatus lulus.",
            [
                "Tiga lapisan piramida pengujian yang saling melengkapi",
                "Barrier kualitas JaCoCo >= 95% yang dikunci pada konfigurasi Maven dan CI/CD",
                "Konfigurasi lombok.config untuk mengecualikan boilerplate dari analisis cakupan"
            ],
            [
                ("Bagaimana mencegah pengujian E2E memperlambat developer?", "Pengujian unit dan WebMvc berjalan kurang dari 45 detik pada langkah build CI. Pengujian E2E live dijalankan secara otomatis di lingkungan preview sebelum proses merge ke branch utama.")
            ],
            lang="id"
        )
    else:
        add_header(s6, "Quality Assurance & Coverage Barrier", "3-Tier Testing Pyramid & JaCoCo Coverage Barrier")
        add_card(s6, Inches(0.8), Inches(1.6), Inches(3.7), Inches(4.3), "Tier 1: Unit Test Suite", [
            ("Domain & Business Logic", "Comprehensive unit tests covering TransferService, AccountService, and IdempotencyService."),
            ("Isolated Mocking", "Mockito verification of Redis lock acquisition, Lua release, and Oracle transaction rollback."),
            ("Negative & Edge Cases", "Exhaustive tests for zero balances, transfer to self, and currency mismatch."),
            ("Kafka Producer & Consumer", "Verified event publication, fraud rule triggering, and DLQ dispatching.")
        ], ACCENT_BLUE)
        add_card(s6, Inches(4.8), Inches(1.6), Inches(3.7), Inches(4.3), "Tier 2: WebMvc Integration", [
            ("MockMvc HTTP Verification", "@WebMvcTest testing TransferController and AccountController in isolated web slice."),
            ("Header & Bean Validation", "Tests required Idempotency-Key header, @Pattern 10-digit check, and @DecimalMax limits."),
            ("Global Exception Mapping", "Verifies automatic mapping to RFC 7807 HTTP 400, 404, 409, and 422 status codes."),
            ("DTO JSON Serialization", "Ensures ISO-8601 timestamps, BigDecimal precision, and response headers.")
        ], ACCENT_AMBER)
        add_card(s6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(4.3), "Tier 3: Live End-to-End E2E", [
            ("Live GKE Execution", "test-scenarios.sh runs 7 real-world banking journeys against live production and preview domains."),
            ("Scenario 1: Accounts Query", "Queries initial balances from live Oracle DB."),
            ("Scenario 2 & 3: Idempotency", "Executes transfer, then replays exact same key to verify identical cached receipt."),
            ("Scenario 4 & 5: AML Kafka", "Executes Rp 150M transfer and verifies live Kafka fraud alert stream ticker."),
            ("Scenario 6 & 7: Audit & Limits", "Verifies Oracle double-entry journal balance and insufficient balance 422 error.")
        ], ACCENT_GREEN)
        
        j_banner = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.9))
        j_banner.fill.solid()
        j_banner.fill.fore_color.rgb = CARD_BG
        j_banner.line.color.rgb = ACCENT_GREEN
        j_tf = j_banner.text_frame
        jp = j_tf.paragraphs[0]
        jp.text = "🏆 MANDATORY QUALITY BARRIER: >= 95% COVERAGE ENFORCED IN CI/CD"
        jp.font.name = FONT_HEADING
        jp.font.size = Pt(11)
        jp.font.bold = True
        jp.font.color.rgb = ACCENT_GREEN
        jp2 = j_tf.add_paragraph()
        jp2.text = "Verified Results: 70 Tests Passing • 99.27% Line Coverage (410/413) • 99.04% Instruction Coverage (1,652/1,668)"
        jp2.font.name = FONT_BODY
        jp2.font.size = Pt(12)
        jp2.font.bold = True
        jp2.font.color.rgb = TEXT_MAIN
        
        set_speaker_notes(
            s6, "2 minutes",
            "Let's turn to quality engineering. We implemented a rigorous 3-tier testing pyramid: "
            "At Tier 1, our unit tests isolate all core domain logic, testing distributed lock acquisition, idempotency states, and edge cases. "
            "At Tier 2, WebMvc integration tests use MockMvc to verify HTTP headers, Bean Validation constraints, and RFC 7807 error status codes. "
            "At Tier 3, our automated bash test suite `test-scenarios.sh` executes 7 live banking journeys against the running GKE cluster. "
            "Crucially, our CI/CD pipeline enforces a strict JaCoCo quality barrier: any pull request with less than 95% line or instruction coverage is automatically rejected. "
            "Our current test suite achieves 99.27% Line Coverage and 99.04% Instruction Coverage with 70 passing tests.",
            [
                "Explain the three distinct layers of the testing pyramid",
                "Highlight the 95% JaCoCo coverage barrier configured in pom.xml and CI/CD",
                "Mention lombok.config exclusion of boilerplate getters/setters"
            ],
            [
                ("How do you prevent slow E2E tests from blocking developers?", 
                 "Unit and WebMvc integration tests run in under 45 seconds in the CI build step. The live E2E test suite runs against the deployed preview domain asynchronously before final production merge.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 7: SRE & OBSERVABILITY
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s7, "Site Reliability Engineering", "Framework SRE Produksi, SLO, & Telemetri Real-Time")
        add_card(s7, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "SLO & Error Budget", [
            ("SLO Ketersediaan", ">= 99.99% (Empat Angka Sembilan) dihitung rolling 30 hari (anggaran downtime 4.32 menit/bulan)."),
            ("SLO Latensi (p95)", "<= 150 ms end-to-end waktu settlement transaksi."),
            ("SLO Latensi (p99)", "<= 500 ms kasus terburuk termasuk waktu lock terdistribusi dan publikasi Kafka."),
            ("SLO Invariansi Buku Besar", "Zero drift (|Debit - Kredit| == 0.00 IDR) dengan toleransi NOL (Hard Stop)."),
            ("Multi-Burn Rate Alerting", "Burn rate 1 jam >= 14.4x memicu pager P1; deployment freeze otomatis jika budget sisa < 10%.")
        ], ACCENT_BLUE)
        add_card(s7, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Empat Sinyal Emas", [
            ("Latency", "Histogram persentil (p50, p95, p99) dicatat per endpoint dan channel via Micrometer."),
            ("Traffic", "Meteran throughput dan RPS real-time dipartisi berdasarkan mata uang dan status."),
            ("Errors", "Memisahkan error 4xx validasi nasabah (tidak membakar error budget) dari error 5xx sistem server."),
            ("Saturation", "Koneksi pending pool HikariCP, consumer group lag Kafka, dan memori ZGC."),
            ("Endpoint Live", "Diekspos secara real-time di /actuator/prometheus untuk scraping monitoring.")
        ], ACCENT_AMBER)
        add_card(s7, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Alerting & Autoscaling", [
            ("Aturan Alert Prometheus", "monitoring/prometheus-alerts.yaml mendefinisikan peringatan untuk error 5xx, lonjakan latensi, dan kelaparan pool DB."),
            ("Kelaparan Pool Oracle", "Memicu alert kritis saat hikaricp_connections_pending > 0 selama lebih dari 30 detik."),
            ("Lag Consumer Kafka", "Memicu alert peringatan saat antrean consumer fraud melebihi 500 pesan."),
            ("Kubernetes HPA", "k8s/hpa.yaml mengotomatiskan penskalaan pod 1 hingga 5 replika berdasar utilisasi CPU 70% dan Memori 80%."),
            ("Runbook Insiden SOP", "Dokumentasi SOP-01 sampai SOP-03 untuk panduan teknis penanganan insiden SRE on-call.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s7, "2 menit",
            "Mari kita tinjau aspek Site Reliability Engineering (SRE). Pada core banking, SRE bertujuan memastikan prediktabilitas dan pembatasan dampak kegagalan (blast radius). "
            "Kami menetapkan SLO yang ketat: ketersediaan 99.99% dengan batas error budget 4.3 menit per bulan. "
            "Target latensi adalah sub-150ms untuk p95 dan sub-500ms untuk p99. Dan invariansi saldo buku besar memiliki toleransi nol: jika ada drift sepeser pun, sistem akan menghentikan transaksi secara aman. "
            "Kami memantau Empat Sinyal Emas via metrik Prometheus di `/actuator/prometheus`. "
            "Sangat penting: kami membedakan error 4xx validasi bisnis nasabah, seperti saldo kurang, dari error 5xx server, sehingga kesalahan input nasabah tidak menghanguskan error budget ketersediaan sistem. "
            "Kami juga memasang Kubernetes Horizontal Pod Autoscaler (HPA) untuk autoscaling 1 sampai 5 pod, serta menyusun runbook SOP penanganan insiden.",
            [
                "Pemisahan tegas antara error 4xx bisnis dan 5xx server dalam kalkulasi error budget",
                "Strategi multi-window multi-burn-rate alerting (burn rate 1 jam dan 6 jam)",
                "Autoscaling Kubernetes HPA dan aturan alert Prometheus produksi"
            ],
            [
                ("Bagaimana cara menangani kelaparan koneksi database (HikariCP starvation)?", "Alert Prometheus kami mendeteksi jika ada thread pending lebih dari 30 detik. Bersamaan dengan itu, HPA menskalakan pod aplikasi dan rate limiter Redis melindungi database dari lonjakan trafik mendadak.")
            ],
            lang="id"
        )
    else:
        add_header(s7, "Site Reliability Engineering", "Production SRE Framework, SLOs, & Real-Time Telemetry")
        add_card(s7, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "SLOs & Error Budgets", [
            ("Availability SLO", ">= 99.99% (Four Nines) measured on a rolling 30-day window (4.32 min/month error budget)."),
            ("Latency SLO (p95)", "<= 150 ms end-to-end settlement latency."),
            ("Latency SLO (p99)", "<= 500 ms worst-case latency including distributed locking and Kafka publish."),
            ("Ledger Invariance SLO", "Zero mathematical drift (|Debit - Credit| == 0.00 IDR) with ZERO error tolerance."),
            ("Multi-Burn Alerting", "1-hour burn rate >= 14.4x triggers P1 pager alert; automated release freeze if budget drops < 10%.")
        ], ACCENT_BLUE)
        add_card(s7, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Four Golden Signals", [
            ("Latency", "Histogram percentiles (p50, p95, p99) tracked per endpoint and channel via Micrometer."),
            ("Traffic", "Real-time RPS and throughput counters partitioned by currency and status."),
            ("Errors", "Distinguishes 4xx business validations (which don't burn budget) from 5xx server faults."),
            ("Saturation", "HikariCP Oracle pool pending threads, Kafka consumer group lag, and ZGC heap memory."),
            ("Live Endpoint", "Exposed live at /actuator/prometheus for automated scraping.")
        ], ACCENT_AMBER)
        add_card(s7, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Alerting & Autoscaling", [
            ("Prometheus Alert Rules", "monitoring/prometheus-alerts.yaml defines production alerts for 5xx errors, latency, and pool starvation."),
            ("Oracle Pool Starvation", "Alerts when hikaricp_connections_pending > 0 for > 30s."),
            ("Kafka Consumer Lag", "Alerts when fraud consumer lag exceeds 500 messages."),
            ("Kubernetes HPA", "k8s/hpa.yaml scales replicas from 1 to 5 based on 70% CPU and 80% Memory utilization."),
            ("Incident SOP Runbooks", "Standard Operating Procedures (SOP-01 to SOP-03) documented for on-call SREs.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s7, "2 minutes",
            "Let's look at Site Reliability Engineering. In core banking, SRE is about predictability and blast-radius control. "
            "We defined clear SLOs: 99.99% availability, which allows just 4.3 minutes of downtime per month. "
            "Our latency targets are sub-150ms for p95 and sub-500ms for p99. And our ledger invariance SLO has zero tolerance: mathematical drift is an immediate hard system stop. "
            "We monitor the Four Golden Signals via Prometheus metrics exposed at `/actuator/prometheus`. "
            "Importantly, we distinguish 4xx client errors, like an insufficient balance, from 5xx system errors, ensuring user validation failures don't consume our reliability error budget. "
            "We also implemented Kubernetes Horizontal Pod Autoscaling (HPA) to scale between 1 and 5 replicas based on CPU and memory thresholds, and provided SOP runbooks for incident response.",
            [
                "Distinction between 4xx business errors and 5xx system errors in error budgeting",
                "Multi-window multi-burn-rate alerting strategy (1h and 6h burn rates)",
                "Kubernetes HPA scaling policies and Prometheus alert rules"
            ],
            [
                ("How do you handle database connection pool saturation under spike load?", 
                 "Our Prometheus alert triggers if HikariCP pending threads exist for more than 30 seconds. In parallel, our Kubernetes HPA scales application replicas, and Redis rate limiters protect the database from query storms.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 8: CI/CD & BLUE-GREEN
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s8, "Deployment & Rekayasa Rilis", "Deployment Blue-Green Zero-Downtime & Domain Preview")
        add_card(s8, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "Proteksi Branch Utama", [
            ("Kunci Branch Main", "Push langsung ke branch 'main' diblokir permanen dengan aturan enforce_admins: true."),
            ("Wajib Pull Request", "Semua modifikasi kode wajib ditinjau dan digabungkan melalui proses PR."),
            ("Gerbang Kualitas 95%", "Pengecekan CI 'Build & Verify 95% Coverage Barrier' wajib berstatus hijau sebelum tombol merge terbuka."),
            ("Histori Git Bersih", "Penerapan conventional commits (feat, fix, docs, chore) dengan histori linier.")
        ], ACCENT_BLUE)
        add_card(s8, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Domain Preview Fitur", [
            ("Lingkungan Staging Ephemeral", "Push ke branch fitur apa pun otomatis memicu build kontainer preview."),
            ("Ingress Khusus", "Dideploy ke pod indibank-core-preview, dapat diakses publik di https://test.indibank.aldianapps.com."),
            ("Verifikasi QA & Stakeholder", "Memungkinkan pengetesan manual dan otomatis di lingkungan nyata sebelum merge."),
            ("Nol Dampak Produksi", "Isolasi pod mencegah pengujian fitur baru mengganggu transaksi nasabah live.")
        ], ACCENT_AMBER)
        add_card(s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Blue-Green Produksi", [
            ("Deployment Kembar", "Dua deployment produksi identik: indibank-core-blue dan indibank-core-green."),
            ("Kesiapan Atomik", "Slot standby dinaikkan ke 1 replika; CI/CD memverifikasi rollout status sebelum switch."),
            ("Pengalihan Trafik Instan", "Satu perintah patch selector Service Kubernetes mengalihkan trafik seketika."),
            ("Rollback Sub-Detik", "Jika terjadi anomali pasca-rilis, pengembalian ke slot lama berlangsung dalam waktu < 1 detik.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s8, "2 menit",
            "Pipeline rilis kami menjamin zero-downtime dan pengendalian radius dampak (blast radius) secara aman. "
            "Pertama, push langsung ke branch `main` diblokir total melalui GitHub Branch Protection dengan penegakan level admin. Setiap perubahan wajib melalui branch fitur dan PR. "
            "Kedua, setiap kali branch fitur di-push, pipeline CI/CD kami mendeploy kontainer preview ke `https://test.indibank.aldianapps.com`. "
            "Hal ini memungkinkan developer dan stakeholder memverifikasi fungsionalitas secara langsung di domain aktif sebelum digabungkan. "
            "Ketiga, ketika PR di-merge ke `main`, pipeline Blue-Green kami secara otomatis mendeploy image baru ke slot standby (misal green), "
            "menunggu pod siap sempurna, dan mem-patch selector Service Kubernetes secara atomik. "
            "Pengalihan trafik terjadi secara instan tanpa ada request yang terputus. Jika terdeteksi masalah, kami dapat melakukan rollback dalam waktu kurang dari satu detik.",
            [
                "Branch protection dengan enforce_admins: true dan required status checks",
                "Pemisahan domain uji: test.indibank.aldianapps.com vs indibank.aldianapps.com",
                "Mekanisme rollback atomik sub-detik menggunakan selector Service Kubernetes"
            ],
            [
                ("Mengapa memilih Blue-Green dibanding Canary untuk core banking?", "Pada sistem pembukuan finansial, menjalankan dua versi aplikasi berbeda secara bersamaan ke database yang sama berisiko menimbulkan inkonsistensi skema. Blue-Green memberikan batasan versi yang tegas dan kemampuan rollback instan.")
            ],
            lang="id"
        )
    else:
        add_header(s8, "Deployment & Release Engineering", "Zero-Downtime Blue-Green Deployment & Preview Domains")
        add_card(s8, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "Branch Protection Gate", [
            ("Main Branch Lock", "Direct pushes to 'main' are permanently blocked with enforce_admins: true."),
            ("Pull Request Mandatory", "All code modifications must be reviewed and merged via PR."),
            ("95% Coverage Gate", "GitHub Actions check 'Build & Verify 95% Coverage Barrier' must pass before merge button is unlocked."),
            ("Clean Git History", "Strict conventional commits (feat, fix, docs, chore) with linear history.")
        ], ACCENT_BLUE)
        add_card(s8, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Feature Preview Domain", [
            ("Ephemeral Testing", "Pushing to any feature branch automatically builds a preview container."),
            ("Dedicated Ingress", "Deploys to indibank-core-preview, accessible at https://test.indibank.aldianapps.com."),
            ("Manual & Automated QA", "Allows stakeholders and engineers to test new endpoints in a real environment before merge."),
            ("Zero Production Impact", "Isolated pods prevent preview testing from impacting live banking traffic.")
        ], ACCENT_AMBER)
        add_card(s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Blue-Green Production Deploy", [
            ("Dual Deployments", "Two identical production deployments: indibank-core-blue and indibank-core-green."),
            ("Atomic Readiness", "Standby slot scales to 1 replica; CI/CD waits for rollout status before traffic switch."),
            ("Atomic Traffic Switch", "Single kubectl patch on the Service selector instantly points live traffic to new slot."),
            ("Sub-Second Rollback", "If an anomaly occurs post-cutover, rolling back takes < 1s with a one-line service patch.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s8, "2 minutes",
            "Our release pipeline guarantees zero-downtime deployments and safe blast-radius containment. "
            "First, direct pushes to `main` are strictly blocked via GitHub Branch Protection with admin enforcement. Every change requires a feature branch and pull request. "
            "Second, when a feature branch is pushed, our CI/CD pipeline deploys a preview container to `https://test.indibank.aldianapps.com`. "
            "This allows engineers and testers to verify changes on a live domain before merging. "
            "Third, when the PR merges to `main`, our Blue-Green deployment pipeline automatically deploys the new image to the standby slot, "
            "waits for pod readiness, and atomically patches the Kubernetes Service selector. "
            "Traffic cutover happens instantaneously with zero dropped requests. If a regression is detected post-deployment, we can roll back in under one second by flipping the selector back.",
            [
                "Branch protection with enforce_admins: true and required status checks",
                "Dual-domain routing: test.indibank.aldianapps.com vs indibank.aldianapps.com",
                "Sub-second atomic rollback mechanism using Kubernetes service selectors"
            ],
            [
                ("Why did you choose Blue-Green over Canary for this system?", 
                 "In core banking financial ledgers, running two different versions concurrently against shared state can cause subtle schema inconsistencies. Blue-Green provides a deterministic, atomic version boundary with immediate rollback capability.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 9: MULTI-PLATFORM PORTABILITY
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s9, "Arsitektur Cloud Multi-Platform", "Portabilitas Lintas GCP, AWS, Azure, OpenShift, & Lokal")
        add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Matriks Portabilitas Cloud & On-Premise", [
            ("Google Cloud (GKE)", "Target produksi live di region Jakarta (asia-southeast2). Dikelola otomatis via Terraform IaC."),
            ("Amazon Web Services (EKS)", "Dapat dideploy langsung menggunakan Helm chart dengan AWS Load Balancer Controller dan RDS Oracle."),
            ("Microsoft Azure (AKS)", "Mendukung deployment AKS dengan Azure Application Gateway Ingress dan Azure Managed Disks."),
            ("Red Hat OpenShift", "Mendukung lingkungan perbankan on-premise dengan OpenShift Security Context Constraints (SCC) dan Routes."),
            ("Minikube / Kind Lokal", "Lingkungan offline lengkap untuk kebutuhan pengembangan lokal via helm/indibank/values-local.yaml."),
            ("Panduan Deployment Lengkap", "Didokumentasikan rinci di docs/deployment/MULTI_PLATFORM.md dengan langkah operasional.")
        ], ACCENT_BLUE)
        add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Helm Chart Produksi & Pengerasan Kontainer", [
            ("Helm Chart Enterprise", "helm/indibank/ menyediakan konfigurasi parameter terpadu untuk dev, preview, dan produksi."),
            ("Keamanan Kontainer Ketat", "Berjalan sebagai non-root unprivileged user (UID 10001) berbasis image ringan distroless."),
            ("Alokasi Kuota Sumber Daya", "Batas alokasi kuota CPU dan Memori (requests & limits) yang ketat mencegah kelaparan resource."),
            ("ConfigMap & Secret Eksternal", "Pemisahan tegas antara variabel lingkungan kredensial dan artefak build aplikasi."),
            ("Probe Kesehatan Otomatis", "Liveness dan readiness probe otomatis di /actuator/health untuk auto-healing cluster.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s9, "1.5 menit",
            "Meskipun demonstrasi live kami berjalan di Google Kubernetes Engine region Jakarta, seluruh platform ini dirancang dengan portabilitas multi-cloud dan on-premise. "
            "Banyak institusi perbankan yang mengoperasikan arsitektur hybrid atau menggunakan AWS, Azure, maupun on-premise Red Hat OpenShift. "
            "Kami telah menyusun Helm chart produksi di `helm/indibank/` yang memungkinkan deployment ke cluster Kubernetes standar mana pun, termasuk Minikube lokal untuk pengembangan offline. "
            "Arsitektur deployment ini dijelaskan secara mendalam di `docs/deployment/MULTI_PLATFORM.md`. "
            "Selain itu, kontainer kami mematuhi standar keamanan enterprise: berjalan sebagai user non-root dan memiliki kuota resource CPU serta memori yang terkelola.",
            [
                "Kesiapan multi-cloud (GCP, AWS, Azure, OpenShift, lokal)",
                "Helm chart terpadu di helm/indibank/",
                "Pengerasan kontainer enterprise (user non-root, batas resource ketat)"
            ],
            [
                ("Bagaimana menangani persistensi database di berbagai provider cloud?", "Kami menggunakan Kubernetes PersistentVolumeClaims (PVC) yang dipetakan ke StorageClass bawaan masing-masing cloud—Persistent Disk di GCP, EBS di AWS, dan Managed Disk di Azure.")
            ],
            lang="id"
        )
    else:
        add_header(s9, "Multi-Platform Cloud Architecture", "Portability Across GCP, AWS, Azure, OpenShift, & Local")
        add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Cloud & On-Premise Portability Matrix", [
            ("Google Cloud (GKE)", "Live production target in Jakarta (asia-southeast2). Provisioned via Terraform IaC."),
            ("Amazon Web Services (EKS)", "Deployable via Helm chart using AWS Load Balancer Controller and RDS Oracle / self-hosted."),
            ("Microsoft Azure (AKS)", "Deployable on AKS with Azure Application Gateway Ingress and Azure Files / Managed Disks."),
            ("Red Hat OpenShift", "Enterprise on-premise banking support with OpenShift SCC and declarative Routes."),
            ("Local Minikube / Kind", "Complete local offline developer environment configured via helm/indibank/values-local.yaml."),
            ("Deployment Guide", "Fully documented in docs/deployment/MULTI_PLATFORM.md with step-by-step commands.")
        ], ACCENT_BLUE)
        add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Production Helm Chart & Container Hardening", [
            ("Enterprise Helm Chart", "helm/indibank/ provides unified parameterization across environments (dev, preview, prod)."),
            ("Container Security", "Runs as unprivileged non-root user (UID 10001) in distroless/alpine lightweight base."),
            ("Resource Governance", "Rigorous CPU and Memory requests and limits preventing noisy neighbor resource starvation."),
            ("ConfigMaps & Secrets", "Externalized configuration separating environment settings from application binaries."),
            ("Readiness & Liveness", "Native HTTP health check probes at /actuator/health for automated cluster healing.")
        ], ACCENT_GREEN)
        set_speaker_notes(
            s9, "1.5 minutes",
            "While our live demonstration runs on Google Kubernetes Engine in the Jakarta region, the entire platform is designed for multi-cloud and on-premise portability. "
            "Many financial institutions operate hybrid environments or deploy across AWS, Azure, or on-premise Red Hat OpenShift. "
            "We built a comprehensive Helm chart in `helm/indibank/` that allows deploying IndiBank Core to any CNCF-conformant Kubernetes cluster, including local Minikube or Kind for offline development. "
            "The deployment architecture is fully documented in `docs/deployment/MULTI_PLATFORM.md`. "
            "Furthermore, our containers adhere to strict enterprise security standards: they run as unprivileged non-root users with strict CPU and memory resource quotas.",
            [
                "Multi-cloud readiness (GCP, AWS, Azure, OpenShift, local)",
                "Unified production Helm chart in helm/indibank/",
                "Enterprise container hardening (non-root execution, resource limits)"
            ],
            [
                ("How do you handle database storage persistence across different cloud providers?", 
                 "We use standard Kubernetes PersistentVolumeClaims (PVC) mapped to the default StorageClass of each cloud provider—Compute Engine persistent disks on GKE, EBS on AWS, and Managed Disks on Azure.")
            ],
            lang="en"
        )

    # -------------------------------------------------------------
    # SLIDE 10: LIVE DEMO & SUMMARY
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    if is_id:
        add_header(s10, "Demonstrasi Langsung & Kesimpulan", "Verifikasi Produksi Langsung & Rangkuman Eksekutif")
        add_card(s10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "Endpoint Produksi Aktif", [
            ("Dashboard Perbankan", "https://indibank.aldianapps.com (Simulasi transfer interaktif dan inquiry saldo live)."),
            ("Domain Uji Preview", "https://test.indibank.aldianapps.com (Lingkungan uji fitur branch)."),
            ("Swagger / OpenAPI UI", "https://indibank.aldianapps.com/swagger-ui.html (Penjelajah kontrak interaktif)."),
            ("Telemetri Prometheus", "https://indibank.aldianapps.com/actuator/prometheus (Metrik operasional real-time)."),
            ("Repositori GitHub", "Repositori privat dengan branch protection dan automasi CI/CD.")
        ], ACCENT_BLUE)
        add_card(s10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Hasil Verifikasi Live (7/7)", [
            ("Skenario 1: Query Akun", "LULUS - Rekening aktif berhasil diambil langsung dari Oracle DB."),
            ("Skenario 2: Transfer Antarbank", "LULUS - Settlement real-time dengan nomor referensi unik."),
            ("Skenario 3: Replay Idempotensi", "LULUS - Resi cache identik dikembalikan tanpa pemotongan saldo ganda."),
            ("Skenario 4: AML Nilai Tinggi", "LULUS - Transfer Rp 150 Juta memicu alert fraud Kafka."),
            ("Skenario 5: Ticker Stream", "LULUS - Topic Kafka terverifikasi via API recent events."),
            ("Skenario 6: Audit Buku Besar", "LULUS - Baris jurnal DEBIT dan KREDIT terbukti seimbang."),
            ("Skenario 7: Proteksi Saldo", "LULUS - Saldo kurang ditolak aman dengan format error RFC 7807.")
        ], ACCENT_GREEN)
        add_card(s10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Rangkuman Eksekutif", [
            ("Integritas Finansial", "Invariansi buku besar Zero-Loss dengan pembukuan berpasangan dan constraint ketat."),
            ("Defensive Concurrency", "Mesin idempotensi dan locking terdistribusi menghilangkan risiko double-spending."),
            ("Streaming Throughput Tinggi", "Pemisahan asinkron Kafka KRaft dan deteksi fraud AML real-time."),
            ("Operasional Zero-Downtime", "Rilis Blue-Green dengan rollback sub-detik dan barrier pengujian 95%."),
            ("Siap Produksi Penuh", "Platform transaksi core banking yang fungsional, teruji, dan telah dideploy secara nyata.")
        ], ACCENT_AMBER)
        set_speaker_notes(
            s10, "2 menit",
            "Sebagai penutup, IndiBank Core Engine bukan sekadar prototipe di atas kertas—ini adalah sistem transaksi perbankan inti aktif yang sedang berjalan di Google Cloud saat ini. "
            "Bapak dan ibu dapat membuka `https://indibank.aldianapps.com` melalui browser laptop atau ponsel untuk mengeksekusi transfer antarbank langsung, memeriksa buku besar umum, dan melihat ticker event Kafka bergerak secara real-time. "
            "Rangkaian pengujian otomatis kami telah memvalidasi seluruh 7 skenario perbankan inti terhadap lingkungan produksi aktif, dan semuanya berhasil lulus dengan sempurna. "
            "Sebagai rangkuman apa yang telah kita bangun: "
            "Pertama, konsistensi finansial absolut berbasis akuntansi berpasangan di Oracle 23c. "
            "Kedua, konkurensi defensif dengan idempotensi Redis dan distributed locking yang mencegah pendebetan ganda. "
            "Ketiga, streaming event throughput tinggi dengan Kafka KRaft. "
            "Dan keempat, operasi rilis Blue-Green zero-downtime dengan barrier pengujian 95% dan observabilitas SRE lengkap. "
            "Terima kasih banyak atas waktu dan perhatiannya, dan saya siap menjawab pertanyaan teknis dari bapak/ibu sekalian.",
            [
                "Undang evaluator untuk mencoba dashboard live di https://indibank.aldianapps.com",
                "Tekankan tingkat kelulusan 100% pada 7 skenario verifikasi otomatis",
                "Ulangi empat pilar utama: konsistensi, keamanan konkurensi, streaming event, dan SRE"
            ],
            [
                ("Apa roadmap arsitektur berikutnya untuk sistem ini?", "Fase berikutnya adalah integrasi replikasi database active-active lintas region dengan Oracle GoldenGate, MirrorMaker 2 untuk Kafka antar-cluster, dan otentikasi mTLS dengan OAuth2/OIDC di API Gateway.")
            ],
            lang="id"
        )
    else:
        add_header(s10, "Live Demonstration & Summary", "Live Production Verification & Executive Summary")
        add_card(s10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "Live Production Endpoints", [
            ("Banking Dashboard", "https://indibank.aldianapps.com (Live interactive transfers and balance inquiries)."),
            ("Preview Test Domain", "https://test.indibank.aldianapps.com (Feature branch staging environment)."),
            ("Swagger / OpenAPI UI", "https://indibank.aldianapps.com/swagger-ui.html (Interactive contract explorer)."),
            ("Prometheus Telemetry", "https://indibank.aldianapps.com/actuator/prometheus (Real-time operational metrics)."),
            ("GitHub Repository", "Private repository with branch protection and complete CI/CD automation.")
        ], ACCENT_BLUE)
        add_card(s10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Verification Results (7/7)", [
            ("Scenario 1: Accounts Query", "PASSED - Active accounts fetched from live Oracle DB."),
            ("Scenario 2: Interbank Transfer", "PASSED - Real-time settlement with unique transaction reference."),
            ("Scenario 3: Idempotency Replay", "PASSED - Exact cached response returned without duplicate deduction."),
            ("Scenario 4: High-Value AML", "PASSED - Rp 150M transfer triggered Kafka fraud alert."),
            ("Scenario 5: Stream Ticker", "PASSED - Kafka topics verified via recent events API."),
            ("Scenario 6: Double-Entry Audit", "PASSED - Equal DEBIT and CREDIT journal lines verified."),
            ("Scenario 7: Balance Protection", "PASSED - Insufficient balance rejected with RFC 7807 error.")
        ], ACCENT_GREEN)
        add_card(s10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Executive Summary", [
            ("Financial Consistency", "Zero-Loss ledger invariance with strict double-entry bookkeeping and non-negative constraints."),
            ("Defensive Concurrency", "Idempotency state machine and distributed locking eliminating double-spending."),
            ("High-Throughput Streaming", "Kafka KRaft async decoupling and real-time AML fraud detection."),
            ("Zero-Downtime Operations", "Blue-Green production releases with sub-second rollback and 95% test coverage barrier."),
            ("Ready for Production", "Fully functional, deployed, and validated core banking transaction platform.")
        ], ACCENT_AMBER)
        set_speaker_notes(
            s10, "2 minutes",
            "To conclude, IndiBank Core Engine is not a theoretical prototype—it is a live, production-grade core banking engine running in Google Cloud right now. "
            "You can open `https://indibank.aldianapps.com` on your browser or phone to execute live interbank transfers, inspect the double-entry general ledger, and watch the real-time Kafka event ticker. "
            "Our automated verification suite tested all 7 key banking scenarios against live production, and every single scenario passed. "
            "To summarize what we've built: "
            "First, absolute financial consistency backed by double-entry accounting in Oracle 23c. "
            "Second, defensive concurrency with Redis idempotency and distributed locking preventing double debits. "
            "Third, high-throughput asynchronous event streaming with Kafka KRaft. "
            "And fourth, zero-downtime Blue-Green deployments backed by an enforced 95% test coverage barrier and full SRE observability. "
            "Thank you, and I look forward to taking your questions.",
            [
                "Invite evaluators to try the live dashboard at https://indibank.aldianapps.com",
                "Emphasize the 100% pass rate across the 7 verification scenarios",
                "Reiterate the core pillars: consistency, concurrency safety, event streaming, and SRE"
            ],
            [
                ("What would be your next architectural phase for this system?", 
                 "Phase two would introduce multi-region active-active database replication using Oracle GoldenGate, Kafka cross-cluster MirrorMaker 2, and tokenized API security using OAuth2 / OpenID Connect with mTLS at the edge gateway.")
            ],
            lang="en"
        )

    if not output_path:
        suffix = "_ID" if is_id else "_EN"
        output_path = f"docs/presentation/IndiBank_Core_Architecture_Presentation{suffix}.pptx"
        
    prs.save(output_path)
    print(f"Presentation ({lang.upper()}) saved to: {output_path}")

if __name__ == "__main__":
    # Generate English Deck
    build_deck(lang="en", output_path="docs/presentation/IndiBank_Core_Architecture_Presentation_EN.pptx")
    # Also save as default canonical deck
    build_deck(lang="en", output_path="docs/presentation/IndiBank_Core_Architecture_Presentation.pptx")
    # Generate Bahasa Indonesia Deck
    build_deck(lang="id", output_path="docs/presentation/IndiBank_Core_Architecture_Presentation_ID.pptx")
    print("All presentation decks (EN & ID) generated successfully!")
