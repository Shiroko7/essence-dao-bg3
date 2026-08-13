# -*- coding: utf-8 -*-
"""Earth — 15 techniques.

Note: the source tags Earthen Ward as `tier: active`, which is not one of the
five tiers. Treated as Initiate here; flagged upstream as a data bug.
"""
from ._schema import P, A, S

PATH = "Earth"

S("ESSDAO_STONEARMOR", "Stone Armor",
  "Resistance to Bludgeoning, Piercing and Slashing damage.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Resistance(Bludgeoning,Resistant);Resistance(Piercing,Resistant);"
                    "Resistance(Slashing,Resistant)",
           "Icon": "Spell_Abjuration_Stoneskin",
          "StackId": "ESSDAO_STONEARMOR", "TickType": "EndTurn"})
S("ESSDAO_IMMOVABLE", "Immovable Mountain",
  "Cannot be moved, knocked Prone, Grappled, Restrained, Paralysed or Stunned. "
  "Melee hits may push or knock down.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "StatusImmunity(PRONE);StatusImmunity(GRAPPLED);"
                    "StatusImmunity(RESTRAINED);StatusImmunity(PARALYZED);"
                    "StatusImmunity(STUNNED);Advantage(SavingThrow,Strength)",
           "Icon": "Spell_Transmutation_EnhanceAbility_BullsStrenght",
          "StackId": "ESSDAO_IMMOVABLE", "TickType": "EndTurn"})
S("ESSDAO_MOVESMOUNTAINS", "Moves Mountains",
  "Your Spell Save DC is increased.",
  fields={"StatusPropertyFlags": "IgnoreResting", "Boosts": "SpellSaveDC(1)",
           "Icon": "Status_Bless",
          "StackId": "ESSDAO_MOVESMOUNTAINS", "TickType": "EndTurn"})

# ---------------------------------------------------------------- Initiate ---
P(PATH, "initiate", "Stonecunning",
  "You gain Proficiency in History. If already Proficient, you gain Expertise.",
  boosts="IF(not HasProficiency(Skill.History)):ProficiencyBonus(Skill,History);"
         "IF(HasProficiency(Skill.History)):ExpertiseBonus(History)",
  icon="PassiveFeature_Stonecunning")

P(PATH, "initiate", "Earth Sense",
  "You have Advantage on Survival and Perception Checks.",
  boosts="Advantage(Skill,Survival);Advantage(Skill,Perception)",
  icon="PassiveFeature_Stonecunning",
  grade="C", note="'Underground or rocky terrain' has no query; made unconditional.")

P(PATH, "initiate", "Stone Fist I",
  "Your Unarmed Strikes deal 1d6 Bludgeoning damage and count as magical.",
  boosts="CharacterUnarmedDamage(1d6,Bludgeoning);"
         "IF(IsUnarmedAttack()):DamageBonus(0,Bludgeoning,Magical)",
  icon="Skill_Monk_MartialArts")

A(PATH, "initiate", "Pebble Barrage",
  "Hurl a barrage of stones. On a failed Dexterity Saving Throw the target "
  "takes 4d4 Bludgeoning damage and falls Prone.",
  spell_type="Projectile",
  fields={"SpellRoll": "not SavingThrow(Ability.Dexterity, SourceSpellDC())",
          "SpellSuccess": "DealDamage(4d4,Bludgeoning,Magical);ApplyStatus(PRONE,100,1)",
          "SpellFail": "", "TargetRadius": "9", "ProjectileCount": "1",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Bludgeoning", "TooltipDamageList": "DealDamage(4d4,Bludgeoning)",
          "TooltipAttackSave": "Dexterity", "Icon": "Spell_Conjuration_ConjureBarrage",
          "Trajectories": "f5855e43-2e8f-4971-b8c2-7faa36e3381b"})

A(PATH, "initiate", "Earthen Ward",
  "As a reaction, earth hardens around you. You gain 1d10 + your Constitution "
  "Modifier Temporary Hit Points.",
  spell_type="Shout",
  fields={"SpellProperties": "RegainTemporaryHitPoints(1d10+ConstitutionModifier)",
          "TargetConditions": "Self()", "UseCosts": "ReactionActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Abjuration_Stoneskin"},
  grade="B", note="Source tags this 'tier: active' - normalised to Initiate.")

# ------------------------------------------------------------------ Adept ---
P(PATH, "adept", "Earthen Resilience",
  "You gain Proficiency in Constitution Saving Throws.",
  boosts="ProficiencyBonus(SavingThrow,Constitution)",
  icon="PassiveFeature_Resilient_Constitution")

P(PATH, "adept", "Terramancer",
  "You gain Expertise in Athletics.",
  boosts="ExpertiseBonus(Athletics)", icon="Skill_Athletics",
  grade="C", note="Stone-lifting qualifier dropped.")

P(PATH, "adept", "Stone Camouflage",
  "You gain Expertise in Stealth.",
  boosts="ExpertiseBonus(Stealth)", icon="Skill_Stealth",
  grade="C", note="Rocky-terrain qualifier dropped.")

P(PATH, "adept", "Stone Fist II",
  "Your Unarmed Strikes deal 1d8 Bludgeoning damage and count as magical.",
  boosts="CharacterUnarmedDamage(1d8,Bludgeoning)", icon="Skill_Monk_MartialArts")

A(PATH, "adept", "Earthen Grasp",
  "The ground seizes a creature, Restraining it. It can attempt a Strength "
  "Saving Throw at the end of each of its turns to break free.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Strength, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(ENSNARED,100,10)", "SpellFail": "",
          "TargetRadius": "9", "TargetConditions": "Character() and not Self()",
          "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Strength", "Icon": "Spell_Conjuration_Entangle"})

A(PATH, "adept", "Stone Armor",
  "Encase yourself in stone for 10 turns, gaining Resistance to Bludgeoning, "
  "Piercing and Slashing damage.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_STONEARMOR,100,10)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Buff",
          "Icon": "Spell_Abjuration_Stoneskin"})

A(PATH, "adept", "Sandstorm",
  "A storm of sand tears through the area. On a failed Constitution Saving "
  "Throw creatures take 3d6 Slashing damage and are Blinded. The ground "
  "becomes Difficult Terrain.",
  spell_type="Zone",
  fields={"AreaRadius": "6", "TargetRadius": "6",
          "SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "DealDamage(3d6,Slashing,Magical);ApplyStatus(BLINDED,100,2)",
          "SpellFail": "DealDamage((3d6)/2,Slashing,Magical)",
          "SpellProperties": "GROUND:CreateSurface(6,10,Sand)",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Damage", "DamageType": "Slashing",
          "TooltipDamageList": "DealDamage(3d6,Slashing)",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Conjuration_CloudOfDaggers"})

# ----------------------------------------------------------------- Master ---
P(PATH, "master", "Stone Fist III",
  "Your Unarmed Strikes deal 1d10 Bludgeoning damage and count as magical.",
  boosts="CharacterUnarmedDamage(1d10,Bludgeoning)", icon="Skill_Monk_MartialArts")

P(PATH, "master", "Foolish Old Man Moves Mountains",
  "Each time you fail a Saving Throw your Spell Save DC increases by 1, up to "
  "+3, until you Long Rest.",
  icon="Status_Bless",
  fields={"StatsFunctorContext": "OnDamaged",
          "Conditions": "Self() and not HasStatus('ESSDAO_MOVESMOUNTAINS',context.Source)"
                        " or HasStatusCountLessThan('ESSDAO_MOVESMOUNTAINS',3)",
          "StatsFunctors": "ApplyStatus(SELF,ESSDAO_MOVESMOUNTAINS,100,-1)"},
  grade="B", note="Stack cap relies on HasStatusCountLessThan - verify in game.")

A(PATH, "master", "Immovable Mountain",
  "For 10 turns you cannot be moved, knocked Prone, Grappled, Restrained, "
  "Paralysed or Stunned.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_IMMOVABLE,100,10)",
          "TargetConditions": "Self()", "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_EnhanceAbility_BullsStrenght"})
