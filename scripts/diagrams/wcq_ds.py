"""Diagrams for the WorkCover Queensland design system case study.

    python scripts/diagrams/wcq_ds.py <fonts-dir> public/media/wcq-ds

<fonts-dir> needs: Redaction-Regular.otf, Redaction35-Regular.otf, Redaction70-Regular.otf,
intertight-400.ttf, intertight-500.ttf, intertight-600.ttf, jbmono-500.ttf
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sketch import *  # noqa: E402,F401,F403

FONTS, OUT = sys.argv[1], sys.argv[2]
F = lambda name: os.path.join(FONTS, name)
RED, RED35, RED70 = F("Redaction-Regular.otf"), F("Redaction35-Regular.otf"), F("Redaction70-Regular.otf")
IT4, IT5, IT6 = F("intertight-400.ttf"), F("intertight-500.ttf"), F("intertight-600.ttf")
MONO = F("jbmono-500.ttf")

W, H = 1600, 840


def backdrop(seed, variant=0):
    """Eggshell paper with two soft dusty-pink blobs (a nod to the original pink shapes)."""
    left = [(0, 260), (220, 330), (520, 360), (640, 520), (600, 700), (720, H), (0, H)]
    right = [(860, 0), (W, 0), (W, 520), (1380, 420), (1080, 360), (980, 220)]
    if variant:
        left = [(0, 380), (260, 420), (420, 560), (640, 600), (760, H), (0, H)]
        right = [(900, 0), (W, 0), (W, 380), (1300, 300), (1060, 240)]
    return f'<rect width="{W}" height="{H}" fill="{PAPER}"/>' + blob(left) + blob(right)


def label(s, x, y=730, sub=None):
    out = text(s, IT6, 30, x, y, anchor="middle")
    if sub:
        out += text(sub, IT4, 28, x, y + 38, anchor="middle")
    return out


def plus_circle(cx, cy, r, rnd, color=INK, width=2.5):
    return (circle(cx, cy, r, rnd, width=width, color=color)
            + line(cx - r * 0.5, cy, cx + r * 0.5, cy, rnd, width=width, color=color)
            + line(cx, cy - r * 0.5, cx, cy + r * 0.5, rnd, width=width, color=color))


def save(name, body, title):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg(W, H, body, title))
    print("wrote", name)


# ---------- 1. Inconsistent styles ----------
def inconsistent():
    r = rng(1)
    b = backdrop(1)
    # Headings: same word, four different treatments.
    for s, path, size, y in (("Heading", RED, 76, 200), ("Heading", RED35, 66, 300),
                             ("Heading", IT6, 58, 392), ("Heading", RED70, 70, 490)):
        b += text(s, path, size, 175, y)
    b += label("Inconsistent headings", 320)
    # Buttons: different case, icons, padding and radius.
    cx = 800
    b += box(cx - 110, 140, 220, 66, r, r=12) + text("BUTTON", IT5, 26, cx, 183, anchor="middle", tracking=4)
    b += box(cx - 95, 240, 190, 62, r, r=26) + plus_circle(cx - 58, 271, 15, r) + text("Button", RED, 30, cx + 18, 282, anchor="middle")
    b += box(cx - 120, 336, 240, 78, r, r=8) + text("Button", IT4, 30, cx - 18, 385, anchor="middle") + plus_circle(cx + 62, 375, 15, r)
    b += box(cx - 88, 450, 176, 54, r, r=4) + text("BUTTON", IT6, 22, cx, 486, anchor="middle", tracking=3)
    b += label("Inconsistent buttons", cx)
    # Colours: four blues that should have been one.
    for (x, y, c) in ((1150, 150, "#6FA6E6"), (1330, 160, "#9BBFEB"), (1150, 330, SYSTEM), (1330, 335, "#5598E2")):
        b += box(x, y, 150, 150, r, r=6, fill=c)
    b += label("Inconsistent colours", 1300)
    save("inconsistent-styles.svg", b, "Inconsistent headings, buttons and colours")


# ---------- 2. Atomic layers ----------
def avatar(cx, cy, rad, rnd, color=INK, opacity=None):
    return (circle(cx, cy, rad, rnd, color=color, opacity=opacity)
            + circle(cx, cy - rad * 0.22, rad * 0.3, rnd, color=color, width=2.5, opacity=opacity)
            + stroke(f"M{cx - rad * 0.58:.1f},{cy + rad * 0.62:.1f} Q{cx:.1f},{cy - rad * 0.05:.1f} {cx + rad * 0.58:.1f},{cy + rad * 0.62:.1f}",
                     width=2.5, color=color, opacity=opacity))


def text_lines(x, y, widths, rnd, color=INK, opacity=None, gap=16):
    out = ""
    for i, row in enumerate(widths):
        xx = x
        for seg in row:
            out += line(xx, y + i * gap, xx + seg, y + i * gap, rnd, width=3, color=color, opacity=opacity)
            xx += seg + 10
    return out


def pill_button(x, y, w, h, rnd, color=INK, opacity=None, fill=SYSTEM):
    return (box(x, y, w, h, rnd, r=10, color=color, opacity=opacity)
            + box(x + 16, y + h / 2 - 5, w * 0.36, 10, rnd, r=5, fill=fill, width=0, opacity=opacity)
            + circle(x + w - 26, y + h / 2, 8, rnd, width=2, color=color, opacity=opacity))


def card(x, y, rnd, color=INK, opacity=None, accent=SYSTEM):
    return (box(x, y, 210, 160, rnd, r=14, fill="#FFFFFF", color=color, opacity=opacity)
            + avatar(x + 42, y + 42, 24, rnd, color=color, opacity=opacity)
            + text_lines(x + 22, y + 88, [[50, 14, 30, 50], [22, 54, 14, 44]], rnd, color=color, opacity=opacity)
            + pill_button(x + 22, y + 116, 110, 32, rnd, color=color, opacity=opacity, fill=accent))


def atomic():
    r = rng(2)
    b = backdrop(2)
    # Atoms
    b += avatar(170, 210, 30, r)
    b += text("Aa", RED, 64, 140, 320)
    b += text_lines(140, 360, [[60, 14, 30, 50], [22, 54, 14, 50], [40, 28, 60]], r)
    b += pill_button(140, 430, 120, 36, r)
    b += label("Atoms", 200)
    # Molecules
    b += card(500, 250, r)
    b += label("Molecules", 605)
    # Organisms: faded and struck out
    b += text("People", RED, 40, 905, 175, fill=MUTED, opacity=0.5)
    b += card(905, 195, r, color=MUTED, opacity=0.45, accent=MUTED)
    b += card(905, 380, r, color=MUTED, opacity=0.45, accent=MUTED)
    b += text("Organisms", IT6, 30, 1010, 730, anchor="middle", fill=MUTED)
    b += line(935, 720, 1088, 718, r, width=3.5, color=FOCUS)
    # Templates
    b += box(1250, 105, 270, 520, r, r=18, fill="#FFFFFF")
    b += text("People", RED, 40, 1280, 165, fill=INK)
    b += card(1280, 195, r)
    b += card(1280, 380, r)
    b += label("Templates", 1385)
    save("atomic-layers.svg", b, "Atoms, molecules and templates, with the organism layer removed")


# ---------- 3. Maturity curve ----------
def maturity():
    r = rng(3)
    b = backdrop(3, variant=1)
    ox, oy, ex, ty = 260, 700, 1300, 110
    b += line(ox, oy, ox, ty, r, width=4) + line(ox, oy, ex, oy - 12, r, width=4)
    b += text("Time", IT4, 26, (ox + ex) / 2, 760, anchor="middle")
    b += f'<g transform="rotate(-90 205 {(oy + ty) / 2})">' + text("Design system maturity", IT4, 26, 205, (oy + ty) / 2, anchor="middle") + "</g>"
    # S-curve: slow start, steep middle, plateau.
    pts = []
    for i in range(41):
        t = i / 40
        x = ox + 20 + t * 880
        y = oy - 20 - 500 / (1 + math.exp(-11 * (t - 0.48)))
        pts.append((x, y))
    from sketch import _smooth
    b += stroke(_smooth(pts), width=5)
    at = lambda t: pts[round(t * 40)]
    dots = [(0.12, PEOPLE), (0.42, SYSTEM), (0.66, DATA), (0.93, FOCUS)]
    for t, c in dots:
        x, y = at(t)
        b += circle(x, y, 12, r, fill=c, color=c)
    note = lambda rows, x, y: lines(rows, IT5, 24, x, y, 32)
    # 1: creating new components
    x, y = at(0.12)
    b += note(["Creating new", "components to meet", "needs of first", "applications"], 330, 380)
    b += arrow([(380, 510), (395, 580), (x - 14, y - 22)], r)
    # 2: approx half built
    x, y = at(0.42)
    b += note(["Approx. half the components", "built, beginning to reuse", "existing ones"], 840, 520)
    b += arrow([(830, 520), (720, 500), (x + 22, y + 6)], r)
    # 3: majority built
    x, y = at(0.66)
    b += note(["Majority of components built,", "time to increase discipline", "about new components"], 330, 175)
    b += arrow([(660, 180), (800, 175), (x - 18, y - 18)], r)
    # 4: fully functioning
    x, y = at(0.93)
    b += note(["Fully functioning design", "system. Groom and review", "components to keep", "up to date"], 1180, 330)
    b += arrow([(1220, 300), (1190, 230), (x + 8, y + 22)], r)
    save("maturity-curve.svg", b, "Climbing the hill of design system maturity")


# ---------- 4. Tools ----------
def figma_logo(cx, cy, s=1.0):
    u = 34 * s
    x0, y0 = cx - u, cy - 1.5 * u
    def half(x, y, side, c):  # rectangle with one side fully rounded
        if side == "left":
            return f'<path fill="{c}" d="M{x + u:.1f},{y:.1f} H{x + u / 2:.1f} A{u / 2:.1f},{u / 2:.1f} 0 0 0 {x + u / 2:.1f},{y + u:.1f} H{x + u:.1f} Z"/>'
        return f'<path fill="{c}" d="M{x:.1f},{y:.1f} H{x + u / 2:.1f} A{u / 2:.1f},{u / 2:.1f} 0 0 1 {x + u / 2:.1f},{y + u:.1f} H{x:.1f} Z"/>'
    return (half(x0, y0, "left", "#F24E1E") + half(x0 + u, y0, "right", "#FF7262")
            + half(x0, y0 + u, "left", "#A259FF")
            + f'<circle cx="{x0 + 1.5 * u:.1f}" cy="{y0 + 1.5 * u:.1f}" r="{u / 2:.1f}" fill="#1ABCFE"/>'
            + f'<path fill="#0ACF83" d="M{x0 + u:.1f},{y0 + 2 * u:.1f} H{x0 + u / 2:.1f} A{u / 2:.1f},{u / 2:.1f} 0 1 0 {x0 + u:.1f},{y0 + 2.5 * u:.1f} Z"/>')


def zeroheight_logo(cx, cy):
    grad = ('<defs><linearGradient id="zh" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#FF8A1F"/><stop offset="1" stop-color="#E9456B"/></linearGradient></defs>')
    pencil = (f'<path fill="url(#zh)" d="M{cx - 52},{cy - 52} l12,-24 l12,24 Z"/>'
              f'<rect fill="url(#zh)" x="{cx - 52}" y="{cy - 46}" width="24" height="92"/>'
              f'<rect fill="#FFFFFF" x="{cx - 52}" y="{cy + 26}" width="24" height="5"/>')
    chevron = f'<path fill="url(#zh)" d="M{cx - 6},{cy - 70} l68,70 l-68,70 l-16,-16 l52,-54 l-52,-54 Z"/>'
    return grad + pencil + chevron


def storybook_logo(cx, cy):
    return (f'<path fill="#FF4785" d="M{cx - 58},{cy - 76} L{cx + 50},{cy - 82} Q{cx + 60},{cy - 82} {cx + 60},{cy - 72} '
            f'L{cx + 60},{cy + 76} Q{cx + 60},{cy + 86} {cx + 50},{cy + 85} L{cx - 56},{cy + 80} Q{cx - 64},{cy + 79} {cx - 64},{cy + 71} '
            f'L{cx - 68},{cy - 66} Q{cx - 68},{cy - 75} {cx - 58},{cy - 76} Z"/>'
            f'<path fill="#FFFFFF" d="M{cx + 28},{cy - 82} v34 l10,-8 l10,8 v-35 Z"/>'
            + text("S", IT6, 150, cx - 4, cy + 52, anchor="middle", fill="#FFFFFF"))


def tools():
    r = rng(4)
    b = backdrop(4)
    for cx, logo, name, sub in ((400, figma_logo(400, 340), "Figma", "To design components"),
                                (800, zeroheight_logo(800, 340), "Zeroheight", "To document the system"),
                                (1200, storybook_logo(1200, 340), "Storybook", "To document the code")):
        b += box(cx - 140, 200, 280, 280, r, r=18, fill="#FFFFFF", width=3.5)
        b += logo
        b += label(name, cx, 590, sub)
    save("design-system-tools.svg", b, "Figma to design components, Zeroheight to document the system, Storybook to document the code")


# ---------- 5. Documentation attributes ----------
def button_sketch(x, y, w, h, rnd, label_size=30):
    return (box(x, y, w, h, rnd, r=8, fill="#FFFFFF")
            + text("Button", RED, label_size, x + w / 2 - 20, y + h / 2 + 10, anchor="middle")
            + circle(x + w - 40, y + h / 2, 13, rnd, width=2.5)
            + stroke(f"M{x + w - 47},{y + h / 2} H{x + w - 33} M{x + w - 38},{y + h / 2 - 5} L{x + w - 33},{y + h / 2} L{x + w - 38},{y + h / 2 + 5}", width=2.5))


def documentation():
    r = rng(5)
    b = backdrop(5)
    b += '<g transform="translate(0 90)">'
    # Components: numbered annotation + button
    b += circle(260, 290, 28, r, fill=INK) + text("1", IT6, 30, 260, 301, anchor="middle", fill="#FFFFFF")
    b += button_sketch(160, 340, 210, 70, r)
    b += label("Components", 265, 560)
    # Colour: swatch strip + token
    for i, (w, h, c) in enumerate(((62, 58, "#F5F4F0"), (52, 58, STRUCTURE_TINT), (88, 84, "#DCDAD3"), (74, 64, "#BDBBB4"))):
        x = 520 + sum(v[0] for v in ((62,), (52,), (88,), (74,))[:i])
        y = 300 - (h - 58) / 2
        b += box(x, y, w, h, r, r=4, fill=c, width=2.5)
    b += text("$neutral-tint-1", MONO, 24, 658, 420, anchor="middle")
    b += label("Colour", 658, 560)
    # Structure: button + dashed spacing token
    b += button_sketch(930, 230, 220, 70, r)
    b += box(940, 318, 200, 54, r, r=4, dash="10 9", fill=BLUSH, width=2.5)
    b += text("$space-02", MONO, 24, 1040, 354, anchor="middle")
    b += text("margin-bottom", MONO, 22, 1040, 420, anchor="middle", fill=MUTED)
    b += label("Structure", 1040, 560)
    # Typography: specimen + mixin
    b += text("Button text", RED, 40, 1390, 310, anchor="middle")
    b += text("@mixin: paragraph", MONO, 24, 1390, 380, anchor="middle")
    b += label("Typography", 1390, 560)
    b += "</g>"
    save("documentation-attributes.svg", b, "Components, colour, structure and typography documented with development tokens")


os.makedirs(OUT, exist_ok=True)
inconsistent()
atomic()
maturity()
tools()
documentation()
