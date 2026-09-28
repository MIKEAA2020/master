#!/usr/bin/env python3
"""Screenshot an HTML diagram at 2x device scale (the skill's diagram pipeline)."""
import sys
from playwright.sync_api import sync_playwright

html_path, out_png = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1000, "height": 600}, device_scale_factor=2)
    page.goto("file://" + html_path)
    page.wait_for_timeout(1200)          # font load
    el = page.query_selector(".diagram")
    el.screenshot(path=out_png)
    b.close()
print("saved", out_png)
