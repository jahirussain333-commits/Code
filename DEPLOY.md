# Portfolio — build &amp; deploy

## What to upload

**`dist/index.html`** — that one file is the whole site. Your photo, all CSS and all
JavaScript are inside it. Nothing else needs to go up.

| File | What it is |
| --- | --- |
| `dist/index.html` | **Upload this.** Self-contained, ~232 KB. |
| `index.html` | Editable source. Same page, but loads the photo from `assets/`. |
| `assets/images/jahir-hussain.webp` | The original photo. |

Only the fonts come from Google Fonts over the network; everything else is embedded.

## Uploading to InfinityFree

You already run the Leo Sports Store (WordPress) on `jahir.rf.gd`. WordPress serves
`index.php` from the root of `htdocs`, and most servers try `index.html` **first** — so
putting this at the root would hide the store behind the portfolio. Use a subfolder:

1. InfinityFree → **Control Panel** → **File Manager** (or FTP).
2. Open `htdocs`, create a folder named `portfolio`.
3. Upload `dist/index.html` into `htdocs/portfolio/` (keep the name `index.html`).
4. Open **`https://jahir.rf.gd/portfolio/`**

Then enable the free SSL certificate from the control panel so it serves over `https`.

New uploads can take a few minutes to appear; a hard refresh (Ctrl/Cmd + Shift + R)
clears a stale copy.

To host it on its own address instead, add a subdomain under **Domains** and upload the
same file to that domain's own `htdocs`.

## Editing later

Edit `index.html` (the readable one), then rebuild the upload file:

```bash
python3 build.py          # writes dist/index.html
```

Common changes, all in `index.html`:

- **Text, jobs, skills** — plain HTML, edit in place. Skill chips need a
  `data-cat` of `data`, `crm`, `out` or `mkt` so the filter picks them up.
- **Colours** — the `:root` block at the top of the `<style>`. `--signal` is the ember,
  `--data` the teal.
- **Job duration bars** — each has `data-m="<months>"`; the `MAX` constant in the
  experience script is the longest tenure, so bars stay proportional.
- **Rotating tool ticker** — the `tools` array near the top of the `<script>`.

## Link previews

Shared on LinkedIn or WhatsApp the page shows its title and description but no picture.
To add one, upload an image next to the page and add this to `<head>` with the real URL:

```html
<meta property="og:image" content="https://jahir.rf.gd/portfolio/preview.jpg">
```

## Notes

- Everything degrades safely: with JavaScript blocked the full page still renders and
  reads — animations simply don't run.
- `prefers-reduced-motion` is respected throughout; the particle field renders one
  static resolved frame instead of animating.
- The hero canvas stops drawing once scrolled out of view, so it doesn't drain battery.
