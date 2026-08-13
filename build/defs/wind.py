# -*- coding: utf-8 -*-
"""Wind — 18 techniques."""
from ._schema import P, A, S

PATH = "Wind"

S("ESSDAO_ECHOFOOT", "Echoing Footsteps",
  "Advantage on Stealth Checks.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Advantage(Skill,Stealth)", 
          "Icon": "Skill_Stealth", "StackId": "ESSDAO_ECHOFOOT", "TickType": "EndTurn"})
S("ESSDAO_CALMBREEZE", "Calm Breeze",
  "Advantage on Saving Throws against being Frightened or Charmed.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Advantage(SavingThrow,Wisdom);"
                    "Advantage(SavingThrow,Charisma)",
           "Icon": "Spell_Enchantment_CalmEmotions",
          "StackId": "ESSDAO_CALMBREEZE", "TickType": "EndTurn"})
S("ESSDAO_WINDBARRIER", "Wind Barrier",
  "+2 Armour Class and Saving Throws. Attacks against you have Disadvantage.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "AC(2);RollBonus(SavingThrow,2);Disadvantage(AttackTarget)",
           "Icon": "Spell_Abjuration_Shield",
          "StackId": "ESSDAO_WINDBARRIER", "TickType": "EndTurn"})
S("ESSDAO_WINDSPRINT", "Wind Sprint",
  "Movement Speed doubled.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "ActionResourceMultiplier(Movement,200,0)",
           "Icon": "Spell_Transmutation_ExpeditiousRetreat",
          "StackId": "ESSDAO_WINDSPRINT", "TickType": "EndTurn"})
S("ESSDAO_JUSTPASSING", "Just Passing By",
  "Immune to nonmagical Slashing, Piercing and Bludgeoning damage; Resistant "
  "to the magical kinds.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Resistance(Slashing,Immune);Resistance(Piercing,Immune);"
                    "Resistance(Bludgeoning,Immune)",
           "Icon": "Spell_Transmutation_GaseousForm",
          "StackId": "ESSDAO_JUSTPASSING", "TickType": "EndTurn"})
S("ESSDAO_LIBERATION", "Liberation's Gale",
  "Advantage on Saving Throws against binding conditions.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "Advantage(SavingThrow,Strength);"
                    "Advantage(SavingThrow,Constitution);"
                    "Advantage(SavingThrow,Wisdom)",
           "Icon": "Spell_Abjuration_FreedomOfMovement",
          "StackId": "ESSDAO_LIBERATION", "TickType": "EndTurn"})

# ---------------------------------------------------------------- Initiate ---
P(PATH, "initiate", "Mistbound Step",
  "Misty Step costs no Spell Slot while you are Obscured.",
  boosts="UnlockSpellVariant(MistboundStepCheck(),"
         "ModifyUseCosts(Replace,SpellSlot,0,-1,SpellSlot),"
         "ModifyIconGlow(),ModifyTooltipDescription())",
  icon="Spell_Conjuration_MistyStep",
  grade="B", note="Freecast pattern; obscurement condition needs an in-game check.")

P(PATH, "initiate", "Whispers of the Gale",
  "When you miss with a ranged attack you can expend a Spell Slot to reroll it.",
  boosts="UnlockInterrupt(Interrupt_EssenceDao_WhispersOfTheGale)",
  icon="Spell_Divination_Portent",
  grade="B", note="OnPostRoll interrupt.")

A(PATH, "initiate", "Thunderous Roar",
  "Roar with the force of a shockwave. On a failed Constitution Saving Throw "
  "creatures are pushed 3m away and Dazed.",
  spell_type="Shout",
  fields={"AreaRadius": "3",
          "SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "Force(3,FromPosition,DamageAtEnd);ApplyStatus(DAZED,100,10)",
          "SpellFail": "", "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:1",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Evocation_Thunderwave"})

# ------------------------------------------------------------------ Adept ---
P(PATH, "adept", "Sound Analysis",
  "You have Advantage on Perception Checks.",
  boosts="Advantage(Skill,Perception)", icon="Skill_Perception",
  grade="C", note="Sound-pinpointing has no query; reduced to Perception advantage.")

P(PATH, "adept", "Misty Escape",
  "When you take damage you can expend a Spell Slot to turn to mist, causing "
  "the attack to miss.",
  boosts="UnlockInterrupt(Interrupt_EssenceDao_MistyEscape)",
  icon="Spell_Transmutation_GaseousForm",
  grade="B", note="OnPreDamage interrupt, Uncanny Dodge shape.")

P(PATH, "adept", "Fortune Favors the Swift",
  "Whenever you expend a Spell Slot you gain a d6 Wind Die, which you can add "
  "to one d20 roll before the end of your next turn.",
  boosts="UnlockSpell(Shout_EssenceDao_Wind_WindDie)",
  icon="Spell_Divination_Portent",
  grade="B", note="Bardic Inspiration machinery; the slot-spend trigger needs testing.")

A(PATH, "adept", "Echoing Footsteps",
  "Move with unnatural quiet, gaining Advantage on Stealth Checks for 100 turns.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_ECHOFOOT,100,100)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff", "Icon": "Skill_Stealth"})

A(PATH, "adept", "Thunderstep",
  "A thunderclap staggers nearby creatures. On a failed Constitution Saving "
  "Throw they are Stunned until the end of your next turn.",
  spell_type="Shout",
  fields={"AreaRadius": "9",
          "SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(STUNNED,100,2)", "SpellFail": "",
          "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent", "VerbalIntent": "Debuff",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Evocation_Thunderwave"})

A(PATH, "adept", "Calm Breeze",
  "A soothing breeze grants you and nearby allies Advantage on Saving Throws "
  "against being Frightened or Charmed.",
  spell_type="Shout",
  fields={"AreaRadius": "9",
          "SpellProperties": "IF(Ally() or Self()):ApplyStatus(ESSDAO_CALMBREEZE,100,100)",
          "TargetConditions": "Character()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Enchantment_CalmEmotions"})

A(PATH, "adept", "Wind Barrier",
  "As a reaction, wind wraps around you. You gain +2 Armour Class and Saving "
  "Throws, and attacks against you have Disadvantage until your next turn.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_WINDBARRIER,100,1)",
          "TargetConditions": "Self()", "UseCosts": "ReactionActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff", "Icon": "Spell_Abjuration_Shield"})

A(PATH, "adept", "Wind Sprint",
  "Double your Movement Speed for 3 turns.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_WINDSPRINT,100,3)",
          "TargetConditions": "Self()", "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_ExpeditiousRetreat"})

A(PATH, "adept", "Cyclone Step",
  "Dash within a swirling vortex. Creatures you pass must succeed a Strength "
  "Saving Throw or be knocked Prone.",
  spell_type="Shout",
  fields={"AreaRadius": "3",
          "SpellRoll": "not SavingThrow(Ability.Strength, SourceSpellDC())",
          "SpellSuccess": "ApplyStatus(PRONE,100,1)", "SpellFail": "",
          "SpellProperties": "ApplyStatus(SELF,DASH,100,1)",
          "TargetConditions": "Character() and not Self()",
          "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful", "VerbalIntent": "Utility",
          "TooltipAttackSave": "Strength", "Icon": "Action_Dash"},
  grade="B", note="Knockdown resolved at cast rather than along the movement path.")

A(PATH, "adept", "Gale Force Strike",
  "A gust drives a creature back. On a failed Strength Saving Throw it is "
  "pushed 3m.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Strength, SourceSpellDC())",
          "SpellSuccess": "Force(3,FromTarget,DamageAtEnd)", "SpellFail": "",
          "TargetRadius": "9", "TargetConditions": "Character() and not Self()",
          "UseCosts": "BonusActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful", "VerbalIntent": "Utility",
          "TooltipAttackSave": "Strength", "Icon": "Spell_Evocation_GustOfWind"},
  grade="B", note="Size gating dropped; offered as its own action.")

A(PATH, "adept", "Ascending Dragon Gale",
  "Strike upward with a piercing weapon. On a failed Strength Saving Throw the "
  "target takes 3d10 Thunder damage, is Restrained, and falls Prone.",
  spell_type="Target",
  fields={"SpellRoll": "not SavingThrow(Ability.Strength, SourceSpellDC())",
          "SpellSuccess": "DealDamage(3d10,Thunder,Magical);"
                          "ApplyStatus(RESTRAINED,100,2);ApplyStatus(PRONE,100,1)",
          "SpellFail": "DealDamage((3d10)/2,Thunder,Magical)",
          "TargetRadius": "MeleeMainWeaponRange",
          "TargetConditions": "Character() and not Self()",
          "UseCosts": "ActionPoint:1;EssencePoint:2",
          "SpellFlags": "IsSpell;IsHarmful;IsMelee", "VerbalIntent": "Damage",
          "DamageType": "Thunder", "TooltipDamageList": "DealDamage(3d10,Thunder)",
          "TooltipAttackSave": "Strength", "Icon": "Spell_Evocation_Thunderwave"},
  grade="C", note="20ft launch and fall damage dropped - BG3 has no airborne state.")

# ----------------------------------------------------------------- Master ---
A(PATH, "master", "Liberation's Gale",
  "A cleansing wind frees you and nearby allies from binding conditions and "
  "grants Advantage against them for 10 turns.",
  spell_type="Shout",
  fields={"AreaRadius": "18",
          "SpellProperties": "IF(Ally() or Self()):RemoveStatus(SG_Blinded);"
                             "IF(Ally() or Self()):RemoveStatus(SG_Charmed);"
                             "IF(Ally() or Self()):RemoveStatus(SG_Frightened);"
                             "IF(Ally() or Self()):RemoveStatus(SG_Restrained);"
                             "IF(Ally() or Self()):RemoveStatus(SG_Paralyzed);"
                             "IF(Ally() or Self()):RemoveStatus(SG_Poisoned);"
                             "IF(Ally() or Self()):ApplyStatus(ESSDAO_LIBERATION,100,10)",
          "TargetConditions": "Character()", "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;HasVerbalComponent;HasSomaticComponent",
          "VerbalIntent": "Utility", "Icon": "Spell_Abjuration_FreedomOfMovement"},
  grade="B", note="Source text has Immovable Mountain's paragraph pasted on the end; ignored.")

A(PATH, "master", "Just Passing By",
  "As a reaction, dissolve into wind until the start of your next turn, "
  "becoming immune to nonmagical physical damage.",
  spell_type="Shout",
  fields={"SpellProperties": "ApplyStatus(SELF,ESSDAO_JUSTPASSING,100,1)",
          "TargetConditions": "Self()", "UseCosts": "ReactionActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
          "Icon": "Spell_Transmutation_GaseousForm"},
  grade="B", note="Passing through solid objects cannot be granted; dropped.")

A(PATH, "master", "Waning Moon Sabers",
  "Launch three crescent blades. Each deals 1d4+1 Radiant damage and may Blind "
  "the target. They ignore cover.",
  spell_type="Projectile",
  fields={"SpellRoll": "Attack(AttackType.RangedSpellAttack)",
          "SpellSuccess": "DealDamage(1d4+1,Radiant,Magical);"
                          "IF(not SavingThrow(Ability.Constitution,SourceSpellDC())):"
                          "ApplyStatus(BLINDED,100,2)",
          "TargetRadius": "27", "ProjectileCount": "3",
          "UseCosts": "BonusActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent;CannotTargetItems",
          "VerbalIntent": "Damage", "DamageType": "Radiant",
          "TooltipDamageList": "DealDamage(1d4+1,Radiant)",
          "Icon": "Spell_Evocation_MoonBeam",
          "Trajectories": "f5855e43-2e8f-4971-b8c2-7faa36e3381b"})

A(PATH, "master", "Lunar Wind Spiral",
  "A cylinder of moonlit wind erupts. On a failed Constitution Saving Throw "
  "creatures take 6d8 Radiant damage, half on a success. The area persists.",
  spell_type="Zone",
  fields={"AreaRadius": "9", "TargetRadius": "45",
          "SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
          "SpellSuccess": "DealDamage(6d8,Radiant,Magical)",
          "SpellFail": "DealDamage((6d8)/2,Radiant,Magical)",
          "UseCosts": "ActionPoint:1;EssencePoint:3",
          "SpellFlags": "IsSpell;IsHarmful;IsConcentration;HasVerbalComponent;"
                        "HasSomaticComponent",
          "VerbalIntent": "Damage", "DamageType": "Radiant",
          "TooltipDamageList": "DealDamage(6d8,Radiant)",
          "TooltipAttackSave": "Constitution", "Icon": "Spell_Evocation_MoonBeam"},
  grade="C", note="The 20ft lift and the bonus-action repositioning were dropped.")
