"""Copy the built site into a GitHub Pages checkout with clean URLs (no .html in links).

Usage: python3 build/publish.py /path/to/octos-repo
GitHub Pages serves /about for about.html, so only the links change; files keep their names.
"""
import os, re, shutil, sys

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = sys.argv[1]
SKIP = {"README.txt"}

def clean(html):
    def fix(m):
        url = m.group(2)
        url = re.sub(r'(^|/)index\.html(?=$|[?#])', lambda k: k.group(1) or './', url)
        url = re.sub(r'\.html(?=$|[?#])', '', url)
        return m.group(1) + url + '"'
    return re.sub(r'(href=")((?![a-z]+:)[^"]*?)"', fix, html)

for root, dirs, files in os.walk(SRC):
    for f in files:
        if f in SKIP:
            continue
        s = os.path.join(root, f)
        rel = os.path.relpath(s, SRC)
        d = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if f.endswith(".html"):
            open(d, "w").write(clean(open(s).read()))
        else:
            shutil.copy2(s, d)
print("published to", DST)
