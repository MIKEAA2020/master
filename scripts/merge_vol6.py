#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_vol6.py — insert Playwright cover as page 0 of the ReportLab body PDF (Vol VI)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/github_master/scripts/cover_vol6.pdf"
BODY = "/home/z/my-project/github_master/scripts/body_vol6.pdf"
OUT = "/home/z/my-project/github_master/download/The_Resolution_Programme_VI_The_Dictionary.pdf"


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
        "/Title": "The Dictionary — The Resolution Programme, Volume VI",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "BT1a attacked inside the enrichment: the dictionary-plus-recovery "
                    "theorem stated as a morphism of sheaves on the budget lattice, its "
                    "six clauses proved, the recovery audited at 600/600, and the corpus "
                    "confronted on the quantum strobe's rank law and RockSample's "
                    "compression break.",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
