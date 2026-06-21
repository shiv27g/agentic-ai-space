import argparse
import textwrap
from pathlib import Path

from ragkit import extract_naive, extract_structured


def render_side_by_side(left, right, out_path, title_left="NAIVE", title_right="STRUCTURED",
                        width=800, padding=20, font=None):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception as e:
        raise RuntimeError("Pillow is required to render images. Install with 'pip install pillow'")

    # choose font
    try:
        f = ImageFont.load_default() if font is None else ImageFont.truetype(font, 12)
    except Exception:
        f = ImageFont.load_default()

    col_w = (width - padding * 3) // 2
    left_lines = []
    for line in left.splitlines():
        left_lines.extend(textwrap.wrap(line, col_w // 8) or [""])
    right_lines = []
    for line in right.splitlines():
        right_lines.extend(textwrap.wrap(line, col_w // 8) or [""])

    lines = max(len(left_lines), len(right_lines))
    # measure line height using a temporary draw (font.getsize may not be present)
    # compute line height: prefer font.getmetrics(), fallback to textbbox
    try:
        ascent, descent = f.getmetrics()
        line_h = ascent + descent + 2
    except Exception:
        temp_img = Image.new("RGB", (10, 10), "white")
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), "A", font=f)
        line_h = (bbox[3] - bbox[1]) + 2
    img_h = padding * 2 + line_h * (lines + 2)

    img = Image.new("RGB", (width, img_h), "white")
    d = ImageDraw.Draw(img)

    # titles
    d.text((padding, padding), title_left, fill="black", font=f)
    d.text((padding * 2 + col_w, padding), title_right, fill="black", font=f)

    y = padding + line_h * 2
    for i in range(lines):
        lx = left_lines[i] if i < len(left_lines) else ""
        rx = right_lines[i] if i < len(right_lines) else ""
        d.text((padding, y), lx, fill="black", font=f)
        d.text((padding * 2 + col_w, y), rx, fill="black", font=f)
        y += line_h

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True, help="PDF path")
    ap.add_argument("--out", default="RAG/outputs/extraction_compare.png")
    args = ap.parse_args()

    naive_pages = extract_naive(args.doc)
    struct_pages = extract_structured(args.doc)

    # choose a representative page: last page (most likely has two-column issues)
    left = naive_pages[-1].text if naive_pages else ""
    right = struct_pages[-1].text if struct_pages else ""

    render_side_by_side(left, right, args.out)
    print(f"Saved comparison image to {args.out}")


if __name__ == '__main__':
    main()
