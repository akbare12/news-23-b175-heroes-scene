#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Monday 23 November 2026 (31 stories).
Front page, 1024x1024. Heroes-scene variant: 3 big illustrated scenes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"

def f(path, size):
    return ImageFont.truetype(FD + path, size)

SERIF_B = f("DejaVuSerif-Bold.ttf", 40)
SERIF_I = f("DejaVuSerif.ttf", 15)
SANS_B = lambda s: f("DejaVuSans-Bold.ttf", s)
SANS = lambda s: f("DejaVuSans.ttf", s)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
INK = (20, 20, 20)
GRAY = (110, 110, 110)
LGRAY = (210, 210, 210)
RED = (178, 34, 34)
NAVY = (13, 27, 62)
TEAL = (10, 60, 70)
GOLD = (212, 160, 23)
ORANGE = (230, 110, 20)
GREEN = (20, 120, 60)
BLUE = (30, 80, 160)
CREAM = (248, 246, 240)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def wrap(s, font, maxw):
    """Greedy wrap; returns list of lines, each <= maxw."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(x, y, label, color=GREEN):
    """Outlined chip, right-aligned at x. Returns left edge."""
    fb = SANS_B(9)
    w = int(d.textlength(label, font=fb)) + 10
    d.rectangle([x - w, y, x, y + 14], outline=color, width=1)
    d.text((x - w + 5, y + 2), label, font=fb, fill=color)
    return x - w


# ---------- masthead ----------
d.rectangle([0, 0, W, 4], fill=BLACK)
text(W // 2, 10, "THE WORLD TODAY", SERIF_B, anchor="ma")
text(12, 58, "MONDAY 23 NOVEMBER 2026", SANS_B(15))
text(W - 12, 58, "31 STORIES  ·  ONE DAY", SANS_B(13), fill=GRAY, anchor="ra")
d.line([12, 80, W - 12, 80], fill=BLACK, width=1)
text(W // 2, 86, "The AI rout, a call to regulate it, and a power shift — Monday's world in one page.",
     SERIF_I, fill=(60, 60, 60), anchor="ma")

# ---------- number strip ----------
NUMS = [
    ("−3.3%", "KOSPI FALLS"), ("5.3", "POWER GAP"), ("11,762", "EBOLA CASES"),
    ("10T won", "SEOUL FUND"), ("2%", "BILLIONAIRE TAX"), ("$450M", "SKUBAL DEAL"),
    ("165", "MISSILES / WK"), ("12,000", "MANCHESTER"),
    ("264 kg", "EXPLOSIVES"), ("$107.3B", "ANTHROPIC IPO"),
]
sy, sh = 108, 46
d.rectangle([12, sy, W - 12, sy + sh], outline=LGRAY, width=1)
cw = 1000 / 10
for i, (v, lab) in enumerate(NUMS):
    cx = 12 + i * cw
    text(cx + cw / 2, sy + 3, v, SANS_B(17), anchor="ma")
    text(cx + cw / 2, sy + 27, lab, SANS_B(8), fill=GRAY, anchor="ma")
    if i:
        d.line([cx, sy + 6, cx, sy + sh - 6], fill=LGRAY, width=1)

# ---------- region bar ----------
REGIONS = [("ASIA-PACIFIC", 7, RED), ("AMERICAS", 8, BLUE), ("MIDDLE EAST", 6, ORANGE),
           ("EUROPE", 5, GREEN), ("AFRICA", 3, (120, 70, 140)), ("WORLD", 2, GRAY)]
ry = 162
parts, total_w = [], 0
for name, n, c in REGIONS:
    parts.append((f"{name} {n}", c))
    total_w += d.textlength(f"{name} {n}", font=SANS_B(12)) + 26
x = (W - total_w) // 2
for label, c in parts:
    d.ellipse([x, ry + 2, x + 9, ry + 11], fill=c)
    text(x + 13, ry, label, SANS_B(12))
    x += d.textlength(label, font=SANS_B(12)) + 26

# ---------- heroes ----------
HX = [12, 354, 696]
HW = 316
HY, SCENE_H = 182, 146

# --- scene 1: Kospi skyline + falling chart ---
x0 = HX[0]
d.rectangle([x0, HY, x0 + HW, HY + SCENE_H], fill=NAVY)
# buildings with lit windows along the bottom
import random
random.seed(23)
bx = x0 + 8
while bx < x0 + HW - 20:
    bw = random.randint(22, 38)
    bh = random.randint(34, 62)
    d.rectangle([bx, HY + SCENE_H - 34 - bh, bx + bw, HY + SCENE_H - 34], fill=(24, 44, 92))
    for wy in range(HY + SCENE_H - 30 - bh, HY + SCENE_H - 36, 10):
        for wx in range(bx + 4, bx + bw - 4, 9):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=GOLD)
    bx += bw + 4
# falling orange chart line, routed clear of the big number (top-left)
d.line([(x0 + 150, HY + 62), (x0 + 200, HY + 78), (x0 + 250, HY + 92), (x0 + 305, HY + 108)],
       fill=ORANGE, width=4)
d.ellipse([x0 + 299, HY + 102, x0 + 311, HY + 114], fill=ORANGE)
text(x0 + 12, HY + 6, "−3.3%", SANS_B(36), fill=WHITE)
d.rectangle([x0, HY + SCENE_H - 26, x0 + HW, HY + SCENE_H], fill=(8, 18, 48))
text(x0 + 10, HY + SCENE_H - 22, "KOSPI 4,708.54  ·  −161 PTS  ·  INTRADAY −5.8%",
     SANS_B(11), fill=WHITE)

# --- scene 2: Guterres globe + flags ---
x0 = HX[1]
d.rectangle([x0, HY, x0 + HW, HY + SCENE_H], fill=TEAL)
text(x0 + 12, HY + 8, "150 DELEGATES", SANS_B(22), fill=GOLD)
text(x0 + 12, HY + 38, "BACK A RISK", SANS_B(17), fill=WHITE)
text(x0 + 12, HY + 60, "FRAMEWORK", SANS_B(17), fill=WHITE)
text(x0 + 12, HY + 86, "BRIDGETOWN  ·  BARBADOS", SANS_B(11), fill=(180, 220, 220))
# globe, right side, clear of the text
gx, gy, gr = x0 + 245, HY + 62, 34
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(150, 200, 200), width=2)
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(16, 90, 100))
for dy in (-16, 0, 16):
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill=(150, 200, 200), width=1)
    d.line([gx - gr, gy + dy, gx + gr, gy + dy], fill=(120, 180, 180), width=1)
d.ellipse([gx - 10, gy - gr, gx + 10, gy + gr], outline=(150, 200, 200), width=1)
# 4 small flags, bottom-right, below the globe
fx, fy = x0 + 200, HY + SCENE_H - 26
for i, fc in enumerate([(200, 60, 60), (60, 120, 200), (220, 180, 40), (60, 160, 90)]):
    d.rectangle([fx + i * 28, fy, fx + i * 28 + 20, fy + 13], fill=fc)
    d.line([fx + i * 28, fy, fx + i * 28, fy + 18], fill=WHITE, width=1)

# --- scene 3: Asia Power Index bars ---
x0 = HX[2]
d.rectangle([x0, HY, x0 + HW, HY + SCENE_H], fill=CREAM)
text(x0 + 10, HY + 6, "ASIA POWER INDEX 2026", SANS_B(12))
bars = [("US", 78.9, RED), ("CHINA", 73.6, GOLD), ("INDIA", 40.5, BLUE)]
by = HY + 30
for name, val, c in bars:
    text(x0 + 10, by + 2, name, SANS_B(11))
    bw = int(val * 2.1)
    d.rectangle([x0 + 72, by, x0 + 72 + bw, by + 16], fill=c)
    text(x0 + 78 + bw, by + 2, f"{val}", SANS_B(11))
    by += 26
text(x0 + 10, by + 2, "GAP 5.3 — NARROWEST SINCE 2018", SANS_B(12), fill=RED)

# --- hero headlines / bodies / source+chip ---
HEROES = [
    ("AI ROUT HITS ASIA",
     "Kospi closes 4,708.54, sheds 161 pts; Samsung −3.1%, SK Hynix −2.5%."),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "Bridgetown summit: 150 delegates back a risk framework — blueprint, not treaty."),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "US 78.9, China 73.6 — gap 5.3, the narrowest since 2018; India 3rd at 40.5."),
]
hy = HY + SCENE_H + 8
for i, (head, body) in enumerate(HEROES):
    x0 = HX[i]
    hl = wrap(head, SANS_B(15), HW)
    assert len(hl) <= 2, f"hero {i} headline wraps to {len(hl)}"
    yy = hy
    for ln in hl:
        text(x0, yy, ln, SANS_B(15))
        yy += 18
    bl = wrap(body, SANS(11), HW)
    assert len(bl) <= 2, f"hero {i} body wraps to {len(bl)}"
    yy += 2
    for ln in bl:
        text(x0, yy, ln, SANS(11), fill=(50, 50, 50))
        yy += 14
    text(x0, hy + 84, "AP · REUTERS", SANS(10), fill=GRAY)
    chip(x0 + HW, hy + 82, "REPORTED")

# ---------- MORE OF THE DAY bar ----------
d.rectangle([12, 436, W - 12, 458], fill=BLACK)
text(20, 441, "MORE OF THE DAY", SANS_B(13), fill=WHITE)
text(W - 20, 441, "10 STORIES", SANS_B(11), fill=(200, 200, 200), anchor="ra")

# ---------- 10 cards ----------
CARDS = [
    ("MARKETS", "BESSENT DEMANDS NVIDIA ANSWERS", "Treasury presses chipmaker.", "REPORTED"),
    ("CYBER", "FBI PROBES POLICE-DATABASE HACK", "NCIC breach probed.", "REPORTED"),
    ("MIDDLE EAST", "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may return in New Year.", "REPORTED"),
    ("MARKETS", "NASDAQ FUTURES +3% HOLIDAY WEEK", "Thanksgiving week rally eyed.", "REPORTED"),
    ("SPORT", "SKUBAL SIGNS $450M METS DEAL", "Largest ever for a pitcher.", "REPORTED"),
    ("OBITUARY", "TOM JACKSON DIES AT 75", "NFL star turned broadcaster.", "REPORTED"),
    ("TECH", "STATES SUE SPACEX OVER AI CLAIMS", "AI safety claims challenged.", "REPORTED"),
    ("TECH", "ANTHROPIC IPO HITS $107.3B", "Raised at $83; debut $97.17.", "REPORTED"),
    ("EUROPE", "POLAND: MISSILES CROSSED AIRSPACE", "Warsaw says 3 Kh-101s entered.", "CLAIM"),
    ("SECURITY", "INTEL WARNS OF RUSSIAN NUKE SAT", "Satellite threat flagged.", "CLAIM"),
]
cy0, ch, cgap = 466, 60, 8
cw = (1000 - 4 * cgap) // 5
for i, (cat, head, body, tag) in enumerate(CARDS):
    r, c = divmod(i, 5)
    x0 = 12 + c * (cw + cgap)
    y0 = cy0 + r * (ch + cgap)
    d.rectangle([x0, y0, x0 + cw, y0 + ch], outline=LGRAY, width=1)
    text(x0 + 6, y0 + 4, cat, SANS_B(8), fill=RED)
    chip(x0 + cw - 6, y0 + 3, tag, GREEN if tag == "REPORTED" else RED)
    hl = wrap(head, SANS_B(11), cw - 12)
    assert len(hl) <= 2, f"card {i} headline wraps to {len(hl)}"
    yy = y0 + 16
    for ln in hl:
        text(x0 + 6, yy, ln, SANS_B(11))
        yy += 13
    assert d.textlength(body, font=SANS(10)) <= cw - 12, f"card {i} body too long"
    text(x0 + 6, y0 + ch - 15, body, SANS(10), fill=(60, 60, 60))

# ---------- map + ALSO ----------
MY = 600
d.rectangle([12, MY, 500, 884], outline=LGRAY, width=1)
text(20, MY + 6, "THE WORLD IN 13 PINS", SANS_B(12))
# stylised blobs
d.polygon([(36, 652), (150, 640), (162, 700), (128, 762), (96, 824), (52, 806), (30, 726)],
          fill=(225, 235, 245))
d.polygon([(172, 632), (468, 626), (484, 696), (424, 742), (300, 738), (198, 716), (166, 676)],
          fill=(225, 235, 245))
d.polygon([(292, 744), (398, 744), (408, 798), (362, 838), (302, 828), (282, 778)],
          fill=(225, 235, 245))
PINS = [
    (455, 652, "1"), (120, 748, "2"), (85, 668, "3"), (252, 668, "4"),
    (236, 650, "5"), (219, 642, "6"), (300, 648, "7"), (330, 658, "8"),
    (360, 702, "9"), (344, 722, "10"), (394, 716, "11"), (340, 775, "12"),
    (312, 808, "13"),
]
for (px, py, n) in PINS:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    d.text((px, py - 5), n, font=SANS_B(8), fill=WHITE, anchor="ma")
text(20, 846, "1 Seoul  2 Bridgetown  3 Washington  4 Paris  5 London  6 Manchester  7 Warsaw",
     SANS(9), fill=GRAY)
text(20, 862, "8 Kyiv  9 Beirut  10 Gaza  11 Bahrain  12 Khartoum  13 Kinshasa",
     SANS(9), fill=GRAY)

# ALSO list, right panel
text(516, MY + 6, "ALSO ON MONDAY", SANS_B(12))
ALSO = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: day after Antalya pact",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Benghazi: UN probe demanded [CLAIM]",
    "Sudan: drones downed [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if returns",
    "Seoul minister quits over AI exams",
    "SK Telecom −7.3%",
    "China eases margin rules to 80%",
    "Seoul readies 10T-won fund",
]
ay = MY + 28
for j, item in enumerate(ALSO):
    col = j // 9
    row = j % 9
    xx = 516 + col * 250
    yy = ay + row * 28
    assert d.textlength(item, font=SANS(10)) <= 246, f"ALSO {j} too long: {item}"
    text(xx, yy, "•  " + item, SANS(10))

# ---------- DATE CHECK ----------
DY = 894
d.rectangle([12, DY, W - 12, DY + 78], outline=RED, width=2)
text(20, DY + 6, "DATE CHECK — THESE ARE NOT 23 NOVEMBER", SANS_B(12), fill=RED)
LEFT = ["Dems reach 258 (22 Nov)", "Sparta II fire (22 Nov)", "El Chapo captured (22 Nov)",
        "EU–Indonesia pact (21 Nov)", "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)"]
for i, item in enumerate(LEFT):
    row, col = divmod(i, 3)
    text(20 + col * 330, DY + 26 + row * 15, "✕  " + item, SANS(10))
text(20, DY + 58, "NOT YET:  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating Ebola staff",
     SANS(10), fill=(60, 60, 60))

# ---------- footer ----------
text(12, 982, "SOURCES: AP · REUTERS · BLOOMBERG · YONHAP · AFP", SANS(9), fill=GRAY)
text(12, 998, "REPORTED = confirmed by wires  ·  CLAIM = one side's claim  ·  All figures as reported on 23 November 2026.",
     SANS(9), fill=GRAY)

img.save("entry.png")
print("saved entry.png", img.size)
