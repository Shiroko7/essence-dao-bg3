# -*- coding: utf-8 -*-
"""End-to-end wiring check.

validate.py proves nothing dangles. This proves the pieces are actually joined
up - a different question, and the one that catches the failures that ship
silently because every reference in them resolves.

The checks below are not hypothetical. Each one is a bug that shipped:

  * a 20 MB Osiris story at a path the engine never reads, so not one rule ever
    ran (check 1)
  * consumables whose use-action lived in Object.txt, where it does nothing, so
    drinking a pill had no effect (check 3)
  * an alchemy recipe whose ingredients were already Greater Healing Potion's
    (check 4)
  * a spell unlocked by a passive that no stats entry defined (check 5)
"""
import glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "Public", "EssenceDao")
DATA = os.path.join(PUB, "Stats", "Generated", "Data")
MODS = os.path.join(ROOT, "Mods", "EssenceDao")

problems = []


def stats_text():
    out = []
    for f in glob.glob(os.path.join(DATA, "*.txt")):
        out.append(open(f, encoding="utf-8").read())
    for f in glob.glob(os.path.join(PUB, "Stats", "Generated", "*.txt")):
        out.append(open(f, encoding="utf-8").read())
    return "\n".join(out)


ALL = stats_text()
entries = set(re.findall(r'new entry "([^"]+)"', ALL))

# --- 1. no compiled Osiris story ---------------------------------------------
# An add-on cannot run Osiris rules: the engine loads one compiled story, from
# the campaign module's path. What the Toolkit produces is not "our goals" but
# the whole campaign script with ours folded in - 31 MB - so shipping it would
# replace base-game Withers and break every other Osiris mod if it ever loaded.
#
# Nothing under Story/ ships any more - the NPC and its dialogue are gone. See
# docs/npc-and-dialogue.md before reintroducing either.
STORY = os.path.join(MODS, "Story")
if os.path.isdir(STORY):
    problems.append(("a Story folder is back - the NPC and dialogue were "
                     "removed deliberately; read docs/npc-and-dialogue.md",
                     [os.path.relpath(STORY, ROOT)]))

meta_path = os.path.join(MODS, "meta.lsx")
meta = open(meta_path, encoding="utf-8").read() if os.path.isfile(meta_path) else ""
# Declaring story mode with no story behind it hung save loading at 79%.
if 'value="Story"' in meta:
    problems.append(("meta declares TargetModes:Story but no story ships - "
                     "this hung save loading at 79%", ["TargetModes"]))

# Localization must be the single module-folder english.xml. A root-level
# Localization/ folder makes every name render as "Not Found".
if os.path.isdir(os.path.join(ROOT, "Localization")):
    problems.append(("a root-level Localization/ folder is back - it shadows "
                     "Mods/EssenceDao/Localization and breaks every name",
                     ["Localization/"]))
loc = os.path.join(MODS, "Localization", "English", "english.xml")
if not os.path.isfile(loc):
    problems.append(("Mods/EssenceDao/Localization/English/english.xml is "
                     "missing - no name in the mod will resolve", [loc]))
if '"UUID" type="FixedString"' not in meta:
    problems.append(("meta UUID must be typed FixedString or the module is "
                     "skipped silently", ["UUID"]))

# --- 2. the mod is reachable without a script --------------------------------
# Everything hangs off the Cultivator passive, which is carried by a status,
# which is applied by a drink, which is brewed by a recipe. Break any link and
# the mod is unreachable on a save that is already in progress.
chain = [("EssenceDao_Cultivator", "Passive.txt", 'new entry "EssenceDao_Cultivator"'),
         ("ESSDAO_CULTIVATOR", "Status_BOOST_Pills.txt", 'new entry "ESSDAO_CULTIVATOR"'),
         ("OBJ_EssenceDao_AwakeningBalm", "Object.txt",
          'new entry "OBJ_EssenceDao_AwakeningBalm"'),
         ("ALCH_EssenceDao_AwakeningBalm", "../ItemCombos.txt",
          'new ItemCombination "ALCH_EssenceDao_AwakeningBalm"'),
         # and the book, which is how anyone learns the mod exists at all
         ("OBJ_EssenceDao_Tome", "Object.txt",
          'new entry "OBJ_EssenceDao_Tome"'),
         ("TUT_Chest_Potions", "../TreasureTable.txt",
          'new treasuretable "TUT_Chest_Potions"'),
         ("I_OBJ_EssenceDao_Tome", "../TreasureTable.txt",
          'object category "I_OBJ_EssenceDao_Tome"')]
for what, where, needle in chain:
    if needle not in ALL:
        problems.append((f"the way in is broken: {what} is missing from {where}",
                         [what]))
# and the status must actually carry the passive
m = re.search(r'new entry "ESSDAO_CULTIVATOR"(.*?)(?=\nnew entry|\Z)', ALL, re.S)
if m and "EssenceDao_Cultivator" not in m.group(1):
    problems.append(("ESSDAO_CULTIVATOR does not carry the Cultivator passive - "
                     "drinking the draught would do nothing", ["Passives"]))

# --- 2b. redefining Larian's chest must not empty it -------------------------
# A treasuretable redefinition replaces rather than extends, so our version of
# TUT_Chest_Potions has to carry Larian's contents forward as well as ours.
# Forget that and the tutorial chest silently loses its healing potions.
m = re.search(r'new treasuretable "TUT_Chest_Potions"(.*?)(?=\nnew treasuretable|\Z)',
              ALL, re.S)
if m and "I_OBJ_Potion_Healing" not in m.group(1):
    problems.append(("our TUT_Chest_Potions drops Larian's healing potions - "
                     "redefining a treasuretable replaces it",
                     ["I_OBJ_Potion_Healing"]))

# --- 3. every consumable applies its status from the root template -----------
# Object.txt cannot do this. Larian never once does it there, and neither can we.
#
# By the time this runs, _merged.lsx has been converted to the binary .lsf the
# engine actually loads and the source removed. Checking the .lsx would only
# prove the generator agreed with itself, so decode the shipped .lsf instead -
# that is the artefact the game reads.
rt_manifest = os.path.join(PUB, "RootTemplates", "templates.json")
templates = json.load(open(rt_manifest, encoding="utf-8")) if os.path.isfile(rt_manifest) else {}


def shipped_templates_xml():
    lsf = os.path.join(PUB, "RootTemplates", "_merged.lsf")
    lsx = os.path.join(PUB, "RootTemplates", "_merged.lsx")
    if os.path.isfile(lsx):                       # not yet converted
        return open(lsx, encoding="utf-8").read()
    if not os.path.isfile(lsf):
        return ""
    divine = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "lslib", "Tools", "Divine.exe")
    if not os.path.isfile(divine):
        print("note: Divine.exe missing - root template contents unchecked")
        return None
    tmp = lsf + ".check.lsx"
    r = subprocess.run([divine, "-g", "bg3", "-a", "convert-resource",
                        "-s", lsf, "-d", tmp, "-o", "lsx"],
                       capture_output=True, text=True,
                       env=dict(os.environ, DOTNET_ROLL_FORWARD="Major"))
    if r.returncode != 0 or not os.path.isfile(tmp):
        problems.append(("the shipped _merged.lsf could not be decoded - the "
                         "engine will not read it either", [r.stderr.strip()[:120]]))
        return None
    text = open(tmp, encoding="utf-8").read()
    os.remove(tmp)
    return text


rt_text = shipped_templates_xml()
if rt_text:
    blocks = re.split(r'(?=<node id="GameObjects">)', rt_text)
    by_name = {}
    for b in blocks:
        m = re.search(r'id="Name" type="LSString" value="([^"]+)"', b)
        if m:
            by_name[m.group(1)] = b
    for name, info in templates.items():
        blk = by_name.get(name)
        if blk is None:
            problems.append((f"{name} is missing from the shipped root templates",
                             [name]))
            continue
        if name == "OBJ_EssenceDao_Tome":
            # A book with no BookId inherits GEN_Unreadable from its parent and
            # the game reports it as crumbled to dust. An item Description is a
            # tooltip, not book content.
            m = re.search(r'id="BookId"[^>]*value="([^"]+)"', blk)
            if not m:
                problems.append((f"{name} has no BookId - it will read as "
                                 f"'crumbled to dust'", [name]))
            else:
                bf = glob.glob(os.path.join(MODS, "Localization", "*_Books.lsf"))
                if not bf:
                    problems.append(("no *_Books.lsf ships - the book has no "
                                     "pages", [m.group(1)]))
                else:
                    # And the handle it names must survive into english.xml.
                    # The rewrite pass renames handles; when it skipped the book
                    # file the two sides disagreed and the pages came out blank.
                    import subprocess as _sp
                    tmp = bf[0] + ".check.lsx"
                    _sp.run([os.path.join(os.path.dirname(
                        os.path.abspath(__file__)), "lslib", "Tools",
                        "Divine.exe"), "-g", "bg3", "-a", "convert-resource",
                        "-s", bf[0], "-d", tmp, "-o", "lsx"],
                        capture_output=True, env=dict(os.environ,
                                                      DOTNET_ROLL_FORWARD="Major"))
                    if os.path.isfile(tmp):
                        btxt = open(tmp, encoding="utf-8").read()
                        os.remove(tmp)
                        loc = open(os.path.join(MODS, "Localization", "English",
                                                "english.xml"),
                                   encoding="utf-8").read()
                        for h in re.findall(r'handle="([^"]+)"', btxt):
                            if f'contentuid="{h}"' not in loc:
                                problems.append((
                                    f"book handle {h} has no entry in "
                                    f"english.xml - the pages render blank",
                                    [h]))

        want = info.get("status")
        if want is None:
            # The book. It is meant to have no use-action at all: it is the
            # instructions, not a key. Assert that, so nobody quietly makes it
            # a trigger again.
            if "OnUsePeaceActions" in blk:
                problems.append((f"{name} has a use action - the book is "
                                 f"supposed to do nothing when used", [name]))
            continue
        if "OnUsePeaceActions" not in blk:
            problems.append((f"{name} has no OnUsePeaceActions - drinking it "
                             f"does nothing", [name]))
        elif f'value="{want}"' not in blk:
            problems.append((f"{name}'s use action does not apply {want}",
                             [name]))

for name in re.findall(r'new entry "(OBJ_EssenceDao_[A-Za-z]+)"', ALL):
    if name not in templates:
        problems.append((f"{name} has no root template - it cannot exist", [name]))

# --- 4. no recipe collides with a vanilla one --------------------------------
# Two recipes claiming the same ingredient pair is undefined; ours loses or
# breaks theirs. The list below is Larian's 63 ExtractToSolution pairs, harvested
# from SharedDev/Stats/Generated/ItemCombos.txt.
VANILLA_PAIRS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "vanilla_alchemy_pairs.json")
if os.path.isfile(VANILLA_PAIRS):
    taken = {tuple(p[:2]): p[2] for p in json.load(open(VANILLA_PAIRS, encoding="utf-8"))}
    combos = open(os.path.join(PUB, "Stats", "Generated", "ItemCombos.txt"),
                  encoding="utf-8").read()
    for blk in re.split(r'\n(?=new ItemCombination )', combos):
        o1 = re.search(r'"Object 1" "([^"]+)"', blk)
        o2 = re.search(r'"Object 2" "([^"]+)"', blk)
        if not (o1 and o2):
            continue
        key = (o1.group(1), o2.group(1))
        if key in taken:
            nm = re.match(r'new ItemCombination "([^"]+)"', blk).group(1)
            problems.append((f"{nm} uses the same ingredients as vanilla "
                             f"{taken[key]}", [" + ".join(key)]))
else:
    print("note: vanilla_alchemy_pairs.json missing - recipe collisions unchecked")

# --- 5. every spell a passive unlocks exists ---------------------------------
# UnlockSpell naming a spell that no entry defines is silent: the passive
# applies, the spell is simply absent, and the container looks empty.
passives = "\n".join(open(f, encoding="utf-8").read()
                     for f in glob.glob(os.path.join(DATA, "Passive*.txt")))
# Only our own spells can be checked here. A passive may legitimately unlock a
# vanilla one - the Wind path hands out the monk's Step of the Wind - and those
# live in Larian's stats, which validate.py checks when BG3_DATA is set.
missing = sorted({s for s in re.findall(r'UnlockSpell\(([A-Za-z0-9_]+)\)', passives)
                  if "EssenceDao" in s and s not in entries})
if missing:
    problems.append((f"{len(missing)} unlocked spell(s) are never defined", missing))

# --- 6. every spell needs a cast animation -----------------------------------
#     !ASSERT!Design: Spell prototype 'X' has no cast animations.
# Not fatal, but it floods the log and the spell plays nothing in game.
noanim = []
for f in glob.glob(os.path.join(DATA, "Spell_*.txt")):
    for blk in re.split(r'(?=^new entry )', open(f, encoding="utf-8").read(), flags=re.M):
        if blk.startswith("new entry") and "SpellAnimation" not in blk:
            noanim.append(re.match(r'new entry "([^"]+)"', blk).group(1))
if noanim:
    problems.append((f"{len(noanim)} spell(s) with no SpellAnimation", noanim))

# --- report ------------------------------------------------------------------
print(f"stats entries   : {len(entries)}")
print(f"root templates  : {len(templates)}")
print(f"osiris          : none (correct - see gen_meta.py)")

if problems:
    print()
    for title, items in problems:
        print(f"!! {title}:")
        for i in items[:8]:
            print(f"     {i}")
    sys.exit(1)

print("\nOK - the way in works and every piece is wired to the next.")
