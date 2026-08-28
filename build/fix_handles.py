# -*- coding: utf-8 -*-
"""Rewrite readable localization keys into valid BG3 handles, then build .loca.

The generators use readable keys (`hEssDao_Fire_Flame_Lash_Name`) because they
are legible in source and impossible to mistype. BG3 will not accept them: a
handle must be 'h' plus a GUID with dashes as 'g', fixed length. The Toolkit
rejected all ~1500 of ours:

    !ASSERT!Code: Translation not found for handle [hEssDaoPill_Foundation_Name]

and `divine -a convert-loca` overran its buffer writing fixed-width records.

This runs after every generator and rewrites the keys in place - in the stats,
the .lsx resources and the localization XML alike - so both sides agree by
construction. The mapping is uuid5-derived, so it is stable across rebuilds.

Finally it converts the XML to .loca, which is what the game actually loads.
"""
import glob, io, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from handles import handle, is_valid  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGETS = (
    glob.glob(os.path.join(ROOT, "Public", "**", "*.txt"), recursive=True)
    + glob.glob(os.path.join(ROOT, "Public", "**", "*.lsx"), recursive=True)
    + glob.glob(os.path.join(ROOT, "Mods", "**", "*.xml"), recursive=True)
    + glob.glob(os.path.join(ROOT, "Mods", "**", "*.lsj"), recursive=True)
    # Book content lives in Mods/<Mod>/Localization/*_Books.lsx and names a
    # handle. Miss it here and the handle is rewritten in english.xml but not in
    # the book, so the book resolves to nothing and reads as blank.
    + glob.glob(os.path.join(ROOT, "Mods", "**", "*.lsx"), recursive=True)
)

# Match only our own readable keys. An earlier version matched anything starting
# with 'h' and rewrote the XML attribute name `handle=` into a handle, corrupting
# every .lsx it touched. Anchoring on our prefix makes that impossible.
KEY = re.compile(r'\bhEss[A-Za-z0-9_]+\b')

mapping = {}
changed = 0
for path in TARGETS:
    text = io.open(path, encoding="utf-8").read()
    keys = set(KEY.findall(text))
    keys = {("h" + k[1:]) for k in keys}
    if not keys:
        continue

    def sub(m):
        k = m.group(0)
        mapping.setdefault(k, handle(k))
        return mapping[k]

    new = KEY.sub(sub, text)
    if new != text:
        io.open(path, "w", encoding="utf-8", newline="\n").write(new)
        changed += 1

print(f"rewrote {len(mapping)} handles across {changed} files")
bad = [h for h in mapping.values() if not is_valid(h)]
if bad:
    sys.exit(f"!! {len(bad)} generated handles are still invalid: {bad[:3]}")

# No .loca is built any more. Every working mod on this machine ships raw
# `Mods/<ModFolder>/Localization/English/english.xml` and nothing else; ours
# shipped a root-level .xml *and* .loca, and the game answered "Not Found" for
# every name in it. See gen_localization.py.
loc = os.path.join(ROOT, "Mods", "EssenceDao", "Localization", "English",
                   "english.xml")
if not os.path.isfile(loc):
    sys.exit("english.xml is missing - gen_localization.py must run first")
stale = glob.glob(os.path.join(ROOT, "Localization", "**", "*"), recursive=True)
if stale:
    sys.exit(f"a root-level Localization/ folder is back ({len(stale)} files) - "
             "it shadows the real one and breaks every name")
print(f"localization: {os.path.relpath(loc, ROOT)} "
      f"({os.path.getsize(loc)/1024:.1f} KB, no .loca by design)")
