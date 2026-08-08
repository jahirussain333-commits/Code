# Deploying the portfolio to InfinityFree

`index.html` is the whole site. The photo, all CSS and all JavaScript are embedded
in that one file — there is nothing else to upload for it to work.

(`assets/images/jahir-hussain.webp` is kept only as the original photo, in case the
page needs rebuilding later. It is **not** needed for hosting.)

## Where to put it

You already run the Leo Sports Store (WordPress) on `jahir.rf.gd`. WordPress uses
`index.php` at the root of `htdocs`, so **do not** drop `index.html` directly into
`htdocs` — most servers serve `index.html` before `index.php`, which would hide the
store behind the portfolio.

Pick one of these instead:

**Option A — portfolio as a sub-page of the existing site (recommended)**

1. Log in to InfinityFree → **Control Panel** → **File Manager** (or connect over FTP).
2. Open `htdocs`.
3. Create a new folder called `portfolio`.
4. Upload `index.html` into `htdocs/portfolio/`.
5. Visit **`https://jahir.rf.gd/portfolio/`**

**Option B — portfolio on its own domain/subdomain**

1. InfinityFree → **Domains** → add a subdomain (e.g. `me.jahir.rf.gd`) or a new account.
2. Upload `index.html` into that domain's own `htdocs` folder.
3. Visit the new address.

## After uploading

- Free InfinityFree accounts can take a few minutes to propagate, and new
  subdomains can take longer. A hard refresh (Ctrl/Cmd + Shift + R) clears a stale cache.
- Turn on free SSL from the control panel so the site loads over `https://`.

## Editing later

Everything is in `index.html` — open it in any text editor.

- Text, job entries, skills: edit the HTML directly.
- Colours: the `:root` block at the top of the `<style>` tag. `--accent` is the crimson.
- Rotating headline words: the `words` array in the `<script>` at the bottom.

## Optional: link preview image

When the page is shared on LinkedIn or WhatsApp it currently shows the title and
description but no picture. To add one, upload a photo (e.g. `preview.jpg`) next to
`index.html` and add this line inside `<head>`, using the real URL:

```html
<meta property="og:image" content="https://jahir.rf.gd/portfolio/preview.jpg">
```
