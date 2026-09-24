#!/usr/bin/env python3
"""
IndiBank Core Transaction & Ledger Engine - Slide Deck Generator
Generates a widescreen (16:9) executive presentation (.pptx)
with dark enterprise banking styling, structured layouts, and speaker notes.
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
    """Sets a solid deep navy background."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, category, title):
    """Adds standard category badge and slide title."""
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
    """Adds a dark slate container card with structured content."""
    # Shape
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = CARD_BORDER
    shape.line.width = Pt(1)
    
    # Card Header
    header_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.45))
    tf_h = header_box.text_frame
    tf_h.word_wrap = True
    p_h = tf_h.paragraphs[0]
    p_h.text = title
    p_h.font.name = FONT_HEADING
    p_h.font.size = Pt(14)
    p_h.font.bold = True
    p_h.font.color.rgb = accent
    
    # Card Content
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

def set_speaker_notes(slide, timing, script, key_points, anticipated_qa):
    """Attaches complete speaker notes to the slide."""
    notes_tf = slide.notes_slide.notes_text_frame
    notes_tf.text = f"⏱ ESTIMATED TIMING: {timing}\n\n"
    notes_tf.text += f"🎙 TALKING SCRIPT:\n{script}\n\n"
    notes_tf.text += "📌 KEY HIGHLIGHTS TO EMPHASIZE:\n"
    for kp in key_points:
        notes_tf.text += f"- {kp}\n"
    notes_tf.text += "\n💡 ANTICIPATED TECHNICAL Q&A:\n"
    for q, a in anticipated_qa:
        notes_tf.text += f"Q: {q}\nA: {a}\n\n"

# ==========================================
# PRESENTATION GENERATOR
# ==========================================
def build_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # -------------------------------------------------------------
    # SLIDE 0: TITLE SLIDE
    # -------------------------------------------------------------
    s0 = prs.slides.add_slide(blank_layout)
    apply_background(s0)
    
    # Title badge
    t_box = s0.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(0.5))
    tf = t_box.text_frame
    p = tf.paragraphs[0]
    p.text = "ENTERPRISE CORE BANKING ARCHITECTURE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    
    # Main Title
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
    p2_sub.text = "Production Architecture, Defensive Concurrency, & Zero-Loss Financial Integrity"
    p2_sub.font.name = FONT_HEADING
    p2_sub.font.size = Pt(18)
    p2_sub.font.color.rgb = ACCENT_BLUE
    p2_sub.space_before = Pt(8)
    
    # Tech stack banner
    banner = s0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.333), Inches(1.4))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = CARD_BORDER
    
    b_tf = banner.text_frame
    b_tf.word_wrap = True
    bp1 = b_tf.paragraphs[0]
    bp1.text = "TECHNOLOGY STACK & CLOUD PLATFORM"
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
    
    # Presenter info
    auth_box = s0.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.3), Inches(1.0))
    a_tf = auth_box.text_frame
    ap1 = a_tf.paragraphs[0]
    ap1.text = "Presenter: Aldian Fazrihady"
    ap1.font.name = FONT_HEADING
    ap1.font.size = Pt(14)
    ap1.font.bold = True
    ap1.font.color.rgb = TEXT_MAIN
    
    ap2 = a_tf.add_paragraph()
    ap2.text = "Lead Platform & Distributed Systems Engineer | Spec-Driven Development Showcase"
    ap2.font.name = FONT_BODY
    ap2.font.size = Pt(12)
    ap2.font.color.rgb = TEXT_MUTED
    
    set_speaker_notes(
        s0,
        "1.5 minutes",
        "Good morning/afternoon everyone. Today I'm excited to present the IndiBank Core Transaction and Ledger Engine. "
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 1: BUSINESS CONTEXT & BANKING CHALLENGES
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
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
        s1,
        "2 minutes",
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 2: ARCHITECTURAL BLUEPRINT
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
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
        s2,
        "2 minutes",
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 3: DEFENSIVE CONCURRENCY & ZERO-LOSS GUARANTEES
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
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
        s3,
        "2 minutes",
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 4: EVENT STREAMING & AML FRAUD SCREENING
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
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
        s4,
        "1.5 minutes",
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 5: SPEC-DRIVEN DEVELOPMENT (SDD)
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
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
        s5,
        "1.5 minutes",
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 6: QUALITY ENGINEERING & TESTING PYRAMID
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Quality Assurance & Coverage Barrier", "3-Tier Testing Pyramid & JaCoCo Coverage Barrier")
    
    add_card(s6, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "Tier 1: Unit Test Suite", [
        ("Domain & Business Logic", "Comprehensive unit tests covering TransferService, AccountService, and IdempotencyService."),
        ("Isolated Mocking", "Mockito verification of Redis lock acquisition, Lua release, and Oracle transaction rollback."),
        ("Negative & Edge Cases", "Exhaustive tests for zero balances, transfer to self, and currency mismatch."),
        ("Kafka Producer & Consumer", "Verified event publication, fraud rule triggering, and DLQ dispatching.")
    ], ACCENT_BLUE)
    
    add_card(s6, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Tier 2: WebMvc Integration", [
        ("MockMvc HTTP Verification", "@WebMvcTest testing TransferController and AccountController in isolated web slice."),
        ("Header & Bean Validation", "Tests required Idempotency-Key header, @Pattern 10-digit check, and @DecimalMax limits."),
        ("Global Exception Mapping", "Verifies automatic mapping to RFC 7807 HTTP 400, 404, 409, and 422 status codes."),
        ("DTO JSON Serialization", "Ensures ISO-8601 timestamps, BigDecimal precision, and response headers.")
    ], ACCENT_AMBER)
    
    add_card(s6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Tier 3: Live End-to-End E2E", [
        ("Live GKE Execution", "test-scenarios.sh runs 7 real-world banking journeys against live production and preview domains."),
        ("Scenario 1: Accounts Query", "Queries initial balances from live Oracle DB."),
        ("Scenario 2 & 3: Idempotency", "Executes transfer, then replays exact same key to verify identical cached receipt."),
        ("Scenario 4 & 5: AML Kafka", "Executes Rp 150M transfer and verifies live Kafka fraud alert stream ticker."),
        ("Scenario 6 & 7: Audit & Limits", "Verifies Oracle double-entry journal balance and insufficient balance 422 error.")
    ], ACCENT_GREEN)
    
    # Bottom banner for JaCoCo metrics
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
        s6,
        "2 minutes",
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 7: SRE & OBSERVABILITY
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
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
        s7,
        "2 minutes",
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 8: ZERO-DOWNTIME CI/CD & BLUE-GREEN CUTOVER
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
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
        s8,
        "2 minutes",
        "Our release pipeline guarantees zero-downtime deployments and safe blast-radius containment. "
        "First, direct pushes to `main` are strictly blocked via GitHub Branch Protection with admin enforcement. Every change requires a feature branch and pull request. "
        "Second, when a feature branch is pushed, our CI/CD pipeline deploys a preview container to `https://test.indibank.aldianapps.com`. "
        "This allows engineers and testers to verify changes on a live domain before merging. "
        "Third, when the PR merges to `main`, our Blue-Green deployment pipeline automatically deploys the new image to the standby slot (say, green), "
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 9: MULTI-PLATFORM PORTABILITY
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
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
        s9,
        "1.5 minutes",
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
        ]
    )

    # -------------------------------------------------------------
    # SLIDE 10: LIVE PRODUCTION DEMO & SUMMARY
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
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
        s10,
        "2 minutes",
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
        ]
    )

    output_path = "docs/presentation/IndiBank_Core_Architecture_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    build_deck()
