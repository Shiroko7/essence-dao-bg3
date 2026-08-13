# -*- coding: utf-8 -*-
"""Wood — 10 techniques."""
from ._schema import P, A, S

PATH = "Wood"

S("ESSDAO_VERDANTARMOR", "Verdant Armour",
  "Regain 1d6 hit points at the start of each of your turns.",
  fields={"StatusPropertyFlags": "IgnoreResting", 
          "Icon": "Spell_Transmutation_Barkskin", "StackId": "ESSDAO_VERDANTARMOR",
          "TickType": "StartTurn", "TickFunctors": "RegainHitPoints(1d6)"})
S("ESSDAO_HEARTEXCHANGE", "Heart Exchange",
  "Your fate is bound to another. Advantage on all Saving Throws.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Advantage(SavingThrow,Strength);"
                    "Advantage(SavingThrow,Dexterity);"
                    "Advantage(SavingThrow,Constitution);"
                    "Advantage(SavingThrow,Intelligence);"
                    "Advantage(SavingThrow,Wisdom);"
                    "Advantage(SavingThrow,Charisma);"
                    "DamageReduction(All,Half)",
           "Icon": "Spell_Abjuration_WardingBond",
          "StackId": "ESSDAO_HEARTEXCHANGE", "TickType": "EndTurn"})

# ---------------------------------------------------------------- Initiate ---
P(PATH, "initiate", "Fertile Ground Resilience",
  "You cannot be knocked Prone or pushed, and you have Advantage on Saving "
  "Throws against being Grappled or Restrained.",
  boosts="StatusImmunity(PRONE);Advantage(SavingThrow,Strength);"
         "Advantage(SavingThrow,Dexterity)",
  icon="Spell_Transmutation_Barkskin",
  grade="C", note="'On fertile soil' has no query; made unconditional.")

P(PATH, "initiate", "Entangling Reach",
  "You can Ensnare up to five creatures at once.",
  boosts="UnlockSpell(Target_EssenceDao_Wood_Entangling_Reach_Cast)",
  icon="Spell_Conjuration_Entangle",
  grade="B", note="Per-target essence cost collapsed to a single flat cost.")

A(PATH, "initiate", "Vine Manipulation",
  "Vines erupt from the ground. On a failed Strength Saving Throw the target "
  "is Ensnared, and the area becomes Difficult Terrain.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Strength, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(ENSNARED,100,10)", "SpellFail": "",
          "SpellProperties": "GROUND:CreateSurface(3,10,Web)",
          "TargetRadius": "9", "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Strength", "Icon": "Spell_Conjuration_Entangle"})

A(PATH, "initiate", "Thorny Defence",
  "As a reaction when hit in melee, thorns erupt from your skin and deal 4d4 "
  "Piercing damage to the attacker.",
  spell_type="Target",
  fields={"SpellProperties": "DealDamage(4d4,Piercing,Magical)",
          "TargetRadius": "3", "TargetConditions": "Character() and not Self()",
          "UseCosts": "ReactionActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful", "VerbalIntent": "Damage",
          "DamageType": "Piercing", "TooltipDamageList": "DealDamage(4d4,Piercing)",
          "Icon": "Spell_Conjuration_SpikeGrowth"})

# ------------------------------------------------------------------ Adept ---
P(PATH, "adept", "Nature's Insight",
  "You gain Proficiency in Nature and Survival. If already Proficient, you "
  "gain Expertise.",
  boosts="IF(not HasProficiency(Skill.Nature)):ProficiencyBonus(Skill,Nature);"
         "IF(HasProficiency(Skill.Nature)):ExpertiseBonus(Nature);"
         "IF(not HasProficiency(Skill.Survival)):ProficiencyBonus(Skill,Survival);"
         "IF(HasProficiency(Skill.Survival)):ExpertiseBonus(Survival)",
  icon="Skill_Nature")

P(PATH, "adept", "Woodland Stride",
  "Moving through plant-based Difficult Terrain costs you no extra movement.",
  boosts="StatusImmunity(WEB)",
  icon="PassiveFeature_WoodlandStride")

A(PATH, "adept", "Verdant Armor",
  "Living wood encases you for 10 turns. You regain 1d6 hit points at the "
  "start of each of your turns.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_VERDANTARMOR,100,10)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_Barkskin"})

A(PATH, "adept", "Needle Barrage",
  "A torrent of wooden needles. On a failed Dexterity Saving Throw the target "
  "takes 8d4 Piercing damage and its Speed is halved; half damage on a success.",
  spell_type="Projectile",
  fields={"SpellRoll": "not SavingThrow(Ability.Dexterity, SourceSpellDC())",
          "SpellSuccess": "DealDamage(8d4,Piercing,Magical);ApplyStatus(SLOW,100,2)",
          "SpellFail": "DealDamage((8d4)/2,Piercing,Magical)",
          "TargetRadius": "18", "ProjectileCount": "1",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Piercing", "TooltipDamageList": "DealDamage(8d4,Piercing)",
          "TooltipAttackSave": "Dexterity", "Icon": "Spell_Conjuration_ConjureBarrage",
          "Trajectories": "f5855e43-2e8f-4971-b8c2-7faa36e3381b"})

A(PATH, "adept", "Tree Form",
  "Take the form of a treelike creature for 10 turns, gaining Temporary Hit "
  "Points and a powerful slam attack.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_TREEFORM,100,10);"
                             "RegainTemporaryHitPoints(LevelMapValue(EssenceDaoTreeForm))",
          "TargetConditions": "Self()", "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_Barkskin"},
  grade="B", note="Approximated with a buff status rather than a full polymorph form.")

# ----------------------------------------------------------------- Master ---
A(PATH, "master", "Heart Exchange",
  "Bind your life to a willing creature for 100 turns. Damage either of you "
  "takes is halved, and you both have Advantage on Saving Throws.",
  spell_type="Target",
  fields={"SpellProperties": "ApplyStatus(ESSDAO_HEARTEXCHANGE,100,100);"
                             "ApplyStatus(SELF,ESSDAO_HEARTEXCHANGE,100,100)",
          "TargetRadius": "18", "TargetConditions": "Character() and Ally() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Buff", "Icon": "Spell_Abjuration_WardingBond"},
  grade="B", note="Shared healing dropped; damage-splitting approximated by halving both.")

S("ESSDAO_TREEFORM", "Tree Form",
  "Bark-hard skin and rooted footing. AC increased, Advantage on Strength and "
  "Constitution Saving Throws.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "AC(4);Advantage(SavingThrow,Strength);"
                    "Advantage(SavingThrow,Constitution);"
                    "CharacterUnarmedDamage(2d6,Bludgeoning)",
           "Icon": "Spell_Transmutation_Barkskin",
          "StackId": "ESSDAO_TREEFORM", "TickType": "EndTurn"})
