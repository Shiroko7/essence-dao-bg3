# -*- coding: utf-8 -*-
"""Lightning — 11 techniques."""
from ._schema import P, A, S

PATH = "Lightning"

S("ESSDAO_LIGHTNINGSTEP", "Lightning Step",
  "Your jump distance is tripled and your movement does not provoke "
  "Opportunity Attacks.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "JumpMaxDistanceMultiplier(3);ActionResource(Movement,3,0)",
           "Icon": "Action_Jump",
          "StackId": "ESSDAO_LIGHTNINGSTEP", "TickType": "EndTurn"})
S("ESSDAO_STORMPRESENCE", "Stormborn Presence",
  "1d4 bonus to Persuasion and Intimidation Checks.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "RollBonus(SkillCheck,1d4,Persuasion);"
                    "RollBonus(SkillCheck,1d4,Intimidation)",
           "Icon": "Status_Guidance",
          "StackId": "ESSDAO_STORMPRESENCE", "TickType": "EndTurn"})
S("ESSDAO_NOREACTIONS", "Grounded",
  "Cannot take Reactions.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "ActionResourceBlock(ReactionActionPoint)",
           "Icon": "Status_Shocked",
          "StackId": "ESSDAO_NOREACTIONS", "TickType": "EndTurn"})
S("ESSDAO_STUNIMMUNE", "Thunder-Numbed",
  "Cannot be Stunned by Thunderous Strike again for a time.",
  fields={"StatusPropertyFlags": "DisableOverhead;IgnoreResting",
          "StatusGroups": "SG_Condition", "Icon": "Status_Shocked",
          "StackId": "ESSDAO_STUNIMMUNE", "TickType": "EndTurn"})

# ---------------------------------------------------------------- Initiate ---
P(PATH, "initiate", "Static Reflexes",
  "You have Advantage on Dexterity Saving Throws.",
  boosts="Advantage(SavingThrow,Dexterity)",
  icon="PassiveFeature_Resilient_Dexterity")

A(PATH, "initiate", "Lightning Step",
  "Your jump distance is tripled and your movement does not provoke "
  "Opportunity Attacks until the end of your turn.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_LIGHTNINGSTEP,100,1);"
                             "ApplyStatus(SELF,DISENGAGE,100,1)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell", "VerbalIntent": "Utility", "Icon": "Action_Jump"})

A(PATH, "initiate", "Stormborn Presence",
  "Invoke your stormy bearing, gaining a 1d4 bonus to Persuasion and "
  "Intimidation Checks.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_STORMPRESENCE,100,100)",
          "TargetConditions": "Self()", "Requirements": "!Combat",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff", "Icon": "Status_Guidance"},
  grade="C", note="'Influence a group' has no representation; flat bonus instead.")

# ------------------------------------------------------------------ Adept ---
P(PATH, "adept", "Thunderous Speed",
  "Your Movement Speed increases by 3m and you can Dash as a bonus action.",
  boosts="ActionResource(Movement,3,0);UnlockSpell(Shout_Dash_StepOfTheWind)",
  icon="Spell_Transmutation_ExpeditiousRetreat")

P(PATH, "adept", "Lightning Sense",
  "You have Advantage on Perception Checks.",
  boosts="Advantage(Skill,Perception)", icon="Skill_Perception",
  grade="C", note="'Stormy environments' qualifier dropped.")

A(PATH, "adept", "Conductive Touch",
  "Your melee attack carries a charge, dealing an additional 2d12 Lightning "
  "damage.",
  spell_type="Target",
  fields={"SpellRoll": "Attack(AttackType.MeleeWeaponAttack)",
          "SpellSuccess": "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType);"
                          "DealDamage(2d12,Lightning,Magical)",
          "TargetRadius": "MeleeMainWeaponRange",
          "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;IsMelee;IsAttack", "VerbalIntent": "Damage",
          "DamageType": "Lightning", "TooltipDamageList": "DealDamage(2d12,Lightning)",
          "Icon": "Spell_Evocation_ShockingGrasp"})

A(PATH, "adept", "Thunderous Strike",
  "Channel a thunderstorm into your strike. On a failed Constitution Saving "
  "Throw the target is Stunned until the end of your next turn.",
  spell_type="Target",
  fields={"SpellRoll": "Attack(AttackType.MeleeWeaponAttack)",
          "SpellSuccess": "DealDamage(MainMeleeWeapon,MainMeleeWeaponDamageType);"
                          "IF(not SavingThrow(Ability.Constitution,SourceSpellDC())):"
                          "ApplyStatus(STUNNED,100,2);"
                          "IF(not SavingThrow(Ability.Constitution,SourceSpellDC())):"
                          "ApplyStatus(ESSDAO_STUNIMMUNE,100,10)",
          "TargetRadius": "MeleeMainWeaponRange",
          "TargetConditions": "Character() and not Self() and "
                              "not HasStatus('ESSDAO_STUNIMMUNE')",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;IsMelee;IsAttack", "VerbalIntent": "Damage",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Evocation_Thunderwave"})

A(PATH, "adept", "Lightning Javelin",
  "Hurl a javelin of lightning dealing 5d12 Lightning damage. The target "
  "cannot take Reactions until the start of its next turn.",
  spell_type="Projectile",
  fields={"SpellRoll": "Attack(AttackType.RangedSpellAttack)",
          "SpellSuccess": "DealDamage(5d12,Lightning,Magical);"
                          "ApplyStatus(ESSDAO_NOREACTIONS,100,1)",
          "TargetRadius": "18", "ProjectileCount": "1",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Lightning", "TooltipDamageList": "DealDamage(5d12,Lightning)",
          "Icon": "Spell_Evocation_LightningBolt",
          "Trajectories": "f5855e43-2e8f-4971-b8c2-7faa36e3381b"})

A(PATH, "adept", "Arc Chain",
  "Lightning leaps between foes. On a failed Dexterity Saving Throw each "
  "creature takes 3d8 Lightning damage, half on a success.",
  spell_type="Zone",
  fields={"AreaRadius": "9", "TargetRadius": "24",
          "SpellRoll": "not SavingThrow(Ability.Dexterity, SourceSpellDC())",
          "SpellSuccess": "DealDamage(3d8,Lightning,Magical)",
          "SpellFail": "DealDamage((3d8)/2,Lightning,Magical)",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent", "VerbalIntent": "Damage",
          "DamageType": "Lightning", "TooltipDamageList": "DealDamage(3d8,Lightning)",
          "TooltipAttackSave": "Dexterity", "Icon": "Spell_Evocation_ChainLightning"},
  grade="B", note="Unbounded chaining collapsed to a zone - recursive jumps need scripting.")

# ----------------------------------------------------------------- Master ---
A(PATH, "master", "Lightning Cage",
  "A crackling cage of lightning. Creatures inside have their Speed halved, "
  "cannot take Reactions, and take 4d10 Lightning damage on contact.",
  spell_type="Zone",
  fields={"AreaRadius": "9", "TargetRadius": "27",
          "SpellRoll": "not SavingThrow(Ability.Strength, SourceSpellDC())",
          "SpellSuccess": "DealDamage(4d10,Lightning,Magical);"
                          "ApplyStatus(ESSDAO_NOREACTIONS,100,10);ApplyStatus(SLOW,100,10)",
          "SpellFail": "DealDamage((4d10)/2,Lightning,Magical)",
          "SpellProperties": "GROUND:CreateSurface(9,10,Lightning)",
          "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Damage", "DamageType": "Lightning",
          "TooltipDamageList": "DealDamage(4d10,Lightning)",
          "TooltipAttackSave": "Strength", "Icon": "Spell_Evocation_ChainLightning"},
  grade="B", note="Edge-contact geometry simplified to a persistent zone.")

A(PATH, "master", "Extinguishing Lightning",
  "Black lightning floods a cone. On a failed Dexterity Saving Throw creatures "
  "take 6d12 Lightning damage and lose Concentration; half damage on a success.",
  spell_type="Zone",
  fields={"AreaRadius": "18", "TargetRadius": "18", "Shape": "Cone", "Angle": "60",
          "SpellRoll": "not SavingThrow(Ability.Dexterity, SourceSpellDC())",
          "SpellSuccess": "DealDamage(6d12,Lightning,Magical);RemoveStatus(SG_Concentration)",
          "SpellFail": "DealDamage((6d12)/2,Lightning,Magical)",
          "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Damage", "DamageType": "Lightning",
          "TooltipDamageList": "DealDamage(6d12,Lightning)",
          "TooltipAttackSave": "Dexterity", "Icon": "Spell_Evocation_ChainLightning"},
  grade="B", note="'End one magical effect of your choice' became stripping Concentration.")
