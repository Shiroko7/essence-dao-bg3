# -*- coding: utf-8 -*-
"""Water — 15 techniques."""
from ._schema import P, A, S

PATH = "Water"

S("ESSDAO_ICEFORM", "Ice Form",
  "Resistance to Cold and Fire damage. Movement Speed reduced by 3m.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Resistance(Cold,Resistant);Resistance(Fire,Resistant);"
                    "ActionResource(Movement,-3,0)",
           "Icon": "Spell_Abjuration_FireShield_Chill",
          "StackId": "ESSDAO_ICEFORM", "TickType": "EndTurn"})
S("ESSDAO_FROZENINSIGHT", "Frozen Insight",
  "Advantage on Arcana and Investigation Checks.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Advantage(Skill,Arcana);Advantage(Skill,Investigation)",
           "Icon": "Status_Guidance",
          "StackId": "ESSDAO_FROZENINSIGHT", "TickType": "EndTurn"})
S("ESSDAO_RESTORATIVERAIN", "Restorative Rain",
  "Regain 1 hit point at the start of each turn.",
  fields={"StatusPropertyFlags": "IgnoreResting", 
          "Icon": "Spell_Conjuration_CreateWater", "StackId": "ESSDAO_RESTORATIVERAIN",
          "TickType": "StartTurn", "TickFunctors": "RegainHitPoints(1)"})
S("ESSDAO_MOONREGEN", "Emerald Moon Regeneration",
  "Regain 1 hit point at the start of each turn.",
  fields={"StatusPropertyFlags": "DisableOverhead;IgnoreResting", 
          "Icon": "Status_Regeneration", "StackId": "ESSDAO_MOONREGEN",
          "TickType": "StartTurn", "TickFunctors": "RegainHitPoints(1)"})
S("ESSDAO_GLACIALSHIELD", "Glacial Shield",
  "Encased in ice.",
  fields={"StatusPropertyFlags": "IgnoreResting", 
          "Icon": "Spell_Abjuration_ArmorOfAgathys", "StackId": "ESSDAO_GLACIALSHIELD",
          "TickType": "EndTurn"})

# ---------------------------------------------------------------- Initiate ---
A(PATH, "initiate", "Ice Form",
  "Turn your body to ice for 10 turns. You gain Resistance to Cold and Fire "
  "damage, but your Movement Speed is reduced by 3m.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_ICEFORM,100,10)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Buff",
          "Icon": "Spell_Abjuration_FireShield_Chill"})

A(PATH, "initiate", "Restorative Rain",
  "Call a gentle rain. Creatures within it regain 1 hit point at the start of "
  "each of their turns.",
  spell_type="Zone",
  fields={"AreaRadius": "6", "TargetRadius": "6",
          "SpellProperties": "GROUND:SurfaceChange(Water);"
                             "IF(Character()):ApplyStatus(ESSDAO_RESTORATIVERAIN,100,5)",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;HasVerbalComponent", "VerbalIntent": "Healing",
          "Icon": "Spell_Conjuration_CreateWater"})

A(PATH, "initiate", "Raincaller",
  "Call a light rain that lightly obscures the area and extinguishes fires.",
  spell_type="Zone",
  fields={"AreaRadius": "9", "TargetRadius": "9",
          "SpellProperties": "GROUND:SurfaceChange(Water);GROUND:SurfaceChange(Douse)",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;HasVerbalComponent", "VerbalIntent": "Utility",
          "Icon": "Spell_Conjuration_CreateWater"},
  grade="B", note="Obscurement approximated by the water surface.")

A(PATH, "initiate", "Frozen Insight",
  "Turn your thoughts to ice. You gain Advantage on Arcana and Investigation "
  "Checks for 100 turns.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_FROZENINSIGHT,100,100)",
          "TargetConditions": "Self()", "UseCosts": "ActionPoint:1;EssencePoint:1",
          "Requirements": "!Combat", "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Status_Guidance"},
  grade="C", note="'Intelligence checks about mysteries' becomes Arcana + Investigation.")

A(PATH, "initiate", "Tide's Reflection Art I",
  "Summon a Water Clone to fight alongside you for 10 turns.",
  spell_type="Shout",
  fields={"SpellProperties": "GROUND:Summon(f21e144a-3237-4faa-a99c-a15e1937bc2c,10,Projectile_AiHelper_Summon_Strong,,'EssenceDaoCloneStack',UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Summon",
          "Icon": "Spell_Conjuration_ConjureElemental_Water"},
  grade="B", note="Reuses BG3's Water Elemental. Casting spells through the clone was dropped.")

# ------------------------------------------------------------------ Adept ---
P(PATH, "adept", "Glacial Shield",
  "As a reaction when you take damage, expend a Spell Slot to gain Temporary "
  "Hit Points equal to ten times the Slot Level.",
  boosts="UnlockInterrupt(Interrupt_EssenceDao_GlacialShield)",
  icon="Spell_Abjuration_ArmorOfAgathys")

A(PATH, "adept", "Tidal Surge",
  "A wave of restoring water washes over your allies, healing 3d8 + your "
  "Spellcasting Ability Modifier.",
  spell_type="Shout",
  fields={"AreaRadius": "9",
          "SpellProperties": "IF(Ally() or Self()):RegainHitPoints(3d8+SpellCastingAbilityModifier)",
          "TargetConditions": "Character()", "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Healing", "Icon": "Spell_Conjuration_MassHealingWord"})

A(PATH, "adept", "Moonlit Verdant Beam",
  "Fire a beam of toxic moonlight. On a hit the target takes 3d6 Radiant and "
  "3d6 Poison damage and must succeed a Constitution Saving Throw or be "
  "Blinded and Poisoned.",
  spell_type="Projectile",
  fields={"SpellRoll": "Attack(AttackType.RangedSpellAttack)",
          "SpellSuccess": "DealDamage(3d6,Radiant,Magical);DealDamage(3d6,Poison,Magical);"
                          "IF(not SavingThrow(Ability.Constitution,SourceSpellDC())):"
                          "ApplyStatus(BLINDED,100,2);"
                          "IF(not SavingThrow(Ability.Constitution,SourceSpellDC())):"
                          "ApplyStatus(POISONED,100,2)",
          "TargetRadius": "18", "ProjectileCount": "1",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Radiant",
          "TooltipDamageList": "DealDamage(3d6,Radiant);DealDamage(3d6,Poison)",
          "Icon": "Spell_Evocation_MoonBeam",
          "Trajectories": "f5855e43-2e8f-4971-b8c2-7faa36e3381b"})

A(PATH, "adept", "Hydroportation",
  "Teleport up to 18m to a space you can see. You must be standing in water.",
  spell_type="Teleportation" if False else "Shout",
  fields={"SpellProperties": "TeleportSource()", "TargetRadius": "18",
          "TargetConditions": "not Character()",
          "Requirements": "!Immobile",
          "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Utility",
          "Icon": "Spell_Conjuration_MistyStep"},
  grade="B", note="Water-contact requirement not enforced; verify TeleportSource targeting.")

A(PATH, "adept", "Tide of Emotions",
  "Sway the emotions of nearby creatures. They must succeed a Wisdom Saving "
  "Throw or be Frightened.",
  spell_type="Shout",
  fields={"AreaRadius": "9",
          "SpellRoll": "not SavingThrow(Ability.Wisdom, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(SG_Frightened,100,10)", "SpellFail": "",
          "TargetConditions": "Character() and not Self() and not Ally()",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Wisdom", "Icon": "Spell_Enchantment_CalmEmotions"},
  grade="B", note="Only the fear branch of the three emotions is represented.")

P(PATH, "adept", "Tide's Reflection Art II",
  "Your Water Clone can be detonated as a reaction, dealing Cold damage in a "
  "3m radius.",
  boosts="UnlockSpell(Shout_EssenceDao_Water_CloneDetonate)",
  icon="Spell_Conjuration_ConjureElemental_Water",
  grade="B", note="Detonation spell granted to the summoner, not the clone.")

# ----------------------------------------------------------------- Master ---
P(PATH, "master", "Draconic Regeneration of the Emerald Moon",
  "You regain 1 hit point at the start of each of your turns.",
  boosts="", passive_properties="Highlighted",
  icon="Status_Regeneration",
  fields={"StatsFunctorContext": "OnTurn",
          "Conditions": "Self()",
          "StatsFunctors": "RegainHitPoints(1)"},
  grade="C", note="Moonlight requirement dropped - BG3 has no day/night state.")

A(PATH, "master", "Moonfall Condemnation",
  "A pillar of moonlight descends. On a failed Dexterity Saving Throw the "
  "target takes 6d8 Radiant and 3d8 Cold damage and is Restrained. A target "
  "left below 50 hit points must succeed a Constitution Saving Throw or be "
  "Petrified.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Dexterity, SourceSpellDC())",
          "SpellSuccess": "DealDamage(6d8,Radiant,Magical);DealDamage(3d8,Cold,Magical);"
                          "ApplyStatus(RESTRAINED,100,2);"
                          "IF(HasHPLessThan(50) and not SavingThrow(Ability.Constitution,"
                          "SourceSpellDC())):ApplyStatus(PETRIFIED,100,-1)",
          "SpellFail": "DealDamage((6d8)/2,Radiant,Magical);DealDamage((3d8)/2,Cold,Magical)",
          "TargetRadius": "24", "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Damage", "DamageType": "Radiant",
          "TooltipDamageList": "DealDamage(6d8,Radiant);DealDamage(3d8,Cold)",
          "TooltipAttackSave": "Dexterity", "Icon": "Spell_Evocation_MoonBeam"})

A(PATH, "master", "Lunar Tide",
  "As a reaction, a protective wave reduces damage from an area effect by "
  "2d8 + your Spellcasting Ability Modifier for you and nearby allies.",
  spell_type="Shout",
  fields={"AreaRadius": "9",
          "SpellProperties": "IF(Ally() or Self()):ApplyStatus(ESSDAO_LUNARTIDE,100,1)",
          "TargetConditions": "Character()", "UseCosts": "ReactionActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Abjuration_ShieldOfFaith"},
  grade="B", note="Offered as a castable reaction rather than an interrupt on the save itself.")

P(PATH, "master", "Tide's Reflection Art III",
  "You can swap places with your Water Clone as a bonus action, and your "
  "reflection now takes the form of a Water Myrmidon.",
  boosts="UnlockSpell(Shout_EssenceDao_Water_CloneSwap);UnlockSpell(Shout_EssenceDao_Water_SummonMyrmidon)",
  icon="Spell_Conjuration_ConjureElemental_Water",
  grade="B")

S("ESSDAO_LUNARTIDE", "Lunar Tide",
  "Incoming damage reduced by 2d8 + your Spellcasting Ability Modifier.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "DamageReduction(All,Flat,2d8+SpellCastingAbilityModifier)",
           "Icon": "Spell_Abjuration_ShieldOfFaith",
          "StackId": "ESSDAO_LUNARTIDE", "TickType": "EndTurn"})
