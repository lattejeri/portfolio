"""Tiny SVG sketching kit for case-study diagrams.

- Text is converted to outlines (an SVG used as <img> can't load web fonts).
- Lines, boxes and circles get a slight hand-drawn wobble.
"""
import math
import random
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

INK = "#2C2C2A"
MUTED = "#6B6B66"
PAPER = "#FAF9F5"
BLUSH = "#FAECE7"  # palette: focus tint
FOCUS = "#D85A30"  # palette: focus line
PEOPLE = "#7F77DD"
SYSTEM = "#378ADD"
DATA = "#1D9E75"
FRICTION = "#BA7517"
STRUCTURE_TINT = "#F1EFE8"
STRUCTURE_LINE = "#888780"

_fonts = {}


def font(path):
    if path not in _fonts:
        f = TTFont(path)
        _fonts[path] = (f, f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _fonts[path]


def text_width(s, path, size, tracking=0):
    f, gs, cmap, hmtx, upm = font(path)
    w = 0
    for ch in s:
        g = cmap.get(ord(ch))
        if g:
            w += hmtx[g][0] * size / upm + tracking
    return w - (tracking if s else 0)


def text(s, path, size, x, y, fill=INK, anchor="start", tracking=0, opacity=None):
    """Outlined text. (x, y) is the baseline start / middle / end."""
    f, gs, cmap, hmtx, upm = font(path)
    scale = size / upm
    w = text_width(s, path, size, tracking)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    parts = []
    for ch in s:
        g = cmap.get(ord(ch))
        if not g:
            continue
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
        d = pen.getCommands()
        if d:
            parts.append(d)
        x += hmtx[g][0] * scale + tracking
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<path fill="{fill}"{op} d="{" ".join(parts)}"/>'


def lines(rows, path, size, x, y, leading, **kw):
    return "".join(text(r, path, size, x, y + i * leading, **kw) for i, r in enumerate(rows))


# ---------- hand-drawn geometry ----------

def _smooth(pts, closed=False):
    """Catmull-Rom through points → cubic Bézier path."""
    n = len(pts)
    if closed:
        get = lambda i: pts[i % n]
        rng = range(n)
    else:
        get = lambda i: pts[max(0, min(n - 1, i))]
        rng = range(n - 1)
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in rng:
        p0, p1, p2, p3 = get(i - 1), get(i), get(i + 1), get(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")


def wobble_line(x1, y1, x2, y2, rnd, amount=1.6, step=40):
    n = max(2, int(math.hypot(x2 - x1, y2 - y1) / step))
    pts = []
    for i in range(n + 1):
        t = i / n
        j = 0 if i in (0, n) else amount
        pts.append((x1 + (x2 - x1) * t + rnd.uniform(-j, j), y1 + (y2 - y1) * t + rnd.uniform(-j, j)))
    return pts


def stroke(d, width=3, color=INK, dash=None, opacity=None, cap="round"):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    extra += f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="{cap}" stroke-linejoin="round"{extra}/>')


def line(x1, y1, x2, y2, rnd, **kw):
    return stroke(_smooth(wobble_line(x1, y1, x2, y2, rnd)), **kw)


def _rounded_rect_points(x, y, w, h, r, step=36):
    """Points around a rounded rectangle as (x, y, wobble): corners stay clean, straight edges wobble."""
    def arc(cx, cy, a0):
        return [(cx + r * math.cos(math.radians(a0 + k * 22.5)), cy + r * math.sin(math.radians(a0 + k * 22.5)), 0)
                for k in range(1, 4)]
    def edge(p, q):
        n = max(1, int(math.hypot(q[0] - p[0], q[1] - p[1]) / step))
        return [(p[0] + (q[0] - p[0]) * k / n, p[1] + (q[1] - p[1]) * k / n, 0 if k == 0 else 1) for k in range(n)]
    tl, tr = (x + r, y), (x + w - r, y)
    rt, rb = (x + w, y + r), (x + w, y + h - r)
    br, bl = (x + w - r, y + h), (x + r, y + h)
    lb, lt = (x, y + h - r), (x, y + r)
    return (edge(tl, tr) + [(tr[0], tr[1], 0)] + arc(x + w - r, y + r, -90)
            + edge(rt, rb) + [(rb[0], rb[1], 0)] + arc(x + w - r, y + h - r, 0)
            + edge(br, bl) + [(bl[0], bl[1], 0)] + arc(x + r, y + h - r, 90)
            + edge(lb, lt) + [(lt[0], lt[1], 0)] + arc(x + r, y + r, 180))


def box(x, y, w, h, rnd, r=10, fill="none", width=3, color=INK, dash=None, opacity=None, amount=1.4):
    """Rounded rectangle drawn with a slightly unsteady hand."""
    r = max(2, min(r, w / 2, h / 2))
    pts = [(px + rnd.uniform(-amount, amount) * k, py + rnd.uniform(-amount, amount) * k)
           for px, py, k in _rounded_rect_points(x, y, w, h, r, step=36 if amount < 4 else 90)]
    d = _smooth(pts, closed=True)
    out = ""
    if fill != "none":
        op = f' opacity="{opacity}"' if opacity is not None else ""
        out += f'<path d="{d}" fill="{fill}"{op}/>'
    if width:
        out += stroke(d, width=width, color=color, dash=dash, opacity=opacity)
    return out


def circle(cx, cy, r, rnd, fill="none", width=3, color=INK, opacity=None):
    pts = []
    n = 14
    a0 = rnd.uniform(0, math.tau)
    for i in range(n):
        a = a0 + i * math.tau / n
        rr = r * (1 + rnd.uniform(-0.025, 0.025))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = _smooth(pts, closed=True)
    out = ""
    if fill != "none":
        op = f' opacity="{opacity}"' if opacity is not None else ""
        out += f'<path d="{d}" fill="{fill}"{op}/>'
    if width:
        out += stroke(d, width=width, color=color, opacity=opacity)
    return out


def arrow(points, rnd, width=3, color=INK, head=14):
    """Curved arrow through points, with an open arrowhead at the end."""
    d = _smooth(points)
    (x1, y1), (x2, y2) = points[-2], points[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    hd = ""
    for s in (-1, 1):
        hx = x2 - head * math.cos(a + s * 0.5)
        hy = y2 - head * math.sin(a + s * 0.5)
        hd += f" M{hx:.1f},{hy:.1f} L{x2:.1f},{y2:.1f}"
    return stroke(d + hd, width=width, color=color)


def blob(points, fill=BLUSH):
    return f'<path d="{_smooth(points, closed=True)}" fill="{fill}"/>'


def _trim(body):
    """Round coordinates to 1 decimal place to keep files small."""
    import re
    return re.sub(r"(-?\d+\.\d{2,})", lambda m: f"{float(m.group(1)):.1f}".rstrip("0").rstrip("."), body)


def svg(w, h, body, title):
    body = _trim(body)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def rng(seed):
    return random.Random(seed)
