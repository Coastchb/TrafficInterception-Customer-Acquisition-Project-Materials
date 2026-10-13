#!/usr/bin/env python3
"""Audit the LIVE site against the local products/ source of truth."""
import html as ihtml
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_specs import FILES, PRODUCTS, parse_file, text_of  # noqa

LIVE = "/tmp/live2"
PAGES = {
    "S1": "s1.html", "A1": "a1.html", "X1": "x1.html", "RG": "rg.html",
    "FAYA": "faya.html", "DISP": "disp.html", "VEND": "vend.html",
}


def live_cards(fn):
    h = open(os.path.join(LIVE, fn), encoding="utf-8").read()
    m = re.search(r'<div class="specs-wrap" id="[^"]*">([\s\S]*?)\s*<script>', h)
    if not m:
        return None, []
    b = m.group(1)
    tabs = [text_of(x) for x in re.findall(r'<button class="stab[^"]*"[^>]*>([\s\S]*?)</button>', b)]
    out = []
    for cm in re.finditer(r'<div class="card[^"]*">([\s\S]*?)(?=<div class="card|<div class="spanel|$)', b):
        c = cm.group(1)

        def one(cls):
            mm = re.search(r'<div class="%s">([\s\S]*?)</div>' % cls, c)
            return text_of(mm.group(1)) if mm else ""

        out.append((one("lbl"), one("val"), one("sub")))
    return tabs, out


def local(key):
    tabs, panels = parse_file(os.path.join(PRODUCTS, FILES[key]))
    cards = []
    for t in tabs:
        for sec in panels.get(t["pid"], []):
            cards.extend((c["label"], c["value"], c.get("sub", "")) for c in sec["cards"])
    return [t["label"] for t in tabs], cards


def norm(s):
    return re.sub(r"\s+", " ", ihtml.unescape(s or "")).strip()


print("### 1. Spec tables: live vs products/")
bad = 0
for key, fn in PAGES.items():
    ltabs, lcards = local(key)
    ptabs, pcards = live_cards(fn)
    if ptabs is None:
        print("  %-5s ❌ no specs block on live page" % key)
        bad += 1
        continue
    ok_t = ltabs == ptabs
    if len(lcards) != len(pcards):
        print("  %-5s ❌ count local=%d live=%d" % (key, len(lcards), len(pcards)))
        bad += 1
        continue
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(lcards, pcards))
             if tuple(norm(x) for x in a) != tuple(norm(x) for x in b)]
    status = "✅" if ok_t and not diffs else "❌"
    print("  %-5s %s items=%d tabs=%d %s" % (key, status, len(pcards), len(ptabs),
                                             "" if ok_t else "TAB-DIFF %s vs %s" % (ltabs, ptabs)))
    for i, a, b in diffs[:6]:
        print("        #%d local=%s" % (i, a))
        print("            live=%s" % (b,))
    bad += len(diffs) + (0 if ok_t else 1)
print("  spec diffs:", bad)

print("\n### 2. Key facts on live pages")
facts = {
    "s1": ["$42,516.00", "6.0 × 3.8 × 2.8 meters"],
    "a1": ["$23,325.00", "5.5 × 3.5 × 2.8 meters"],
    "x1": ["$8,829.00", "5.5 × 3.5 × 2.8 meters"],
    "rg": ["$31,464.00", "Fully customizable to your space"],
    "faya": ["$9,384.00", "Fully customizable to your space"],
    "disp": ["$342.00", "0.6 × 0.2 × 0.3 m"],
    "vend": ["$4,830.00", "1.3 × 1.2 × 1.65 m"],
}
for k, needles in facts.items():
    h = open(os.path.join(LIVE, k + ".html"), encoding="utf-8").read()
    miss = [n for n in needles if n not in h]
    print("  %-5s %s %s" % (k, "✅" if not miss else "❌ missing=%s" % miss, needles))

print("\n### 3. Compare page rows")
h = open(os.path.join(LIVE, "compare.html"), encoding="utf-8").read()
i = h.find("Space required")
rows = re.findall(r"<tr>([\s\S]*?)</tr>", h[i:h.find("</table>", i)])
cells = [ihtml.unescape(re.sub(r"<[^>]+>", "|", r)).strip() for r in rows]
for c in cells[:2]:
    print("  ", re.sub(r"\|+", " | ", c)[:200])
