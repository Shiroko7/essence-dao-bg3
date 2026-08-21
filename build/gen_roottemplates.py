# -*- coding: utf-8 -*-
"""Root templates: the consumables, the summoning incense, and the guide.

A stats Object entry describes what an item *is*; a root template is the thing
that actually exists in the world, and - crucially - the thing that says what
happens when you use it.

That last part cost us a working mod. The pills originally carried

    data "OnUsePeaceActions" "UseSpell(SELF,Shout_...,,,)"

in Object.txt, which looks plausible and does nothing: `OnUsePeaceActions` and
`UseSpell` appear exactly zero times across all three of Larian's Object.txt
files. Real consumables put the action in the root template instead. Two action
types matter to us, both copied in shape from Larian's own items:

    ActionType 7   apply a status   (StatsId, StatusDuration -1, Consume)
    ActionType 12  cast a spell     (SkillID, Consume)          - scrolls

The three drinks use 7, so the drink *is* the unlock. The incense uses 12 to
cast a permanent Summon, which is how the guide gets into your camp without a
line of script.

The guide himself is a character template. Two facts make him possible, both
verified against Larian's data and then in game:

  * a character root template carries `DefaultDialog`, and interacting with the
    character starts that dialogue - the engine does it, not Osiris
  * `Summon(<root template uuid>, Permanent)` is a plain stats functor

We author no art. `ParentTemplateId` inherits everything - visuals, animations,
stats - from Larian's generic civilian, so the guide looks like a person and
the potions look like potions.
"""
import json, os, uuid

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "Public", "EssenceDao", "RootTemplates")

NS = uuid.UUID("6bb08ffe-62bc-4cd7-82e5-726d9cd62898")
POTION_PARENT = "8e660fd9-489d-42ff-a762-e4392e826666"   # BASE_ALCH_Solution_Potion
TOME_PARENT = "02f7446a-8150-4401-aab3-384b7c95a0e0"     # BOOK_Wizards_Tome_Ornate_H
# Humans_Male_Liam, not the generic civilian. This is the only character
# template we have *watched* be summoned and then successfully talked to, in the
# probe pak. The civilian base was a guess and produced someone who could be
# summoned, named, and killed - but not spoken to. Prefer the shape with
# evidence behind it; his appearance can be re-skinned once talking works.
# There is no character here any more. A guide NPC in camp needs Osiris, which
# an add-on cannot run - see docs/npc-and-dialogue.md for the full account and
# for what to re-read before anyone tries again. The book replaces him.

# Kept in step with gen_consumables.py - check_wiring verifies they agree.
# `status` -> ActionType 7;  `spell` -> ActionType 12.
ITEMS = [
    dict(name="OBJ_EssenceDao_AwakeningBalm", status="ESSDAO_CULTIVATOR",
         handle="hEssDaoBalm", icon="Item_CONS_Drink_Potion_A"),
    dict(name="OBJ_EssenceDao_FoundationPill", status="ESSDAO_FOUNDATION_TAKEN",
         handle="hEssDaoPill_Foundation", icon="Item_CONS_Potion_Barkskin_A"),
    dict(name="OBJ_EssenceDao_GoldenCoreElixir", status="ESSDAO_GOLDENCORE_TAKEN",
         handle="hEssDaoPill_GoldenCore", icon="Item_CONS_ElixirOfHealth"),
    # The book does nothing when used. It is not a key, a summon or a trigger -
    # it is the instructions, and it is the only thing in the mod that explains
    # itself. It arrives in the tutorial chest so it cannot be missed.
    # `book` is the key into Mods/EssenceDao/Localization/EssenceDao_Books.lsf.
    # Without it the template inherits GEN_Unreadable from its parent, and the
    # game says "this book has all but crumbled to dust" - which is exactly what
    # it did. A description on the item is not book content; BookId is.
    dict(name="OBJ_EssenceDao_Tome", handle="hEssDaoTome",
         icon="Item_BOOK_Wizards_Tome_Simple_C", parent=TOME_PARENT,
         book="EssenceDao_Testament"),
]


def apply_status(status):
    return f'''                            <node id="Action">
                                <attribute id="ActionType" type="int32" value="7"/>
                                <children>
                                    <node id="Attributes">
                                        <attribute id="Animation" type="FixedString" value=""/>
                                        <attribute id="Conditions" type="LSString" value=""/>
                                        <attribute id="Consume" type="bool" value="True"/>
                                        <attribute id="IsHiddenStatus" type="bool" value="False"/>
                                        <attribute id="StatsId" type="FixedString" value="{status}"/>
                                        <attribute id="StatusDuration" type="int32" value="-1"/>
                                    </node>
                                </children>
                            </node>'''


def cast_spell(spell, consume="False"):
    # Consume=False by default: the tome is a book, not a potion. If the summon
    # ever fails, or the guide is lost, you can read it again rather than being
    # locked out of the entire mod by one click.
    return f'''                            <node id="Action">
                                <attribute id="ActionType" type="int32" value="12"/>
                                <children>
                                    <node id="Attributes">
                                        <attribute id="Consume" type="bool" value="{consume}"/>
                                        <attribute id="SkillID" type="FixedString" value="{spell}"/>
                                    </node>
                                </children>
                            </node>'''


def on_use(it):
    if "status" not in it:
        return ""          # the book: readable, but it does nothing when used
    return ('                        <node id="OnUsePeaceActions">\n'
            '                            <children>\n'
            f'{apply_status(it["status"])}\n'
            '                            </children>\n'
            '                        </node>')


nodes = []
for it in ITEMS:
    guid = uuid.uuid5(NS, "rt:" + it["name"])
    nodes.append(f'''                <node id="GameObjects">
                    <attribute id="Description" type="TranslatedString" handle="{it['handle']}_Desc" version="1"/>
                    <attribute id="DisplayName" type="TranslatedString" handle="{it['handle']}_Name" version="1"/>
                    <attribute id="Icon" type="FixedString" value="{it['icon']}"/>
                    <attribute id="LevelName" type="FixedString" value=""/>
                    <attribute id="MapKey" type="FixedString" value="{guid}"/>
                    <attribute id="Name" type="LSString" value="{it['name']}"/>
                    <attribute id="ParentTemplateId" type="FixedString" value="{it.get('parent', POTION_PARENT)}"/>
                    <attribute id="Stats" type="FixedString" value="{it['name']}"/>{f'''
                    <attribute id="BookId" type="FixedString" value="{it["book"]}"/>''' if it.get("book") else ""}
                    <attribute id="Type" type="FixedString" value="item"/>
                    <attribute id="_OriginalFileVersion_" type="int64" value="144115207403209026"/>
                    <children>
{on_use(it)}
                    </children>
                </node>''')

# --- the guide ---------------------------------------------------------------
# Everything except identity and dialogue is inherited. Deliberately minimal:
# the probe that proved this works overrode exactly these fields and nothing
# else, so this is the shape known to function.
xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<save>
    <version major="4" minor="8" revision="0" build="10"/>
    <region id="Templates">
        <node id="Templates">
            <children>
{chr(10).join(nodes)}
            </children>
        </node>
    </region>
</save>
'''

os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "_merged.lsx")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(xml)

# This .lsx is converted to binary .lsf before packing, so the validators cannot
# read MapKeys or use-actions back out of it. Leave them a manifest.
manifest = {it["name"]: {"uuid": str(uuid.uuid5(NS, "rt:" + it["name"])),
                         **({"status": it["status"]} if "status" in it else {})}
            for it in ITEMS}
with open(os.path.join(OUT, "templates.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=1)

print(f"wrote {len(ITEMS)} item templates -> {os.path.normpath(path)}")
for it in ITEMS:
    what = f"applies {it['status']}" if "status" in it else "read only, no action"
    print(f"  {it['name']:<34} {what}")
