# Essence Dao — a Baldur's Gate 3 mod

Adds a pool of Essence and nine paths of cultivation, learned through the
spellbook. It does not replace magic or spellcasting: Essence is a second,
parallel resource, and every technique is paid for out of it.

Ported from [Shiroko7/essence-talent-system](https://github.com/Shiroko7/essence-talent-system).

**No dependencies. Windows and Mac. Overwrites not one Larian file.**
Installs onto a campaign already in progress — no new game, no respec.

---

## Playing it

The **Testament of the Rootless** is in the tutorial chest. It is the journal of
a cultivator with no talent at all, who reached the Master stage anyway by
brewing his way there over sixty years. It explains the whole system and gives
you the three recipes, and that is all it does — it is notes, not a key.

Brewing is the progression. Alchemy is on the inventory screen; each elixir
takes any extract plus a reagent of the right affinity:

| | brewed from | needs | gives |
|---|---|---|---|
| Root-Opening Elixir | any extract + **Water** reagent | — | 8 Essence, Initiate paths |
| Foundation Elixir | any extract + **Earth** reagent | level 5 | 16 Essence, Adept paths |
| Golden Core Elixir | any extract + **Fire** reagent | level 9 | 24 Essence, Master paths |

After the Master stage the book has nothing more to say. Its author ran out of
years before he could write any.

**Set the Dao Aside**, in your spellbook once you are a cultivator, releases
every technique and returns all Attunement. Breakthroughs are kept — take the
Dao up again and your Foundation and Core are as you left them.

---

## Building

```
python build/build.py              # generate + validate
python build/build.py --pack       # also build build/EssenceDao.pak
python build/build.py --install    # also install it and register it
```

Packing needs `Divine.exe` from [Norbyte's LSLib](https://github.com/Norbyte/lslib),
looked for at `build/lslib/Tools/Divine.exe`, or set `DIVINE=<path>`.

Set `BG3_DATA` to a folder of the game's unpacked stats to have `validate.py`
check every reference against Larian's own entries — without it, roughly a
hundred references to vanilla spells and statuses report as unverifiable rather
than passing. To produce one:

```
Divine.exe -g bg3 -a extract-package -s <game>/Data/Shared.pak \
           -d <dest> -x "*/Stats/Generated/Data/*.txt"
```

`--install` copies the pak into your Mods folder **and** adds it to
`modsettings.lsx`. That second step is not optional: the in-game mod manager
lists mod.io mods only, so a local pak that is merely copied in is ignored.

Close the game first — a running BG3 holds the installed pak open.

---

## How it works

**There is no Osiris rule in this mod, anywhere.** That is a constraint, not a
choice, and it is the single most important thing to know before changing
anything here.

The engine loads exactly one compiled story, from the *campaign module's* path,
`Mods/GustavX/Story/story.div.osi`. This mod shipped its own for a while — 31 MB
— and not one rule ever executed. The size is the tell: the Toolkit does not
compile *your goals*, it compiles the entire campaign script with yours folded
in. Loading it would have replaced base-game Withers and broken every other
Osiris mod installed. It was never read, which is the only reason nothing broke.

So every state change here is an item or a passive. Those are additive, conflict
with nothing, and apply to a save already in progress the moment the pak is
installed.

**There is no NPC and no dialogue**, and that was not for lack of trying. A
guide who stands in your camp needs `RequestGatherAtCamp`, an Osiris call, and
camp is not a place a mod can statically put anyone — Larian populates it at
runtime, and it moves between acts. Summoning produces something you can see,
name and kill, but not talk to. The full account, including the four structural
requirements of a BG3 dialogue that nothing in our pipeline knew about, is in
[docs/npc-and-dialogue.md](docs/npc-and-dialogue.md). Read it before
reintroducing either.

The book replaced him, and carries everything he would have said.

**Two resources, because the source system tracks two things.**
`EssenceAttunement` is how much technique you may know — every technique claims
part of it permanently. `EssencePoint` is what you spend to use active
techniques, and it refills on a Long Rest. Passive techniques permanently reduce
the pool as well as the budget; that is what "binding essence" means.

**The pool follows cultivation stage, not character level.** 8 Essence as a
Cultivator, 16 with a Foundation, 24 with a Golden Core. The source system
scaled with level, and so did this mod until the Osiris rule that read your
level turned out never to run. The three numbers are the ones that curve
reached at its caps, so a full cultivator is exactly as strong as before — but
power now comes from breaking through rather than from killing things, which is
what the system was always about.

**The spellbook is the talent tree.** Nine containers, one per path, each
holding that path's techniques. BG3 does the enforcement itself: a technique
costing more Attunement than you have greys itself out.

**Breakthroughs are structural, not conditional.** Each stage's nine containers
are unlocked by that stage's passive, and the passive is carried by the status
its drink applies. Without the Foundation Elixir the Adept containers
are simply not on your character, so an over-stage technique cannot be browsed,
learned or cast. There is nothing to check at cast time and nothing to get wrong.

**Drinking is what unlocks.** The use-action lives in the item's root template
(`OnUsePeaceActions` → `ActionType 7`, apply status, duration -1), which is
where Larian puts it. It does *not* work from `Object.txt`; ours tried that for
a while and the pills silently did nothing.

---

## Layout

```
Mods/EssenceDao/
  meta.lsx                        module manifest (no TargetModes:Story)
  Localization/English/english.xml every handle - this path matters, see below
Public/EssenceDao/
  ActionResourceDefinitions/      EssencePoint + EssenceAttunement
  RootTemplates/                  the book, the three elixirs, and what drinking does
  Stats/Generated/                all generated stat entries + TreasureTable
build/
  defs/                           ability specs, one module per path
  gen_*.py                        generators
  validate.py                     whole-mod reference validation
  check_wiring.py                 the pieces are actually joined up
  check_containers.py             cycles - the shape that makes BG3 hang
  check_field_sizes.py            fields far larger than anything Larian ships
  build.py                        orchestrator
docs/npc-and-dialogue.md          why there is no NPC; read before adding one
```

Localization must be `Mods/<ModFolder>/Localization/English/english.xml`, raw
XML, no `.loca`. A root-level `Localization/` folder makes every name in the mod
render as **"Not Found"** while validating perfectly on disk. `check_wiring`
fails the build if one appears.

Everything under `Public/` and `Mods/EssenceDao/Localization/` is **generated**.
Edit `build/defs/*.py` and re-run the build; do not hand-edit the stat files.

---

## Status

Built and validated. The full-strength `validate.py` run (with `BG3_DATA` set)
resolves all 1,030 of our entries plus every reference into Larian's data.

Two validators run on every build:

| | |
|---|---|
| `validate.py` | no dangling statuses, spells, passives or localization handles |
| `check_wiring.py` | the pieces are joined — the way in works end to end, consumables actually do something, no recipe collides with a vanilla one |

The second exists because the first passed while the mod was entirely
unreachable. Reference checks cannot catch a dead end, so `check_wiring` asserts
the specific failures that have shipped: an Osiris folder coming back, a
consumable whose use-action does nothing, a recipe colliding with Greater
Healing Potion, a passive unlocking a spell nobody defined. It decodes the
shipped binary `.lsf` rather than the source `.lsx`, so it checks the artefact
the game reads.

Known things to verify in play:

- **Container behaviour.** The design assumes a container shows only the
  children your character has unlocked. If BG3 instead greys locked children,
  the stage gating still holds but reads differently.
- **`CharacterLevelGreaterThan` in `UseConditions`.** Verified to exist as a
  condition and used correctly in spell properties by Larian; using it to gate
  an item's use is the one unproven construct left. If a pill is greyed out at
  level 6, this is why.
- **Interrupt conditions.** All four are authored, but conditions like
  `RollResultIsLowerThan` are used from pattern rather than from a reference.
- **Summon balance.** The Water Myrmidon at Master tier is probably too strong.
  One line in `build/defs/water.py`.
- **Tree balance.** Poison ships 30 entries against Metal's 11.

## Content

211 shipping entries: 122 custom techniques and 89 spells reused from BG3.
166 entries from the source system were cut for having no BG3 representation.
Full triage in `docs/feasibility.html`.

## The book, and the guide that isn't

The system was originally introduced by Withers, then by a guide of our own, and
now by a dead man's journal. That is a retreat, and it is worth being honest
about why: **an NPC standing in your camp is an Osiris feature**, an add-on
cannot run Osiris rules, and every scriptless route we tried — summoning,
placement, faction and dialogue plumbing — failed for reasons recorded in
[docs/npc-and-dialogue.md](docs/npc-and-dialogue.md).

The design absorbs it better than expected. Nothing in the mod ever needed a
conversation:

- the elixirs gate themselves by level through `UseConditions`
- a stage's containers simply do not exist on a character who has not broken
  through, so there is nothing to check
- the book can hold every rule a guide would have explained, and unlike a guide
  it cannot be missed, killed, or left behind in the wrong act

A cultivator who got there with no talent, purely by brewing, is also a better
fit for a system whose entire progression is brewing.
