# The NPC and the dialogue: what we tried, and why it is gone

**Closed 9 August 2026.** Kept because everything below was learned the
expensive way, and because the next person to think "we should just add a guide
NPC" deserves to start from here rather than from scratch.

The short version: **an NPC standing in the player's camp is an Osiris feature,
and an add-on mod cannot run Osiris rules.** Every other part of it — the
character, the dialogue file, the merchant inventory — turned out to be
achievable. The camp was not.

---

## What we were trying to build

A guide in camp. Talk to him, he explains cultivation, he provides the way in
and the two breakthroughs. Originally this was Withers himself; when that turned
out to mean overwriting Larian's campaign, it became a character of our own.

## Why it is not there

Three findings, in the order they mattered.

### 1. Osiris cannot be added by an add-on

The Toolkit does not compile *your goals*. It compiles the **entire campaign
script with your goals folded in** — ours came out at **31 MB** against 27 KB of
our own source. The engine loads exactly one compiled story, from the campaign
module's path: `Mods/GustavX/Story/story.div.osi`.

So shipping Osiris means shipping a replacement for Larian's whole campaign
script. That overwrites base-game Withers and breaks every other Osiris mod
installed alongside — here that meant Mystra's Spells, Extra Encounters and
All-Players-In-Dialogue. Rejected on those grounds, not on technical ones.

> **Honest caveat.** We never cleanly proved that an add-on story at *its own*
> path fails to load. The evidence used at the time — a `SavegameLoaded` passive
> absent from a save — had two other explanations that only surfaced later: the
> mod was repeatedly being dropped from `modsettings.lsx` by the in-game mod
> manager, and our story was compiled against `GustavDev` while the campaign
> runs `GustavX`. If anyone revisits this, **that is the experiment to run**:
> one goal that adds a passive on save load, compiled against GustavX, shipped
> at our own path, with registration confirmed first.

### 2. Camp is not a place you can put someone

This is the finding that ended it.

The player's camp changes throughout the game — Act 1 wilderness, Last Light,
the Elfsong, the Slums. Act 3's trigger data alone carries `S_CAMP_Elfsong_*`
and `S_CAMP_VampireAmbush_Slums_*` variants. A hardcoded position pins an NPC to
one spot in one act and strands him the moment the camp moves.

Larian does not hardcode positions either. There are **zero** camp-named placed
characters in `Globals/CTY_Main_A/Characters`. Camp is populated at runtime, by
Osiris, using a call that takes no coordinates at all:

```
call RequestGatherAtCamp((CHARACTER)_Character)
event TeleportedToCamp((CHARACTER)_Character)
event TeleportToFromCamp((CHARACTER)_Character)
```

The engine resolves "camp" to whichever camp is currently yours. That is how
Withers and the companions follow the player around. **There is no static
equivalent.** Placement can put a character in the world; it cannot put one in
your camp.

### 3. Summoning is not a substitute

We reached the guide by having an item cast `Summon(<template>, Permanent)`,
because it was the only scriptless way to get a character into the world without
a coordinate. It produces a character you can see, name, kill or make
invulnerable — and cannot talk to.

No template field fixed it. `Faction`, `IsTrader`, `CanFight`, `CanJoinCombat`,
`Stats`, parent template — all tried, none worked. No modding tutorial describes
summoning as a way to make an NPC conversable; the documented route is
consistently *"list your DialogResourceID as a DefaultDialog for a new character
in their **Global** or RootTemplate"*, where Global means a character placed in
a level.

There is also an explicit Osiris call for the thing we wanted:

```
call SetHasDialog((GUIDSTRING)_Speaker, (INTEGER)_HasDialog)
```

We never confirmed whether interactability depends on it, but its existence is
suggestive: everything about the character can be correct and nothing has told
the engine he is someone you may speak to.

---

## What we did establish, and it is worth keeping

These were all verified against Larian's own data. If a talking NPC is ever
attempted again — with Script Extender, or in a full campaign replacement —
this is the groundwork, and it is sound.

**A dialogue is a resource, not a rule.** It is looked up by UUID and loads from
any module. `StartDialog` is the Osiris call; `DefaultDialog` on a character's
root template makes the engine open the conversation on interaction with no
script at all.

**A dialogue needs four things we did not know about.** Our file validated clean
without any of them:

| requirement | what goes wrong without it |
|---|---|
| `RootNodes` list, parallel to the nodes, naming every `Root: True` node | no entry point; nothing starts |
| non-empty `TimelineId` | 18 of 18 sampled vanilla dialogues have one; none are empty |
| a `TimelineTemplates/<TimelineId>/<actor>.lsf` | the timeline names nothing |
| a real `category` | ours said `Camp`; Larian's are `Generic NPC Dialog`, `Automated NPC Dialog`, `Repeated automated NPC Dialog`, `Voice bark` |

A timeline template is small — Liam's is **824 bytes**, one stub actor, and it is
the only file in his timeline's folder. We generated ours successfully. This is
not the hard part.

**Divine builds dialogue binaries.** `divine -a convert-resource -o lsf` on a
`.lsj` produces what the Toolkit produces (18,801 bytes against 18,176 for the
same conversation). **The Toolkit was never needed at any point in this
project.**

**Level placement is additive and works.** A mod can drop one `.lsf` per
character into `Globals/<Level>/Characters/` alongside Larian's `_merged.lsf`;
the engine reads every file in the directory. Extra Encounters places 286
characters this way. Nothing is overwritten and mods do not collide. The
instance carries `TradeTreasures` and `StatusList` directly, so a placed NPC can
be a merchant and can be made invulnerable without any stats work.

**Invulnerable but interactable** is the `INVULNERABLE` status
(`Boosts "Invulnerable()"`) applied via the template's `StatusList` — not the
`Flags "InvulnerableAndInteractive"` field, which we tried first and which did
nothing.

**Localization has one correct location.** `Mods/<ModFolder>/Localization/
English/english.xml`, raw XML, no `.loca`. Every working mod on the test machine
does exactly this. A root-level `Localization/` folder makes every name in the
mod render as **"Not Found"** while validating perfectly on disk.

---

## Script Extender, for the record

Checked 9 August 2026, since it kept being raised.

- Osiris does **not** need Script Extender. Osiris is the game's native engine;
  SE adds *Lua* and exposes Osiris functions to it.
- Official [BG3SE](https://github.com/Norbyte/bg3se) is **Windows only**. Latest
  release v32, 21 June 2026, ships a single `DWrite.dll` for
  `Baldurs Gate 3\bin`. Linux works via Proton. No macOS assets or instructions.
- An unofficial macOS port exists —
  [tdimino/bg3se-macos](https://github.com/tdimino/bg3se-macos), v0.42.0, ~94.8%
  self-reported parity — but requires macOS 12+, Xcode CLT, CMake, **building
  from source**, and a Steam launch-option wrapper.

With SE, the camp guide is straightforward: `Osi.RequestGatherAtCamp`,
`Osi.SetHasDialog`, `Osi.StartDialog`. The cost is a hard dependency that Mac
users must compile themselves.

---

## What replaced it

A book, from the tutorial chest — the legacy of a cultivator who reached the
Master stage with no talent at all, purely by brewing and drinking. It carries
the entire explanation the guide would have given, and the three recipes.

Progression is the brewing: Initiate, then Adept, then Master. When the book
runs out of answers, that is not a gap in the design. He died before he could
write any more.

Which is a better mod than one that needs a scripting dependency to introduce
itself.
