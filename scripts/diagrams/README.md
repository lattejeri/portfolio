# Diagrams

Hand-drawn-style SVG diagrams for case studies. Text is converted to outlines so the SVGs
render correctly as images (they can't load web fonts).

- `sketch.py`: the drawing kit (outlined text, wobbly boxes/lines/circles, arrows, blobs).
- `wcq_ds.py`: diagrams for the WorkCover Queensland design system case study.

Needs Python with `fonttools`, plus a folder of font files: Redaction (Regular, 35, 70) from the
Redaction download, Inter Tight 400/500/600 and JetBrains Mono 500 from Google Fonts (TTF).

    python3 -m venv .venv && .venv/bin/pip install fonttools
    .venv/bin/python scripts/diagrams/wcq_ds.py <fonts-dir> public/media/wcq-ds
