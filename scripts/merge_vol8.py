#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_vol8.py — insert Playwright cover as page 0 of the ReportLab body PDF (Vol VIII)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/scripts/cover_vol8.pdf"
BODY = "/home/z/my-project/github_master/scripts/body_vol8.pdf"
OUT = "/home/z/my-project/github_master/download/The_Resolution_Programme_VIII_The_Abelianized_Rung.pdf"


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
        "/Title": "The Abelianized Rung and the T_k Classification — The Resolution Programme, Volume VIII",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "The two remaining links of Volume VII, discharged: the abelianized class as the intermediate rung where the transport fails by exactly the multinomial weights (the exact Parikh reduction, the forced-weight lemma, the localization theorem with the defect ratio rho(gamma) = sqrt(mu(gamma)), the spectral and rank-inflation laws, the atom classification and the budget obstruction), and the T_k classification beyond k = 0 (the homomorphism classification plus the isometric rigidity to the multiplicative gradings, the per-letter geometric family), with the sandwich measured honestly: closed on the graded class, open on the cell, strictly failed and witnessed on the two-axis amalgam.",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
