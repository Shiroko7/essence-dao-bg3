# -*- coding: utf-8 -*-
"""Metal — 7 techniques.

The thinnest path by some margin: 7 shipping against Poison's 22. Flagged in the
plan as needing either more Metal content or a trim elsewhere before release.
"""
from ._schema import P, A, S

PATH = "Metal"

S("ESSDAO_KEENEDGE", "Keen Edge",
  "+1 bonus to Attack and Damage Rolls.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "RollBonus(Attack,1);DamageBonus(1)",
           "Icon": "Spell_Transmutation_MagicWeapon",
          "StackId": "ESSDAO_KEENEDGE", "TickType": "EndTurn"})
S("ESSDAO_ENHANCEDARMOR", "Enhanced Armor",
  "Resistance to Slashing, Piercing and Bludgeoning damage.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Resistance(Slashing,Resistant);Resistance(Piercing,Resistant);"
                    "Resistance(Bludgeoning,Resistant)",
           "Icon": "Spell_Abjuration_Stoneskin",
          "StackId": "ESSDAO_ENHANCEDARMOR", "TickType": "EndTurn"})

# ---------------------------------------------------------------- Initiate ---
A(PATH, "initiate", "Keen Edge",
  "Sharpen your weapon. You gain a +1 bonus to Attack and Damage Rolls for "
  "100 turns.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_KEENEDGE,100,100)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_MagicWeapon"})

A(PATH, "initiate", "Magnetic Attraction",
  "Wrench a creature toward you by the metal it carries. On a failed Strength "
  "Saving Throw it is pulled 3m closer and Disarmed.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Strength, SourceSpellDC())",
          "SpellSuccess": "Force(3,FromTarget,DamageAtEnd);ApplyStatus(DISARMED,100,1)",
          "SpellFail": "", "TargetRadius": "18",
          "TargetConditions": "Character() and not Self()",
          "UseCosts": "BonusActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Utility",
          "TooltipAttackSave": "Strength", "Icon": "Spell_Transmutation_MagicWeapon"},
  grade="C", note="Free-form object telekinesis dropped; pull + disarm retained.")

A(PATH, "initiate", "Metallic Echo",
  "Strike a ringing note from your weapon. Nearby creatures must succeed a "
  "Constitution Saving Throw or be Dazed.",
  spell_type="Shout",
  fields={"AreaRadius": "3",
          "SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(DAZED,100,2)", "SpellFail": "",
          "TargetConditions": "Character() and not Self()",
          "UseCosts": "BonusActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Evocation_Shatter"},
  grade="B", note="Trigger changed from 'strike a metal object' to a cast.")

# ------------------------------------------------------------------ Adept ---
A(PATH, "adept", "Enhanced Armor",
  "Reinforce your armour for 100 turns, gaining Resistance to Slashing, "
  "Piercing and Bludgeoning damage.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_ENHANCEDARMOR,100,100)",
          "TargetConditions": "Self()", "Requirements": "!Combat",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Buff",
          "Icon": "Spell_Abjuration_Stoneskin"},
  grade="B", note="Choose-a-damage-type collapsed to the three physical types.")

A(PATH, "adept", "Magnetic Shield",
  "As a reaction, a magnetic field reduces incoming damage by 1d10 + your "
  "Constitution Modifier and may Disarm the attacker.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_MAGSHIELD,100,1)",
          "TargetConditions": "Self()", "UseCosts": "ReactionActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Abjuration_Shield"},
  grade="B", note="Offered as a castable reaction; disarm rider not conditional on metal.")

A(PATH, "adept", "Steel Tornado",
  "A whirlwind of metal shards. On a failed Dexterity Saving Throw creatures "
  "take 7d6 Slashing damage, half on a success.",
  spell_type="Shout",
  fields={"AreaRadius": "9",
          "SpellRoll": "not SavingThrow(Ability.Dexterity, SourceSpellDC())",
          "SpellSuccess": "DealDamage(7d6,Slashing,Magical)",
          "SpellFail": "DealDamage((7d6)/2,Slashing,Magical)",
          "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Slashing", "TooltipDamageList": "DealDamage(7d6,Slashing)",
          "TooltipAttackSave": "Dexterity", "Icon": "Spell_Conjuration_CloudOfDaggers"})

# ----------------------------------------------------------------- Master ---
A(PATH, "master", "Weight of Lives",
  "Press the weight of every life you have taken onto a creature. On a failed "
  "Charisma Saving Throw it takes 8d8 Force damage and is Restrained; on a "
  "success it takes half and its Speed is halved. You gain Temporary Hit "
  "Points equal to the damage dealt.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Charisma, SourceSpellDC())",
          "SpellSuccess": "DealDamage(8d8,Force,Magical);ApplyStatus(RESTRAINED,100,3);"
                          "RegainTemporaryHitPoints(8d8)",
          "SpellFail": "DealDamage((8d8)/2,Force,Magical);ApplyStatus(SLOW,100,2)",
          "TargetRadius": "18", "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Damage", "DamageType": "Force",
          "TooltipDamageList": "DealDamage(8d8,Force)",
          "TooltipAttackSave": "Charisma", "Icon": "Spell_Evocation_MagicMissile"},
  grade="C", note="'2d8 per karmic debt discerned' has no game state; fixed at 8d8.")

S("ESSDAO_MAGSHIELD", "Magnetic Shield",
  "Incoming damage reduced by 1d10 + your Constitution Modifier.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "DamageReduction(All,Flat,1d10+ConstitutionModifier)",
           "Icon": "Spell_Abjuration_Shield",
          "StackId": "ESSDAO_MAGSHIELD", "TickType": "EndTurn"})
