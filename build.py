"""Two builds from one source:
   dist/index.html      -> for hosting (photo inlined, fonts from Google CDN)
   portfolio-preview.html -> for the artifact (photo AND fonts inlined; CSP blocks CDNs)
"""
import base64, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent
scratch = pathlib.Path('/tmp/claude-0/-home-user-Code/49088d2e-9122-5d5a-a0b8-73fa0a091c5a/scratchpad')
src = (root / 'index.html').read_text(encoding='utf-8')

# ---- photo -> data URI -------------------------------------------------
img = (root / 'assets/images/jahir-hussain.webp').read_bytes()
assert img[:4] == b'RIFF' and img[8:12] == b'WEBP', 'photo is not a valid webp'
img_b64 = base64.b64encode(img).decode('ascii')
assert len(img_b64) % 4 == 0

REF = 'src="assets/images/jahir-hussain.webp"'
assert REF in src, 'photo reference not found'
hosted = src.replace(REF, f'src="data:image/webp;base64,{img_b64}"', 1)

dist = root / 'dist'
dist.mkdir(exist_ok=True)
(dist / 'index.html').write_text(hosted, encoding='utf-8')
print(f'dist/index.html      {len(hosted.encode()) / 1024:6.0f} KB  (fonts via CDN)')

# ---- artifact build: inline the fonts too ------------------------------
FONTS = scratch / 'pfonts'
spec = [
    ('Archivo',        'archivo',        [(400, None), (600, None), (800, None), (900, None)]),
    ('IBM Plex Sans',  'ibm-plex-sans',  [(400, None), (500, None)]),
    ('IBM Plex Mono',  'ibm-plex-mono',  [(400, None), (500, None), (600, None)]),
]
faces = []
missing = []
for family, pkg, weights in spec:
    for w, _ in weights:
        f = FONTS / pkg / 'files' / f'{pkg}-latin-{w}-normal.woff2'
        if not f.exists():
            missing.append(str(f)); continue
        b64 = base64.b64encode(f.read_bytes()).decode('ascii')
        faces.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2')}" % (family, w, b64))
if missing:
    print('MISSING FONT FILES:', *missing, sep='\n  '); sys.exit(1)

art = hosted
# drop CDN font tags — unreachable under the artifact CSP
art, n = re.subn(r'<link rel="preconnect"[^>]*>\s*', '', art)
art, n2 = re.subn(r'<link href="https://fonts\.googleapis\.com[^>]*>\s*', '', art)
assert n == 2 and n2 == 1, f'font tag removal off: preconnect={n} css={n2}'

style = re.search(r'<style>(.*?)</style>', art, re.S).group(1)
body = re.search(r'<body>(.*)</body>', art, re.S).group(1)
title = re.search(r'<title>(.*?)</title>', art, re.S).group(1)

# the artifact host supplies <head>, so re-issue the js bootstrap that lived there
boot = "<script>document.documentElement.className += ' js';</script>"
out = f"<title>{title}</title>\n<style>\n{chr(10).join(faces)}\n{style}</style>\n{boot}\n{body}"
(scratch / 'portfolio-preview.html').write_text(out, encoding='utf-8')
print(f'artifact preview     {len(out.encode()) / 1024:6.0f} KB  (fonts inlined)')
