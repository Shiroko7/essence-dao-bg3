# -*- coding: utf-8 -*-
"""Statuses the Fire techniques apply."""
from ._schema import S

S("ESSDAO_DAZZLED", "Dazzled",
  "Disadvantage on the next Attack Roll.",
  fields={"StatusPropertyFlags": "DisableOverhead;IgnoreResting",
          "Boosts": "Disadvantage(AttackRoll)",
          "StatusGroups": "SG_Condition",
          "Icon": "Status_Blinded",
          "StackId": "ESSDAO_DAZZLED",
          "TickType": "EndTurn"})

S("ESSDAO_SEARED", "Seared Gaze",
  "Disadvantage on Saving Throws against being Frightened or Charmed.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Disadvantage(SavingThrow,Wisdom);"
                    "Disadvantage(SavingThrow,Charisma)",
          "StatusGroups": "SG_Condition",
          "Icon": "Status_Hex",
          "StackId": "ESSDAO_SEARED",
          "TickType": "EndTurn"})

S("ESSDAO_BURNINGFURY", "Burning Fury",
  "Advantage on Attack Rolls.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Advantage(AttackRoll)",
          
          "Icon": "Status_Bless",
          "StackId": "ESSDAO_BURNINGFURY",
          "TickType": "EndTurn"})

S("ESSDAO_BLAZINGTRAIL", "Blazing Trail",
  "Leaving a trail of fire in your wake.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          
          "Icon": "Status_Haste",
          "StackId": "ESSDAO_BLAZINGTRAIL",
          "TickType": "StartTurn",
          "OnTickFunctors": "GROUND:SurfaceChange(Ignite)",
          "TickFunctors": "GROUND:SurfaceChange(Ignite)"})

S("ESSDAO_MARTYRFLAME", "Martyr's Flame",
  "Allies within 9m gain Resistance to Fire damage and Temporary Hit Points.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          
          "Icon": "Spell_Abjuration_FireShield_Warm",
          "StackId": "ESSDAO_MARTYRFLAME",
          "TickType": "StartTurn",
          "AuraRadius": "9",
          "AuraStatuses": "IF(Ally() or Self()):ApplyStatus(ESSDAO_MARTYRFLAME_AURA,100,1)"})

S("ESSDAO_MARTYRFLAME_AURA", "Martyr's Flame",
  "Resistance to Fire damage. Gain 2d6 Temporary Hit Points on entering the aura.",
  fields={"StatusPropertyFlags": "DisableOverhead;IgnoreResting",
          "Boosts": "Resistance(Fire, Resistant)",
          
          "Icon": "Spell_Abjuration_FireShield_Warm",
          "StackId": "ESSDAO_MARTYRFLAME_AURA",
          "TickType": "StartTurn",
          "OnApplyFunctors": "RegainTemporaryHitPoints(2d6)"})

S("ESSDAO_HEARTCRUSH", "Heart Crushed",
  "Slain outright if this damage brought you down.",
  fields={"StatusPropertyFlags": "DisableOverhead;IgnoreResting",
          "StatusGroups": "SG_Condition",
          "Icon": "Status_Doomed",
          "StackId": "ESSDAO_HEARTCRUSH",
          "TickType": "EndTurn",
          "OnApplyFunctors": "DealDamage(999,Necrotic,Magical)"})
