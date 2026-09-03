# -*- coding: utf-8 -*-
"""Generate the English localization XML.

Every DisplayName / Description in BG3 is a handle, not a string - an entry
whose handle has no localization row renders blank in game, with no error. So
this is generated from the same registries that emit the stats, which means a
handle can never be forgotten.

Location matters, and we had it wrong. Ours sat at the pak root as
`Localization/English/EssenceDao.xml` plus a built `.loca`. Every working mod
installed on this machine - Mystra's Spells, Extra Encounters, All-Players-In-
Dialogue, PlayMates, Sit This One Out - ships exactly one file:

    Mods/<ModFolder>/Localization/English/english.xml

Raw XML, under the module folder, and no .loca at all. With ours at the root the
game rendered "Not Found" in place of item and character names.

So this writes a single merged english.xml to the module folder, including the
dialogue's own lines, and nothing is converted to .loca.
"""
import html, importlib, os, pkgutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from defs._schema import (all_abilities, all_statuses, all_raw_spells,  # noqa: E402
                          PATHS, TIERS)
import defs                                                        # noqa: E402
for _, m, _ in pkgutil.iter_modules(defs.__path__):
    if not m.startswith("_"):
        importlib.import_module(f"defs.{m}")

OUT = os.path.join(ROOT, "Mods", "EssenceDao", "Localization", "English")
os.makedirs(OUT, exist_ok=True)
# The old root-level folder actively broke name resolution; make sure a stale
# one cannot survive a rebuild and get packed alongside the correct file.
import shutil                                                       # noqa: E402
shutil.rmtree(os.path.join(ROOT, "Localization"), ignore_errors=True)

rows = []


def add(handle, text):
    rows.append((handle, text))


TIER_BLURB = {
    "Initiate": "The first breaths. Techniques any cultivator may attempt.",
    "Adept": "Requires an established Foundation.",
    "Master": "Requires a formed Golden Core.",
}

# --- the system itself ------------------------------------------------------
add("hEssenceDaoResourceName", "Essence")
add("hEssenceDaoResourceDesc",
    "The breath beneath the world, gathered and held. Spent to use techniques. "
    "Recovers on a Long Rest.")
add("hEssenceDaoAttuneName", "Attunement")
add("hEssenceDaoAttuneDesc",
    "How much technique you can hold at once. Every technique you learn claims "
    "part of it, permanently.")
add("hEssenceDao_CultivatorName", "Cultivator")
add("hEssenceDao_CultivatorDesc",
    "You have taken up the Dao. The nine Initiate paths are open to you, and you "
    "can hold up to [1] Essence.")
add("hEssenceDao_Breakthrough_FoundationName", "Foundation Established")
add("hEssenceDao_Breakthrough_FoundationDesc",
    "Your vessel has been widened. The nine Adept paths are open to you, and you "
    "can hold up to [1] Essence.")
add("hEssenceDao_Breakthrough_GoldenCoreName", "Golden Core Formed")
add("hEssenceDao_Breakthrough_GoldenCoreDesc",
    "A core has settled at your centre. The nine Master paths are open to you, "
    "and you can hold up to [1] Essence.")

# --- the book ---------------------------------------------------------------
# This is the entire tutorial. There is no guide NPC to explain any of it, so
# every rule a player needs has to be legible from the item description alone.
add("hEssDaoTome_Name", "Testament of the Rootless")
# The pages themselves, shown when you open the book. The item description is a
# tooltip; this is the actual content, keyed by BookId.
add("hEssDaoBook_Body",
    "<h1>Testament of the Rootless</h1>\n\n"
    "I had no talent. Not a thread of it. The masters put their fingers to my "
    "spine and told me the root is born or it is not, and mine was not, and I "
    "should go and be a farmer and be grateful.\n\n"
    "I was not grateful. I brewed instead.\n\n"
    "<h2>The first drink</h2>\n"
    "Take any extract and marry it to a reagent of Water. Drink it, and the "
    "root wakes whether it was born or not. Nine paths open to you — Water, "
    "Fire, Earth, Metal, Wood, Poison, Acid, Lightning, Wind — and you may hold "
    "eight measures of Essence.\n\n"
    "<h2>The second</h2>\n"
    "Any extract, and a reagent of Earth. Do not attempt it young; the vessel "
    "tears. When you have some living behind you, it widens what you can hold "
    "to sixteen, and the Adept techniques come within reach.\n\n"
    "<h2>The third</h2>\n"
    "Any extract, and a reagent of Fire. This one nearly finished me. A core "
    "settles at your centre, twenty-four measures, and the Master techniques "
    "open.\n\n"
    "<h2>On holding technique</h2>\n"
    "Binding a technique costs Attunement for as long as you hold it. Choose it "
    "again to let it go and the Attunement returns — nothing is spent forever "
    "but the years. Essence itself is spent in use and comes back with a long "
    "rest.\n\n"
    "If you tire of all this, set the Dao aside. Everything unbinds. What you "
    "broke through remains broken through; that much cannot be given back.\n\n"
    "<h2>And then?</h2>\n"
    "I do not know. I am eighty-one and the ink is getting away from me. I "
    "reached the Master stage with no root at all, and I never found what lies "
    "past it.\n\n"
    "Someone else will have to write that page.")
add("hEssDaoTome_Desc",
    "A brittle journal, written in a hand that grows steadier as it goes on.\n\n"
    "<i>I had no talent. Not a thread of it. The masters told me the root is "
    "born or it is not, and mine was not, and I should go and be a farmer.\n\n"
    "So I brewed instead. Three times, over sixty years, I drank what should "
    "have killed me. It did not make me gifted. It made me a Master anyway.\n\n"
    "You will need three, as I did.</i>\n\n"
    "• <b>Root-Opening Elixir</b> — any extract + a Water reagent.\n"
    "Wakes the root. Nine paths open; you may hold 8 Essence.\n\n"
    "• <b>Foundation Elixir</b> — any extract + an Earth reagent. Level 5.\n"
    "Widens the vessel. The Adept techniques open; 16 Essence.\n\n"
    "• <b>Golden Core Elixir</b> — any extract + a Fire reagent. Level 9.\n"
    "Settles a core. The Master techniques open; 24 Essence.\n\n"
    "<i>Binding a technique costs Attunement, and does not give it back until "
    "you release it. Spend Essence to use them; a long rest refills it. If you "
    "wish to be ordinary again, set the Dao aside — everything unbinds, and "
    "what you have broken through is still yours.\n\n"
    "There is no more. I am out of years, and this is as far as I got.</i>")

# --- the brewed consumables -------------------------------------------------
add("hEssDaoBalm_Name", "Root-Opening Elixir")
add("hEssDaoBalm_Desc",
    "Bitter, and colder going down than it has any right to be. It wakes the "
    "root that every living thing is born with and almost none ever feel."
    "\n\nDrink to take up the Dao. The nine Initiate paths become yours to "
    "study, and you may hold [1] Essence.")
add("hEssDaoPill_Foundation_Name", "Foundation Elixir")
add("hEssDaoPill_Foundation_Desc",
    "Dense and earthy, smelling of rain on stone. Widens the vessel so it may "
    "hold more than it was born to.\n\nThe Adept techniques open, and you may "
    "hold [1] Essence. Requires a body that has seen some living — level 5.")
add("hEssDaoPill_GoldenCore_Name", "Golden Core Elixir")
add("hEssDaoPill_GoldenCore_Desc",
    "Amber, and warm to the touch long after it should have cooled. Settles a "
    "core at the centre of a cultivator who has earned one.\n\nThe Master "
    "techniques open, and you may hold [1] Essence. Requires level 9.")


add("hEssDaoSetAside_Name", "Set the Dao Aside")
add("hEssDaoSetAside_Desc",
    "Let the breath settle and go back to what you were. Every technique you "
    "hold is released and all Attunement returns.\n\nWhat you have broken "
    "through remains yours - take up the Dao again and your Foundation and "
    "Core are as you left them.")

# --- path containers ---------------------------------------------------------
# One per path, holding every tier. Split paths get a numbered name; the split
# is by size only, so the description is shared.
import json as _json                                                # noqa: E402
_containers = _json.load(open(os.path.join(
    ROOT, "Public", "EssenceDao", "Stats", "Generated", "containers.json"),
    encoding="utf-8"))
for c in _containers:
    stem = c[len("Shout_EssenceDao_"):]
    if "_" in stem:
        path, n = stem.rsplit("_", 1)
        add(f"hEssDaoP_{path}_{n}_Name", f"{path} — {n}")
    else:
        path = stem
        add(f"hEssDaoP_{path}_Name", path)
for path in PATHS:
    add(f"hEssDaoP_{path}_Desc",
        f"The {path} path. Select a technique to bind it; select it again to "
        f"let it go and take the Attunement back.\n\nTechniques beyond your "
        f"stage are shown but cannot be bound until you break through.")

# --- techniques -------------------------------------------------------------
TIER_NOTE = {"initiate": "", "adept": "  Requires an established Foundation.",
             "master": "  Requires a formed Golden Core."}
for a in all_abilities():
    add(a.h_name, a.name)
    add(a.h_desc, a.blurb)
    # One entry per technique now, and it toggles - so the name is just the
    # technique and the description explains both directions.
    add(a.h_learn_name, a.name)
    add(a.h_learn_desc,
        f"{a.blurb}\n\nCosts {a.cost} Attunement while bound. Select it again "
        f"to release it and take the Attunement back."
        + TIER_NOTE.get(a.tier, ""))
    add(a.h_release_name, a.name)
    add(a.h_release_desc, a.blurb)

# --- technique-granted spells ---------------------------------------------
RAW_TEXT = {
    "hEssDaoX_CloneDetonate": ("Detonate Water Clone",
        "Shatter one of your Water Clones, dealing 4d8 Cold damage nearby."),
    "hEssDaoX_CloneSwap": ("Swap with Water Clone",
        "Instantly trade places with one of your Water Clones."),
    "hEssDaoX_WindDie": ("Wind Die",
        "Spend the die the wind gave you, adding 1d6 to a roll."),
    "hEssDaoX_EntanglingReach": ("Entangling Reach",
        "Vines seize every creature in a wide area."),
    "hEssDaoX_Myrmidon": ("Reflection of the Myrmidon",
        "Your reflection rises as a Water Myrmidon."),
    "hEssDaoI_GlacialShield": ("Glacial Shield",
        "Expend a Spell Slot to encase yourself in ice, gaining Temporary Hit Points."),
    "hEssDaoI_EmbersResilience": ("Ember's Resilience",
        "Reroll a failed Saving Throw. You take 2d6 Fire damage."),
    "hEssDaoI_MistyEscape": ("Misty Escape",
        "Expend a Spell Slot to become mist, halving the damage."),
    "hEssDaoI_WhispersOfTheGale": ("Whispers of the Gale",
        "Expend a Spell Slot to reroll a missed ranged attack."),
}
for stem, (nm, ds) in RAW_TEXT.items():
    add(f"{stem}_Name", nm)
    add(f"{stem}_Desc", ds)

# --- statuses ---------------------------------------------------------------
for s in all_statuses():
    add(s.h_name, s.display)
    add(s.h_desc, s.desc)

# --- the dialogue's own prose ------------------------------------------------
# gen_guide.py stages the recovered dialogue lines here. They are hand-written
# rather than generated, so they live in their own file, but they have to end up
# in the same english.xml - the module folder holds exactly one.
import re                                                           # noqa: E402
staged = os.path.join(HERE, "_dialogue_loca.xml")
dialogue_rows = 0
if os.path.isfile(staged):
    text = open(staged, encoding="utf-8").read()
    for m in re.finditer(r'<content contentuid="([^"]+)"[^>]*>(.*?)</content>',
                         text, re.S):
        rows.append((m.group(1), None))          # None = already escaped
        dialogue_rows += 1
    escaped = {m.group(1): m.group(2) for m in
               re.finditer(r'<content contentuid="([^"]+)"[^>]*>(.*?)</content>',
                           text, re.S)}
else:
    escaped = {}

# --- write ------------------------------------------------------------------
seen, out = set(), []
for handle, text in rows:
    if handle in seen:
        continue
    seen.add(handle)
    body = escaped[handle] if text is None else html.escape(text)
    out.append(f'    <content contentuid="{handle}">{body}</content>')

xml = ('<?xml version="1.0" encoding="utf-8"?>\n<contentList>\n'
       + "\n".join(out) + "\n</contentList>\n")

path = os.path.join(OUT, "english.xml")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(xml)

# --- book content ------------------------------------------------------------
# A readable book is a TranslatedStringKey whose UUID is the BookId named on the
# item's root template. Without one the game falls back to GEN_Unreadable and
# tells you the book has crumbled to dust - which it did, because an item
# Description is not book content.
BOOKS = os.path.join(ROOT, "Mods", "EssenceDao", "Localization",
                     "EssenceDao_Books.lsx")
with open(BOOKS, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<save>
    <version major="4" minor="0" revision="9" build="328"/>
    <region id="TranslatedStringKeys">
        <node id="TranslatedStringKeys">
            <children>
                <node id="TranslatedStringKey">
                    <attribute id="Content" type="TranslatedString" handle="hEssDaoBook_Body" version="1"/>
                    <attribute id="UUID" type="FixedString" value="EssenceDao_Testament"/>
                    <attribute id="Speaker" type="FixedString" value=""/>
                    <attribute id="ExtraData" type="LSString" value=""/>
                    <attribute id="Stub" type="bool" value="True"/>
                </node>
            </children>
        </node>
    </region>
</save>
''')
print(f"wrote book content    -> {os.path.normpath(BOOKS)}")

print(f"wrote {len(out)} localization entries -> {os.path.normpath(path)}")
print(f"  {dialogue_rows} of them are the dialogue's own lines")
print(f"  duplicates collapsed: {len(rows) - len(out)}")
