#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_vol10.py — insert Playwright cover as page 0 of the ReportLab body PDF (Vol X)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/scripts/cover_vol10.pdf"
BODY = "/home/z/my-project/github_master/scripts/body_vol10.pdf"
OUT = "/home/z/my-project/github_master/download/The_Resolution_Programme_X_The_Rank_Defect_Theorem.pdf"


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
        "/Title": "The Rank-Defect Theorem — The Resolution Programme, Volume X",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "The rank-defect theorem beyond the ring: the classification of the arrow-rank equivalence (soundness, the two failure modes, the N-ring rank-doubling law, the one-way valve, the reflection-laundering theorem), and the chat's Experiments 1-3 audited (spectral compression, sensor coarsening, sheaf diagnostics)."
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
