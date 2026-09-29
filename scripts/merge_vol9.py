#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_vol9.py — insert Playwright cover as page 0 of the ReportLab body PDF (Vol IX)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/github_repos/master/scripts/cover_vol9.pdf"
BODY = "/home/z/my-project/github_repos/master/scripts/body_vol9.pdf"
OUT = "/home/z/my-project/github_repos/master/download/The_Resolution_Programme_IX_The_Sandwich_Locus.pdf"


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
        "/Title": "The Sandwich Locus — The Resolution Programme, Volume IX, Second Edition",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "Second edition: the original three links discharged (the amalgam closed form with the retraction, the lens criterion, the first-shell map) plus the cell's D(2) closed at sqrt(lambda*) with its cubic minimal polynomial and global certificate; the corner-reduction strictness chain (the parity-odd shell theorem, the 1-D closure discovery, the trade-off); the complex and affine identity completions with the phase gauge; and the empirical face integrated (the three experiments and the it-and-bit-from-record synthesis).",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
