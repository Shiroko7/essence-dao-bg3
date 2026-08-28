# -*- coding: utf-8 -*-
"""Convert each resource file to the format the game actually loads.

This is the third time the same mistake has cost a debugging round:

    Dialogs/*.lsj          -> the engine reads DialogsBinary/*.lsf
    Story/RawFiles/*.txt   -> the engine reads Story/story.div
    RootTemplates/*.lsx    -> the engine reads RootTemplates/_merged.lsf

Each time the .lsx/.lsj/.txt is *source*, valid and readable by the Toolkit,
and each time the game silently ignores it. A root template that is ignored
means the item cannot spawn - which is why the treatise never appeared, with no
error anywhere to say so.

Not every resource is binary. Larian ships ActionResourceDefinitions,
Progressions and Lists as .lsx. So the rule is per directory, taken from what
Larian actually ships, rather than a blanket "convert everything".
"""
import glob, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "Public", "EssenceDao")

# directory -> extension the engine loads, verified against Shared.pak
REQUIRED = {
    "RootTemplates": "lsf",
    "Flags": "lsf",
    "ActionResourceDefinitions": "lsx",
}

divine = os.environ.get("DIVINE") or os.path.join(
    ROOT, "build", "lslib", "Tools", "Divine.exe")
if not os.path.isfile(divine):
    sys.exit("Divine.exe not found - cannot convert resources")
env = dict(os.environ, DOTNET_ROLL_FORWARD="Major")

converted, kept = 0, 0
for folder, want in REQUIRED.items():
    d = os.path.join(PUBLIC, folder)
    if not os.path.isdir(d):
        continue
    for src in sorted(glob.glob(os.path.join(d, "*.ls[xf]"))):
        have = src.rsplit(".", 1)[1]
        if have == want:
            kept += 1
            continue
        dst = src[: -len(have)] + want
        r = subprocess.run([divine, "-g", "bg3", "-a", "convert-resource",
                            "-s", src, "-d", dst, "-o", want],
                           capture_output=True, text=True, env=env)
        if r.returncode != 0 or not os.path.isfile(dst):
            print(r.stdout, r.stderr)
            sys.exit(f"failed converting {os.path.basename(src)} -> .{want}")
        os.remove(src)          # the source form would shadow nothing, but it
        converted += 1          # is dead weight in the pak and confusing
        print(f"  {folder}/{os.path.basename(src)} -> .{want}")

print(f"\nconverted {converted}, already correct {kept}")

# --- book content -------------------------------------------------------------
# Mods/<Mod>/Localization/*_Books.lsf holds readable book pages. english.xml is
# NOT converted - it ships as raw XML, which is what every working mod does -
# but the books file is binary, exactly like Larian's Generic_Books.lsf.
books = 0
for src in sorted(glob.glob(os.path.join(ROOT, "Mods", "EssenceDao",
                                         "Localization", "*_Books.lsx"))):
    dst = src[:-4] + ".lsf"
    r = subprocess.run([divine, "-g", "bg3", "-a", "convert-resource",
                        "-s", src, "-d", dst, "-o", "lsf"],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0 or not os.path.isfile(dst):
        print(r.stdout, r.stderr)
        sys.exit(f"failed converting {os.path.basename(src)}")
    os.remove(src)
    books += 1
    print(f"  Localization/{os.path.basename(dst)} (book pages)")
if books:
    print(f"converted {books} book file(s)")

# --- timeline templates -------------------------------------------------------
# These live one level deeper - TimelineTemplates/<TimelineId>/<actor>.lsf - so
# the flat per-directory rule above does not reach them.
tl = 0
for src in sorted(glob.glob(os.path.join(PUBLIC, "TimelineTemplates", "**",
                                         "*.lsx"), recursive=True)):
    dst = src[:-4] + ".lsf"
    r = subprocess.run([divine, "-g", "bg3", "-a", "convert-resource",
                        "-s", src, "-d", dst, "-o", "lsf"],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0 or not os.path.isfile(dst):
        print(r.stdout, r.stderr)
        sys.exit(f"failed converting timeline {os.path.basename(src)}")
    os.remove(src)
    tl += 1
if tl:
    print(f"converted {tl} timeline template(s)")

# --- dialogues --------------------------------------------------------------
# Dialogs/<cat>/x.lsj is source; the engine reads DialogsBinary/<cat>/x.lsf.
# Unlike the resources above, the .lsj is kept - Larian ships both, and it is
# the only human-readable form of the conversation we have.
DLG_SRC = os.path.join(ROOT, "Mods", "EssenceDao", "Story", "Dialogs")
DLG_BIN = os.path.join(ROOT, "Mods", "EssenceDao", "Story", "DialogsBinary")
dialogues = 0
for src in sorted(glob.glob(os.path.join(DLG_SRC, "**", "*.lsj"), recursive=True)):
    rel = os.path.relpath(src, DLG_SRC)[: -len(".lsj")] + ".lsf"
    dst = os.path.join(DLG_BIN, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    r = subprocess.run([divine, "-g", "bg3", "-a", "convert-resource",
                        "-s", src, "-d", dst, "-o", "lsf"],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0 or not os.path.isfile(dst):
        print(r.stdout, r.stderr)
        sys.exit(f"failed converting dialogue {os.path.basename(src)}")
    dialogues += 1
    print(f"  Dialogs/{rel[:-4]}.lsj -> DialogsBinary/{rel}")
if dialogues:
    print(f"converted {dialogues} dialogue(s) to the binary the engine reads")

# --- verify -----------------------------------------------------------------
wrong = []
for folder, want in REQUIRED.items():
    d = os.path.join(PUBLIC, folder)
    for f in glob.glob(os.path.join(d, "*.ls[xf]")):
        if not f.endswith("." + want):
            wrong.append(os.path.relpath(f, ROOT))
if wrong:
    print("\n!! still in the wrong format:")
    for w in wrong:
        print(f"   {w}")
    sys.exit(1)
print("every resource is in the format the engine loads")
