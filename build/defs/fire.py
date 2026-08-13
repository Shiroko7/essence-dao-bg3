# -*- coding: utf-8 -*-
"""Fire — 12 techniques (3 of the source's 15 were cut for no BG3 representation)."""
from ._schema import P, A

PATH = "Fire"

# ---------------------------------------------------------------- Initiate ---

P(PATH, "initiate", "Flame Ward",
  "You have Advantage on Saving Throws against being Frightened or Charmed "
  "while standing in fire or on burning ground.",
  boosts="IF(InSurface(SurfaceType.Fire) or HasStatus('BURNING',context.Source)):"
         "Advantage(SavingThrow,Wisdom)",
  icon="PassiveFeature_Generic_Fire",
  grade="B", note="Rebound from 'near a fire source' to standing in fire.")

P(PATH, "initiate", "Ember Strike",
  "When you hit with a weapon attack you can expend a Spell Slot to deal an "
  "additional 1d12 Fire damage per Slot Level. The target must succeed a Wisdom "
  "Saving Throw or be Frightened until the end of its next turn.",
  boosts="UnlockSpellVariant(EmberStrikeCheck(),"
         "ModifyUseCosts(Add,SpellSlot,1,1,SpellSlot),"
         "ModifySpellFlags(IsSpell),ModifyIconGlow(),ModifyTooltipDescription())",
  icon="PassiveFeature_Generic_Fire",
  grade="A", note="Divine Smite pattern, Radiant swapped for Fire.")

P(PATH, "initiate", "Frightful Pursuit",
  "You have Advantage on Attack Rolls against Frightened creatures.",
  boosts="IF(HasStatus('SG_Frightened',context.Target)):Advantage(AttackRoll)",
  icon="PassiveFeature_Generic_Fire")

A(PATH, "initiate", "Flame Lash",
  "Lash out with a whip of fire. Deals 4d6 Fire damage and Dazzles the target, "
  "giving it Disadvantage on its next Attack Roll.",
  spell_type="Target",
  fields={
      "SpellRoll": "Attack(AttackType.MeleeSpellAttack)",
      "SpellSuccess": "DealDamage(4d6,Fire,Magical);"
                      "ApplyStatus(ESSDAO_DAZZLED,100,1)",
      "SpellFail": "",
      "TargetRadius": "4.5",
      "UseCosts": "ActionPoint:1;EssencePoint:1",
      "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent",
      "VerbalIntent": "Damage",
      "DamageType": "Fire",
      "TooltipDamageList": "DealDamage(4d6,Fire)",
      "Icon": "Spell_Evocation_ProduceFlame",
      "PrepareEffect": "fdbf8e88-c3a5-4151-a81d-429985de422c",
      "CastEffect": "69aaec35-fb5f-489e-a4cc-47310f4377e9",
      "TargetEffect": "41de42e1-56d0-4336-8b44-99fc38281525",
  })

A(PATH, "initiate", "Inferno Disengage",
  "Disengage in a burst of flame, dealing 2d6 Fire damage to nearby creatures.",
  spell_type="Shout",
  fields={
      "AreaRadius": "1.5",
      "SpellProperties": "GROUND:SurfaceChange(Ignite);"
                         "IF(not Self()):DealDamage(2d6,Fire,Magical);"
                         "ApplyStatus(SELF,DISENGAGE,100,1)",
      "TargetConditions": "Character()",
      "UseCosts": "BonusActionPoint:1;EssencePoint:1",
      "SpellFlags": "IsSpell;HasSomaticComponent",
      "VerbalIntent": "Utility",
      "DamageType": "Fire",
      "TooltipDamageList": "DealDamage(2d6,Fire)",
      "Icon": "Action_Disengage",
  },
  grade="B", note="Wraps Disengage rather than hooking it.")

A(PATH, "initiate", "Heart Crusher Grip",
  "Crush the heart of a wounded creature. Deals 6d6 Fire damage on a failed "
  "Constitution Saving Throw, half on a success. A creature reduced to 0 hit "
  "points by this dies instantly.",
  spell_type="Target",
  fields={
      "SpellRoll": "not SavingThrow(Ability.Constitution, SourceSpellDC())",
      "SpellSuccess": "DealDamage(6d6,Fire,Magical);"
                      "IF(HasHPPercentageLessThan(1)):ApplyStatus(ESSDAO_HEARTCRUSH,100,1)",
      "SpellFail": "DealDamage((6d6)/2,Fire,Magical)",
      "TargetRadius": "4.5",
      "TargetConditions": "Character() and not Self() and HasHPPercentageLessThan(50)",
      "UseCosts": "ActionPoint:1;EssencePoint:1",
      "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent",
      "VerbalIntent": "Damage",
      "DamageType": "Fire",
      "TooltipDamageList": "DealDamage(6d6,Fire)",
      "TooltipAttackSave": "Constitution",
      "Icon": "Spell_Necromancy_InflictWounds",
  },
  grade="B", note="'Bloodied' becomes below 50% HP; instant death via status.")

A(PATH, "initiate", "Searing Gaze",
  "Fix a creature with a burning stare. It must succeed a Wisdom Saving Throw "
  "or have Disadvantage on Saving Throws against being Frightened or Charmed "
  "by you.",
  spell_type="Target",
  fields={
      "SpellRoll": "not SavingThrow(Ability.Wisdom, SourceSpellDC())",
      "SpellSuccess": "ApplyStatus(ESSDAO_SEARED,100,10)",
      "SpellFail": "",
      "TargetRadius": "9",
      "TargetConditions": "Character() and not Self()",
      "UseCosts": "BonusActionPoint:1;EssencePoint:1",
      "SpellFlags": "IsSpell;IsHarmful",
      "VerbalIntent": "Debuff",
      "TooltipAttackSave": "Wisdom",
      "Icon": "Spell_Enchantment_Command_Halt",
  },
  grade="C", note="Intimidation check replaced with a Wisdom save.")

# ------------------------------------------------------------------ Adept ---

P(PATH, "adept", "Ember's Resilience",
  "As a reaction when you fail a Saving Throw, you can reroll it. If you do, "
  "you take 2d6 Fire damage.",
  boosts="UnlockInterrupt(Interrupt_EssenceDao_EmbersResilience)",
  icon="PassiveFeature_Generic_Fire",
  grade="B", note="OnPostRoll interrupt - the Lucky/Portent shape.")

P(PATH, "adept", "Burning Fury",
  "Immediately after you take Fire damage, you have Advantage on Attack Rolls "
  "until the end of your next turn.",
  boosts="IF(HasStatus('ESSDAO_BURNINGFURY',context.Source)):Advantage(AttackRoll)",
  icon="PassiveFeature_Generic_Fire",
  fields={"StatsFunctorContext": "OnDamaged",
          "Conditions": "IsDamageTypeFire()",
          "StatsFunctors": "ApplyStatus(SELF,ESSDAO_BURNINGFURY,100,2)"})

A(PATH, "adept", "Scorched Ground",
  "Superheat the ground in a wide area. Creatures starting their turn there "
  "take 4d6 Fire damage. The ground becomes Difficult Terrain.",
  spell_type="Zone",
  fields={
      "AreaRadius": "6",
      "TargetRadius": "18",
      "SpellProperties": "GROUND:SurfaceChange(Ignite);GROUND:CreateSurface(6,10,ScorchedGround)",
      "UseCosts": "ActionPoint:1;EssencePoint:2",
      "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent;HasVerbalComponent",
      "VerbalIntent": "Damage",
      "DamageType": "Fire",
      "Icon": "Spell_Conjuration_CreateWaterCone",
  })

A(PATH, "adept", "Blazing Presence",
  "Erupt with heat and light. Creatures nearby must succeed a Wisdom Saving "
  "Throw or be Frightened until the end of your next turn.",
  spell_type="Shout",
  fields={
      "AreaRadius": "6",
      "SpellRoll": "not SavingThrow(Ability.Wisdom, SourceSpellDC())",
      "SpellSuccess": "ApplyStatus(SG_Frightened,100,2)",
      "SpellFail": "",
      "TargetConditions": "Character() and not Self() and not Ally()",
      "UseCosts": "ActionPoint:1;EssencePoint:2",
      "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent",
      "VerbalIntent": "Debuff",
      "TooltipAttackSave": "Wisdom",
      "Icon": "Spell_Illusion_Fear",
  },
  grade="C", note="Intimidation clause dropped; the Frighten burst remains.")

A(PATH, "adept", "Blazing Trail",
  "Dash, leaving a trail of fire behind you. Creatures entering it or ending "
  "their turn in it take Fire damage.",
  spell_type="Shout",
  fields={
      "SpellProperties": "ApplyStatus(SELF,ESSDAO_BLAZINGTRAIL,100,10);"
                         "ApplyStatus(SELF,DASH,100,1)",
      "TargetConditions": "Self()",
      "UseCosts": "BonusActionPoint:1;EssencePoint:2",
      "SpellFlags": "IsSpell;HasSomaticComponent",
      "VerbalIntent": "Utility",
      "DamageType": "Fire",
      "Icon": "Action_Dash",
  },
  grade="B", note="Trail laid by a status that spawns fire surface per turn.")

# ----------------------------------------------------------------- Master ---

A(PATH, "master", "Martyr's Flame Aura",
  "Wreathe yourself in holy fire for 10 turns. Allies within the aura gain "
  "Resistance to Fire damage and 2d6 Temporary Hit Points when they enter it "
  "or start their turn inside.",
  spell_type="Shout",
  fields={
      "SpellProperties": "ApplyStatus(SELF,ESSDAO_MARTYRFLAME,100,10)",
      "TargetConditions": "Self()",
      "UseCosts": "ActionPoint:1;EssencePoint:3",
      "SpellFlags": "IsSpell;IsConcentration;HasVerbalComponent;HasSomaticComponent",
      "VerbalIntent": "Buff",
      "Icon": "Spell_Abjuration_FireShield_Warm",
  })

A(PATH, "master", "Shadowflame Dream",
  "Hurl flames laced with negative energy. On a failed Charisma Saving Throw "
  "the target takes 5d10 Fire and 5d10 Necrotic damage and falls Unconscious "
  "until the start of your next turn. On a success it takes only the Fire "
  "damage.",
  spell_type="Projectile",
  fields={
      "SpellRoll": "not SavingThrow(Ability.Charisma, SourceSpellDC())",
      "SpellSuccess": "DealDamage(5d10,Fire,Magical);"
                      "DealDamage(5d10,Necrotic,Magical);"
                      "ApplyStatus(UNCONSCIOUS,100,1)",
      "SpellFail": "DealDamage(5d10,Fire,Magical)",
      "TargetRadius": "18",
      "ProjectileCount": "1",
      "UseCosts": "ActionPoint:1;EssencePoint:3",
      "SpellFlags": "IsSpell;IsHarmful;HasVerbalComponent;HasSomaticComponent",
      "VerbalIntent": "Damage",
      "DamageType": "Fire",
      "TooltipDamageList": "DealDamage(5d10,Fire);DealDamage(5d10,Necrotic)",
      "TooltipAttackSave": "Charisma",
      "Icon": "Spell_Evocation_Fireball",
      "Trajectories": "f5855e43-2e8f-4971-b8c2-7faa36e3381b",
  })
