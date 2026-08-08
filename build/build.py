# -*- coding: utf-8 -*-
"""Build everything, validate, and pack the .pak.

    python build/build.py            generate + validate
    python build/build.py --pack     also pack to build/EssenceDao.pak
    python build/build.py --install  also copy the pak into the Mods folder

Nothing is copied into the game directory unless --install is passed.
"""
import argparse, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
PAK = os.path.join(BUILD, "EssenceDao.pak")
MODS = os.path.expandvars(r"%LOCALAPPDATA%\Larian Studios\Baldur's Gate 3\Mods")

# gen_consumables reads the manifest gen_roottemplates writes, so it follows it.
# There is no gen_guide any more - the NPC and its dialogue are gone, and
# docs/npc-and-dialogue.md records why so nobody has to rediscover it.
# gen_abilities writes containers.json, which gen_pool_passives reads to know
# what to unlock - so abilities must come first.
STEPS = ["gen_meta.py", "gen_roottemplates.py", "gen_abilities.py",
         "gen_pool_passives.py", "gen_consumables.py", "gen_interrupts.py",
         "gen_localization.py",
         "fix_handles.py", "fix_resource_formats.py"]
# validate  - nothing dangles
# wiring    - the pieces are joined to each other
# containers/field_sizes - the shapes that make BG3 *hang* rather than fail.
#   Both exist because a load hung at 79% with nothing in any log, and neither
#   of the first two could have caught it.
#   spellbook - is the result actually usable? Every other check verifies that
#     references resolve; none of them could tell you that one elixir put 19
#     entries in the spellbook, that 65% of icons were the same image, or that
#     half the entries did nothing when clicked. All three shipped.
CHECKS = ["validate.py", "check_wiring.py", "check_containers.py",
          "check_field_sizes.py", "check_spellbook.py"]


def run(script, quiet=False):
    r = subprocess.run([sys.executable, os.path.join(BUILD, script)],
                       capture_output=True, text=True, cwd=ROOT)
    ok = r.returncode == 0
    if not ok or not quiet:
        head = r.stdout.strip().splitlines()
        print(f"--- {script} {'' if ok else '[FAILED]'}")
        for l in (head if not quiet else head[:3]):
            print(f"    {l}")
        if r.stderr.strip():
            print(r.stderr.strip())
    return ok


def find_divine():
    for env in ("DIVINE", "LSLIB"):
        p = os.environ.get(env)
        if p and os.path.isfile(p):
            return p
    guesses = [os.path.join(BUILD, "lslib", "Tools", "Divine.exe")]
    for g in guesses:
        if os.path.isfile(g):
            return g
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", action="store_true")
    ap.add_argument("--install", action="store_true")
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()

    print("=" * 60)
    print("generating")
    print("=" * 60)
    for s in STEPS:
        if not run(s, args.quiet):
            sys.exit(f"\nbuild failed in {s}")

    print()
    print("=" * 60)
    print("validating")
    print("=" * 60)
    for s in CHECKS:
        if not run(s):
            sys.exit(f"\nvalidation failed in {s}")

    if not (args.pack or args.install):
        print("\ndone (source only - pass --pack to build the .pak)")
        return

    divine = find_divine()
    if not divine:
        sys.exit("\nDivine.exe not found. Set DIVINE=<path to Divine.exe> "
                 "(from Norbyte's LSLib ExportTool) and retry.")

    print()
    print("=" * 60)
    print("packing")
    print("=" * 60)

    # Divine packs everything under the source directory, so stage only the
    # three folders the game reads. Packing the repo root would ship the
    # toolchain, the docs and __pycache__ into the mod.
    stage = os.path.join(BUILD, "_stage")
    shutil.rmtree(stage, ignore_errors=True)
    for folder in ("Mods", "Public", "Localization"):
        src = os.path.join(ROOT, folder)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(stage, folder))
    for root_, dirs, files in os.walk(stage):
        for d in list(dirs):
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root_, d), ignore_errors=True)
                dirs.remove(d)

    env = dict(os.environ, DOTNET_ROLL_FORWARD="Major")
    r = subprocess.run([divine, "-g", "bg3", "-a", "create-package",
                        "-s", stage, "-d", PAK, "-c", "lz4hc"],
                       capture_output=True, text=True, env=env)
    shutil.rmtree(stage, ignore_errors=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit("packing failed")
    print(f"    {PAK}  ({os.path.getsize(PAK)/1024:.0f} KB)")

    if args.install:
        os.makedirs(MODS, exist_ok=True)
        dest = os.path.join(MODS, "EssenceDao.pak")
        shutil.copy2(PAK, dest)
        print(f"    installed -> {dest}")

        # The in-game manager lists mod.io mods only, so a local pak has to be
        # registered in modsettings.lsx by hand or the game ignores it. The MD5
        # there must match the pak we just wrote, which is why this runs last.
        print()
        if not run("install_modsettings.py"):
            sys.exit("\nfailed to register the mod in modsettings.lsx")
        print("\n    Load your save. No new game needed.")


if __name__ == "__main__":
    main()
