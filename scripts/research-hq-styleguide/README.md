# Research HQ style guide

Builds `public/styleguides/research-hq/index.html` from data extracted from the Figma file
"Work Journal JC" (Research HQ page, `StyleGuide` / `Panels` components).

- `tables.json`: the spec and data tables pulled from Figma.
- `build.py`: writes the HTML. Styles live in `public/styleguides/research-hq/style.css`.

Rebuild after editing `build.py` or `tables.json`:

    python3 scripts/research-hq-styleguide/build.py scripts/research-hq-styleguide public/styleguides/research-hq/index.html
