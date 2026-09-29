#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_vol12.py — insert Playwright cover as page 0 of the ReportLab
body PDF (Vol XII)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/github_repos/master/scripts/cover_vol12.pdf"
BODY = "/home/z/my-project/github_repos/master/scripts/body_vol12.pdf"
OUT = "/home/z/my-project/github_repos/master/download/The_Resolution_Programme_XII_The_Grand_Unification.pdf"


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
        "/Title": "The Grand Unification, Adjudicated Across All Works — The Resolution Programme, Volume XII",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "The adjudicated grand unification: the two external top-down syntheses read together and ruled claim by claim against the certified batteries; the missing work (f) retyped and delivered (the enrichment of Volume V, the defect calculus of Volume VII, the discrete viability shadow of Task 24, the intercept arithmetic); the two walls joined by the certified trade-off law (the corner+payment semialgebraic inequality with the mirror-sector certificate, the analytic patches of the core, the phase-gauged complex domain); the grand domain-by-face matrix with every cell ruled; and the open ledger at full scope.",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
