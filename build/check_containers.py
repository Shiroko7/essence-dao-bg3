# -*- coding: utf-8 -*-
"""Look for the shapes that make BG3 hang rather than fail.

A dangling reference makes BG3 do nothing, quietly - that is what validate.py
is for. A *cycle* is different: the engine walks the spell tree to build your
spellbook, and a container that eventually contains itself gives it a walk with
no end. The symptom is a load that stops partway and never finishes, with
nothing in any log.

Also checks how deep containers nest and how long the generated
SpellProperties strings get, since both grew by an order of magnitude in the
rewrite that removed Osiris.
"""
import collections, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "Public", "EssenceDao", "Stats", "Generated", "Data")

edges = collections.defaultdict(set)
defined = set()
unlocks = collections.defaultdict(set)
longest = []

for path in glob.glob(os.path.join(DATA, "*.txt")):
    text = open(path, encoding="utf-8").read()
    for blk in re.split(r"(?=^new entry )", text, flags=re.M):
        m = re.match(r'new entry "([^"]+)"', blk)
        if not m:
            continue
        name = m.group(1)
        defined.add(name)
        for cs in re.findall(r'data "ContainerSpells" "([^"]*)"', blk):
            edges[name] |= {s for s in cs.split(";") if s}
        for boosts in re.findall(r'data "Boosts" "([^"]*)"', blk):
            unlocks[name] |= set(re.findall(r"UnlockSpell\(([A-Za-z0-9_]+)", boosts))
        for props in re.findall(r'data "SpellProperties" "([^"]*)"', blk):
            longest.append((len(props), name))

print(f"entries defined     : {len(defined)}")
print(f"container entries   : {len(edges)}")

problems = []

# --- self reference ---------------------------------------------------------
selfref = sorted(k for k, v in edges.items() if k in v)
if selfref:
    problems.append(("containers that contain themselves", selfref))

# --- cycles -----------------------------------------------------------------
WHITE, GREY, BLACK = 0, 1, 2
color = collections.defaultdict(int)
cycles = []


def dfs(n, stack):
    color[n] = GREY
    stack.append(n)
    for m in edges.get(n, ()):
        if color[m] == GREY:
            cycles.append(stack[stack.index(m):] + [m])
        elif color[m] == WHITE and m in edges:
            dfs(m, stack)
    stack.pop()
    color[n] = BLACK


sys.setrecursionlimit(10000)
for n in list(edges):
    if color[n] == WHITE:
        dfs(n, [])
if cycles:
    problems.append(("container cycles - the engine would walk these forever",
                     [" -> ".join(c) for c in cycles]))

# --- containers pointing at things that do not exist ------------------------
missing = sorted({s for v in edges.values() for s in v} - defined)
ours = [s for s in missing if "EssenceDao" in s]
if ours:
    problems.append(("ContainerSpells naming undefined EssenceDao spells", ours))

# --- scale ------------------------------------------------------------------
longest.sort(reverse=True)
print(f"deepest container   : {max((len(v) for v in edges.values()), default=0)} children")
print(f"longest SpellProperties: {longest[0][0]:,} chars ({longest[0][1]})"
      if longest else "no SpellProperties")

if problems:
    print()
    for title, items in problems:
        print(f"!! {title} ({len(items)}):")
        for i in items[:8]:
            print(f"     {i}")
        if len(items) > 8:
            print(f"     ... and {len(items)-8} more")
    sys.exit(1)

print("\nno cycles, no self-references")
