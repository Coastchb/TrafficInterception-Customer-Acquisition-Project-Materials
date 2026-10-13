#!/usr/bin/env python3
"""NEAGLE GOLF — Product Catalog 2026 (English PDF, A4 portrait)."""
import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

BASE = "/Users/coast/Desktop/截流获客项目资料/高尔夫模拟器项目"
PROD = os.path.join(BASE, "products")
ASSETS = os.path.join(BASE, "tmp", "catalog-assets")
OUT = os.path.join(BASE, "NEAGLE-GOLF-Product-Catalog-2026.pdf")

W, H = A4  # 595 x 842
M = 46     # margin
INK = HexColor("#0A0A0A")
PAPER = HexColor("#FFFFFF")
GREEN = HexColor("#00E676")
GREY = HexColor("#52525B")
LINE = HexColor("#E4E4E7")
DARKSUB = HexColor("#A1A1AA")

# ---------- preprocess photos: downscale + JPEG to keep PDF small ----------
os.makedirs(os.path.join(ASSETS, "processed"), exist_ok=True)
def prep(src, name, maxw=1500):
    dst = os.path.join(ASSETS, "processed", name + ".jpg")
    im = Image.open(src).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=82, optimize=True)
    return dst

IMG = dict(
    S1=prep(os.path.join(PROD, "simulator", "S1", "0.png"), "s1"),
    A1=prep(os.path.join(PROD, "simulator", "A1", "0.png"), "a1"),
    X1=prep(os.path.join(PROD, "simulator", "X1", "0.png"), "x1"),
    RG=prep(os.path.join(PROD, "simulator", "RG", "0.png"), "rg"),
    FAYA=prep(os.path.join(PROD, "simulator", "FAYA_Motion", "0.png"), "faya"),
    DISP=prep(os.path.join(PROD, "Dispenser_Machine", "0.png"), "disp"),
    VEND=prep(os.path.join(PROD, "Vending_Machine", "0.png"), "vend"),
    CASE1=prep(os.path.join(ASSETS, "case-oclock.jpg"), "case1", 900),
    CASE2=prep(os.path.join(ASSETS, "case-clubhouse.jpg"), "case2", 900),
    CASE3=prep(os.path.join(ASSETS, "case-lincoln.png"), "case3", 900),
    CASE4=prep(os.path.join(ASSETS, "case-shanghai.jpg"), "case4", 900),
)

# ---------- crop QR codes (keep QR area only) ----------
for src, dst in [("qr-whatsapp.png", "qr-wa-crop.png"), ("qr-wechat.png", "qr-wc-crop.png")]:
    p = os.path.join(ASSETS, src)
    im = Image.open(p).convert("RGB")
    w, h = im.size
    im = im.crop((int(w*0.05), int(h*0.22), int(w*0.95), int(h*0.80)))
    im = im.resize((500, int(im.height * 500 / im.width)), Image.LANCZOS)
    im.save(os.path.join(ASSETS, dst))

# WeChat QR touches image edges — shrink it onto a white canvas so the code
# occupies the same proportion as the WhatsApp QR (proper quiet zone, no clipping)
wa_im = Image.open(os.path.join(ASSETS, "qr-wa-crop.png"))
wc_im = Image.open(os.path.join(ASSETS, "qr-wc-crop.png"))
sc = 0.76
wc_small = wc_im.resize((int(wc_im.width * sc), int(wc_im.height * sc)), Image.LANCZOS)
qr_canvas = Image.new("RGB", (wa_im.width, wa_im.height), "white")
qr_canvas.paste(wc_small, ((wa_im.width - wc_small.width) // 2, (wa_im.height - wc_small.height) // 2))
qr_canvas.save(os.path.join(ASSETS, "qr-wc-crop.png"))

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("NEAGLE GOLF — Product Catalog 2026")
c.setAuthor("NEAGLE GOLF")

def wrap(text, font, size, maxw):
    return simpleSplit(text, font, size, maxw)

def img_cover(path, x, y, w, h, radius=0, contain=False):
    """Draw image filling the box (cover, center-cropped) or fully visible (contain)."""
    c.saveState()
    p = c.beginPath()
    if radius:
        p.roundRect(x, y, w, h, radius)
    else:
        p.rect(x, y, w, h)
    c.clipPath(p, stroke=0)
    iw, ih = Image.open(path).size
    scale = (min(w / iw, h / ih) if contain else max(w / iw, h / ih))
    dw, dh = iw * scale, ih * scale
    c.drawImage(path, x - (dw - w) / 2, y - (dh - h) / 2, dw, dh)
    c.restoreState()

def add_link(x, y, text, font, size, url):
    """Invisible clickable rectangle over a drawn string."""
    tw = c.stringWidth(text, font, size)
    c.linkURL(url, (x, y - 2.5, x + tw, y + size + 1), relative=0)
    return tw

def footer(page, dark=False):
    col = DARKSUB if dark else GREY
    c.setFont("Helvetica", 7)
    c.setFillColor(col)
    c.drawString(M, 24, "NEAGLE GOLF  ·  Product Catalog 2026")
    t = "neaglegolf.com"
    c.drawRightString(W - M, 24, t)
    add_link(W - M - c.stringWidth(t, "Helvetica", 7), 24, t, "Helvetica", 7, "https://neaglegolf.com")
    c.drawCentredString(W / 2, 24, f"{page:02d}")

def dark_bg():
    c.setFillColor(INK)
    c.rect(0, 0, W, H, stroke=0, fill=1)

def green_tag(x, y, text, size=8, color=GREEN):
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(color)
    c.drawString(x, y, text.upper())

def cta_bar(y, dark=False):
    bh = 34
    c.saveState()
    c.setFillColor(INK if not dark else HexColor("#111111"))
    p = c.beginPath(); p.roundRect(M, y, W - 2*M, bh, 8); c.clipPath(p, stroke=0); c.rect(M, y, W-2*M, bh, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M + 14, y + bh/2 - 3, "Get a tailored quote")
    c.setFont("Helvetica", 9)
    c.setFillColor(GREEN)
    c.drawString(M + 132, y + bh/2 - 3, "WhatsApp +86 132 6156 3523")
    c.setFillColor(DARKSUB)
    c.drawString(M + 300, y + bh/2 - 3, "·")
    c.setFillColor(PAPER)
    c.drawString(M + 308, y + bh/2 - 3, "service@neaglegolf.com")
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(W - M - 14, y + bh/2 - 3, "24 h reply")
    c.restoreState()
    em = "service@neaglegolf.com"
    add_link(M + 308, y + bh/2 - 3, em, "Helvetica", 9, "mailto:" + em)

# ============================== P1 COVER ==============================
dark_bg()
green_tag(M, H - 60, "Product Catalog  2026", 9)
c.setFont("Helvetica-Bold", 34)
c.setFillColor(PAPER)
c.drawString(M, H - 105, "NEAGLE ")
c.setFillColor(GREEN)
c.drawString(M + c.stringWidth("NEAGLE ", "Helvetica-Bold", 34), H - 105, "GOLF")
c.setFont("Helvetica", 12)
c.setFillColor(DARKSUB)
c.drawString(M, H - 130, "Tour-Grade Golf Simulators, Launch Monitors &")
c.drawString(M, H - 146, "Automated Ball Dispensing Systems")

img_cover(IMG["S1"], M, 120, W - 2*M, 528, radius=14)
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 10)
c.setFillColor(GREEN)
c.drawString(M, 96, "OFFICIAL SIMULATOR  —  VOLVO CHINA OPEN  ·  BUICK LPGA CHAMPIONSHIP  ·  CHINA PGA TOUR")
c.setFillColor(DARKSUB)
c.setFont("Helvetica", 9)
c.drawString(M, 78, "Exported to the USA, Canada, UK, Australia, Japan and countries worldwide")
c.setFont("Helvetica", 8)
c.drawString(M, 40, "neaglegolf.com")
add_link(M, 40, "neaglegolf.com", "Helvetica", 8, "https://neaglegolf.com")
c.setFillColor(PAPER)
c.drawRightString(W - M, 40, "WhatsApp  +86 132 6156 3523")
c.showPage()

# ============================== P2 ABOUT ==============================
footer_on_dark = False
c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
green_tag(M, H - 60, "About Us")
c.setFont("Helvetica-Bold", 24); c.setFillColor(INK)
c.drawString(M, H - 88, "Engineering the Future of")
c.drawString(M, H - 114, "Indoor Golf")
y = H - 150
for line in wrap("NEAGLE GOLF is a global provider of tour-grade golf simulators, launch monitors, and 4K golf "
                 "simulation systems for indoor golf studios, commercial driving ranges, clubs, and private homes. "
                 "Our simulation packages combine high-speed camera and radar tracking with photoreal course "
                 "rendering, delivering shot data accurate enough for professional fitting and training.",
                 "Helvetica", 10.5, W - 2*M):
    c.setFillColor(GREY); c.setFont("Helvetica", 10.5); c.drawString(M, y, line); y -= 15
y -= 12
for line in wrap("Beyond simulation, we engineer automated golf ball dispensers and self-service range hardware "
                 "that reduce labor costs and unlock new revenue for facility operators. Every system ships with "
                 "white-glove onboarding, training, and 24/7 concierge support.",
                 "Helvetica", 10.5, W - 2*M):
    c.setFillColor(GREY); c.setFont("Helvetica", 10.5); c.drawString(M, y, line); y -= 15

y -= 30
green_tag(M, y, "Global Reach")
c.setFont("Helvetica", 10.5); c.setFillColor(GREY)
y -= 20
for line in wrap("Our systems are in daily operation across North America, Europe, Asia-Pacific and the Middle East — "
                 "exported to the USA, Canada, UK, Australia, Japan and countries worldwide — with local-language "
                 "software support and worldwide shipping by sea, express sea or air.",
                 "Helvetica", 10.5, W - 2*M):
    c.drawString(M, y, line); y -= 15

y -= 26
green_tag(M, y, "Official Tournament Heritage")
c.setFont("Helvetica", 10.5); c.setFillColor(GREY)
y -= 20
for line in wrap("RUGE RG Eagleye III is the official simulator of the Volvo China Open, the Buick LPGA Championship "
                 "and the China PGA Tour — the same tour-grade technology is built into every NEAGLE system.",
                 "Helvetica", 10.5, W - 2*M):
    c.drawString(M, y, line); y -= 15
cta_bar(52)
footer(2)
c.showPage()

# ============================== P3 DELIVERY & SUPPORT ==============================
c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
green_tag(M, H - 60, "Global Delivery & Support")
c.setFont("Helvetica-Bold", 24); c.setFillColor(INK)
c.drawString(M, H - 88, "Ordered Today. Playing in Weeks.")

# shipping table
rows = [("Preparation", "7 days", "Order confirmed → packing & pre-shipment testing"),
        ("Air Freight", "~ 7 days", "Fastest option for urgent installations"),
        ("Express Sea", "~ 30 days", "Balanced cost & speed for most regions"),
        ("Sea Freight", "~ 45 days", "Most economical for full venue projects")]
ty = H - 130
c.setFillColor(INK); c.rect(M, ty - 6, W - 2*M, 24, stroke=0, fill=1)
c.setFillColor(PAPER); c.setFont("Helvetica-Bold", 9.5)
c.drawString(M + 12, ty + 2, "STEP / METHOD"); c.drawCentredString(M + 200, ty + 2, "TIME"); c.drawString(W - M - 240, ty + 2, "DETAILS")
ty -= 26
for name, t, det in rows:
    c.setFillColor(HexColor("#FAFAFA")); c.rect(M, ty - 8, W - 2*M, 26, stroke=0, fill=1)
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(M, ty - 8, W - M, ty - 8)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 10); c.drawString(M + 12, ty, name)
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 9.5); c.drawCentredString(M + 200, ty, t)
    c.setFillColor(GREY); c.setFont("Helvetica", 8.5); c.drawString(W - M - 240, ty, det)
    ty -= 28

ty -= 30
blocks = [
    ("Warranty & Repair", ["1-year warranty on all systems", "Lifetime repair support", "RUGE RG: 2-year core hardware warranty"]),
    ("Installation", ["Remote installation included worldwide", "Step-by-step engineer guidance", "On-site installation available by negotiation"]),
    ("After-Sales Service", ["7×24 hour concierge support", "Free software & course upgrades (FAYA: lifetime)", "Multi-language software support"]),
]
bw = (W - 2*M - 32) / 3
card_top = ty - 14
for i, (title, items) in enumerate(blocks):
    bx = M + i * (bw + 16)
    c.saveState()
    c.setFillColor(HexColor("#F4F4F5"))
    p = c.beginPath(); p.roundRect(bx, card_top - 126, bw, 130, 10); c.clipPath(p, stroke=0); c.rect(bx, card_top - 126, bw, 130, stroke=0, fill=1)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 11); c.drawString(bx + 14, card_top - 24, title)
    yy = card_top - 48
    for it in items:
        for j, ln in enumerate(wrap(it, "Helvetica", 8.5, bw - 34)):
            if j == 0:
                c.setFillColor(GREEN); c.rect(bx + 14, yy - 2, 4, 4, stroke=0, fill=1)
            c.setFillColor(GREY); c.setFont("Helvetica", 8.5)
            c.drawString(bx + 24, yy - 2, ln); yy -= 11
        yy -= 3
    c.restoreState()
cta_bar(52)
footer(3)
c.showPage()

# ============================== P4 LINEUP ==============================
c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
green_tag(M, H - 60, "At a Glance")
c.setFont("Helvetica-Bold", 24); c.setFillColor(INK)
c.drawString(M, H - 88, "Seven Systems. One Concierge.")

lineup = [
    ("GOLFPAI S1", "Premium Simulator", "6,000 FPS vision · 4K laser · 110+ courses", "$42,516"),
    ("RUGE RG Eagleye III", "Tournament Simulator", "Triple-lens Eagle Eye · UE5 · 180+ courses", "$31,464"),
    ("GOLFPAI A1", "All-in-One Simulator", "24\" touchscreen · 4K DLP laser · 80+ courses", "$23,325"),
    ("FAYA Motion", "Dual-Sensor Simulator", "IDS dual-sensor · Dolby 7.2 · 100+ courses", "$9,384"),
    ("GOLFPAI X1", "Smart Range Simulator", "Radar + vision dual-engine · 43\" sunlight screen", "$8,829"),
    ("Ball Vending Machine", "Self-Service · 24/7", "10k–20k balls · QR / card / face payment", "$4,830"),
    ("Ball Dispenser", "Auto Tee Feeding", "100+ balls · 20 balls/min · 110–220V", "$342"),
]
ty = H - 122
c.setFillColor(INK); c.rect(M, ty - 6, W - 2*M, 24, stroke=0, fill=1)
c.setFillColor(PAPER); c.setFont("Helvetica-Bold", 9.5)
c.drawString(M + 12, ty + 2, "MODEL"); c.drawString(M + 230, ty + 2, "CATEGORY"); c.drawRightString(W - M - 12, ty + 2, "PRICE (USD)")
ty -= 26
for name, cat, hl, price in lineup:
    c.setFillColor(HexColor("#FAFAFA")); c.rect(M, ty - 10, W - 2*M, 34, stroke=0, fill=1)
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(M, ty - 10, W - M, ty - 10)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 10.5); c.drawString(M + 12, ty, name)
    c.setFillColor(GREY); c.setFont("Helvetica", 9); c.drawString(M + 230, ty, cat)
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 11); c.drawRightString(W - M - 12, ty, price)
    ty -= 36

ty -= 6
c.setFont("Helvetica-Oblique", 8); c.setFillColor(GREY)
c.drawString(M, ty, "Prices are reference USD pricing. Contact us for project quotes, volume pricing and distributor terms.")
cta_bar(52)
footer(4)
c.showPage()

# ============================== PRODUCT PAGES ==============================
PRODUCTS = [
    dict(img=IMG["S1"],
         cat="Golf Simulators", name="GOLFPAI S1", sub="Indoor Golf Simulator",
         tag="Premium indoor golf simulator with 6,000 FPS vision tracking, 4K laser projection and 110+ photorealistic courses.",
         price="$42,516", space="6.0 × 3.8 × 2.8 m",
         features=["6,000 FPS dual-camera stereo vision — 99.9%+ ball & clubhead recognition",
                   "8 ms ultra-low latency, 37× faster than a human blink",
                   "4K UHD 6,000 lm laser projection on a 200\" impact screen",
                   "110+ world-famous courses with 4K real-scene modeling",
                   "3-zone hitting mat (fairway / rough / bunker) with Korean imported turf",
                   "32GB RAM + 1TB M.2 SSD — built for high-traffic venues"],
         specs=[("Capture Speed", "6,000 FPS binocular vision"), ("Ball Recognition", "99.9%+"),
                ("System Latency", "8 ms"), ("Shot Shape Detection", "12 types"),
                ("Club Compatibility", "99% mainstream clubs"), ("Computer", "Intel i5-12400 + RTX 4060Ti"),
                ("Memory / Storage", "32GB DDR4 + 1TB M.2 SSD"), ("Projection", "4K UHD laser · 6,000 ANSI lm"),
                ("Contrast Ratio", "3,000,000 : 1"), ("Light Source Life", "20,000+ hrs"),
                ("Impact Screen", "200\" dual-layer anti-impact"), ("Golf Courses", "110+ 4K real-scene"),
                ("Auto Tee", "Motorized with height memory"), ("Hitting Mat", "3-zone Korean turf · 16 mm")]),
    dict(img=IMG["A1"],
         cat="Golf Simulators", name="GOLFPAI A1", sub="All-in-One Golf Simulator",
         tag="All-in-one simulator with integrated 24\" touchscreen, 4K DLP laser projection and 80+ world-class courses.",
         price="$23,325", space="5.5 × 3.5 × 2.8 m",
         features=["Integrated all-in-one unit with built-in 24\" touchscreen",
                   "6,000 FPS dual-camera vision — 99.9%+ recognition",
                   "4K DLP laser projection · 0.65\" DMD · 30,000+ hr light source",
                   "80+ courses with AI caddie & kids' cartoon mode",
                   "Cinema, KTV & meeting modes — full entertainment suite",
                   "Compact footprint for homes, apartments & boutique studios"],
         specs=[("Capture Speed", "6,000 FPS"), ("Recognition", "99.9%+"),
                ("CPU", "Intel i5-12400F · 12-thread"), ("GPU", "NVIDIA RTX 4060Ti 8GB"),
                ("RAM", "16GB DDR4 dual-channel"), ("Touchscreen", "24\" integrated"),
                ("Projection", "4K UHD DLP · 3840 × 2160"), ("Brightness", "5,200 lm"),
                ("Light Source Life", "30,000+ hrs"), ("Impact Screen", "200\" dual-layer"),
                ("Golf Courses", "80+ 4K real-scene"), ("Modes", "Golf / Cinema / KTV / Meeting"),
                ("Auto Tee", "Motorized"), ("Hitting Mat", "3-zone Korean turf")]),
    dict(img=IMG["X1"],
         cat="Golf Simulators", name="GOLFPAI X1", sub="Smart Range Simulator",
         tag="World-first radar + vision dual-engine tracking with self-evolving AI ballistics — built for driving ranges.",
         price="$8,829", space="5.5 × 3.5 × 2.8 m",
         features=["World-first radar + vision dual-engine — up to 99.99% accuracy",
                   "Self-evolving AI learns from every shot",
                   "43\" high-brightness sunlight touchscreen — clear in any light",
                   "50+ courses · 6-player online multiplayer with video call",
                   "Works with any standard golf ball — no custom balls needed",
                   "Full wind / weather / altitude environment simulation"],
         specs=[("Technology", "Radar + 6,000 FPS vision dual-engine"), ("Accuracy", "Up to 99.99% (self-evolving AI)"),
                ("Radar", "High-frequency Doppler"), ("Vision", "Dual industrial cameras · 6,000 FPS"),
                ("Recognition", "99%+"), ("Ball Compatibility", "Any standard golf ball"),
                ("Display", "43\" outdoor sunlight touchscreen"), ("CPU / GPU", "i5-12400F + RTX 4060Ti 8GB"),
                ("RAM", "16GB DDR4"), ("Golf Courses", "50+"),
                ("Multiplayer", "Up to 6 online with video call"), ("Tournaments", "Regular / Tour / Long Drive"),
                ("Environment Sim", "Wind / weather / altitude"), ("Shot Analysis", "Frame-by-frame replay")]),
    dict(img=IMG["RG"],
         cat="Golf Simulators", name="RUGE RG Eagleye III", sub="Tournament Golf Simulator",
         tag="Tournament-proven simulator with triple-lens Eagle Eye tracking, UE5-powered 4K visuals and 180+ real-world courses.",
         badge="OFFICIAL SIMULATOR — VOLVO CHINA OPEN · BUICK LPGA · CHINA PGA TOUR",
         price="$31,464", space="Fully customizable",
         features=["Official simulator of Volvo China Open, Buick LPGA & China PGA Tour",
                   "Eagle Eye III triple-lens sensor — zero-delay ball flight with full 3D data",
                   "UE5 engine, 2K/4K display, 180+ 1:1 real-scene 3D courses",
                   "AIGOLF swing analysis across 6 practice modules",
                   "Year-round online tournaments — club, team & solo events",
                   "7×24 hr support, 2-year core hardware warranty"],
         specs=[("Sensor Type", "Triple-Lens Ultra-High-Speed"), ("Data Output", "Ball · Club · Player 3D"),
                ("Ball Flight Latency", "Zero Delay"), ("Ball Speed", "1.0–200.0 MPH (±0.5)"),
                ("Club Head Speed", "1.6–160.0 MPH (±0.5)"), ("Carry Distance", "2–430 Yards (±2.0)"),
                ("Launch Angle", "0–72° (±1.0°)"), ("Render Engine", "Unreal Engine 5 (UE5)"),
                ("Resolution", "2K / 4K HD"), ("Course Reproduction", "1:1 Real-Scene 3D Modeling"),
                ("Course Library", "180+ Courses"), ("Swing Analysis", "AIGOLF Full-Swing AI"),
                ("Practice Modules", "6 Dedicated Modules"), ("Event Formats", "Multi-level, Multi-format"),
                ("Signature Format", "4-Ball Team Match"), ("Remote Play", "Real-time Online 15-Hole 3v3"),
                ("Customer Support", "7×24 Hours"), ("Warranty", "1-Year + Lifetime Repair")]),
    dict(img=IMG["FAYA"],
         cat="Golf Simulators", name="FAYA Motion", sub="Dual-Sensor Golf Simulator",
         tag="Professional dual-sensor simulator with full-spectrum shot data, 100+ HD courses and one-touch Golf / Cinema / KTV switching.",
         price="$9,384", space="Fully customizable",
         features=["IDS dual-sensor core — high-speed camera + precision rotation sensor",
                   "Full professional data: ball speed, launch angle, backspin & sidespin",
                   "100+ real 18-hole international courses · 64GBit 3D engine",
                   "Golf · Cinema · KTV one-touch switching with Dolby Atmos 7.2",
                   "Epson professional projector · Full HD 2K",
                   "Lifetime free course & software upgrades"],
         specs=[("Sensor", "IDS dual camera + rotation sensor"), ("Detection", "Full 360°, no dead zone"),
                ("High-Loft Launch", "60°+"), ("Ball Data", "Speed / launch / backspin / sidespin"),
                ("Club Data", "Face angle / landing point"), ("Projector", "Epson professional · 3,500+ lm"),
                ("Resolution", "Full HD 2K · 1920 × 1200"), ("Screen", "Custom anti-impact acoustic"),
                ("Golf Courses", "100+ international 18-hole"), ("Audio", "Dolby Atmos 7.2 + DTS:X"),
                ("Players", "1–8 simultaneous"), ("Language Support", "Chinese · Japanese · Korean · English"),
                ("Practice Modes", "Drive / approach / chip / bunker / putt"), ("Upgrades", "Lifetime free")]),
    dict(img=IMG["DISP"],
         cat="Ball Dispensing Systems", name="Automatic Golf Ball Dispenser", sub="Hands-Free Tee Feeding",
         tag="Hands-free automatic ball feeding with dual modes, 100+ ball capacity and wide-voltage compatibility — stay focused on your swing.",
         price="$342", space="0.6 × 0.2 × 0.3 m",
         features=["Fully automatic mode — detects empty tee, feeds instantly",
                   "Semi-auto foot-pedal mode — one press, one ball",
                   "Feeds onto tee or hitting mat — no modification needed",
                   "100+ ball capacity · 20 balls per minute continuous output",
                   "110V–220V wide voltage — stable in any environment",
                   "Galvanized steel body with electrostatic powder coating"],
         specs=[("Output Speed", "20 balls / min continuous"), ("Hopper Capacity", "100+ balls"),
                ("Auto Detection", "Tee-empty sensor"), ("Modes", "Fully automatic / foot pedal"),
                ("Ball Placement", "Tee or hitting mat"), ("Voltage", "110–220V AC wide"),
                ("Material", "Galvanized steel"), ("Finish", "Electrostatic powder coating"),
                ("Environment", "Indoor / outdoor"), ("Footprint", "0.6 × 0.2 × 0.3 m")]),
    dict(img=IMG["VEND"], contain=True,
         cat="Ball Dispensing Systems", name="Automatic Golf Ball Vending Machine", sub="24/7 Self-Service Range",
         tag="High-capacity self-service ball vending with triple smart payment and dynamic pricing — cut labor costs, maximize range revenue.",
         price="$4,830", space="1.3 × 1.2 × 1.65 m",
         features=["10,000–20,000 ball capacity · 100 balls per dispense, jam-free",
                   "Three-in-one payment — QR code, membership card, facial recognition",
                   "Dynamic smart pricing — member/guest tiers, peak & off-peak rates",
                   "24/7 unmanned operation — no attendants required",
                   "Zero human error — every transaction automatically logged",
                   "Instant smart upgrade for any traditional driving range"],
         specs=[("Max Capacity", "10,000–20,000 balls"), ("Output", "100 balls per dispense · jam-free"),
                ("Payment", "QR / membership card / facial recognition"), ("Pricing", "Member tiers · peak/off-peak dynamic"),
                ("Operating Hours", "24 / 7 unmanned"), ("Transaction Logging", "All payments recorded"),
                ("Staff Required", "Zero"), ("Use Frequency", "High-frequency, high-intensity"),
                ("Footprint", "1.3 × 1.2 × 1.65 m"), ("Upgrade Path", "Traditional → smart self-service")]),
]

page = 5
for prod in PRODUCTS:
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    # header
    green_tag(M, H - 56, prod["cat"])
    c.setFont("Helvetica-Bold", 21); c.setFillColor(INK)
    c.drawString(M, H - 80, prod["name"])
    nw = c.stringWidth(prod["name"], "Helvetica-Bold", 21)
    c.setFont("Helvetica", 12); c.setFillColor(GREY)
    c.drawString(M + nw + 10, H - 80, "·  " + prod["sub"])
    yy = H - 98
    for ln in wrap(prod["tag"], "Helvetica", 9.5, W - 2*M)[:2]:
        c.setFillColor(GREY); c.setFont("Helvetica", 9.5); c.drawString(M, yy, ln); yy -= 12.5
    # hero image
    img_cover(prod["img"], M, H - 98 - 236 - 14, W - 2*M, 236, radius=12, contain=prod.get("contain", False))
    iy = H - 98 - 236 - 14
    if prod.get("badge"):
        c.saveState()
        c.setFillColor(INK)
        p = c.beginPath(); p.roundRect(M, iy + 8, W - 2*M - 40, 22, 6); c.clipPath(p, stroke=0); c.rect(M, iy + 8, W - 2*M - 40, 22, stroke=0, fill=1)
        c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 8)
        c.drawString(M + 12, iy + 15, prod["badge"])
        c.restoreState()
    # price + space
    py = iy - 30
    c.setFont("Helvetica", 8); c.setFillColor(GREY); c.drawString(M, py, "REFERENCE PRICE*")
    c.setFont("Helvetica-Bold", 17); c.setFillColor(INK); c.drawString(M, py - 19, prod["price"])
    c.setFont("Helvetica", 8); c.setFillColor(GREY)
    c.drawRightString(W - M, py, "MINIMUM SPACE")
    c.setFont("Helvetica-Bold", 12); c.setFillColor(INK)
    c.drawRightString(W - M, py - 18, prod["space"])
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(M + 150, py + 4, M + 150, py - 22)
    # features + specs side by side
    fy = py - 44
    green_tag(M, fy, "Key Features", 8)
    sy = fy
    green_tag(M + 268, sy, "Specifications", 8)
    yy = fy - 17
    for f in prod["features"]:
        c.setFillColor(GREEN); c.rect(M, yy - 2, 4, 4, stroke=0, fill=1)
        lines = wrap(f, "Helvetica", 8.5, 210)
        for j, ln in enumerate(lines):
            c.setFillColor(GREY); c.setFont("Helvetica", 8.5); c.drawString(M + 10, yy - 2, ln); yy -= 10.5
        yy -= 2.5
    sy2 = sy - 17
    half = (len(prod["specs"]) + 1) // 2
    for col, group in enumerate([prod["specs"][:half], prod["specs"][half:]]):
        xx = M + 268 + col * 145
        yy2 = sy2
        for k, v in group:
            c.setFillColor(GREY); c.setFont("Helvetica", 6.8); c.drawString(xx, yy2, k.upper())
            c.setFillColor(INK); c.setFont("Helvetica-Bold", 7.3)
            for j, ln in enumerate(wrap(v, "Helvetica-Bold", 7.3, 138)[:2]):
                c.drawString(xx, yy2 - 9.5 - j*8.5, ln)
            yy2 -= 9.5 + 8.5 * min(len(wrap(v, "Helvetica-Bold", 7.3, 138)), 2) + 4
    cta_bar(52)
    c.setFont("Helvetica-Oblique", 6.5); c.setFillColor(GREY)
    c.drawString(M, 38, "* Contact us for project quotes, volume pricing and distributor terms.")
    footer(page)
    c.showPage()
    page += 1

# ============================== CASE STUDIES ==============================
c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
green_tag(M, H - 60, "Case Studies")
c.setFont("Helvetica-Bold", 24); c.setFillColor(INK)
c.drawString(M, H - 88, "Venues Running on NEAGLE")

cases = [
    (IMG["CASE1"], "O'Clock Golf Bar — Regina, Canada",
     "Built from a bare concrete shell into a 9-bay golf bar with 2 VIP rooms and a full-service bar."),
    (IMG["CASE2"], "Clubhouse Indoor Golf — Richmond, Vancouver",
     "Indoor golf entertainment center with 6 simulator bays plus 3 private VIP rooms."),
    (IMG["CASE3"], "Lincoln 4S Dealerships — China",
     "Simulators installed in two car dealerships to boost customer dwell time and lead conversion."),
    (IMG["CASE4"], "Jitang Club — Shanghai, China",
     "Curved-screen GOLFPAI S1 bays in a bayside club combining golf, dining and events."),
]
cw = (W - 2*M - 14) / 2
ch = 158
for i, (img, title, desc) in enumerate(cases):
    bx = M + (i % 2) * (cw + 14)
    by = H - 126 - ch - (i // 2) * (ch + 92)
    img_cover(img, bx, by, cw, ch, radius=10)
    yy = by - 16
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 10)
    for j, ln in enumerate(wrap(title, "Helvetica-Bold", 10, cw)):
        c.drawString(bx, yy, ln); yy -= 12
    c.setFillColor(GREY); c.setFont("Helvetica", 8)
    for ln in wrap(desc, "Helvetica", 8, cw)[:2]:
        c.drawString(bx, yy - 2, ln); yy -= 10

yy2 = 214
green_tag(M, yy2, "More References")
c.setFillColor(GREY); c.setFont("Helvetica", 9)
prefix = "Private villa studio (Toronto) · Japanese omakase restaurant lounge · Chinese courtyard villa · and more at "
c.drawString(M, yy2 - 18, prefix)
pw = c.stringWidth(prefix, "Helvetica", 9)
tail = "neaglegolf.com/case-studies/"
c.setFillColor(GREEN); c.drawString(M + pw, yy2 - 18, tail)
add_link(M + pw, yy2 - 18, tail, "Helvetica", 9, "https://neaglegolf.com/case-studies/")
cta_bar(52)
footer(page)
c.showPage()

# ============================== BACK COVER ==============================
page += 1
dark_bg()
green_tag(M, H - 70, "Contact Us", 9)
c.setFont("Helvetica-Bold", 28); c.setFillColor(PAPER)
c.drawString(M, H - 102, "Let's Build Your")
c.setFillColor(GREEN)
c.drawString(M, H - 136, "Golf Venue.")

c.setFont("Helvetica", 10.5); c.setFillColor(DARKSUB)
c.drawString(M, H - 162, "Send us your room dimensions and use case —")
c.drawString(M, H - 177, "we will reply with a tailored proposal within 24 hours.")

# contact rows + QR codes
bx = M
rows = [("WhatsApp", "+86 132 6156 3523", None), ("WeChat", "132 6156 3523", None),
        ("Email", "service@neaglegolf.com", "mailto:service@neaglegolf.com"), ("Website", "neaglegolf.com", "https://neaglegolf.com")]
yy = H - 240
for label, val, url in rows:
    c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 8); c.drawString(bx, yy, label.upper())
    c.setFillColor(PAPER); c.setFont("Helvetica", 12); c.drawString(bx, yy - 16, val)
    if url:
        add_link(bx, yy - 16, val, "Helvetica", 12, url)
    yy -= 46

img_cover(os.path.join(ASSETS, "qr-wa-crop.png"), W - M - 260, 300, 105, 105, radius=8, contain=True)
img_cover(os.path.join(ASSETS, "qr-wc-crop.png"), W - M - 130, 300, 105, 105, radius=8, contain=True)
c.setFillColor(GREEN); c.setFont("Helvetica-Bold", 8)
c.drawCentredString(W - M - 207, 286, "WHATSAPP")
c.drawCentredString(W - M - 77, 286, "WECHAT")
c.setFillColor(DARKSUB); c.setFont("Helvetica", 7.5)
c.drawCentredString(W - M - 207, 274, "Scan to chat now")
c.drawCentredString(W - M - 77, 274, "Scan to add")

c.setStrokeColor(HexColor("#27272A")); c.setLineWidth(1); c.line(M, 100, W - M, 100)
c.setFillColor(DARKSUB); c.setFont("Helvetica", 8)
c.drawString(M, 80, "NEAGLE GOLFING SYSTEMS")
c.drawString(M, 66, "Simulators  ·  Launch Monitors  ·  Ball Dispensers  ·  Vending Systems")
c.setFillColor(PAPER); c.setFont("Helvetica-Bold", 9)
t = "neaglegolf.com"
c.drawRightString(W - M, 80, t)
add_link(W - M - c.stringWidth(t, "Helvetica-Bold", 9), 80, t, "Helvetica-Bold", 9, "https://neaglegolf.com")
footer(page, dark=True)
c.showPage()

c.save()
print("PDF saved:", OUT)
