#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_bridges.py — insert Playwright cover as page 0 of the ReportLab body PDF (Vol II)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/scripts/cover_bridges.pdf"
BODY = "/home/z/my-project/scripts/body_bridges.pdf"
OUT = "/home/z/my-project/download/The_Resolution_Programme_II_The_Bridge_Theorems.pdf"


def normalize_page_to_a4(page):
    box = page.mediabox
    w, h = float(box.width), float(box.height)
    if abs(w - A4_W) > 0.2 or abs(h - A4_H) > 0.2:
        page.scale_to(A4_W, A4_H)
    return page


def main():
    writer = PdfWriter()
    cover_page = PdfReader(COVER).pages[0]
    writer.add_page(normalize_page_to_a4(cover_page))
    for page in PdfReader(BODY).pages:
        writer.add_page(normalize_page_to_a4(page))
    writer.add_metadata({
        "/Title": "The Bridge Theorems — The Resolution Programme, Volume II",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "Adjudication of the DeepSeek unification programme against the "
                    "corpus: the bridge theorems corrected, the two-step obstruction "
                    "chain, the enrichment prerequisite, and the two continuations.",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
