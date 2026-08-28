# -*- coding: utf-8 -*-
"""Whole-mod reference check.

BG3 fails quietly. A spell that references a missing status just does nothing; a
handle with no localization row renders blank. Nothing errors, so every dangling
reference has to be caught here instead.

Checks:
  1. every localization handle used in stats exists in the XML
  2. every status referenced by ApplyStatus exists (ours, or Larian's)
  3. every spell referenced by UnlockSpell / ContainerSpells exists
  4. every passive referenced by a status's Passives field exists
  5. the dialogue's node graph has no dangling children

Larian's own entries are resolved against the unpacked game data when it is
available; without it, unknown names are reported as unverifiable rather than
as errors.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "Public", "EssenceDao", "Stats", "Generated")
# Localization lives under the module folder, not at the pak root - a root-level
# copy makes the game render every name as "Not Found". See gen_localization.py.
LOC = os.path.join(ROOT, "Mods", "EssenceDao", "Localization", "English")

VANILLA = os.environ.get("BG3_DATA", "")

# ---------------------------------------------------------------- our entries ---
ours = {"spell": set(), "status": set(), "passive": set(), "object": set()}
KIND = {"SpellData": "spell", "StatusData": "status",
        "PassiveData": "passive", "Object": "object"}

stat_text = {}
for path in glob.glob(os.path.join(DATA, "**", "*.txt"), recursive=True):
    text = open(path, encoding="utf-8").read()
    stat_text[path] = text
    cur = None
    for line in text.splitlines():
        m = re.match(r'^new entry "([^"]+)"', line)
        if m:
            cur = m.group(1); continue
        m = re.match(r'^type "([^"]+)"', line)
        if m and cur and m.group(1) in KIND:
            ours[KIND[m.group(1)]].add(cur)

# ---------------------------------------------------------------- vanilla ---
van = {"spell": set(), "status": set(), "passive": set()}
if VANILLA and os.path.isdir(VANILLA):
    for path in glob.glob(os.path.join(VANILLA, "**", "*.txt"), recursive=True):
        base = os.path.basename(path)
        bucket = ("spell" if base.startswith("Spell_") else
                  "status" if base.startswith("Status_") else
                  "passive" if base == "Passive.txt" else None)
        if not bucket:
            continue
        for line in open(path, encoding="utf-8", errors="ignore"):
            m = re.match(r'^new entry "([^"]+)"', line)
            if m:
                van[bucket].add(m.group(1))

# ---------------------------------------------------------------- handles ---
handles = set()
for path in glob.glob(os.path.join(LOC, "*.xml")):
    handles |= set(re.findall(r'contentuid="([^"]+)"', open(path, encoding="utf-8").read()))

used_handles = set()
for text in stat_text.values():
    used_handles |= set(re.findall(r'"(h[A-Za-z_0-9]+);\d+"', text))

problems = []

missing_h = used_handles - handles
if missing_h:
    problems.append(("localization handles with no entry", sorted(missing_h)))

# ------------------------------------------------------------- status refs ---
applied = set()
for text in stat_text.values():
    for m in re.finditer(r'ApplyStatus\(\s*(?:SELF|SOURCE|OBSERVER|CAUSE|TARGET)?\s*,?\s*'
                         r'([A-Z][A-Z0-9_]+)\s*,', text):
        applied.add(m.group(1))
unknown_status = {s for s in applied
                  if s not in ours["status"] and s not in van["status"]
                  and not s.startswith("SG_")}
if unknown_status and van["status"]:
    problems.append(("ApplyStatus targets not found", sorted(unknown_status)))
elif unknown_status:
    print(f"note: {len(unknown_status)} status refs unverifiable "
          f"(set BG3_DATA to check against game data)")

# -------------------------------------------------------------- spell refs ---
spell_refs = set()
for text in stat_text.values():
    spell_refs |= set(re.findall(r'UnlockSpell\(([A-Za-z0-9_]+)', text))
    for m in re.finditer(r'data "ContainerSpells" "([^"]*)"', text):
        spell_refs |= {s for s in m.group(1).split(";") if s}
unknown_spell = {s for s in spell_refs
                 if s not in ours["spell"] and s not in van["spell"]}
if unknown_spell and van["spell"]:
    problems.append(("UnlockSpell / ContainerSpells targets not found",
                     sorted(unknown_spell)))
elif unknown_spell:
    print(f"note: {len(unknown_spell)} spell refs unverifiable "
          f"(set BG3_DATA to check against game data)")

# ------------------------------------------------------------ passive refs ---
passive_refs = set()
for text in stat_text.values():
    for m in re.finditer(r'data "Passives" "([^"]*)"', text):
        passive_refs |= {p for p in m.group(1).split(";") if p}
# A Passives field may legitimately name one of Larian's - the guide carries
# Darkvision - so resolve against vanilla too when the game data is available.
missing_p = {p for p in passive_refs
             if p not in ours["passive"] and p not in van["passive"]}
if missing_p and van["passive"]:
    problems.append(("status Passives fields pointing nowhere", sorted(missing_p)))
elif missing_p:
    print(f"note: {len(missing_p)} passive refs unverifiable "
          f"(set BG3_DATA to check against game data)")

# ---------------------------------------------------------------- dialogue ---
for path in glob.glob(os.path.join(ROOT, "Mods", "**", "*.lsj"), recursive=True):
    d = json.load(open(path, encoding="utf-8"))
    nodes = d["save"]["regions"]["dialog"]["nodes"][0]
    ids = {n["UUID"]["value"] for n in nodes["node"]}
    dangling = []
    for n in nodes["node"]:
        for grp in n.get("children", [{}]):
            for c in grp.get("child", []):
                if c["UUID"]["value"] not in ids:
                    dangling.append(c["UUID"]["value"])
    if dangling:
        problems.append((f"dangling dialogue children in {os.path.basename(path)}",
                         dangling))

# ------------------------------------------------------------------ report ---
print(f"our entries     : {sum(len(v) for v in ours.values())} "
      f"({', '.join(f'{k} {len(v)}' for k, v in ours.items())})")
print(f"loc handles     : {len(handles)} defined, {len(used_handles)} used")
print(f"vanilla loaded  : {'yes' if van['spell'] else 'no (set BG3_DATA)'}")

if problems:
    print()
    for title, items in problems:
        print(f"!! {title} ({len(items)}):")
        for i in items[:12]:
            print(f"     {i}")
        if len(items) > 12:
            print(f"     ... and {len(items)-12} more")
    sys.exit(1)

print("\nOK - no dangling references.")
