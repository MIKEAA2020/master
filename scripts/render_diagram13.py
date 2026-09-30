#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_diagram13.py — screenshot the Vol XIII unification map HTML to
PNG at 2x device scale (the corpus's diagram route)."""
from playwright.sync_api import sync_playwright

SRC = ("/home/z/my-project/github_repos/master/download/sources/"
       "diagram_vol13.html")
OUT = ("/home/z/my-project/github_repos/master/download/figures/"
       "unification_map_vol13.png")

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1040, "height": 900},
                      device_scale_factor=2)
    page.goto("file://" + SRC)
    page.wait_for_timeout(1200)          # fonts
    d = page.query_selector(".diagram")
    d.screenshot(path=OUT)
    b.close()
print("OK:", OUT)
