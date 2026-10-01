#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_vol13.py — insert Playwright cover as page 0 of the ReportLab
body PDF (Vol XII)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/github_repos/master/scripts/cover_vol13.pdf"
BODY = "/home/z/my-project/github_repos/master/scripts/body_vol13.pdf"
OUT = "/home/z/my-project/github_repos/master/download/The_Resolution_Programme_XIII_The_Three_Closures_and_the_Escape_Quantified.pdf"


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
        "/Title": "The Three Closures, the Escape Retracted, and the Walls Certified Symmetric — The Resolution Programme, Volume XIII (Second Edition)",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "The consolidation of the three closures and the escape quantified and re-adjudicated (the first edition) — and the corrigendum record through Task 40: the escape retracted (the shadow-equality restored in the closure sense), the two walls certified symmetric (the BDC corner identities on the abelian face, the word-power partial-sum sandwiches on the free face, both at zero stalls), the tail structural law, the gradient-split corollary refuted, and the critical locus closed tight at sqrt(lambda*).",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
