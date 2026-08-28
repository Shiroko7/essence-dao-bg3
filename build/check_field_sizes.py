# -*- coding: utf-8 -*-
"""Compare our generated stat fields against the size Larian actually ships.

Osiris could iterate statuses by prefix; a spell cannot, so "release every
technique you hold" became one SpellProperties string with a RemoveStatus call
per technique. That string is now over 11,000 characters, which is the sort of
thing that works fine in a text file and not at all in a parser with a fixed
buffer.

This does not assert a limit - we do not know one. It reports ours against the
largest Larian ships, so "wildly out of distribution" is visible rather than
guessed at. Set BG3_DATA to the unpacked stats.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OURS = os.path.join(ROOT, "Public", "EssenceDao", "Stats", "Generated", "Data")
VANILLA = os.environ.get("BG3_DATA", "")

FIELDS = ("SpellProperties", "SpellSuccess", "SpellFail", "Boosts",
          "StatsFunctors", "ContainerSpells", "Passives")


def scan(paths):
    worst = {}
    for path in paths:
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        cur = None
        for line in text.splitlines():
            m = re.match(r'^new entry "([^"]+)"', line)
            if m:
                cur = m.group(1)
                continue
            m = re.match(r'^data "([A-Za-z]+)" "(.*)"$', line)
            if m and m.group(1) in FIELDS:
                f, v = m.group(1), m.group(2)
                if len(v) > worst.get(f, (0, ""))[0]:
                    worst[f] = (len(v), cur)
    return worst


ours = scan(glob.glob(os.path.join(OURS, "*.txt")))
van = scan(glob.glob(os.path.join(VANILLA, "**", "*.txt"), recursive=True)) \
    if VANILLA and os.path.isdir(VANILLA) else {}

if not van:
    print("BG3_DATA not set - cannot compare against Larian's own entries")

print(f"{'field':<18}{'ours':>9}  {'entry':<44}{'largest Larian ships':>22}")
print("-" * 96)
flags = []
for f in FIELDS:
    o_len, o_name = ours.get(f, (0, "-"))
    v_len, v_name = van.get(f, (0, "-"))
    mark = ""
    if v_len and o_len > v_len * 2:
        mark = "  <-- far beyond anything Larian ships"
        flags.append((f, o_name, o_len, v_len))
    print(f"{f:<18}{o_len:>9,}  {str(o_name)[:42]:<44}{v_len:>22,}{mark}")

if flags:
    print()
    for f, name, o, v in flags:
        print(f"!! {name}.{f} is {o:,} chars; Larian's largest is {v:,} "
              f"({o/max(v,1):.0f}x)")
    sys.exit(1)
