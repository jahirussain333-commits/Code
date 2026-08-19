# Portfolio — deploy &amp; link from the WordPress store

`dist/index.html` is the entire site: photo, CSS and JavaScript are all inside that one
file. Nothing else needs uploading. Only the web fonts load from Google over the network.

| File | What it is |
| --- | --- |
| `dist/index.html` | **Upload this.** Self-contained, ~230 KB. |
| `dist/studio.html` | The second design — same content, video-inspired treatment. Also self-contained. |
| `index.html` | Editable source (loads the photo from `assets/`). |
| `build.py` | Regenerates `dist/index.html` after you edit the source. |

---

## Step 1 — Put the file on the server

Do **not** put it in the root of `htdocs`. WordPress serves `index.php` from there, and
most servers load `index.html` first — a root upload would hide your store behind the
portfolio. It goes in its own folder.

1. Log in at **infinityfree.com** → your account → **Control Panel**.
2. Open **File Manager** (or connect with FTP).
3. Go into **`htdocs`**. You should see WordPress files here — `wp-admin`, `wp-content`,
   `index.php`.
4. Create a new folder called **`portfolio`**.
5. Go inside `htdocs/portfolio/` and upload **`dist/index.html`**.
   Keep the filename exactly `index.html`.

The path must end up as: `htdocs/portfolio/index.html`

## Step 2 — Test it before touching WordPress

Open **`https://jahir.rf.gd/portfolio/`** in your browser. Get this working first — if
the link is broken, adding a menu item just hides the problem.

- Include the **trailing slash**.
- New uploads can take a minute. Hard-refresh with **Ctrl + Shift + R** (Cmd + Shift + R
  on Mac) to bypass the cache.
- If you get a 404, see Troubleshooting below.

WordPress will not interfere: its rewrite rules deliberately skip requests that match a
real file or folder on disk, so `/portfolio/` is served straight by the web server.

## Step 3 — Add the menu item in WordPress

Log in at `https://jahir.rf.gd/wp-admin`.

WordPress has two different menu systems. Check **Appearance** in the left sidebar:

- If you see **Appearance → Menus**, follow **3A** (classic theme).
- If there is no "Menus" entry, only **Appearance → Editor**, follow **3B** (block theme).

### 3A — Classic theme (Appearance → Menus)

1. **Appearance → Menus**.
2. At the top, in *Select a menu to edit*, choose your main navigation menu (often called
   "Primary", "Main Menu" or "Header"), then click **Select**.
3. In the left column, click **Custom Links** to expand it.
4. Fill in:
   - **URL** — `https://jahir.rf.gd/portfolio/`
   - **Link Text** — `Portfolio`
5. Click **Add to Menu**. It appears at the bottom of the menu structure on the right.
6. **Drag it** up or down to position it where you want.
7. Click **Save Menu**.

Visit your store and the Portfolio item should be in the navigation.

### 3B — Block theme (Appearance → Editor)

1. **Appearance → Editor**.
2. Click **Navigation** in the sidebar (or open a template and click the header's
   navigation block directly).
3. Click the **+** where you want the new item.
4. Choose **Custom Link**, paste `https://jahir.rf.gd/portfolio/`, press Enter, then set
   the label to `Portfolio`.
5. Click **Save** (top right).

## Step 4 (optional) — Open it in a new tab

Keeps your store open in the original tab.

**Classic theme:** the checkbox is hidden by default.

1. On the **Appearance → Menus** screen, click **Screen Options** in the very top-right.
2. Tick **Link Target**.
3. Expand your Portfolio item using the small arrow on its right.
4. Tick **Open link in a new tab**.
5. **Save Menu**.

**Block theme:** select the link, open the settings sidebar, enable **Open in new tab**.

---

## Getting back to the store

The portfolio header has a teal **↩ Store** link, and the mobile menu has
**↩ Back to the store**, so visitors are not stranded.

Both point to `/` — the root of whatever domain the page is on, which is your store. If
you ever host the portfolio on a *different* domain from the store, change those two
`href="/"` values in `index.html` to the full store URL and rebuild.

## Troubleshooting

**`/portfolio/` shows 404**
- Confirm the file is at `htdocs/portfolio/index.html` — not `htdocs/index.html`, and not
  `htdocs/portfolio/dist/index.html` (easy to do if you upload the folder by accident).
- Confirm the filename is exactly `index.html`, lowercase.

**It shows a file listing instead of the page** — the file is named something other than
`index.html`. Rename it.

**The store's homepage now shows the portfolio** — the file went into `htdocs` root.
Delete `htdocs/index.html` and re-upload into `htdocs/portfolio/` instead.

**Menu item 404s but the direct URL works** — a typo in the Custom Link URL, or a missing
trailing slash. Re-check it in the menu editor.

**Browser warns about the connection** — turn on the free SSL certificate in the
InfinityFree control panel so the page serves over `https`.

**Do not create a WordPress Page with the slug `portfolio`.** The real folder on disk wins,
so the WP page would silently never appear and be confusing later.

---

## Editing the portfolio later

Edit `index.html` (the readable one), then rebuild the upload file:

```bash
python3 build.py     # writes dist/index.html
```

It also writes `build/portfolio-preview.html` — the same page with the fonts
embedded instead of loaded from Google, for previewing somewhere that blocks
outside requests. You do not upload that one. The first run downloads the fonts
into `.fontcache/` and reuses them after that; both folders are gitignored.

Re-upload `dist/index.html`, overwriting the old one, and hard-refresh.

- **Text, jobs, skills** — plain HTML. Skill chips need a `data-cat` of `data`, `crm`,
  `out` or `mkt` so the filter picks them up. If you add or remove chips, update the
  matching `data-to` on the "Skills listed" counter so the number stays honest.
- **Colours** — the `:root` block at the top of the `<style>`. `--signal` is the ember,
  `--data` the teal.
- **Duration bars** — each has `data-m="<months>"`; the `MAX` constant in the experience
  script is the longest tenure, keeping bars proportional.
- **Tool ticker** — the `tools` array near the top of the `<script>`.

## Notes

- With JavaScript blocked the full page still renders and reads; animations just don't run.
- `prefers-reduced-motion` is respected: the particle field draws one static resolved
  frame and the ticker becomes a plain wrapped list.
- The hero canvas stops drawing when scrolled out of view.
