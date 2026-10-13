#!/usr/bin/env python3
"""Full sync: products/*.html (source of truth) -> website/index.html specs data.

Rewrites the SPECS_DATA_START..SPECS_DATA_END block in website/index.html with
data parsed straight from the local product spec files, so the live site and the
local product sheets are word-for-word identical.
"""
import html as ihtml
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS = os.path.join(ROOT, "products")
INDEX = os.path.join(ROOT, "website", "index.html")

# ---------------------------------------------------------------- tabler -> FA
TI2FA = {
    "eye": "fa-eye", "cpu": "fa-microchip", "target": "fa-bullseye", "leaf": "fa-leaf",
    "gift": "fa-gift", "world": "fa-globe", "users": "fa-users", "tournament": "fa-trophy",
    "server": "fa-server", "school": "fa-graduation-cap", "rotate": "fa-rotate",
    "robot": "fa-robot", "map": "fa-map", "headset": "fa-headset", "golf": "fa-golf-ball",
    "flag": "fa-flag", "device-gamepad": "fa-gamepad", "cloud-upload": "fa-cloud-arrow-up",
    "cloud": "fa-cloud", "clock": "fa-clock", "chart-line": "fa-chart-line",
    "camera": "fa-camera", "brand-nvidia": "fa-microchip",
    "arrows-left-right": "fa-arrow-right-arrow-left", "tools": "fa-screwdriver-wrench",
    "sun": "fa-sun", "photo": "fa-image", "maximize": "fa-expand",
    "layers-subtract": "fa-layer-group", "hand-click": "fa-hand-pointer",
    "grid-dots": "fa-grip", "focus-2": "fa-crosshairs", "device-tv": "fa-tv",
    "device-gamepad-2": "fa-gamepad", "device-desktop": "fa-desktop",
    "circuit-board": "fa-microchip", "bolt": "fa-bolt", "wave-square": "fa-wave-square",
    "trophy": "fa-trophy", "radar": "fa-satellite-dish", "player-play": "fa-play",
    "palette": "fa-palette", "info-circle": "fa-circle-info", "flower": "fa-seedling",
    "database": "fa-database", "contrast": "fa-circle-half-stroke", "adjustments": "fa-sliders",
}

# ------------------------------------------------------- local tab id -> JS key
TAB_MAP = {
    "S1": {"s1-track": "track", "s1-perf": "perf", "s1-display": "display",
           "s1-soft": "soft", "s1-hw": "hw", "s1-svc": "svc"},
    "A1": {"a1-track": "track", "a1-perf": "perf", "a1-display": "display",
           "a1-soft": "soft", "a1-hw": "hw", "a1-svc": "svc"},
    "X1": {"x1-track": "track", "x1-perf": "perf", "x1-soft": "soft", "x1-svc": "svc"},
    "RG": {"tracking": "track", "display": "display", "software": "soft", "service": "svc"},
    "FAYA": {"tracking": "track", "display": "display", "software": "soft",
             "entertain": "entertain", "solution": "solution", "faya-svc": "svc"},
    "DISP": {"performance": "performance", "modes": "modes", "build": "build",
             "disp-svc": "disp-svc"},
    "VEND": {"capacity": "capacity", "payment": "payment", "pricing": "pricing",
             "operation": "operation", "vend-svc": "vend-svc"},
}

# specTabDefs group each product uses (unchanged binding in catalogDb)
DEFS_GROUP = {"S1": "simulator", "A1": "simulator", "X1": "x1", "RG": "rg",
              "FAYA": "faya", "DISP": "dispenser", "VEND": "vending"}

FILES = {
    "S1": "simulator/S1/golfpai_s1_specs_en.html",
    "A1": "simulator/A1/golfpai_a1_specs_en.html",
    "X1": "simulator/X1/golfpai_x1_specs_en.html",
    "RG": "simulator/RG/ruge_specs_tabs.html",
    "FAYA": "simulator/FAYA_Motion/faya_motion_specs.html",
    "DISP": "Dispenser_Machine/golf_ball_dispenser_specs.html",
    "VEND": "Vending_Machine/golf_ball_vending_specs.html",
}

DATA_VAR = {
    "S1": "s1SpecsData", "A1": "a1SpecsData", "X1": "x1SpecsData", "RG": "rgSpecsData",
    "FAYA": "fayaSpecsData", "DISP": "dispenserSpecsData", "VEND": "vendingSpecsData",
}

# ------------------------------------------------------------------- html utils
TAG_RE = re.compile(r"<div\b|</div>")


def balanced(s, start):
    """Return substring from `start` (a '<div' offset) through its matching </div>."""
    depth, pos = 0, start
    while True:
        m = TAG_RE.search(s, pos)
        if not m:
            return s[start:]
        depth += 1 if m.group(0) == "<div" else -1
        pos = m.end()
        if depth == 0:
            return s[start:pos]


def text_of(fragment):
    t = re.sub(r"<[^>]+>", "", fragment or "")
    return re.sub(r"\s+", " ", ihtml.unescape(t)).strip()


def find_block(s, cls_pattern):
    """First balanced <div ...> whose class matches cls_pattern; return (html, end)."""
    for m in re.finditer(r'<div class="([^"]*)"', s):
        if re.search(cls_pattern, m.group(1)):
            body = balanced(s, m.start())
            return body, m.start() + len(body)
    return None, -1


def grab(fragment, cls):
    """Extract inner html of <div class="cls">...</div> (first match, balanced)."""
    m = re.search(r'<div class="%s"[^>]*>' % cls, fragment)
    if not m:
        return None
    return balanced(fragment, m.start())


# ------------------------------------------------------------------ parse cards
def parse_card(div_html, class_attr):
    def one(*classes):
        for c in classes:
            m = re.search(r'<div class="%s"[^>]*>([\s\S]*?)</div>' % c, div_html)
            if m:
                return m.group(1)
        return None

    lbl_frag = one("lbl", "card-lbl", "range-name")
    val = text_of(one("val", "card-val", "range-val"))
    sub = text_of(one("sub", "card-sub", "range-acc"))
    badge_m = re.search(r'<span class="badge"[^>]*>([\s\S]*?)</span>', div_html)
    icon = None
    if lbl_frag:
        im = re.search(r'<i class="ti ti-([a-z0-9-]+)"', lbl_frag)
        if im:
            icon = TI2FA.get(im.group(1))
        lbl_frag = re.sub(r'<i[^>]*></i>', "", lbl_frag)
    card = {"label": text_of(lbl_frag), "value": val}
    if sub:
        card["sub"] = sub
    if badge_m:
        card["badge"] = text_of(badge_m.group(1))
    if "hi" in class_attr.split():
        card["highlight"] = True
    if icon:
        card["icon"] = icon
    return card


def parse_grid(grid_html):
    cards = []
    for m in re.finditer(r'<div class="(card[^"]*|range-card)"[^>]*>', grid_html):
        body = balanced(grid_html, m.start())
        cls = m.group(1)
        if not (cls == "range-card" or cls == "card" or cls.startswith("card ")):
            continue
        cards.append(parse_card(body, cls))
    return cards


def parse_panel(body):
    """-> [ {section, cards:[...]} ]"""
    sections = []
    order = []
    for m in re.finditer(r'<p class="sec"[^>]*>', body):
        order.append((m.start(), "sec", m))
    for m in re.finditer(r'<div class="grid"[^>]*>', body):
        order.append((m.start(), "grid", m))
    order.sort(key=lambda x: x[0])
    for pos, kind, m in order:
        if kind == "sec":
            end = body.find("</p>", pos)
            sections.append({"section": text_of(body[pos:end]), "cards": []})
        else:
            grid = balanced(body, m.start())
            cards = parse_grid(grid)
            if not sections:
                sections.append({"section": "", "cards": []})
            sections[-1]["cards"].extend(cards)
    return sections


def parse_file(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    s = re.sub(r"<style.*?</style>", "", raw, flags=re.S)
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    tabs = []
    for m in re.finditer(r'<button[^>]*class="[^"]*\b(?:stab|tab)\b[^"]*"[^>]*data-p="([^"]+)"[^>]*>([\s\S]*?)</button>', s):
        tabs.append({"pid": m.group(1), "label": text_of(m.group(2))})
    panels = {}
    for t in tabs:
        i = s.find('id="%s"' % t["pid"])
        start = s.rfind("<div", 0, i)
        panels[t["pid"]] = parse_panel(balanced(s, start))
    return tabs, panels


# -------------------------------------------------------------------- JS writer
def js_str(v):
    return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"


def card_js(c, ind):
    parts = ["label: %s" % js_str(c["label"]), "value: %s" % js_str(c["value"])]
    if c.get("sub"):
        parts.append("sub: %s" % js_str(c["sub"]))
    if c.get("badge"):
        parts.append("badge: %s" % js_str(c["badge"]))
    if c.get("highlight"):
        parts.append("highlight: true")
    if c.get("icon"):
        parts.append("icon: %s" % js_str(c["icon"]))
    return ind + "{ " + ", ".join(parts) + " }"


def data_js(data):
    """data: ordered dict key -> sections"""
    out = []
    for key, secs in data.items():
        out.append("            %s: [" % js_str(key) if not key.replace("_", "a").isalnum()
                   else "            %s: [" % key)
        for sec in secs:
            head = "section: %s" % js_str(sec["section"])
            if sec["cards"] and all(c.get("highlight") for c in sec["cards"]):
                head += ", highlight: true"
            out.append("                { %s, cards: [" % head)
            out.extend(card_js(c, "                    ") + "," for c in sec["cards"])
            if out and out[-1].endswith(","):
                out[-1] = out[-1][:-1]
            out.append("                ]},")
        if out and out[-1].endswith("},"):
            out[-1] = out[-1][:-1]
        out.append("            ],")
    if out and out[-1].endswith(","):
        out[-1] = out[-1][:-1]
    return "\n".join(out)


# existing tab icons (Font Awesome) per defs group — kept so the site look is stable
def load_existing_icons(src):
    icons = {}
    m = re.search(r"const specTabDefs = \{([\s\S]*?)\n        \};", src)
    if not m:
        return icons
    for grp in re.finditer(r"(\w+): \[\n([\s\S]*?)\n            \]", m.group(1)):
        name = grp.group(1)
        for item in re.finditer(r"id: '([^']+)', label: '[^']*', icon: '([^']+)'", grp.group(2)):
            icons.setdefault(name, {})[item.group(1)] = item.group(2)
    return icons


FALLBACK_ICON = {"track": "fa-eye", "perf": "fa-microchip", "display": "fa-tv",
                 "soft": "fa-gamepad", "hw": "fa-wrench", "svc": "fa-headset",
                 "entertain": "fa-music", "solution": "fa-box", "performance": "fa-gauge-high",
                 "modes": "fa-sliders", "build": "fa-bolt", "disp-svc": "fa-headset",
                 "capacity": "fa-boxes-stacked", "payment": "fa-credit-card",
                 "pricing": "fa-tags", "operation": "fa-clock", "vend-svc": "fa-headset"}


def main():
    src = open(INDEX, encoding="utf-8").read()
    existing_icons = load_existing_icons(src)

    data_blocks = []
    defs = {}
    report = []

    for key in ["S1", "A1", "X1", "RG", "FAYA", "DISP", "VEND"]:
        tabs, panels = parse_file(os.path.join(PRODUCTS, FILES[key]))
        mapping = TAB_MAP[key]
        ordered = {}
        tab_defs = []
        total = 0
        for t in tabs:
            jskey = mapping[t["pid"]]
            secs = panels.get(t["pid"], [])
            ordered[jskey] = secs
            n = sum(len(s["cards"]) for s in secs)
            total += n
            grp = DEFS_GROUP[key]
            icon = existing_icons.get(grp, {}).get(jskey) or FALLBACK_ICON.get(jskey, "fa-circle")
            tab_defs.append({"id": jskey, "label": t["label"], "icon": icon})
        data_blocks.append("        const %s = {\n%s\n        };" % (DATA_VAR[key], data_js(ordered)))
        defs[DEFS_GROUP[key]] = tab_defs
        report.append("  %-5s tabs=%d cards=%d  keys=%s" % (key, len(tabs), total, list(ordered)))
        if len(tabs) != len(mapping):
            print("  ⚠ %s: parsed %d tabs, expected %d" % (key, len(tabs), len(mapping)))

    defs_lines = []
    for grp in ["simulator", "rg", "faya", "x1", "dispenser", "vending"]:
        items = defs[grp]
        body = ",\n".join("                { id: %s, label: %s, icon: %s }"
                          % (js_str(d["id"]), js_str(d["label"]), js_str(d["icon"]))
                          for d in items)
        defs_lines.append("            %s: [\n%s\n            ]" % (grp, body))

    new_block = "\n\n".join(data_blocks) + "\n\n        const specTabDefs = {\n" + ",\n".join(defs_lines) + "\n        };"

    start_marker = "        /* SPECS_DATA_START */"
    end_marker = "        /* SPECS_DATA_END */"
    i = src.index(start_marker) + len(start_marker)
    j = src.index(end_marker)
    out = src[:i] + "\n" + new_block + "\n" + src[j:]

    if "--dry" in sys.argv:
        print("\n".join(report))
        print(new_block[:1500])
        return

    open(INDEX, "w", encoding="utf-8").write(out)
    print("synced ->", INDEX)
    print("\n".join(report))
    # sanity: JS syntax of the whole inline script
    json.dumps(report)


if __name__ == "__main__":
    main()
