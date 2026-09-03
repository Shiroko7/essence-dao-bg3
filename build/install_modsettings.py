# -*- coding: utf-8 -*-
"""Register the mod in modsettings.lsx.

BG3's in-game mod manager lists mods from mod.io only. A local .pak dropped into
the Mods folder is never shown there and never loads on its own - it has to be
declared in modsettings.lsx, which is what BG3 Mod Manager writes for you and
what this does directly.

Patch 8 tightened the schema: every ModuleShortDesc needs PublishHandle and
Version64, and the dependency validator refuses to start the game if an entry is
missing them. We write the full set.

    python build/install_modsettings.py            add the entry
    python build/install_modsettings.py --remove   take it out again

A timestamped backup is written before any change.
"""
import argparse, hashlib, os, re, shutil, sys, time

PROFILE = os.path.expandvars(
    r"%LOCALAPPDATA%\Larian Studios\Baldur's Gate 3\PlayerProfiles\Public")
SETTINGS = os.path.join(PROFILE, "modsettings.lsx")
MODS = os.path.expandvars(r"%LOCALAPPDATA%\Larian Studios\Baldur's Gate 3\Mods")
PAK = os.path.join(MODS, "EssenceDao.pak")

FOLDER = "EssenceDao"
NAME = "Essence Dao"
UUID = "6bb08ffe-62bc-4cd7-82e5-726d9cd62898"
VERSION64 = "36028797018963968"


def entry(md5):
    return f'''                        <node id="ModuleShortDesc">
                            <attribute id="Folder" type="LSString" value="{FOLDER}"/>
                            <attribute id="MD5" type="LSString" value="{md5}"/>
                            <attribute id="Name" type="LSString" value="{NAME}"/>
                            <attribute id="PublishHandle" type="uint64" value="0"/>
                            <attribute id="UUID" type="guid" value="{UUID}"/>
                            <attribute id="Version64" type="int64" value="{VERSION64}"/>
                        </node>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--remove", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(SETTINGS):
        sys.exit(f"modsettings.lsx not found at {SETTINGS}")

    text = open(SETTINGS, encoding="utf-8").read()
    backup = f"{SETTINGS}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
    shutil.copy2(SETTINGS, backup)

    already = UUID in text

    if args.remove:
        if not already:
            print("not present - nothing to remove")
            os.remove(backup)
            return
        text = re.sub(
            r'\s*<node id="ModuleShortDesc">(?:(?!</node>).)*?'
            + re.escape(UUID) + r'(?:(?!</node>).)*?</node>',
            "", text, flags=re.S)
        open(SETTINGS, "w", encoding="utf-8", newline="\n").write(text)
        print(f"removed {NAME} from the load order")
        print(f"backup: {os.path.basename(backup)}")
        return

    if already:
        print(f"{NAME} is already in the load order - refreshing its entry")
        text = re.sub(
            r'\s*<node id="ModuleShortDesc">(?:(?!</node>).)*?'
            + re.escape(UUID) + r'(?:(?!</node>).)*?</node>',
            "", text, flags=re.S)

    md5 = ""
    if os.path.isfile(PAK):
        md5 = hashlib.md5(open(PAK, "rb").read()).hexdigest()
    else:
        print(f"warning: {PAK} not found - install the pak first")

    # Append last. Nothing depends on us, and we depend on GustavDev, which is
    # always loaded, so the tail of the list is the safe place to sit.
    marker = "                    </children>\n                </node>"
    if marker not in text:
        sys.exit("could not find the Mods children block - file layout unexpected")
    text = text.replace(marker, entry(md5) + marker, 1)

    open(SETTINGS, "w", encoding="utf-8", newline="\n").write(text)
    print(f"added {NAME} to the load order (last)")
    print(f"  md5    : {md5 or '(pak missing)'}")
    print(f"  backup : {os.path.basename(backup)}")
    print()
    print("Note: opening the in-game mod manager can rewrite this file and drop")
    print("local entries. If that happens, re-run this script.")


if __name__ == "__main__":
    main()
