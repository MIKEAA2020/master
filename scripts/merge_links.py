#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_links.py — insert Playwright cover as page 0 of the ReportLab body PDF (Vol V)."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/github_master/scripts/cover_links.pdf"
BODY = "/home/z/my-project/github_master/scripts/body_links.pdf"
OUT = "/home/z/my-project/github_master/download/The_Resolution_Programme_V_The_Remaining_Open_Links.pdf"


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
        "/Title": "The Remaining Open Links — The Resolution Programme, Volume V",
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": "The remaining open links of the Resolution Programme, attacked "
                    "in order: BT3's enrichment construction (the cost-enriched graded "
                    "category of interfaces, built), BT2's equality (the graded "
                    "small-gain law, closed on the computed class), and Risk 3 (the "
                    "RockSample benchmark confrontation).",
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
