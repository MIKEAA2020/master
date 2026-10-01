#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_vol14.py — insert Playwright cover as page 0 of the ReportLab
body PDF (Vol XIV).  Metadata: the post-far-field state, decided."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

COVER = "/home/z/my-project/github_repos/master/scripts/cover_vol14.pdf"
BODY = "/home/z/my-project/github_repos/master/scripts/body_vol14.pdf"
OUT = ("/home/z/my-project/github_repos/master/download/"
       "The_Resolution_Programme_XIV_The_Post_Far_Field_State.pdf")


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
        "/Title": ("The Post-Far-Field State: the Grind Certified, the "
                   "Boundary Decided, and the Method Itself Measured — "
                   "The Resolution Programme, Volume XIV"),
        "/Author": "Z.ai",
        "/Creator": "Z.ai",
        "/Subject": ("The post-far-field state recorded and decided: the "
                     "grind rule-stopped by its own census (the wall arm "
                     "STOP, the cover arm HOLD; 29,924,011 + 346,400 "
                     "certificates standing, the residue priced and "
                     "declined, every measured center above lambda*); the "
                     "seed-level boundary closed as a LAW by the "
                     "programme's first pre-registered experiment (the "
                     "scope law, TOST-replicated) with the commissioned "
                     "dose-response pool decided — the cliff absolute (err "
                     "= 1.000 at 44-48/49, 2160/2160 failed, train "
                     "accuracy 1.0000, wrong-confidence 0.749) while E's "
                     "coverage dose runs monotone (0.5699 to 0.5491, "
                     "Spearman 0.899); the method itself measured; the "
                     "synthesis statement in final form with the "
                     "unification map's final face; the ledger at zero "
                     "open mathematical links."),
    })
    with open(OUT, "wb") as f:
        writer.write(f)
    n = len(PdfReader(OUT).pages)
    print("OK merged:", OUT, "pages:", n)


if __name__ == "__main__":
    main()
