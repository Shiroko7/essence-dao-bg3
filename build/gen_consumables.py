# -*- coding: utf-8 -*-
"""The brewed consumables, their statuses, the guide's incense, and the way out.

This file is the whole on/off switch for the mod, and it contains no script.

    Guide's Incense                 summons the guide    (any level, once)
    Spiritual Root Awakening Balm   take up the Dao      (any level)
    Foundation Establishment Pill   first breakthrough   (level 5+)
    Golden Core Elixir              second breakthrough  (level 9+)

The guide never changes your state. He explains the system, and that is all -
turning it on is the Balm, turning it off is Shout_EssenceDao_SetAside. That
division is not a stylistic choice: a dialogue node cannot grant a passive
without Osiris, but an item can, so the switches have to be items.

Each is brewed at any alchemy station from ingredients that already exist in the
world, drunk like any potion, and applies a permanent status whose `Passives`
field carries the stage passive. The passive is what unlocks that stage's nine
path containers and widens the Essence pool, so the drink *is* the unlock -
nothing checks a flag afterwards, because there is nothing left to check.

Setting the Dao aside is a spell the Cultivator passive grants, so it is only
ever in the spellbook of someone who has taken the Dao up. It strips the
Cultivator status and every bound technique, returning all Attunement.

Two things here were bugs found by reading Larian's data rather than guessing:

  * The use-action lives in the root template, not in Object.txt - see
    gen_roottemplates.py. This file only names the status; that file applies it.

  * Recipe ingredients must not collide with a vanilla pair. Balsam + Earth,
    which the Foundation Pill used to claim, is already Greater Healing Potion.
    Every pair below was checked against Larian's 63 ExtractToSolution recipes
    and is unclaimed; check_wiring re-checks on every build.

Breakthroughs are *not* removed when you set the Dao aside. A Foundation once
established is a fact about the character, not a technique, and re-brewing both
pills to come back would be a miserable tax.
"""
import importlib, json, os, pkgutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from defs._schema import all_abilities                              # noqa: E402
import defs                                                         # noqa: E402
for _, _m, _ in pkgutil.iter_modules(defs.__path__):
    if not _m.startswith("_"):
        importlib.import_module(f"defs.{_m}")

ANIM = json.load(open(os.path.join(HERE, "spell_animations.json"), encoding="utf-8"))
DATA = os.path.join(ROOT, "Public", "EssenceDao", "Stats", "Generated", "Data")
GEN = os.path.join(ROOT, "Public", "EssenceDao", "Stats", "Generated")

# `level` gates the drink; None means no gate. The reagent pairs are all
# unclaimed by vanilla - see the module docstring.
CONSUMABLES = [
    dict(id="OBJ_EssenceDao_AwakeningBalm",
         passive="EssenceDao_Cultivator",
         status="ESSDAO_CULTIVATOR",
         handle="hEssDaoBalm",
         # Real icon names, read out of Larian's own Object entries. The three
         # Item_LOOT_Alchemy_Ingredient_Herb_* names used before were invented
         # and rendered as nothing at all.
         icon="Item_CONS_Drink_Potion_A",
         value="100", level=None,
         recipe="ALCH_EssenceDao_AwakeningBalm",
         base="ALCH_Extract_Balsam",
         affinity="ALCH_Affinity_Water"),
    dict(id="OBJ_EssenceDao_FoundationPill",
         passive="EssenceDao_Breakthrough_Foundation",
         status="ESSDAO_FOUNDATION_TAKEN",
         handle="hEssDaoPill_Foundation",
         icon="Item_CONS_Potion_Barkskin_A",
         value="400", level=4,
         recipe="ALCH_EssenceDao_FoundationPill",
         base="ALCH_Extract_AutumnCrocus",
         affinity="ALCH_Affinity_Earth"),
    dict(id="OBJ_EssenceDao_GoldenCoreElixir",
         passive="EssenceDao_Breakthrough_GoldenCore",
         status="ESSDAO_GOLDENCORE_TAKEN",
         handle="hEssDaoPill_GoldenCore",
         icon="Item_CONS_ElixirOfHealth",
         value="1200", level=8,
         recipe="ALCH_EssenceDao_GoldenCoreElixir",
         base="ALCH_Extract_FireAmber",
         affinity="ALCH_Affinity_Fire"),
]

# The book. It arrives in the tutorial chest and it is the entire tutorial: what
# Essence is, what the three stages cost, and the three recipes.
#
# It has no use-action. Nothing is unlocked by carrying or reading it - the
# brewing is the progression. That is deliberate: it is a dead man's notes, not
# a key.
#
# It replaced a guide NPC, at length and painfully. An NPC who stands in your
# camp needs Osiris (RequestGatherAtCamp), an add-on cannot run Osiris rules,
# and summoning produces something you can see and kill but not talk to.
# docs/npc-and-dialogue.md has the whole account.
TOME = dict(id="OBJ_EssenceDao_Tome",
            handle="hEssDaoTome",
            icon="Item_BOOK_Generic_A",
            value="0")


def entry(name, etype, fields, kind="new entry", using=None):
    out = [f'{kind} "{name}"']
    if etype:
        out.append(f'type "{etype}"')
    if using:
        out.append(f'using "{using}"')
    for k, v in fields.items():
        out.append(f'data "{k}" "{v}"')
    out.append("")
    return out


# ---------------------------------------------------------------- objects ---
# `using "_Potion"` inherits Larian's consumable behaviour - bonus-action use,
# the Consumable inventory tab, the drink animation - so we override only what
# is ours. The root template supplies the effect.
obj = ["// GENERATED by build/gen_consumables.py - do not edit by hand", ""]
with open(os.path.join(ROOT, "Public", "EssenceDao", "RootTemplates",
                       "templates.json"), encoding="utf-8") as fh:
    TEMPLATES = json.load(fh)

for c in CONSUMABLES:
    cond = "not IsSummonWithoutMouth()"
    if c["level"]:
        cond += f" and CharacterLevelGreaterThan({c['level']})"
    obj += entry(c["id"], "Object", {
        "RootTemplate": TEMPLATES[c["id"]]["uuid"],
        "Rarity": "VeryRare",
        "ValueOverride": c["value"],
        "UseConditions": cond,
        "DisplayName": f"{c['handle']}_Name;1",
        "Description": f"{c['handle']}_Desc;1",
        "Icon": c["icon"],
    }, using="_Potion")

obj += entry(TOME["id"], "Object", {
    "RootTemplate": TEMPLATES[TOME["id"]]["uuid"],
    "Rarity": "Common",
    "ValueOverride": TOME["value"],
    "UseConditions": "!Combat",
    "DisplayName": f"{TOME['handle']}_Name;1",
    "Description": f"{TOME['handle']}_Desc;1",
    "Icon": TOME["icon"],
}, using="_Potion")

with open(os.path.join(DATA, "Object.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(obj))

# --------------------------------------------------------------- statuses ---
# StatusType BOOST with no duration handling of its own; the -1 duration comes
# from the root template's use action. `Passives` is the entire payload.
status = ["// GENERATED by build/gen_consumables.py - do not edit by hand", ""]
for c in CONSUMABLES:
    status += entry(c["status"], "StatusData", {
        "StatusType": "BOOST",
        "DisplayName": f"{c['handle']}_Name;1",
        "Description": f"{c['handle']}_Desc;1",
        "Icon": c["icon"],
        "Passives": c["passive"],
        "StatusPropertyFlags": "DisableOverhead;DisableCombatlog;IgnoreResting;"
                               "ExcludeFromPortraitRendering",
        "StackId": c["status"],
        "TickType": "None",
    })

with open(os.path.join(DATA, "Status_BOOST_Pills.txt"), "w",
          encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(status))

# ------------------------------------------------------- setting it aside ---
# One shout, granted by the Cultivator passive, and it removes exactly one
# status.
#
# It used to name all 122 techniques explicitly, because Osiris could iterate
# statuses by prefix and a spell cannot. That produced an 11,344-character
# SpellProperties string - Larian's largest anywhere is 4,052 - and a save that
# hung on load at 79% with nothing in any log.
#
# The techniques now remove themselves: each ESSDAO_LEARN_* status carries
# `RemoveConditions "not HasStatus('ESSDAO_CULTIVATOR')"` and
# `RemoveEvents "OnStatusRemoved"`, so dropping the Cultivator status cascades
# through every technique bound to it. See gen_abilities.py.
abilities = all_abilities()
props = ["RemoveStatus(SELF,ESSDAO_CULTIVATOR)"]

spells = ["// GENERATED by build/gen_consumables.py - do not edit by hand", ""]
spells += entry("Shout_EssenceDao_SetAside", "SpellData", {
    "SpellType": "Shout",
    "Level": "0",
    "SpellSchool": "Transmutation",
    "SpellProperties": ";".join(props),
    "TargetConditions": "Self()",
    "Requirements": "!Combat",
    "SpellFlags": "IsSpell",
    "Cooldown": "None",
    "VerbalIntent": "Utility",
    "Icon": "PassiveFeature_Generic_Magical",
    "DisplayName": "hEssDaoSetAside_Name;1",
    "Description": "hEssDaoSetAside_Desc;1",
    "PreviewCursor": "Cast",
    "CastTextEvent": "Cast",
    "SpellAnimation": ANIM["Shout"],
})

with open(os.path.join(DATA, "Spell_Shout_Pills.txt"), "w",
          encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(spells))

# ----------------------------------------------------------------- recipes ---
# One recipe per item is not discoverable. BG3 only surfaces a combination once
# you have met its ingredients, so a single recipe means a player who never
# picked up that one herb never learns the mod exists - which is exactly what
# happened: nothing appeared on the alchemy tab at all.
#
# The probe pak was findable because it shipped 156 combinations per item. So
# each consumable now accepts *any* extract, paired with the affinity that suits
# it thematically. Whatever reagents you are carrying, one of them works.
#
# `base` above stays as the signature recipe - the one the README quotes - and
# is simply first in the list.
GUIDE_TRADE = "EssenceDao_GuideStock"      # matches gen_roottemplates.py
PAIRS = json.load(open(os.path.join(HERE, "vanilla_alchemy_pairs.json"),
                       encoding="utf-8"))
TAKEN = {(p[0], p[1]) for p in PAIRS}
EXTRACTS = sorted({p[0] for p in PAIRS})

combo = ["// GENERATED by build/gen_consumables.py - do not edit by hand", ""]
recipe_count = 0
# Alchemy is now the *second* way to get these - the guide sells them - so it
# does not have to be exhaustively discoverable any more. A dozen extracts each
# is enough that something in your bag will match, without burying the alchemy
# tab under 150 near-identical entries per item, which is what fixing the
# discoverability bug the blunt way produced.
RECIPES_PER_ITEM = 12
for c in CONSUMABLES:
    aff = c["affinity"]
    # signature pair first, then other extracts vanilla has not claimed here
    bases = ([c["base"]] + [e for e in EXTRACTS
                            if e != c["base"] and (e, aff) not in TAKEN]
             )[:RECIPES_PER_ITEM]
    for n, base in enumerate(bases):
        name = c["recipe"] if n == 0 else f"{c['recipe']}_{n}"
        combo += entry(name, None, {
            "Type 1": "Object", "Object 1": base,
            "Combine 1": "Base", "Transform 1": "Consume",
            "Type 2": "Category", "Object 2": aff,
            "Combine 2": "Base", "Transform 2": "Consume",
            "AlchemyCombinationType": "ExtractToSolution",
        }, kind="new ItemCombination")
        combo += entry(f"{name}_1", None, {
            "ResultAmount 1": "1",
            "Result 1": c["id"],
            "PreviewStatsID": c["id"],
        }, kind="new ItemCombinationResult")
        recipe_count += 1

with open(os.path.join(GEN, "ItemCombos.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(combo))

# ------------------------------------------------------------ treasure ------
# Two tables.
#
# TUT_Chest_Potions is Larian's, and redefining a treasuretable replaces it
# rather than extending it - so the vanilla contents are reproduced verbatim
# below and ours appended. Get that wrong and the tutorial chest loses its
# healing potions. Larian's version, from Gustav's TreasureTable.txt, is:
#
#     new treasuretable "TUT_Chest_Potions"
#     new subtable "2,1"
#     object category "I_OBJ_Potion_Healing",1,0,0,0,0,0,0,0
#
# This is the one place the mod touches something of Larian's, and it is a
# redefinition rather than an overwritten file. Any other mod that adds to the
# tutorial chest will conflict with us here; that is inherent to the convention
# and is why the alchemy recipes are kept as a second route in.
#
# The object category name is the stats entry prefixed with `I_`.
treasure = ["// GENERATED by build/gen_consumables.py - do not edit by hand", ""]
treasure += [
    'new treasuretable "TUT_Chest_Potions"',
    'new subtable "2,1"',
    'object category "I_OBJ_Potion_Healing",1,0,0,0,0,0,0,0',
    'new subtable "1,1"',
    f'object category "I_{TOME["id"]}",1,0,0,0,0,0,0,0',
    "",
]

with open(os.path.join(GEN, "TreasureTable.txt"), "w",
          encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(treasure))

# ------------------------------------------------------------- the guide ----
# Without this he inherits Humans_Male_Civilian's stats and stands in camp as a
# level 1 with 7 hit points, which reads as a bug even though he never fights.
# `Human_Caster` is the most-used base in Larian's own Character.txt (28 NPCs)
# and suits someone who teaches breathing for a living.

print(f"wrote {len(CONSUMABLES)} consumables + the tome, {len(CONSUMABLES)} "
      f"statuses, {recipe_count} recipes, 1 set-aside spell")
print(f"  {TOME['id']:<34} in the tutorial chest -> summons the guide")
for c in CONSUMABLES:
    gate = f"level {c['level']+1}+" if c.get("level") else "any level"
    print(f"  {c['id']:<34} from the guide, or extract + {c['affinity']}  ({gate})")
print(f"  set-aside removes 1 status; {len(abilities)} techniques cascade off it")
