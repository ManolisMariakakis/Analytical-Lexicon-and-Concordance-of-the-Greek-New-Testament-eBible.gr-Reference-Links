# ---------------------------------------------------------------------------
# Project: Analytical Lexicon and Concordance of the Greek New Testament
#          – Bible Reference Linking Tool
#
# Description:
# This script adds interactive Bible reference hyperlinks to a PDF file of the
# work "Analytical Lexicon and Concordance of the Greek New Testament".
# Detected references (e.g. Mt 7:3, Lk 6:14, Jn 1:19–23) are converted into
# clickable links pointing to the ebible.gr website.
#
# The generated links lead to a Textual Criticism and Manuscript Collation
# interface, where Greek New Testament manuscripts are compared verse by verse,
# highlighting textual variants between early witnesses and modern critical
# editions. The linked pages also include three modern Greek translations to
# support clearer understanding of the ancient Greek text.
#
# Creator / Maintainer:
# Manolis Mariakakis
#
# Source Text:
# Analytical Lexicon and Concordance of the Greek New Testament
# Copyright © 2025 by Alan Bunning
# Center for New Testament Restoration
# January 28, 2025 electronic edition
#
# License (Source Text):
# Creative Commons Attribution–ShareAlike 4.0 International License (CC BY-SA 4.0)
# Attribution must be given to Alan Bunning and the Center for New Testament
# Restoration, and any changes must be clearly indicated.
#
# Note:
# This repository contains code only. The original PDF is not distributed.
# The script is intended for academic, educational, and research use.
#
# ---------------------------------------------------------------------------

import re
import fitz  # PyMuPDF
import statistics

SRC_PDF = r"ALC.pdf"
OUT_PDF = r"ALC_ebible_links.pdf"

abbr_to_code = {
    "Mt": "mat", "Mat": "mat",
    "Mk": "mrk", "Mrk": "mrk",
    "Lk": "luk", "Luk": "luk",
    "Jn": "jhn", "Jhn": "jhn",
    "Act": "act",
    "Rom": "rom",
    "1Co": "1co", "2Co": "2co",
    "Gal": "gal", "Eph": "eph", "Php": "php", "Col": "col",
    "1Th": "1th", "2Th": "2th",
    "1Ti": "1ti", "2Ti": "2ti", "Tit": "tit", "Phm": "phm",
    "Heb": "heb", "Jas": "jas",
    "1Pe": "1pe", "2Pe": "2pe",
    "1Jn": "1jn", "2Jn": "2jn", "3Jn": "3jn",
    "Jud": "jud",
    "Rev": "rev",
}

alt = "|".join(sorted(map(re.escape, abbr_to_code.keys()), key=len, reverse=True))

# token-level strict matches
full_re = re.compile(
    rf"^(?P<book>{alt})\s*(?P<chap>\d+)(?::(?P<v1>\d+)(?:-(?P<v2>\d+))?)?$"
)
chapverse_re = re.compile(r"^(?P<chap>\d+):(?P<v1>\d+)(?:-(?P<v2>\d+))?$")
verseonly_re = re.compile(r"^(?P<v1>\d+)(?:-(?P<v2>\d+))?$")

# Superscript digits (¹²³ and ⁰⁴⁵⁶⁷⁸⁹). Used to ignore footnote markers like 6:14³⁵
SUPDIG_RE = re.compile(r"[\u00B9\u00B2\u00B3\u2070\u2074-\u2079]+")

# token finder within line_text
token_re = re.compile(
    rf"\b(?:{alt})\b\s*\d+(?::\d+(?:-\d+)?)?(?:[\u00B9\u00B2\u00B3\u2070\u2074-\u2079]+)?"
    r"|\b\d+:\d+(?:-\d+)?(?:[\u00B9\u00B2\u00B3\u2070\u2074-\u2079]+)?"
    r"|\b\d+(?:-\d+)?(?:[\u00B9\u00B2\u00B3\u2070\u2074-\u2079]+)?\b"
)

def make_url(book_code, chap, v1=None, v2=None):
    if v1 is None:
        return f"https://ebible.gr/collate/{book_code}.{chap}"
    if v2 is not None:
        return f"https://ebible.gr/collate/{book_code}.{chap}.{v1}-{v2}"
    return f"https://ebible.gr/collate/{book_code}.{chap}.{v1}"

def union_rect(rects):
    rr = None
    for r in rects:
        rr = r if rr is None else (rr | r)
    return rr

def line_chars_from_rawdict(page):
    """
    Yield lines as list of char records (per-character bbox + span font size).
    """
    d = page.get_text("rawdict")
    for b_idx, block in enumerate(d.get("blocks", [])):
        if block.get("type") != 0:
            continue
        for l_idx, line in enumerate(block.get("lines", [])):
            out = []
            for span in line.get("spans", []):
                size = float(span.get("size", 0.0) or 0.0)
                for ch in span.get("chars", []):
                    c = ch.get("c", "")
                    rect = fitz.Rect(ch.get("bbox"))
                    out.append({
                        "c": c,
                        "rect": rect,
                        "size": size,
                        "block_no": b_idx,
                        "line_no": l_idx
                    })
            yield out

def build_line_text_and_map(chars, sup_ratio=0.85):
    """
    Build line_text from chars while removing superscript digits by font size.
    Returns: line_text, char_rects, meta
    """
    sizes = [x["size"] for x in chars if x["c"].strip() and x["size"]]
    base = statistics.median(sizes) if sizes else 0.0

    line_text_parts = []
    char_rects = []
    removed_sup = 0

    for x in chars:
        c = x["c"]
        if c == "":
            continue

        # drop brackets always (covers [05])
        if c in "[]":
            removed_sup += 1
            continue

        is_digit = c.isdigit()
        is_small = (base > 0 and x["size"] < sup_ratio * base)

        if is_small and is_digit:
            removed_sup += 1
            continue

        line_text_parts.append(c)
        char_rects.append(x["rect"])

    line_text = "".join(line_text_parts)
    return line_text, char_rects, {"base_size": base, "removed_sup_chars": removed_sup}

def rect_for_span_chars(char_rects, s, e):
    rects = char_rects[s:e]
    if not rects:
        return None
    rr = union_rect(rects)
    if rr is None:
        return None
    return fitz.Rect(rr.x0 - 0.3, rr.y0 - 0.3, rr.x1 + 0.3, rr.y1 + 0.3)

def inherits_context_at(line_text, start_idx):
    """
    Allow context inheritance if token is at beginning of line
    or preceded by delimiter (, ;).
    This fixes line-wrap cases like:
      ... Mt 1:8,
      11, 21:6 ...
    or
      ... Mt 13:17,
      18,19 ...
    """
    j = start_idx - 1
    while j >= 0 and line_text[j].isspace():
        j -= 1
    if j < 0:
        return True
    return line_text[j] in {",", ";"}  # treat line-break as implicit delimiter

def add_links(doc):
    logged = 0
    total_added = 0

    # ✅ GLOBAL context across lines (and pages)
    ctx_book = None
    ctx_chap = None

    for pno in range(len(doc)):
        page = doc[pno]

        for chars in line_chars_from_rawdict(page):
            if not chars:
                continue

            block_no = chars[0]["block_no"]
            line_no = chars[0]["line_no"]

            line_text, char_rects, meta = build_line_text_and_map(chars, sup_ratio=0.85)

            # ✅ Start line with previous context
            current_book = ctx_book
            current_chap = ctx_chap

            # Process tokens in this line
            for m in token_re.finditer(line_text):
                token = m.group(0)
                s, e = m.span()
                token_clean = SUPDIG_RE.sub("", token)

                url = None
                rule = None

                fm = full_re.match(token_clean)
                if fm:
                    code = abbr_to_code.get(fm.group("book"))
                    if not code:
                        continue
                    chap = int(fm.group("chap"))
                    v1 = fm.group("v1")
                    v2 = fm.group("v2")

                    current_book = code
                    current_chap = chap
                    rule = "FULL"

                    if v1 is None:
                        url = make_url(code, chap)
                    else:
                        url = make_url(code, chap, int(v1), int(v2) if v2 else None)

                else:
                    cv = chapverse_re.match(token_clean)
                    if cv and current_book:
                        chap = int(cv.group("chap"))
                        v1 = int(cv.group("v1"))
                        v2 = int(cv.group("v2")) if cv.group("v2") else None

                        current_chap = chap
                        rule = "CHAP:VERSE"
                        url = make_url(current_book, chap, v1, v2)

                    else:
                        vo = verseonly_re.match(token_clean)
                        if vo and current_book and current_chap and inherits_context_at(line_text, s):
                            # ✅ verse-only can inherit at start-of-line too
                            v1 = int(vo.group("v1"))
                            v2 = int(vo.group("v2")) if vo.group("v2") else None
                            rule = "VERSE_ONLY_INHERIT"
                            url = make_url(current_book, current_chap, v1, v2)

                if not url:
                    continue

                rr = rect_for_span_chars(char_rects, s, e)
                if not rr:
                    continue

                page.insert_link({"kind": fitz.LINK_URI, "from": rr, "uri": url, "is_external": True})
                total_added += 1

            # ✅ Save context for NEXT line (only if we learned something)
            if current_book is not None:
                ctx_book = current_book
            if current_chap is not None:
                ctx_chap = current_chap

    return total_added

def main():
    doc = fitz.open(SRC_PDF)
    total = add_links(doc)

    doc.save(OUT_PDF, deflate=True)
    doc.close()
    print(f"Done. Links added: {total}")
    print(f"Output: {OUT_PDF}")

if __name__ == "__main__":
    main()
