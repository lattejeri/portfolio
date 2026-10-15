"""Crayon stroke that degrades into pixels, left to right. viewBox 500x100 (5:1)."""
import math, random, sys
random.seed(3)
W, H = 500, 100
COLOR = sys.argv[2] if len(sys.argv) > 2 else "#D85A30"

def centre(x):  # gentle hand-drawn wobble
    return 52 + 3.5 * math.sin(x / 70) - 0.012 * (x - 250)

def half(x):  # thickness: swells in, tapers slightly to the right
    t = x / W
    return 34 * min(1, (x - 6) / 18) ** 0.5 * (1 - 0.12 * t) if x > 6 else 0

# Rough-edged band outline (crayon part is only drawn up to ~80%; mask fades it).
top, bot = [], []
x = 6.0
while x <= W * 0.82:
    h = half(x)
    top.append((x, centre(x) - h + random.uniform(-2.2, 2.2)))
    bot.append((x, centre(x) + h + random.uniform(-2.2, 2.2)))
    x += random.uniform(3, 6)
outline = top + bot[::-1]
band = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in outline) + "Z"

# Pixels: square cells on a grid, density rises through the middle then thins out to scattered dust.
CELL = 5
pix = []
def smooth(a, b, v):
    t = max(0, min(1, (v - a) / (b - a)))
    return t * t * (3 - 2 * t)
for gx in range(int(W * 0.34) // CELL, W // CELL):
    x = gx * CELL
    rise = smooth(0.34, 0.6, x / W)
    fall = 1 - 0.8 * smooth(0.72, 1.0, x / W)
    for gy in range(0, H // CELL):
        y = gy * CELL
        d = abs(y + CELL / 2 - centre(x)) / max(half(min(x, W * 0.82)), 1)
        inside = d <= 1
        p = rise * fall * (0.85 if inside else 0.18 * max(0, 1.6 - d))
        if random.random() < p:
            op = random.choice([1, 1, 0.85, 0.7, 0.55])
            pix.append((x, y, op))

def rects(group_op):
    return "".join(f'M{x} {y}h{CELL}v{CELL}h-{CELL}z' for x, y, op in pix if op == group_op)

pixel_paths = "".join(
    f'<path fill-opacity="{op}" d="{rects(op)}"/>' for op in sorted({p[2] for p in pix})
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">
  <defs>
    <!-- Waxy crayon: streaky grain knocks holes in the fill; displacement roughens the edges. -->
    <filter id="wax" x="-5%" y="-20%" width="110%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="5" result="warp"/>
      <feDisplacementMap in="SourceGraphic" in2="warp" scale="7" xChannelSelector="R" yChannelSelector="G" result="rough"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.06 0.75" numOctaves="3" seed="8" result="grain"/>
      <feColorMatrix in="grain" result="grainAlpha" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -3.4 2.2"/>
      <feComposite in="rough" in2="grainAlpha" operator="in"/>
    </filter>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0.42" stop-color="#fff"/>
      <stop offset="0.74" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="fadeMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="url(#fade)"/>
    </mask>
  </defs>
  <g fill="{COLOR}">
    <g mask="url(#fadeMask)"><path d="{band}" filter="url(#wax)"/></g>
    <g shape-rendering="crispEdges">{pixel_paths}</g>
  </g>
</svg>
'''
open(sys.argv[1], "w").write(svg)
print(len(svg), "bytes,", len(pix), "pixels")
