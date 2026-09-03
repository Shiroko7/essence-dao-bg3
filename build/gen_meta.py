# -*- coding: utf-8 -*-
"""Generate meta.lsx.

The first version of this file did not appear in the in-game mod manager at all.
Diffing it against a mod.io mod that does load showed four differences, and the
first one is almost certainly fatal:

  * UUID was typed `guid`. Working mods type it `FixedString`. Larian's loader
    reads ModuleInfo/UUID as a FixedString, so a guid-typed one is not found and
    the module is skipped silently.
  * no <Conflicts/> node - present in every working meta, even when empty.
  * no Dependencies. A mod with Osiris goals has to declare GustavDev, or its
    story never compiles against the main campaign.
  * missing FileSize / MD5 / PublishHandle, which the manager reads when
    listing.

`Type "Add-on"` and `Tags` were also dropped: loading mods do not carry them.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "Mods", "EssenceDao", "meta.lsx")

UUID = "6bb08ffe-62bc-4cd7-82e5-726d9cd62898"
FOLDER = "EssenceDao"
NAME = "Essence Dao"
AUTHOR = "Shiroko7"
DESC = ("Adds a pool of Essence and nine paths of cultivation, learned through "
        "the spellbook. Does not replace magic or spellcasting.")
VERSION64 = "36028797018963968"          # 1.0.0.0

# We ship a Story folder, but no compiled story. The distinction is the whole
# architecture of this mod, so it is worth being exact about it.
#
# We spent a long time shipping Mods/EssenceDao/Story/story.div.osi and could not
# work out why not one Osiris rule ever fired. That file was 31 MB: the Toolkit
# does not compile "your goals", it compiles the entire campaign script with your
# goals folded in. And the engine loads exactly one compiled story, from the
# *campaign module's* path - Mods/GustavX/Story/story.div.osi. Ours, at our own
# path, was simply never read.
#
# Which is fortunate, because if it had been read it would have replaced
# base-game Withers and broken every other Osiris mod installed. So an add-on
# gets no Osiris rules, and every state change here is an item or a passive.
#
# Dialogues are different, and this is the part we got wrong for a week. A
# dialogue is a *resource*, looked up by UUID, not a rule. It loads from any
# module. What needs Osiris is StartDialog - and we no longer call it, because a
# character root template's `DefaultDialog` makes the engine start the
# conversation on interaction by itself. Verified in game: a summoned character
# carrying DefaultDialog opens its dialogue when you talk to it.
#
# TargetModes:Story is OFF by default, and that is a deliberate, evidence-backed
# choice rather than caution.
#
# Declaring story mode tells the engine this module carries story content. The
# 20 MB build declared it and loaded fine - but it also shipped a compiled
# story.div.osi. This build declares no story and ships none, and saves hung at
# 79% on load. The probe pak, which shipped a character, a summon and an item
# but no story mode, loaded fine.
#
# So the working configurations are "story mode + a compiled story" and "neither"
# - not "story mode with nothing behind it". Dialogues are resources looked up
# by UUID, so they should not need the declaration.
#
#   ESSDAO_STORYMODE=1   put it back, if a Story folder ever ships again
#
# OFF, and it should stay off: nothing under Story/ ships any more. It was on
# briefly while the mod carried a dialogue, and declaring it with nothing behind
# it hung save loading at 79%.
STORY_MODE = os.environ.get("ESSDAO_STORYMODE") == "1"
#
# The GustavX dependency below was written by the Toolkit, which reads the values
# from the installed game, so it is correct by construction.

TARGET_MODES = '''
                        <node id="TargetModes">
                            <children>
                                <node id="Target">
                                    <attribute id="Object" type="FixedString" value="Story"/>
                                </node>
                            </children>
                        </node>''' if STORY_MODE else ""

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<save>
    <version major="4" minor="8" revision="0" build="10"/>
    <region id="Config">
        <node id="root">
            <children>
                <node id="Conflicts"/>
                <node id="Dependencies">
                    <children>
                        <node id="ModuleShortDesc">
                            <attribute id="Folder" type="LSString" value="GustavX"/>
                            <attribute id="MD5" type="LSString" value=""/>
                            <attribute id="Name" type="LSString" value="GustavX"/>
                            <attribute id="PublishHandle" type="uint64" value="0"/>
                            <attribute id="UUID" type="guid" value="cb555efe-2d9e-131f-8195-a89329d218ea"/>
                            <attribute id="Version64" type="int64" value="145241946983300916"/>
                        </node>
                    </children>
                </node>
                <node id="ModuleInfo">
                    <attribute id="Author" type="LSString" value="{AUTHOR}"/>
                    <attribute id="CharacterCreationLevelName" type="FixedString" value=""/>
                    <attribute id="Description" type="LSString" value="{DESC}"/>
                    <attribute id="FileSize" type="uint64" value="0"/>
                    <attribute id="Folder" type="LSString" value="{FOLDER}"/>
                    <attribute id="LobbyLevelName" type="FixedString" value=""/>
                    <attribute id="MD5" type="LSString" value=""/>
                    <attribute id="MenuLevelName" type="FixedString" value=""/>
                    <attribute id="Name" type="LSString" value="{NAME}"/>
                    <attribute id="NumPlayers" type="uint8" value="4"/>
                    <attribute id="PhotoBooth" type="FixedString" value=""/>
                    <attribute id="PublishHandle" type="uint64" value="0"/>
                    <attribute id="StartupLevelName" type="FixedString" value=""/>
                    <attribute id="UUID" type="FixedString" value="{UUID}"/>
                    <attribute id="Version64" type="int64" value="{VERSION64}"/>
                    <children>
                        <node id="PublishVersion">
                            <attribute id="Version64" type="int64" value="{VERSION64}"/>
                        </node>
                        <node id="Scripts"/>{TARGET_MODES}
                    </children>
                </node>
            </children>
        </node>
    </region>
</save>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(xml)

print(f"wrote {os.path.normpath(OUT)}")
print(f"  UUID typed FixedString (was guid - the likely reason it never listed)")
print(f"  declares the GustavX dependency the Toolkit resolved")
