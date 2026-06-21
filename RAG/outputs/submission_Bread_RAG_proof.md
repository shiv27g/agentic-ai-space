# RAG Ingestion Proof — Bread documents

- **Name:** Siva
- **Documents processed:**
  - RAG/test_documents/Bread_Annual_Report_2026.pdf
  - RAG/test_documents/Bread_Earnings_Call_Q1_2026.pdf

- **Extraction issue I caught:**
  - The naive extraction (pypdf) flattens layout, producing many very short lines
    and split words (e.g., `effecti\nve`), which indicates flattened tables/columns
    and risks creating confidently-wrong chunks. Structured extraction (pdfplumber)
    preserves columns and recovers tables as atomic units, reducing split words and
    short-line counts.

- **Chunks + metadata (5 examples from the Annual Report):**

1. chunk_id: `Bread_Annual_Report_2026_p1_2025_000_e4c25d` — page 1 — section: `2025`
   - content (excerpt): "Annual\nReport\nBread\nFinancial\n|"
   - Query it answers: "What is the document title and year?"
   - Short answer: "2025 Annual Report — Bread Financial"

2. chunk_id: `Bread_Annual_Report_2026_p3_dear-bread-financial_000_a1dd17` — page 3 — section: `Dear Bread Financial`
   - content (excerpt): "Stakeholders\nOur 2025 financial results reflect disciplined execution,"
   - Query it answers: "How did management summarize 2025 results?"
   - Short answer: "Management described 2025 as reflecting disciplined execution."

3. chunk_id: `Bread_Annual_Report_2026_p3_2025-business-driver_000_35dc7e` — page 3 — section: `2025 Business Drivers`
   - content (excerpt): "financial resilience, and meaningful progress across\nIn 2025, consumer financial health remained resilient,\nour strategic priorities..."
   - Query it answers: "What were the main business drivers in 2025?"
   - Short answer: "Resilient consumer financial health, strategic priorities driving credit sales growth, and focus on deposits and partnerships."

4. chunk_id: `Bread_Annual_Report_2026_p3_2025-business-driver_001_f149be` — page 3 — section: `2025 Business Drivers`
   - content (excerpt): "ormance metrics, optimizing our capital structure, brand partners by signing and renewing programs..."
   - Query it answers: "Which partner additions or renewals were highlighted?"
   - Short answer: "Notable partners include Bed Bath & Beyond, Raymour & Flanagan, Vivint, and crypto.com."

5. chunk_id: `Bread_Annual_Report_2026_p3_2025-business-driver_002_b9f4bd` — page 3 — section: `2025 Business Drivers`
   - content (excerpt): "our & Flanagan, Vivint, and crypto.com. The multi- and positive outlooks from leading rating agencies."
   - Query it answers: "What was said about credit ratings or outlooks?"
   - Short answer: "The company noted positive outlooks from leading rating agencies."

- **Files produced:**
  - Chunks JSON (annual report): [RAG/outputs/chunks_Bread_Annual_Report_2026.json](RAG/outputs/chunks_Bread_Annual_Report_2026.json)
  - Chunks JSON (earnings call): [RAG/outputs/chunks_Bread_Earnings_Call_Q1_2026.json](RAG/outputs/chunks_Bread_Earnings_Call_Q1_2026.json)
  - Extraction comparison screenshot: [RAG/outputs/extraction_Bread_Annual_Report_2026.png](RAG/outputs/extraction_Bread_Annual_Report_2026.png)

## 5-line reflection

1. I processed `Bread_Annual_Report_2026.pdf` and `Bread_Earnings_Call_Q1_2026.pdf`.
2. Naive extraction flattened columns/tables, producing many very short lines and split words; structured extraction recovered table rows and reduced those errors.
3. Chunks are retrieval-ready because they respect section headings, keep tables atomic (label:value rows), and use recursive splitting to avoid chopping sentences.
4. Preserved metadata: `source`, `page`, `section`, `chunk_id`, `chunk_index`, and `char_len` (see JSON files).
5. Bad extraction or chunking would create confidently-wrong chunks (mixed columns or split sentences), leading to bad embeddings and unreliable retrieval answers.

## Quick QA examples (question → best chunk → short answer)

- Q: "What is the document title?" → `Bread_Annual_Report_2026_p1_2025_000_e4c25d` → "2025 Annual Report — Bread Financial"
- Q: "How did management summarize 2025 results?" → `Bread_Annual_Report_2026_p3_dear-bread-financial_000_a1dd17` → "Reflect disciplined execution."
- Q: "Which partners were added in 2025?" → `Bread_Annual_Report_2026_p3_2025-business-driver_001_f149be` → "Bed Bath & Beyond, Raymour & Flanagan, Vivint, crypto.com."

---

Place this file or the screenshot/JSON links in the cohort WhatsApp as your proof (or paste a GitHub link). Replace **YOUR NAME HERE** with your name before posting.

## Assignment Questions (explicit Q&A)

1. What document did I process?

- Answer: `Bread_Annual_Report_2026.pdf` and `Bread_Earnings_Call_Q1_2026.pdf` (paths shown above).

2. What extraction issue did I find?

- Answer: The naive extractor flattened columns and tables, producing many very short lines and split words (e.g., `effecti\nve`). This creates noisy, confidently-wrong chunks. The structured extractor (pdfplumber) preserves columns and recovers tables as atomic rows, reducing those failures.

3. What makes my chunks retrieval-ready?

- Answer: Chunks are section-aware (headings kept with their paragraphs), tables are kept atomic and rendered as label:value rows, and recursive splitting respects paragraph/sentence boundaries to avoid chopping meaning.

4. What metadata did I preserve?

- Answer: Each chunk includes `source`, `page`, `section`, `chunk_id`, `chunk_index`, `char_len`, and `document_type` (the JSON files also contain `global_index`).

5. Why would bad extraction or bad chunking break retrieval later?

- Answer: Bad extraction produces corrupted text (mixed columns, split sentences) that creates wrong or partial chunks; those chunks lead to poor embeddings and therefore wrong retrieval results and higher hallucination risk.
