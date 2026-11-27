#!/usr/bin/env python3
"""Draw the news-image-20261126 front page: 36 stories of Thu 26 Nov 2026.
Written from scratch in this session. PIL + DejaVu only. Output: entry.png 1024x1024.
Layout: masthead / 4 numeral leads / numbers strip / world map + UTC timeline /
32-story grid / MORE TODAY ticker / DATE CHECK footer.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (20, 20, 20)
RED = (168, 30, 36)
MUTED = (96, 89, 76)
RULE = (20, 20, 20)
PANEL = (255, 253, 246)
BLACK = (18, 18, 18)
CREAM = (248, 244, 232)
TAGC = {"CONFIRMED": (29, 107, 47), "REPORTED": (154, 106, 0),
        "OFFICIAL": (31, 78, 121), "ONGOING": (107, 63, 160)}

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(text, font):
    return d.textlength(text, font=font)

def wrap(text, font, maxw):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(text, font, maxw, maxlines):
    lines = wrap(text, font, maxw)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        while lines and tw(lines[-1] + " …", font) > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + " …"
    return lines

def para(text, font, x, y, maxw, maxlines, fill=INK, leading=None):
    lh = leading or int(font.size * 1.22)
    for i, ln in enumerate(fit_lines(text, font, maxw, maxlines)):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(fit_lines(text, font, maxw, maxlines)) * lh

def hline(x0, x1, y, fill=RULE, wdt=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)

def tagchip(text, x, y):
    f = SANS_B(8)
    wdt = int(tw(text, f)) + 8
    d.rounded_rectangle([x, y, x + wdt, y + 12], radius=2, fill=TAGC[text])
    d.text((x + 4, y + 2), text, font=f, fill=(255, 255, 255))
    return wdt

# ---------------------------------------------------------------- masthead
d.text((512, 8), "THE WORLD IN ONE PAGE", font=SERIF_B(40), fill=INK, anchor="mt")
d.text((512, 52), "THURSDAY  26  NOVEMBER  2026", font=SANS_B(19), fill=RED, anchor="mt")
hline(12, 1012, 80, wdt=2)
d.text((512, 84), "36 STORIES  ·  ONE DAY  ·  EVERY TIMEZONE  —  THE NEWS OF 26 NOVEMBER 2026, AS REPORTED THAT DAY",
       font=SANS_B(10), fill=MUTED, anchor="mt")

# ---------------------------------------------------------------- leads
LEADS = [
    ("2", "KUWAIT · DRONE ATTACK", "Two Italians killed in drone strike blamed on Iran",
     "Technicians hit at an air-defence station; two more wounded. Tehran denies it; Italy to complain to Iran's embassy.",
     "CNN · REUTERS · WSJ", "CONFIRMED"),
    ("12,000", "DR CONGO · EBOLA", "Ebola cases pass 12,000 in second-biggest outbreak",
     "Responders evacuated amid fighting; UN peacekeepers step up protection in Ituri.",
     "CBC · NPR · FRANCE 24", "CONFIRMED"),
    ("€45bn", "BRUSSELS · EU SUMMIT", "Leaders fail on €45bn Ukraine loan after 12 hours",
     "No deal either on the €1.582tn budget; Macron sets an end-of-year deadline; next try 17–18 Dec.",
     "AP", "CONFIRMED"),
    ("490,334", "LEAKED DATA · RUSSIA'S WAR DEAD", "BBC counts 490,334 Russian soldiers dead",
     "Analysis of leaked Russian data; other counts top 700,000; Kremlin dismisses the higher figure.",
     "BBC · CBS", "REPORTED"),
]
lx, ly, lw, lh = 12, 100, 244, 182
for i, (num, kick, head, body, src, tag) in enumerate(LEADS):
    x = lx + i * (lw + 8)
    d.rectangle([x, ly, x + lw, ly + lh], fill=PANEL, outline=RULE, width=1)
    d.rectangle([x, ly, x + lw, ly + 4], fill=RED)
    numf = SERIF_B(40 if len(num) <= 5 else 34)
    d.text((x + 10, ly + 12), num, font=numf, fill=RED)
    d.text((x + 10, ly + 62), kick, font=SANS_B(9), fill=MUTED)
    para(head, SANS_B(13), x + 10, ly + 78, lw - 20, 2, leading=16)
    para(body, SANS(10), x + 10, ly + 114, lw - 20, 3, leading=12)
    d.text((x + 10, ly + 162), src, font=SANS(8), fill=MUTED)
    tagchip(tag, x + lw - 78, ly + 160)

# ---------------------------------------------------------------- numbers strip
STRIP = [
    ("300,000", "US homes dark in Thanksgiving storms"),
    ("77,000", "UK net migration, lowest since 1997"),
    ("3.25%", "Bank of Korea rate, a 2-year high"),
    ("$91.21", "Brent crude, +0.63% on Gulf risk"),
    ("$220M", "meth seized in Nigeria"),
    ("13", "dead in Indonesia mine flood"),
    ("9", "hurt in Bangkok refinery blast"),
    ("€1.582tn", "EU budget left undecided"),
]
sy = 290
d.rectangle([12, sy, 1012, sy + 42], fill=BLACK)
cw = 1000 / 8
for i, (num, lab) in enumerate(STRIP):
    cx = 12 + i * cw
    d.text((cx + cw / 2, sy + 4), num, font=SANS_B(15), fill=CREAM, anchor="mt")
    for ln_i, ln in enumerate(fit_lines(lab, SANS(8), cw - 10, 2)):
        d.text((cx + cw / 2, sy + 22 + ln_i * 9), ln, font=SANS(8), fill=(207, 200, 184), anchor="mt")
    if i:
        d.line([(cx, sy + 5), (cx, sy + 37)], fill=(70, 70, 70), width=1)

# ---------------------------------------------------------------- world map
MAP = {"x0": 12, "y0": 340, "x1": 648, "y1": 534}
LAND = (196, 209, 199)
LANDLINE = (122, 136, 128)
MAPBG = (233, 237, 231)

def project(lon, lat):
    mx0, my0, mx1, my1 = MAP["x0"], MAP["y0"], MAP["x1"], MAP["y1"]
    x = mx0 + (lon + 180) / 360 * (mx1 - mx0)
    y = my0 + (84 - lat) / 140 * (my1 - my0)
    return (x, y)

CONTINENTS = [
    [(-168, 66), (-145, 70), (-130, 71), (-120, 72), (-110, 73), (-100, 74), (-95, 80), (-88, 74), (-85, 70), (-80, 73), (-76, 62), (-70, 62), (-65, 60), (-60, 55), (-55, 52), (-53, 47), (-60, 46), (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-88, 29), (-90, 21), (-94, 17), (-97, 16), (-100, 17), (-105, 20), (-110, 23), (-114, 28), (-118, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 54), (-135, 58), (-145, 60), (-152, 58), (-158, 58), (-162, 55), (-165, 60), (-168, 66)],
    [(-79, 9), (-77, 7), (-72, 11), (-64, 10), (-59, 8), (-52, 5), (-50, 0), (-44, -3), (-38, -5), (-35, -8), (-38, -15), (-40, -22), (-48, -27), (-52, -33), (-58, -38), (-62, -41), (-65, -45), (-68, -50), (-70, -54), (-73, -50), (-73, -42), (-72, -35), (-70, -25), (-70, -18), (-76, -14), (-80, -6), (-81, -1), (-80, 6), (-79, 9)],
    [(-6, 35), (0, 36), (10, 37), (15, 32), (20, 32), (25, 32), (30, 31), (32, 31), (34, 28), (37, 22), (39, 18), (43, 12), (48, 11), (51, 11), (50, 5), (46, 0), (40, -5), (40, -12), (36, -18), (33, -25), (28, -33), (20, -35), (17, -32), (14, -28), (12, -18), (13, -12), (12, -6), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12), (-17, 15), (-16, 20), (-15, 25), (-10, 30), (-6, 35)],
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (0, 46), (-2, 48), (-1, 50), (2, 51), (5, 53), (7, 54), (8, 57), (10, 59), (12, 56), (18, 56), (21, 55), (24, 58), (28, 59), (30, 60), (30, 66), (32, 70), (40, 68), (45, 68), (52, 69), (58, 69), (65, 69), (70, 72), (75, 73), (80, 73), (85, 74), (90, 75), (95, 76), (100, 77), (105, 77), (110, 74), (115, 73), (120, 73), (125, 72), (130, 72), (135, 72), (140, 72), (145, 72), (150, 70), (155, 70), (160, 69), (165, 67), (170, 67), (175, 65), (178, 65), (173, 64), (170, 60), (165, 60), (162, 56), (158, 52), (156, 51), (150, 59), (145, 59), (142, 55), (140, 50), (140, 45), (138, 43), (135, 43), (132, 43), (130, 42), (128, 38), (126, 38), (124, 40), (122, 38), (120, 35), (120, 32), (118, 28), (115, 23), (112, 22), (110, 20), (108, 18), (106, 10), (104, 9), (101, 7), (99, 10), (97, 15), (95, 16), (93, 20), (91, 22), (89, 22), (87, 21), (85, 19), (82, 17), (80, 13), (78, 8), (76, 10), (74, 15), (73, 20), (71, 21), (68, 23), (66, 25), (63, 25), (60, 25), (57, 26), (54, 26), (52, 27), (50, 29), (49, 30), (47, 30), (44, 29), (42, 31), (39, 32), (36, 36), (33, 36), (30, 36), (27, 37), (26, 40), (23, 40), (22, 37), (20, 40), (19, 42), (16, 44), (14, 45), (12, 44), (10, 44), (8, 44), (6, 43), (3, 43), (0, 40), (-1, 37), (-3, 36), (-6, 36), (-9, 37), (-10, 36)],
    [(114, -22), (113, -26), (114, -30), (115, -34), (118, -35), (122, -34), (124, -33), (128, -32), (130, -32), (132, -32), (135, -35), (137, -35), (139, -37), (141, -38), (144, -38), (147, -39), (150, -37), (152, -35), (153, -32), (153, -28), (151, -24), (149, -20), (146, -19), (143, -15), (142, -11), (141, -13), (138, -15), (136, -15), (135, -12), (133, -12), (131, -12), (129, -14), (127, -14), (125, -16), (122, -17), (120, -20), (117, -20), (114, -22)],
    [(-5, 50), (-4, 53), (-5, 56), (-4, 58), (-2, 58), (-1, 57), (0, 54), (1, 52), (1, 51), (-2, 50), (-5, 50)],
    [(130, 31), (131, 33), (133, 34), (135, 34), (137, 35), (139, 35), (140, 37), (141, 39), (141, 41), (143, 42), (144, 44), (142, 44), (141, 41), (140, 38), (139, 36), (137, 34), (134, 34), (131, 32), (130, 31)],
    [(-45, 60), (-42, 64), (-38, 66), (-32, 68), (-28, 70), (-22, 72), (-20, 74), (-25, 76), (-32, 77), (-40, 77), (-48, 76), (-55, 74), (-58, 72), (-56, 68), (-53, 64), (-48, 62), (-45, 60)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (178, -37), (176, -40), (174, -42), (171, -43), (168, -46), (167, -45)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25), (43, -22), (43, -18), (44, -16)],
    [(95, 5), (98, 3), (100, 0), (103, -3), (105, -5), (104, -6), (102, -4), (100, 0), (97, 4), (95, 5)],
    [(109, 1), (111, 2), (114, 4), (117, 6), (118, 2), (117, -2), (115, -4), (111, -3), (109, 1)],
    [(131, -1), (134, -2), (137, -3), (140, -4), (143, -6), (146, -7), (149, -9), (147, -8), (144, -6), (141, -4), (138, -2), (135, -1), (131, -1)],
    [(105, -6), (108, -7), (111, -7), (114, -8), (113, -8), (110, -7), (107, -7), (105, -6)],
]

d.rectangle([MAP["x0"], MAP["y0"], MAP["x1"], MAP["y1"]], fill=MAPBG, outline=RULE, width=1)
for lon in range(-150, 181, 30):
    x, _ = project(lon, 0)
    d.line([(x, MAP["y0"]), (x, MAP["y1"])], fill=(218, 224, 218), width=1)
for lat in (60, 30, 0, -30):
    _, y = project(0, lat)
    d.line([(MAP["x0"], y), (MAP["x1"], y)], fill=(218, 224, 218), width=1)
for poly in CONTINENTS:
    pts = [project(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=LAND, outline=LANDLINE)
d.text((MAP["x0"] + 8, MAP["y0"] + 5), "WHERE IT HAPPENED — 10 PLACES ON THE MAP",
       font=SANS_B(10), fill=INK)

# pins: (number, lon, lat, label, label dx, dy, pin offset x, y)
# offsets separate circles that would overlap in crowded Europe / Gulf;
# a small dot + leader marks the true location when a pin is offset.
PINS = [
    (1, 47.5, 29.4, "KUWAIT", 8, -14, 0, -8),
    (2, 34.5, 31.5, "GAZA", -40, -8, -6, -6),
    (3, 100.5, 13.8, "BANGKOK", 8, -6, 0, 0),
    (4, 4.4, 50.8, "BRUSSELS", -58, -4, -16, -10),
    (5, 8.7, 50.1, "FRANKFURT", 6, -12, 14, -12),
    (6, 29.2, -1.7, "E. CONGO", 8, 2, 0, 0),
    (7, 1.4, 39.0, "IBIZA", -46, 4, -10, 10),
    (8, 31.2, 30.0, "CAIRO", -8, 12, -2, 10),
    (9, -15.6, 11.9, "BISSAU", -52, -6, 0, 0),
    (10, 56.5, 26.5, "HORMUZ", 8, 6, 12, 8),
]
for n, lon, lat, lab, dx, dy, ox, oy in PINS:
    px, py = project(lon, lat)
    cx, cy = px + ox, py + oy
    if ox or oy:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
        d.line([(px, py), (cx, cy)], fill=INK, width=1)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
    nf = SANS_B(8)
    d.text((cx, cy - 1), str(n), font=nf, fill=(255, 255, 255), anchor="mm")
    d.text((cx + dx, cy + dy), lab, font=SANS_B(8), fill=INK)

# ---------------------------------------------------------------- timeline
TX0, TY0, TX1 = 656, 340, 1012
d.text((TX0, TY0), "THROUGH THE DAY — UTC", font=SANS_B(11), fill=INK)
hline(TX0, TX1, TY0 + 18, wdt=2)
TL = [
    ("OVERNIGHT", "Gaza strikes kill 10 — third night of attacks", False),
    ("MORNING", "Kuwait drone attack; ECB picks Hernández de Cos", False),
    ("08:00 UTC", "Bangkok refinery blast injures 9", True),
    ("AFTERNOON", "EU summit deadlocks after 12+ hours of talks", False),
    ("EVENING", "Thanksgiving storms; Depardieu to stand trial", False),
]
tlx, tly = TX0 + 6, TY0 + 30
d.line([(tlx, tly + 4), (tlx, tly + 128)], fill=RULE, width=2)
for i, (when, what, hot) in enumerate(TL):
    y = tly + i * 27
    d.ellipse([tlx - 5, y - 1, tlx + 5, y + 9], fill=RED if hot else INK)
    wf = SANS_B(10)
    d.text((tlx + 14, y), when, font=wf, fill=RED if hot else INK)
    wx = tlx + 14 + int(tw(when, wf)) + 8
    for ln_i, ln in enumerate(fit_lines(what, SANS(10), TX1 - wx, 1)):
        d.text((wx, y), ln, font=SANS(10), fill=INK)
d.text((TX0, TY0 + 168), "Only 08:00 UTC is a verified clock time; the other",
       font=SANS(8), fill=MUTED)
d.text((TX0, TY0 + 179), "nodes are placed by reported sequence, not by clock.",
       font=SANS(8), fill=MUTED)

# ---------------------------------------------------------------- grid: 32 stories
# (headline <= 1 line, body <= 2 lines, source + tag)
GRID = [
    ("GAZA: 10 KILLED OVERNIGHT", "Strikes and shooting kill 10, incl. a Hamas deputy minister; third night of attacks.", "AP · REUTERS", "CONFIRMED"),
    ("ECB PICKS HERNANDEZ DE COS", "Ex-Bank of Spain chief, 55, succeeds Lagarde on 7 Feb 2027; first Spaniard in job.", "REUTERS · AP", "CONFIRMED"),
    ("IRGC: MINES HIT GULF TANKERS", "Two tankers hit mines near Oman; an LNG carrier also struck; Saudi stops a drone.", "AP", "REPORTED"),
    ("BANGKOK REFINERY BLAST HURTS 9", "Blast at Bangchak plant, 08:00 UTC; 3 critical; 120,000 bpd, Thailand's 5th-biggest.", "AP · CNN", "CONFIRMED"),
    ("CAIRO: TANKER-CRASH DRIVER HELD", "Driver detained after Wed's fire killed 31; he told police he drove at 110 km/h.", "CNN · AP", "CONFIRMED"),
    ("STORMS WRECK THANKSGIVING", "Macy's parade postponed to Saturday, a first; ~300,000 lose power; flights cancelled.", "BBC · GUARDIAN", "CONFIRMED"),
    ("VOTE PUSHED TO 2028", "Junta postpones elections to 26 Nov 2028, exactly a year after the coup.", "AP · REUTERS", "CONFIRMED"),
    ("DEPARDIEU MUST FACE RAPE TRIAL", "Paris appeals court rejects bid; actor, 77, to stand trial over alleged 2018 rape.", "AP · REUTERS", "CONFIRMED"),
    ("MISSILES KILL 3 OVERNIGHT", "Russia fires missiles and drones; Kyiv says 87 downed; Ukraine hits airbase, oil site.", "EURONEWS · CNBC", "REPORTED"),
    ("TANKER CAPSIZES OFF IBIZA", "Maltese tanker sinks with ~7,000t diesel; 16–17 crew rescued, 1 dies.", "BBC · AL JAZEERA", "CONFIRMED"),
    ("IRAN OIL 'COULD HIT ZERO'", "US naval blockade could halt crude exports by mid-Dec, analysts say.", "OILPRICE · YONHAP", "REPORTED"),
    ("'TRIAL HAS FALLEN APART'", "PM says corruption trial collapsed after judges floated dropping bribery charge.", "EURONEWS · FOX NEWS", "REPORTED"),
    ("CHINA, EU, JAPAN HIT BACK", "Beijing reserves right to act over US tariff plan; EU and Japan reject rationale.", "CNBC · BBC", "CONFIRMED"),
    ("DRONES KILL 15 IN BLUE NILE", "Drone attacks kill at least 15 as WFP warns of severe food shortage.", "AL JAZEERA", "REPORTED"),
    ("VOTE LOOMS AS RIVALS DEBATE", "Election Sunday; People's Party leads polls, may need Vox; rivals debated Thursday.", "STRAITS TIMES", "ONGOING"),
    ("FLOOD MISSING DECLARED DEAD", "Legal process begins for thousands missing after summer floods; wait cut to ~6 weeks.", "SCMP · LE MONDE", "OFFICIAL"),
    ("STORMS FLOOD US COAST", "King tides swamp California coast; part of Pacifica pier destroyed; record tides in LA.", "GUARDIAN · PHYS.ORG", "REPORTED"),
    ("CUTS 'COULD RAISE HIV CASES'", "UN warns funding cuts could push HIV infections up; Afghan women lose services.", "FRANCE 24 · DW", "OFFICIAL"),
    ("AIRLINE GROUNDS ALL FLIGHTS", "Norwegian carrier suspends flights, says it will file for bankruptcy without funding.", "BBC · GUARDIAN", "CONFIRMED"),
    ("RATE UP TO 3.25%", "Central bank lifts benchmark 25bp to a two-year high; growth forecast upgraded.", "CNBC", "OFFICIAL"),
    ("MINE FLOOD KILLS 13", "Heavy rain floods illegal gold mine on Java; 13 dead, ~13 missing after river burst.", "BBC · EURONEWS", "REPORTED"),
    ("ENVOY PULLED FROM ARGENTINA", "Brazil permanently withdraws ambassador; Milei not invited to Lula's inauguration.", "MERCOPRESS · STRAITS TIMES", "CONFIRMED"),
    ("SET TO MISS 2035 TARGET", "Australia projected to miss emissions goal; Flinders Island fire destroys ≥6 homes.", "PHYS.ORG · GUARDIAN", "REPORTED"),
    ("ISIL BOMBER KILLS 2", "Suicide attack at a Hasakah checkpoint kills two security staff, wounds five.", "AA", "REPORTED"),
    ("AFRICA CUP TITLE RESTORED", "CAS hands Senegal's title back; Morocco's federation vows to keep fighting.", "NPR · RFI", "OFFICIAL"),
    ("RETURN ROW SPLITS DELHI, DHAKA", "India separates Hasina's planned return from Dhaka's extradition request.", "THE HINDU · BBC", "REPORTED"),
    ("FOREIGN TROOPS PULL OUT", "Uganda and Somalia step up anti-al-Shabaab operations as foreign forces withdraw.", "BBC · ALLAFRICA", "REPORTED"),
    ("OUT OF AUSTRALIAN OPEN", "Jannik Sinner to miss the Open after knee surgery; out about four months.", "GUARDIAN · JAPAN TIMES", "CONFIRMED"),
    ("PUERTO RICO WINS", "Jennifer Barreto wins in San Juan; first married winner, first mother since 2023.", "EURONEWS", "CONFIRMED"),
    ("MIRAVAL FEUD SETTLED", "Ex-couple settle dispute over the French winery where they married.", "BBC · CBC", "CONFIRMED"),
    ("RAMSAY TO HOST REVIVAL", "Gordon Ramsay to front the revived show when filming starts next year.", "BBC", "CONFIRMED"),
    ("HIV SHOT REACHES AFRICA", "Cheaper twice-yearly injection, nearly 100% effective, reaching Africa.", "BBC", "REPORTED"),
]
gx, gy = 12, 540
gw, gh = 244, 44
for idx, (head, body, src, tag) in enumerate(GRID):
    col, row = idx % 4, idx // 4
    x = gx + col * (gw + 8)
    y = gy + row * gh
    if row:
        hline(x, x + gw, y - 2, fill=(200, 192, 176), wdt=1)
    hf = SANS_B(11)
    hl = fit_lines(head, hf, gw - 6, 1)
    d.text((x + 2, y), hl[0], font=hf, fill=INK)
    by = y + 13
    blines = fit_lines(body, SANS(9), gw - 6, 2)
    for j, ln in enumerate(blines):
        d.text((x + 2, by + j * 10), ln, font=SANS(9), fill=(48, 48, 48))
    sy2 = y + 34
    sf = SANS(7)
    d.text((x + 2, sy2), src, font=sf, fill=MUTED)
    sw = int(tw(src, sf))
    d.text((x + 2 + sw + 4, sy2), "— " + tag, font=SANS_B(7), fill=TAGC[tag])

# ---------------------------------------------------------------- MORE TODAY ticker
d.text((12, 902), "MORE TODAY", font=SANS_B(11), fill=RED)
hline(92, 1012, 908, wdt=1)
TICKER = [
    "Pig-kidney patient Molly Falco one year off dialysis — CBC",
    "Iraq court backs federal control of Kurdish oil; protests in Duhok — STRAITS TIMES",
    "UK–EU treaty texts published, with a 10-year exit clause — BBC",
    "Huang back at Nvidia as Congress presses FBI/CIA on vetting — NPR",
    "UK sent refugees to Eswatini in first permanent relocation — BBC",
    "Most distant quasar yet found, 630m years after the Big Bang — PHYS.ORG",
    "Rare lakes found more than a mile beneath the Red Sea — SCIENCEDAILY",
    "Euclid telescope finds its first comet — SCIENCEDAILY",
    "Canadian astronaut welcomes baby girl from space — BBC",
    "China–Cambodia begin Golden Dragon drills, ~3,000 troops — AFP",
    "Veruschka dies at 87; King Crimson's Michael Giles dies at 84 — BBC / GUARDIAN",
    "Judge blocks early review of ABC station licences — UPI / CNBC",
]
# (two-column flow: 6 rows x 2 cols)
for i, item in enumerate(TICKER):
    col, row = i % 2, i // 2
    x = 12 + col * 502
    y = 916 + row * 11
    d.text((x, y), "•  " + item, font=SANS(8), fill=(48, 48, 48))

# ---------------------------------------------------------------- DATE CHECK footer
fy = 986
d.rectangle([12, fy - 4, 1012, 1018], fill=(243, 226, 216), outline=RED, width=1)
d.text((20, fy), "DATE CHECK — NOT 26 NOVEMBER:", font=SANS_B(9), fill=RED)
dc = ("COP31 collapsed 22 Nov · Huang returned, NATO AWACS, Colombia bomb 23 Nov · "
      "Shenzhou-24 docking, KOSPI plunge 24 Nov · Kim's nuclear vow, birthright block, "
      "Lille 2–1 Bayern, Solomon treaty, Lukoil deal, FCC SpaceX, Bangladesh wage, "
      "HK tributes, Abrego Garcia 25 Nov · Cairo fire 25 Nov — today: driver detained · "
      "Savasleyka 24–25 Nov · Iowa blast 23 Nov · Chen Jining 24–25 Nov · "
      "Myanmar ICJ ~19–20 Nov · UK energy bills since ~12 Nov")
# wrap the DATE CHECK text into 2 lines
lines = wrap(dc, SANS(8), 972)
for j, ln in enumerate(lines[:2]):
    d.text((20, fy + 11 + j * 10), ln, font=SANS(8), fill=(60, 40, 32))

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
