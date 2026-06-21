import json
import os
from pathlib import Path

from ragkit import extract_structured, records_from_pages


def generate_for(path, max_chunks=10, out_dir="RAG/outputs"):
    pages = extract_structured(path)
    records = records_from_pages(pages)
    selected = records[:max_chunks]
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    base = Path(path).stem
    fn = out_path / f"chunks_{base}.json"
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(selected, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(selected)} chunks to {fn}")
    for r in selected:
        print(f"- {r['chunk_id']} (page {r['page']} section={r['section']} len={r['char_len']})")
    return fn


def main():
    docs = [
        "test_documents/Bread_Annual_Report_2026.pdf",
        "test_documents/Bread_Earnings_Call_Q1_2026.pdf",
    ]
    outputs = []
    for d in docs:
        if not os.path.exists(d):
            print(f"Missing: {d}")
            continue
        outputs.append(generate_for(d))
    print("Done.")


if __name__ == '__main__':
    main()
