# -*- coding: utf-8 -*-
"""Acid — 10 techniques."""
from ._schema import P, A, S

PATH = "Acid"

S("ESSDAO_ACIDWEAPON", "Acidic Embrace",
  "Your weapon deals an additional 2d4 Acid damage.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "IF(IsWeaponAttack()):DamageBonus(2d4,Acid)",
           "Icon": "Spell_Transmutation_MagicWeapon",
          "StackId": "ESSDAO_ACIDWEAPON", "TickType": "EndTurn"})
S("ESSDAO_DISSOLVING", "Dissolving",
  "Banished to a harmless demiplane, taking 2d8 Acid damage each turn.",
  fields={"StatusPropertyFlags": "IgnoreResting;DisableInteractions",
          "StatusGroups": "SG_Incapacitated", "Icon": "Status_Banishment",
          "StackId": "ESSDAO_DISSOLVING", "TickType": "EndTurn",
          "TickFunctors": "DealDamage(2d8,Acid,Magical)"})

# ---------------------------------------------------------------- Initiate ---
P(PATH, "initiate", "Acidic Precision",
  "You gain Proficiency with thrown weapons.",
  boosts="Proficiency(Daggers);Proficiency(HandCrossbows);Proficiency(LightHammers)",
  icon="Action_Throw")

P(PATH, "initiate", "Acidic Insight",
  "You have Advantage on Arcana and Nature Checks.",
  boosts="Advantage(Skill,Arcana);Advantage(Skill,Nature)",
  icon="Skill_Arcana",
  grade="C", note="'Identify unknown substances' has no representation.")

A(PATH, "initiate", "Caustic Bomb",
  "Hurl an improvised explosive. On a failed Dexterity Saving Throw creatures "
  "take 4d6 Acid damage, half on a success.",
  spell_type="Projectile",
  fields={"SpellRoll": "not SavingThrow(Ability.Dexterity, SourceSpellDC())",
          "SpellSuccess": "DealDamage(4d6,Acid,Magical)",
          "SpellFail": "DealDamage((4d6)/2,Acid,Magical)",
          "SpellProperties": "GROUND:SurfaceChange(Acid)",
          "TargetRadius": "18", "AreaRadius": "3", "ExplodeRadius": "3",
          "ProjectileCount": "1", "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Acid", "TooltipDamageList": "DealDamage(4d6,Acid)",
          "TooltipAttackSave": "Dexterity", "Icon": "Spell_Conjuration_AcidSplash",
          "Trajectories": "f5855e43-2e8f-4971-b8c2-7faa36e3381b"})

# ------------------------------------------------------------------ Adept ---
P(PATH, "adept", "Explosive Savant",
  "Thrown alchemical items deal an additional damage die.",
  boosts="IF(IsWeaponAttack() and IsRangedAttack()):DamageBonus(1d6,Acid)",
  icon="Action_Throw",
  grade="B", note="Approximated - BG3 has no clean 'is an alchemical grenade' hook.")

P(PATH, "adept", "Expanded Explosion",
  "Your Caustic Bomb affects a wider area.",
  boosts="UnlockSpellVariant(EssenceDaoBombCheck(),ModifyAreaRadius(Additive,3),"
         "ModifyTooltipDescription())",
  icon="Action_Throw",
  grade="B", note="Applies to our own bomb only, not to every thrown item.")

P(PATH, "adept", "Extended Reach",
  "Your Caustic Bomb can be thrown twice as far.",
  boosts="UnlockSpellVariant(EssenceDaoBombCheck(),ModifyTargetRadius(Multiplicative,2),"
         "ModifyTooltipDescription())",
  icon="Action_Throw",
  grade="B", note="Same limitation as Expanded Explosion.")

A(PATH, "adept", "Acidic Embrace",
  "Coat your weapon in acid for 10 turns. It deals an additional 2d4 Acid damage.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_ACIDWEAPON,100,10)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_MagicWeapon"})

A(PATH, "adept", "Miasmic Cloud",
  "A cloud of acidic mist surrounds you. Creatures starting their turn inside "
  "must succeed a Constitution Saving Throw or take 6d6 Acid damage and be "
  "Blinded.",
  spell_type="Zone",
  fields={"AreaRadius": "3", "TargetRadius": "3",
          "SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "DealDamage(6d6,Acid,Magical);ApplyStatus(BLINDED,100,2)",
          "SpellFail": "DealDamage((6d6)/2,Acid,Magical)",
          "SpellProperties": "GROUND:SurfaceChange(Acid)",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Acid", "TooltipDamageList": "DealDamage(6d6,Acid)",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Conjuration_CloudkillSpell"})

# ----------------------------------------------------------------- Master ---
A(PATH, "master", "Erosion of Being",
  "On a failed Constitution Saving Throw the target takes 6d8 Acid damage and "
  "begins dissolving, banished for 10 turns and taking 2d8 Acid damage each "
  "turn. Half damage on a success.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "DealDamage(6d8,Acid,Magical);ApplyStatus(ESSDAO_DISSOLVING,100,10)",
          "SpellFail": "DealDamage((6d8)/2,Acid,Magical)",
          "TargetRadius": "18", "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Damage", "DamageType": "Acid",
          "TooltipDamageList": "DealDamage(6d8,Acid)",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Abjuration_Banishment"},
  grade="B", note="Permanent destruction on 0 HP dropped - no custom death path.")

A(PATH, "master", "Seven-Color Elixir",
  "Drink one of seven elixirs at random, gaining Invisibility, True Sight, "
  "Mirror Image, Confusion, Blur, or Fear.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_ELIXIR_ROLL,100,1)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_Alchemy"},
  grade="B", note="Randomisation via a roll status; hallucinatory terrain and mislead "
                  "have no BG3 equivalent and were replaced with Blur and Fear.")

S("ESSDAO_ELIXIR_ROLL", "Seven-Color Elixir",
  "One of seven effects takes hold.",
  fields={"StatusPropertyFlags": "DisableOverhead;IgnoreResting",
           "Icon": "Spell_Transmutation_Alchemy",
          "StackId": "ESSDAO_ELIXIR_ROLL", "TickType": "EndTurn",
          "OnApplyFunctors":
              "IF(RandomIsAtLeast(0.85)):ApplyStatus(SELF,INVISIBLE,100,10);"
              "IF(RandomIsAtLeast(0.70) and not HasStatus('INVISIBLE',context.Source)):"
              "ApplyStatus(SELF,ALCH_ELIXIR_SEE_INVISIBILITY,100,10);"
              "IF(RandomIsAtLeast(0.55) and not HasStatus('INVISIBLE',context.Source)):"
              "ApplyStatus(SELF,MIRROR_IMAGE_3,100,10);"
              "IF(RandomIsAtLeast(0.40) and not HasStatus('INVISIBLE',context.Source)):"
              "ApplyStatus(SELF,BLUR,100,10);"
              "IF(RandomIsAtLeast(0.20) and not HasStatus('INVISIBLE',context.Source)):"
              "ApplyStatus(SELF,BLADE_WARD,100,10)"})
