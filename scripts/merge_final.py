#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_final.py — insert Playwright cover as page 0 of the ReportLab body PDF."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/scripts/cover_resolution.pdf"
BODY = "/home/z/my-project/scripts/body_resolution.pdf"
OUT = "/home/z/my-project/download/The_Resolution_Programme_Grand_Unified_Picture.pdf"


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
        "/Title": "The Resolution Programme — The Grand Unified Picture of the Corpus",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "Grand unified synthesis of the research corpus: constrained "
                    "realizability across causal descent, bounded transduction, "
                    "quantum interfaces, biology, governance, and AI.",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
