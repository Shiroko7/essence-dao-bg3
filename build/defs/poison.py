# -*- coding: utf-8 -*-
"""Poison — 22 techniques, the densest path.

Six of these are the Mutagen Formula family, which differ only in which ability
score they raise and which they lower, so they are generated from a table rather
than written out six times.
"""
from ._schema import P, A, S

PATH = "Poison"

for _n, _up, _down in [("Strength", "Strength", "Intelligence"),
                       ("Dexterity", "Dexterity", "Wisdom"),
                       ("Constitution", "Constitution", "Charisma"),
                       ("Intelligence", "Intelligence", "Strength"),
                       ("Wisdom", "Wisdom", "Dexterity"),
                       ("Charisma", "Charisma", "Constitution")]:
    S(f"ESSDAO_MUTAGEN_{_n.upper()}", f"Mutagen: {_n}",
      f"+2 {_up}, -2 {_down}.",
      fields={"StatusPropertyFlags": "IgnoreResting",
              "Boosts": f"Ability({_up},2);Ability({_down},-2)",
              
              "Icon": "Spell_Transmutation_EnhanceAbility_BullsStrenght",
              "StackId": f"ESSDAO_MUTAGEN_{_n.upper()}", "TickType": "EndTurn"})

S("ESSDAO_STRENGTHBOOST", "Strength Booster",
  "1d4 bonus to Strength Checks.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "RollBonus(SkillCheck,1d4,Athletics)",
           "Icon": "Status_Guidance",
          "StackId": "ESSDAO_STRENGTHBOOST", "TickType": "EndTurn"})
S("ESSDAO_QUICKENING", "Quickening Draught",
  "Movement Speed increased by 3m.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "ActionResource(Movement,3,0)",
           "Icon": "Spell_Transmutation_ExpeditiousRetreat",
          "StackId": "ESSDAO_QUICKENING", "TickType": "EndTurn"})
S("ESSDAO_PERFUME", "Enchanting Perfume",
  "1d4 bonus to Persuasion and Deception Checks.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "RollBonus(SkillCheck,1d4,Persuasion);"
                    "RollBonus(SkillCheck,1d4,Deception)",
           "Icon": "Status_Guidance",
          "StackId": "ESSDAO_PERFUME", "TickType": "EndTurn"})
S("ESSDAO_PILLOFFOCUS", "Pill of Focus",
  "Advantage on Constitution Saving Throws to maintain Concentration.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Advantage(SavingThrow,Constitution)",
           "Icon": "Status_Guidance",
          "StackId": "ESSDAO_PILLOFFOCUS", "TickType": "EndTurn"})
S("ESSDAO_HALLUCINATING", "Hallucinogenic Trance",
  "Disadvantage on Intelligence, Wisdom and Charisma Saving Throws and Checks.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Disadvantage(SavingThrow,Intelligence);"
                    "Disadvantage(SavingThrow,Wisdom);"
                    "Disadvantage(SavingThrow,Charisma);"
                    "Disadvantage(Ability,Intelligence);"
                    "Disadvantage(Ability,Wisdom);"
                    "Disadvantage(Ability,Charisma)",
          "StatusGroups": "SG_Condition", "Icon": "Status_Confusion",
          "StackId": "ESSDAO_HALLUCINATING", "TickType": "EndTurn"})
S("ESSDAO_VESTIBULAR", "Vestibular Trance",
  "Disadvantage on Strength, Dexterity and Constitution Saving Throws and Checks.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Disadvantage(SavingThrow,Strength);"
                    "Disadvantage(SavingThrow,Dexterity);"
                    "Disadvantage(SavingThrow,Constitution);"
                    "Disadvantage(Ability,Strength);"
                    "Disadvantage(Ability,Dexterity);"
                    "Disadvantage(Ability,Constitution)",
          "StatusGroups": "SG_Condition", "Icon": "Status_Nauseated",
          "StackId": "ESSDAO_VESTIBULAR", "TickType": "EndTurn"})
S("ESSDAO_VENOMWEAPON", "Venomous Strike",
  "Your next attack deals an additional 2d6 Poison damage.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "IF(IsWeaponAttack()):DamageBonus(2d6,Poison)",
           "Icon": "Spell_Transmutation_MagicWeapon",
          "StackId": "ESSDAO_VENOMWEAPON", "TickType": "EndTurn",
          "RemoveEvents": "OnAttack"})
S("ESSDAO_TOXICSLOW", "Toxic Secretion",
  "Poisoned, and Movement Speed halved.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "ActionResourceMultiplier(Movement,50,0)",
          "StatusGroups": "SG_Poisoned", "Icon": "Status_Poisoned",
          "StackId": "ESSDAO_TOXICSLOW", "TickType": "EndTurn"})

# ---------------------------------------------------------------- Initiate ---
P(PATH, "initiate", "Herbalist's Knowledge",
  "You gain Proficiency in Medicine and Advantage on Medicine Checks.",
  boosts="ProficiencyBonus(Skill,Medicine);Advantage(Skill,Medicine)",
  icon="Skill_Medicine")

P(PATH, "initiate", "Toxic Skin Secretion I",
  "Once per turn, a creature that hits you with a melee attack must succeed a "
  "Constitution Saving Throw or be Poisoned until the end of its next turn.",
  icon="Status_Poisoned",
  fields={"StatsFunctorContext": "OnAttacked",
          "Conditions": "IsMeleeAttack() and not SavingThrow(Ability.Constitution,"
                        "SourceSpellDC())",
          "StatsFunctors": "ApplyStatus(SOURCE,POISONED,100,2)"})

A(PATH, "initiate", "Venomous Touch",
  "Poison a creature with a touch. On a failed Constitution Saving Throw it is "
  "Poisoned and takes 1d6 Poison damage at the start of each of its turns.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(ESSDAO_VENOMOUSTOUCH,100,10)", "SpellFail": "",
          "TargetRadius": "1.5", "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Necromancy_RayOfSickness"})

A(PATH, "initiate", "Venomous Bite",
  "Bite a creature, dealing 1d12 Piercing damage. On a failed Constitution "
  "Saving Throw it is Poisoned.",
  spell_type="Target",
  fields={"SpellRoll": "Attack(AttackType.MeleeWeaponAttack)",
          "SpellSuccess": "DealDamage(1d12,Piercing,Magical);"
                          "IF(not SavingThrow(Ability.Constitution,SourceSpellDC())):"
                          "ApplyStatus(POISONED,100,10)",
          "TargetRadius": "1.5", "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful;IsMelee", "VerbalIntent": "Damage",
          "DamageType": "Piercing", "TooltipDamageList": "DealDamage(1d12,Piercing)",
          "Icon": "Spell_Necromancy_VampiricTouch"})

A(PATH, "initiate", "Strength Booster",
  "Drink a mutagen, gaining a 1d4 bonus to Strength Checks for 100 turns.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_STRENGTHBOOST,100,100)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff", "Icon": "Status_Guidance"})

A(PATH, "initiate", "Quickening Draught",
  "Drink a draught, gaining 3m Movement Speed for 100 turns.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_QUICKENING,100,100)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_ExpeditiousRetreat"})

A(PATH, "initiate", "Enchanting Perfume",
  "Apply a perfume, gaining a 1d4 bonus to Persuasion and Deception Checks.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_PERFUME,100,100)",
          "TargetConditions": "Self()", "Requirements": "!Combat",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff", "Icon": "Status_Guidance"})

# ------------------------------------------------------------------ Adept ---
P(PATH, "adept", "Venomous Precision",
  "You have Advantage on Attack Rolls against Poisoned creatures.",
  boosts="IF(HasStatus('SG_Poisoned',context.Target)):Advantage(AttackRoll)",
  icon="Status_Poisoned")

P(PATH, "adept", "Toxic Skin Secretion II",
  "As Toxic Skin Secretion I, and the attacker also takes Poison damage equal "
  "to your Proficiency Bonus.",
  icon="Status_Poisoned",
  fields={"StatsFunctorContext": "OnAttacked",
          "Conditions": "IsMeleeAttack() and not SavingThrow(Ability.Constitution,"
                        "SourceSpellDC())",
          "StatsFunctors": "ApplyStatus(SOURCE,POISONED,100,10);"
                           "DealDamage(SOURCE,ProficiencyBonus,Poison)"})

for _n in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
    A(PATH, "adept", f"Mutagen Formula ({_n})",
      f"Drink a mutagen for 100 turns, gaining +2 {_n} at the cost of another "
      f"ability score.",
      spell_type="Shout",
      fields={"SpellProperties": f"ApplyStatus(SELF,ESSDAO_MUTAGEN_{_n.upper()},100,100)",
              "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
              "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
              "Icon": "Spell_Transmutation_EnhanceAbility_BullsStrenght"})

A(PATH, "adept", "Venomous Strike",
  "Coat your weapon. Your next attack deals an additional 2d6 Poison damage "
  "and may Poison the target.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_VENOMWEAPON,100,10)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_MagicWeapon"})

A(PATH, "adept", "Hallucinogenic Trance",
  "A Poisoned creature must succeed a Wisdom Saving Throw or suffer "
  "Disadvantage on Intelligence, Wisdom and Charisma Saving Throws and Checks.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Wisdom, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(ESSDAO_HALLUCINATING,100,10)", "SpellFail": "",
          "TargetRadius": "9",
          "TargetConditions": "Character() and not Self() and HasStatus('SG_Poisoned')",
          "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Wisdom", "Icon": "Status_Confusion"})

A(PATH, "adept", "Vestibular Trance",
  "A Poisoned creature must succeed a Constitution Saving Throw or suffer "
  "Disadvantage on Strength, Dexterity and Constitution Saving Throws and Checks.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(ESSDAO_VESTIBULAR,100,10)", "SpellFail": "",
          "TargetRadius": "9",
          "TargetConditions": "Character() and not Self() and HasStatus('SG_Poisoned')",
          "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Constitution", "Icon": "Status_Nauseated"})

A(PATH, "adept", "Pill of Focus",
  "Swallow a pill, gaining Advantage on Concentration Saving Throws.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_PILLOFFOCUS,100,100)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff", "Icon": "Status_Guidance"})

A(PATH, "adept", "Moonlit Verdant Beam",
  "Fire a beam of toxic moonlight dealing 3d6 Radiant and 3d6 Poison damage. "
  "On a failed Constitution Saving Throw the target is Blinded and Poisoned.",
  spell_type="Projectile",
  fields={"SpellRoll": "Attack(AttackType.RangedSpellAttack)",
          "SpellSuccess": "DealDamage(3d6,Radiant,Magical);DealDamage(3d6,Poison,Magical);"
                          "IF(not SavingThrow(Ability.Constitution,SourceSpellDC())):"
                          "ApplyStatus(BLINDED,100,2)",
          "TargetRadius": "18", "ProjectileCount": "1",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Poison",
          "TooltipDamageList": "DealDamage(3d6,Radiant);DealDamage(3d6,Poison)",
          "Icon": "Spell_Evocation_MoonBeam",
          "Trajectories": "f5855e43-2e8f-4971-b8c2-7faa36e3381b"})

# ----------------------------------------------------------------- Master ---
P(PATH, "master", "Toxic Skin Secretion III",
  "As Toxic Skin Secretion II, but the attacker is Poisoned for far longer, "
  "takes twice your Proficiency Bonus in Poison damage, and has its Movement "
  "Speed halved.",
  icon="Status_Poisoned",
  fields={"StatsFunctorContext": "OnAttacked",
          "Conditions": "IsMeleeAttack() and not SavingThrow(Ability.Constitution,"
                        "SourceSpellDC())",
          "StatsFunctors": "ApplyStatus(SOURCE,ESSDAO_TOXICSLOW,100,100);"
                           "DealDamage(SOURCE,ProficiencyBonus,Poison)"})

A(PATH, "master", "Apex Toxinator",
  "Conjure a venomous woodland horror to fight for you.",
  spell_type="Shout",
  fields={"SpellProperties": "GROUND:Summon(42da1663-b150-4e9b-abc8-8cdc7240fd56,100,Projectile_AiHelper_Summon_Strong,,'EssenceDaoSummonStack',UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK)",
          "TargetConditions": "Self()", "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Summon", "Icon": "Spell_Conjuration_ConjureWoodlandBeing_Wood_Woad"},
  grade="B", note="Reuses BG3's Conjure Woodland Being template - no new creature assets.")

S("ESSDAO_VENOMOUSTOUCH", "Venomous Touch",
  "Poisoned. Takes 1d6 Poison damage at the start of each turn.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "StatusGroups": "SG_Poisoned", "Icon": "Status_Poisoned",
          "StackId": "ESSDAO_VENOMOUSTOUCH", "TickType": "StartTurn",
          "TickFunctors": "DealDamage(1d6,Poison,Magical)",
          "RemoveEvents": "OnHeal"})
