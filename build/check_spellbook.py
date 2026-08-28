# -*- coding: utf-8 -*-
"""What the spellbook actually looks like, before anyone has to load a save.

Every other validator checks that references resolve. None of them could tell
you that drinking one elixir put 19 entries in your spellbook, that 724 of 1,035
icons were the same string, or that half those entries did nothing when clicked.
This one answers "is it usable", which is the question that kept going unasked.
"""
import glob, json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, "Public", "EssenceDao", "Stats", "Generated")
DATA = os.path.join(GEN, "Data")
txt = "".join(open(f, encoding="utf-8").read()
              for f in glob.glob(os.path.join(DATA, "*.txt")))

MAX_CONTAINER = 32          # Larian's largest


def blocks():
    for blk in re.split(r"(?=^new entry )", txt, flags=re.M):
        m = re.match(r'new entry "([^"]+)"', blk)
        if m:
            yield m.group(1), blk


B = dict(blocks())


def field(name, key):
    m = re.search(r'data "%s" "([^"]*)"' % key, B.get(name, ""))
    return m.group(1) if m else None


problems = []

# --- top level ---------------------------------------------------------------
m = re.search(r'new entry "EssenceDao_Cultivator"(.*?)(?=\nnew entry|\Z)', txt, re.S)
top = re.findall(r"UnlockSpell\((\w+)\)", m.group(1))
print(f"top-level spellbook entries after the first elixir : {len(top)}")

later = 0
for stage in ("EssenceDao_Breakthrough_Foundation",
              "EssenceDao_Breakthrough_GoldenCore"):
    s = re.search(r'new entry "%s"(.*?)(?=\nnew entry|\Z)' % stage, txt, re.S)
    later += len(re.findall(r"UnlockSpell\((\w+)\)", s.group(1)))
print(f"added by the two later breakthroughs               : {later}")
print(f"total, ever                                        : {len(top) + later}")
if later:
    problems.append(("breaking through still adds spellbook icons - stage "
                     "gating should happen inside the containers", [str(later)]))

# --- containers --------------------------------------------------------------
print()
icons = {}
for name in top:
    cs = field(name, "ContainerSpells")
    if cs is None:
        continue
    kids = [k for k in cs.split(";") if k]
    icon = field(name, "Icon")
    icons.setdefault(icon, []).append(name)
    flag = "  <-- OVER LARIAN'S MAX" if len(kids) > MAX_CONTAINER else ""
    print(f"  {name:<34} {len(kids):>3} techniques   {icon}{flag}")
    if len(kids) > MAX_CONTAINER:
        problems.append((f"{name} holds {len(kids)}, above Larian's largest "
                         f"({MAX_CONTAINER})", [name]))

# Two halves of the same path *should* share an icon - they are "Wood - 1" and
# "Wood - 2", told apart by name. Two different paths sharing one is the bug.
def path_of(container):
    stem = container[len("Shout_EssenceDao_"):]
    return stem.rsplit("_", 1)[0] if stem.rsplit("_", 1)[-1].isdigit() else stem


dupes = {k: v for k, v in icons.items() if len({path_of(n) for n in v}) > 1}
if dupes:
    problems.append(("different paths sharing an icon - they are "
                     "indistinguishable in the spellbook",
                     [f"{k}: {', '.join(v)}" for k, v in dupes.items()]))

# --- every entry must do something -------------------------------------------
print()
dead = []
for name in top:
    cs = field(name, "ContainerSpells")
    for kid in ([k for k in cs.split(";") if k] if cs else [name]):
        props = field(kid, "SpellProperties") or ""
        if not props:
            dead.append(kid)
        # a toggle must handle both directions
        elif "ApplyStatus" in props and "RemoveStatus" not in props:
            dead.append(kid + " (binds but cannot release)")
print(f"entries that do nothing, or cannot be undone: {len(dead)}")
for d in dead[:6]:
    print(f"   {d}")
if dead:
    problems.append(("entries that are a no-op in one direction", dead))

# --- icon spread -------------------------------------------------------------
print()
all_icons = re.findall(r'data "Icon" "([^"]*)"', txt)
c = Counter(all_icons)
top_icon, top_n = c.most_common(1)[0]
share = top_n / len(all_icons)
print(f"icons: {len(all_icons)} fields, {len(c)} distinct; "
      f"most common {top_icon} at {share:.0%}")
if share > 0.5:
    problems.append((f"{share:.0%} of all icons are {top_icon} - the spellbook "
                     f"is unreadable", [top_icon]))

# --- report ------------------------------------------------------------------
if problems:
    print()
    for title, items in problems:
        print(f"!! {title}:")
        for i in items[:6]:
            print(f"     {i}")
    sys.exit(1)
print("\nOK - the spellbook is navigable.")
