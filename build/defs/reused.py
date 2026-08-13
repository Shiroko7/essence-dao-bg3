# -*- coding: utf-8 -*-
"""The 90 spells BG3 already implements.

These cost nothing to build - we grant Larian's own stat entry, so they arrive
with their icons, VFX, tooltips and upcast variants intact. Registered through
the same Ability machinery as custom techniques so they land in the same
containers and obey the same Attunement budget.

Spell level maps onto tier exactly as isTierUnlocked() does in the source:
    cantrip / 1st / 2nd -> Initiate
    3rd / 4th           -> Adept
    5th / 6th           -> Master
7th and above are cut: BG3 grants no spell slot past 6th.
"""
import json, os
from ._schema import Ability

_HERE = os.path.dirname(os.path.abspath(__file__))
_XREF = os.path.join(_HERE, "..", "spell_xref.json")

TIER_OF_LEVEL = {"cantrip": "initiate", "1st": "initiate", "2nd": "initiate",
                 "3rd": "adept", "4th": "adept",
                 "5th": "master", "6th": "master"}

_seen = set()
for row in json.load(open(_XREF, encoding="utf-8")):
    if row["status"] not in ("PLAYER", "NPC_ONLY"):
        continue
    tier = TIER_OF_LEVEL.get(row["tier"])
    if not tier:
        continue                      # 7th+ has no slot in BG3
    path = (row["essence"] if row["essence"] != "air" else "wind").capitalize()
    entry = row["bg3"][0]             # the BG3 stat entry to grant

    key = (path, row["name"])
    if key in _seen:                  # source lists a few spells twice
        continue
    _seen.add(key)

    a = Ability(
        path, tier, row["name"],
        f"Learn {row['name']}. This is the spell as it exists in Baldur's Gate 3, "
        f"cast using Essence rather than a Spell Slot.",
        kind="passive",               # the learned thing is a passive that unlocks a spell
        boosts=f"UnlockSpell({entry},,,,)",
        icon="PassiveFeature_Generic_Magical",
        grade="A",
        note=f"Grants Larian's {entry}.",
    )
    # A granted spell does not bind essence the way a custom passive does - it
    # is a spell you may cast, so it costs Attunement only. Suppress the
    # EssencePoint reduction that `kind="passive"` would otherwise add.
    a.is_reused_spell = True
