"""Two builds from one source:
   dist/index.html        -> for hosting (photo inlined, fonts from Google CDN)
   build/portfolio-preview.html -> single-file preview (photo AND fonts inlined,
                                   for hosts whose CSP blocks CDNs)

Fonts are fetched once from the npm registry into .fontcache/ and reused.
"""
import base64, os, pathlib, re, shutil, subprocess, sys, tarfile, tempfile

root = pathlib.Path(__file__).resolve().parent
src = (root / 'index.html').read_text(encoding='utf-8')

# ---- photo -> data URI -------------------------------------------------
img = (root / 'assets/images/jahir-hussain.webp').read_bytes()
assert img[:4] == b'RIFF' and img[8:12] == b'WEBP', 'photo is not a valid webp'
img_b64 = base64.b64encode(img).decode('ascii')
assert len(img_b64) % 4 == 0

REF = 'src="assets/images/jahir-hussain.webp"'
DATA_URI = f'src="data:image/webp;base64,{img_b64}"'
assert REF in src, 'photo reference not found'
hosted = src.replace(REF, DATA_URI, 1)

dist = root / 'dist'
dist.mkdir(exist_ok=True)
(dist / 'index.html').write_text(hosted, encoding='utf-8')
print(f'dist/index.html      {len(hosted.encode()) / 1024:6.0f} KB  (fonts via CDN)')

# ---- second design: studio.html -> dist/studio.html ---------------------
studio_src = (root / 'studio.html').read_text(encoding='utf-8')
assert REF in studio_src, 'photo reference not found in studio.html'
studio = studio_src.replace(REF, DATA_URI, 1)
(dist / 'studio.html').write_text(studio, encoding='utf-8')
print(f'dist/studio.html     {len(studio.encode()) / 1024:6.0f} KB  (fonts via CDN)')

# ---- font cache --------------------------------------------------------
# Override with PORTFOLIO_FONT_CACHE=/some/dir if you already have the files.
FONTS = pathlib.Path(os.environ.get('PORTFOLIO_FONT_CACHE', root / '.fontcache'))

spec = [
    ('Archivo',         'archivo',         [400, 600, 800, 900]),
    ('IBM Plex Sans',   'ibm-plex-sans',   [400, 500]),
    ('IBM Plex Mono',   'ibm-plex-mono',   [400, 500, 600]),
    ('Anton',           'anton',           [400]),
    ('Instrument Sans', 'instrument-sans', [400, 500, 600]),
    ('Martian Mono',    'martian-mono',    [400, 600, 700]),
]


def face_path(pkg, weight):
    return FONTS / pkg / 'files' / f'{pkg}-latin-{weight}-normal.woff2'


def fetch(pkg):
    """Pull @fontsource/<pkg> from the npm registry into the cache."""
    dest = FONTS / pkg
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        r = subprocess.run(['npm', 'pack', f'@fontsource/{pkg}', '--silent'],
                           cwd=tmp, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f'npm pack @fontsource/{pkg} failed: {r.stderr.strip()}')
        tgz = next(tmp.glob('*.tgz'))
        with tarfile.open(tgz) as t:
            members = [m for m in t.getmembers() if m.name.startswith('package/files/')]
            t.extractall(tmp, members=members)
        dest.mkdir(parents=True, exist_ok=True)
        if (dest / 'files').exists():
            shutil.rmtree(dest / 'files')
        shutil.copytree(tmp / 'package' / 'files', dest / 'files')


faces = []
for family, pkg, weights in spec:
    if any(not face_path(pkg, w).exists() for w in weights):
        print(f'fetching @fontsource/{pkg} ...')
        fetch(pkg)
    for w in weights:
        f = face_path(pkg, w)
        if not f.exists():
            sys.exit(f'font file still missing after fetch: {f}')
        b64 = base64.b64encode(f.read_bytes()).decode('ascii')
        faces.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2')}" % (family, w, b64))

# ---- preview builds: inline the fonts too -------------------------------
def preview(page, name):
    """Strip the CDN font tags and re-emit as a head-less fragment with the
    faces inlined, for hosts whose CSP blocks outside requests."""
    art, n = re.subn(r'<link rel="preconnect"[^>]*>\s*', '', page)
    art, n2 = re.subn(r'<link href="https://fonts\.googleapis\.com[^>]*>\s*', '', art)
    assert n == 2 and n2 == 1, f'{name}: font tag removal off (preconnect={n} css={n2})'

    style = re.search(r'<style>(.*?)</style>', art, re.S).group(1)
    body = re.search(r'<body>(.*)</body>', art, re.S).group(1)
    title = re.search(r'<title>(.*?)</title>', art, re.S).group(1)

    # the preview host supplies <head>, so re-issue the js bootstrap that lived there
    boot = "<script>document.documentElement.className += \' js\';</script>"
    out = f"<title>{title}</title>\n<style>\n{chr(10).join(faces)}\n{style}</style>\n{boot}\n{body}"

    build = root / 'build'
    build.mkdir(exist_ok=True)
    (build / name).write_text(out, encoding='utf-8')
    print(f'build/{name:<24} {len(out.encode()) / 1024:6.0f} KB  (fonts inlined)')

preview(hosted, 'portfolio-preview.html')
preview(studio, 'studio-preview.html')
