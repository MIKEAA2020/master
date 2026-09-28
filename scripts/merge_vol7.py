#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_vol7.py — insert Playwright cover as page 0 of the ReportLab body PDF (Vol VII)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/github_master/scripts/cover_vol7.pdf"
BODY = "/home/z/my-project/github_master/scripts/body_vol7.pdf"
OUT = "/home/z/my-project/github_master/download/The_Resolution_Programme_VII_The_Multiletter_Analytic_Theorem.pdf"


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
        "/Title": "The Multiletter Analytic Theorem — The Resolution Programme, Volume VII",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "The multiletter analytic theorem in full: the six demands of the "
                    "full-proof order discharged — the partial realization "
                    "characterization, the uniform 2-eps law in general norms, the "
                    "graded Fliess theorem, the multiletter AAK equality on the exact "
                    "class of level-constant symbols with the golden-ratio witness, "
                    "the norm-universal wall, the enriched naturality, and the global "
                    "sheaf morphism — with the off-class boundary stated honestly as "
                    "the open nc-AAK problem.",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
