"""Builds the Research HQ style guide as static HTML from data extracted from Figma."""
import html, json, sys

S = sys.argv[1]  # scratchpad/figma
OUT = sys.argv[2]  # public/styleguides/research-hq/index.html
tables = json.load(open(f"{S}/tables.json"))
e = html.escape

# ---------- building blocks ----------

def chevron():
    return '<img class="chev" src="assets/chevron.svg" alt="" width="20" height="20">'

def dropdown(value="No researcher selected", width=280):
    return f'<span class="input dropdown" style="width:{width}px"><span class="input-text">{e(value)}</span>{chevron()}</span>'

def textbox(value, width=106):
    return f'<span class="input" style="width:{width}px"><span class="input-text value">{e(value)}</span></span>'

def field(label, control, layout="left"):
    return f'<div class="field field-{layout}"><span class="label">{e(label)}</span>{control}</div>'

def slider(a="Author Faculty", b="To", width=224, fill=(0.11, 0.58)):
    half = (width - 12) // 2
    return (
        f'<div class="slider" style="width:{width}px">'
        f'<div class="slider-fields">{field(a, textbox("2021", half), "top")}{field(b, textbox("2025", half), "top")}</div>'
        f'<div class="track"><span class="fill" style="left:{fill[0]*100:.0f}%;right:{(1-fill[1])*100:.0f}%"></span>'
        f'<span class="thumb" style="left:{fill[0]*100:.0f}%"></span><span class="thumb" style="left:{fill[1]*100:.0f}%"></span></div>'
        "</div>"
    )

def button(text, kind="primary", disabled=False):
    return f'<span class="btn btn-{kind}{" is-disabled" if disabled else ""}">{e(text)}</span>'

def report_header(back=False):
    back_html = (
        '<span class="back"><img src="assets/arrow-left.svg" alt="" width="28" height="25"><span>Back</span></span>'
        if back else ""
    )
    return (
        '<div class="rh">'
        f'<div class="rh-top">{back_html}<div class="rh-titles"><div class="rh-title">Report name</div>'
        '<div class="rh-meta">Report metadata</div></div>'
        '<img class="qut" src="assets/qut-logo.svg" alt="QUT" width="48" height="48"></div>'
        f'<div class="rh-bar">{field("Researcher name", dropdown())}'
        f'<div class="rh-actions">{button("Drill through on selection", "primary", True)}'
        f'{button("Export paginated view", "secondary")}</div></div>'
        "</div>"
    )

def spec_table(rows):
    """Figma 'Style' tables: Element / State / Property / Value, grouped by rule lines."""
    head, body = rows[0]["cells"], rows[1:]
    out = ['<div class="scroll-x"><table class="spec"><thead><tr>']
    out += [f"<th>{e(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        cls = ' class="group-end"' if r["rule"] else ""
        cells = []
        for i, c in enumerate(r["cells"]):
            txt = e(c)
            if c.startswith("See "):
                txt = f'See <strong>{e(c[4:])}</strong>'
            cells.append(f'<td{" class=el" if i == 0 else ""}>{txt}</td>')
        out.append(f"<tr{cls}>{''.join(cells)}</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)

def section(id_, title, body):
    # Section ids are prefixed so the browser doesn't jump to them; app.js maps #font → sg-font.
    return f'<section class="page" id="sg-{id_}" data-page="{id_}" aria-labelledby="sg-{id_}-title"><h1 id="sg-{id_}-title">{e(title)}</h1>{body}</section>'

def group(title, body, level=2, cls=""):
    return f'<div class="group {cls}"><h{level}>{e(title)}</h{level}>{body}</div>'

def variant(component, caption):
    return f'<figure class="variant">{component}<figcaption>{e(caption)}</figcaption></figure>'

# ---------- pages ----------

fonts = [
    ("Caption 1", "Regular", 9, 12, 16), ("Caption 1 Strong", "Bold", 9, 12, 16),
    ("Caption 2", "Regular", 8, 10, 14), ("Caption 2 Strong", "Bold", 8, 10, 14),
    ("Body 1", "Regular", 10, 14, 20), ("Body 1 Strong", "Bold", 10, 14, 20),
    ("Body 1 Stronger", "Bold", 10, 14, 20), ("Body 2", "Regular", 12, 16, 22),
    ("Subtitle 1", "Bold", 15, 20, 26), ("Title 1", "Bold", 24, 32, 40),
    ("Title 2", "Bold", 21, 28, 36), ("Title 3", "Bold", 18, 24, 32),
    ("Large Title", "Bold", 30, 40, 52), ("Display", "Bold", 50, 68, 92),
]
font_html = '<div class="type-list">' + "".join(
    f'<div class="type-style"><div class="type-name">{name}</div>'
    f'<dl class="type-meta"><div><dt>Font</dt><dd>Arial</dd></div><div><dt>Weight</dt><dd>{w}</dd></div>'
    f'<div><dt>Size</dt><dd>{pt}</dd></div></dl>'
    f'<div class="type-preview"><p style="font-size:{px}px;line-height:{lh}px;font-weight:{700 if w == "Bold" else 400}">'
    "The quick brown fox jumps over the lazy dog.</p></div></div>"
    for name, w, pt, px, lh in fonts
) + "</div>"

def swatches(items):
    return '<div class="swatches">' + "".join(
        f'<div class="swatch"><span class="chip{" chip-light" if hx.upper() in ("#F9F9F9", "#F5F5F5", "#DBDBDB") else ""}" style="background:{hx}"></span>'
        f'<span class="sw-name">{e(n)}</span><span class="sw-hex">{hx}</span></div>'
        for n, hx in items
    ) + "</div>"

colour_html = (
    group("Theme colour", swatches([(f"Color {i+1}", h) for i, h in enumerate(
        ["#E37774", "#9F82BB", "#76A8FA", "#3FACC1", "#4DB58A", "#D797AF", "#D29342", "#7CBA79"])]))
    + group("Sentiment", swatches([("Negative", "#CF636E"), ("Positive", "#7CBA79"), ("Neutral", "#D9B300")]))
    + group("Advanced", swatches([("First", "#1C1C1C"), ("Second", "#616161"), ("Third", "#DBDBDB"),
                                  ("Fourth", "#B6B6B6"), ("Backgnd", "#F9F9F9"), ("2nd Bkgd", "#F5F5F5")]))
)

def slicer_column(first=("From", "To")):
    return f'<div class="slicer">{slider(*first)}</div>'

def report(content, faded=False, grid_strength="strong"):
    return (
        f'<div class="mock-fit"><div class="report{" faded" if faded else ""} grid-{grid_strength}">'
        f'<div class="report-chrome">{report_header(back=True)}</div>'
        f'<div class="report-body"><div class="report-chrome">{slicer_column()}</div>'
        f'<div class="canvas"><div class="cols" aria-hidden="true"><i></i><i></i><i></i><i></i></div>{content}</div></div>'
        "</div></div>"
    )

def card(label, icon):
    return f'<div class="card"><span class="card-label">{label}</span><img src="assets/{icon}.svg" alt="" class="card-icon"></div>'

layout_html = (
    group("Report view", report(
        '<div class="canvas-note"><p class="note-title">Placing objects in the content area</p>'
        '<p>Try to place every object in the layout within a 4 column grid with approx. 20px space on all sides (green spacers)</p>'
        '<p>Allow approx. 20px space around the outside of the content place in the content area (pink spacers)</p></div>'))
    + '<div class="group"><h2>Example layouts</h2>'
    + group("Full width chart and table", report(
        f'<div class="cards cards-stack">{card("Chart", "chart-line")}{card("Table", "table-cells")}</div>',
        faded=True, grid_strength="soft"), level=3)
    + group("3:1 table with chart", report(
        f'<div class="cards cards-1-3">{card("Chart", "chart-bars")}{card("Table", "table-cells")}</div>',
        faded=True, grid_strength="soft"), level=3)
    + group("2x2", report(
        f'<div class="cards cards-2x2">{card("Chart", "chart-bars")}{card("Chart", "chart-bars")}'
        f'{card("Table", "table-cells")}{card("Table", "table-cells")}</div>',
        faded=True, grid_strength="soft"), level=3)
    + "</div>"
)

ctrl = tables["controls"]
controls_html = (
    group("Dropdown slicer",
        group("Variations",
            '<div class="variants">'
            + variant(field("Researcher name", dropdown()), "Label left, no background")
            + variant(field("Researcher name", dropdown(), "top"), "Label top, no background")
            + variant(f'<div class="panel">{field("Researcher name", dropdown())}</div>', "Label left, background")
            + variant(f'<div class="panel">{field("Researcher name", dropdown(), "top")}</div>', "Label top, background")
            + "</div>", level=3)
        + group("Style", spec_table(ctrl[0][1]), level=3))
    + group("Slider slicer",
        group("Variations",
            '<div class="variants">'
            + variant(slider(), "No background")
            + variant(f'<div class="panel">{slider(width=237)}</div>', "Background")
            + "</div>", level=3)
        + group("Style", spec_table(ctrl[1][1]), level=3))
)

button_html = (
    group("Variations", '<div class="variants variants-tight">'
          + variant(button("Text"), "Primary") + variant(button("Text", "secondary"), "Secondary") + "</div>")
    + group("States", '<div class="variants variants-tight">'
          + variant(button("Text"), "Primary - default") + variant(button("Text", "secondary"), "Secondary - default")
          + variant(button("Text", "primary", True), "Primary - disabled")
          + variant(button("Text", "secondary", True), "Secondary - disabled") + "</div>")
    + group("Style", spec_table(tables["button"][0][1]))
)

hdr = tables["header"]
header_html = (
    group("States",
        group("On load", report_header(), level=3)
        + group("With back button", report_header(back=True), level=3)
        + group("With ‘drill through’ enabled", report_header(), level=3))
    + group("Style", spec_table(hdr[0][1]))
    + group("Structure", spec_table(hdr[1][1]))
)

filter_html = (
    '<div class="filter-layout">'
    '<aside class="filter-col"><div class="filter-heading">Report filters</div>'
    f'<div class="slicer">{field("Output classification", dropdown("All", 224), "top")}</div>'
    f'<div class="slicer">{slider()}</div>'
    f'<div class="slicer">{field("Author School", dropdown("All", 224), "top")}</div>'
    f'<div class="slicer">{field("Author School", dropdown("All", 224), "top")}</div>'
    "</aside>"
    + group("Style", spec_table(tables["filterbar"][0][1]))
    + "</div>"
)

data_rows = tables["table"][0][1]
widths = [128, 246, 72, 150, 116, 192, 114, 96]  # Figma widths, with Researcher name widened so its header fits
bar_widths = [79, 105, 74, 64]  # researcher names are redacted in the design
data = ['<div class="data-scroll" tabindex="0" role="region" aria-label="Example data table"><table class="data"><colgroup>']
data += [f'<col style="width:{w}px">' for w in widths]
data.append("</colgroup><thead><tr>" + "".join(f"<th>{e(c)}</th>" for c in data_rows[0]["cells"]) + "</tr></thead><tbody>")
for i, r in enumerate(data_rows[1:]):
    cells = []
    for j, c in enumerate(r["cells"]):
        if j == 3:
            cells.append(f'<td><span class="redacted" style="width:{bar_widths[i]}px" aria-label="Name redacted"></span></td>')
        elif j == 7 and c:
            cells.append(f'<td><span class="link">{e(c)}</span></td>')
        else:
            cells.append(f"<td>{e(c)}</td>")
    data.append(f"<tr>{''.join(cells)}</tr>")
data.append("</tbody></table></div>")
table_html = group("Data table", "".join(data)) + group("Style", spec_table(tables["table"][1][1]))

pages = [
    ("font", "Font", font_html), ("colour", "Colour", colour_html), ("layout", "Layout", layout_html),
    ("controls", "Controls", controls_html), ("button", "Button", button_html),
    ("header", "Header", header_html), ("filter-bar", "Filter bar", filter_html), ("table", "Table", table_html),
]
nav = [("Foundations", ["font", "colour", "layout"]), ("Components", ["controls", "button"]),
       ("Panels", ["header", "filter-bar", "table"])]
titles = {p[0]: p[1] for p in pages}

nav_html = "".join(
    f'<p class="nav-group">{g}</p><ul>' + "".join(f'<li><a href="#{p}">{titles[p]}</a></li>' for p in ps) + "</ul>"
    for g, ps in nav
)

doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research HQ global styling</title>
<meta name="description" content="Power BI style guide for Research HQ: type, colour, layout, controls, buttons, header, filter bar and table.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="sidebar" aria-label="Style guide">
  <a class="brand" href="#font">
    <span class="brand-mark"><img src="assets/rhq-logo.svg" alt="" width="24" height="23"></span>
    <span class="brand-name">Research HQ global styling</span>
  </a>
  {nav_html}
</nav>
<main class="content">
{''.join(section(i, t, b) for i, t, b in pages)}
</main>
<script src="app.js"></script>
</body>
</html>
"""
open(OUT, "w").write(doc)
print("wrote", OUT, len(doc), "bytes")
