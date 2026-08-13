# -*- coding: utf-8 -*-
"""Spells granted by techniques rather than learned directly, plus fixes for
conditions BG3 does not actually have.

BG3 has no Deafened condition at all, so the two techniques that called for it
now apply DAZED - a real BG3 condition - rather than inventing one.
"""
from ._schema import S, RawSpell

S("ESSDAO_WINDDIE", "Wind Die",
  "You hold a d6 you may add to one d20 roll.",
  fields={"StatusPropertyFlags": "IgnoreResting",
          "Boosts": "RollBonus(Attack,1d6);RollBonus(SavingThrow,1d6)",
           "Icon": "Spell_Divination_Portent",
          "StackId": "ESSDAO_WINDDIE", "TickType": "EndTurn"})

# --- Water Clone follow-ups -------------------------------------------------
RawSpell("Shout_EssenceDao_Water_CloneDetonate", "Shout", {
    "Level": "0", "SpellSchool": "Evocation",
    "AreaRadius": "3",
    "SpellRoll": "not SavingThrow(Ability.Dexterity, SourceSpellDC())",
    "SpellSuccess": "DealDamage(4d8,Cold,Magical)",
    "SpellFail": "DealDamage((4d8)/2,Cold,Magical)",
    "TargetConditions": "Character() and not Self()",
    "UseCosts": "ReactionActionPoint:1;EssencePoint:1",
    "SpellFlags": "IsSpell;IsHarmful", "VerbalIntent": "Damage",
    "DamageType": "Cold", "TooltipDamageList": "DealDamage(4d8,Cold)",
    "TooltipAttackSave": "Dexterity",
    "Icon": "Spell_Evocation_IceKnife",
    "DisplayName": "hEssDaoX_CloneDetonate_Name;1",
    "Description": "hEssDaoX_CloneDetonate_Desc;1",
    "PreviewCursor": "Cast", "CastTextEvent": "Cast",
})

RawSpell("Shout_EssenceDao_Water_CloneSwap", "Shout", {
    "Level": "0", "SpellSchool": "Conjuration",
    "SpellProperties": "TeleportSource()",
    "TargetConditions": "Self()",
    "UseCosts": "BonusActionPoint:1",
    "SpellFlags": "IsSpell", "VerbalIntent": "Utility",
    "Icon": "Spell_Conjuration_MistyStep",
    "DisplayName": "hEssDaoX_CloneSwap_Name;1",
    "Description": "hEssDaoX_CloneSwap_Desc;1",
    "PreviewCursor": "Cast", "CastTextEvent": "Cast",
})

# --- Wind Die ---------------------------------------------------------------
RawSpell("Shout_EssenceDao_Wind_WindDie", "Shout", {
    "Level": "0", "SpellSchool": "Divination",
    "SpellProperties": "ApplyStatus(SELF,ESSDAO_WINDDIE,100,2)",
    "TargetConditions": "Self()",
    "UseCosts": "EssencePoint:1",
    "SpellFlags": "IsSpell", "VerbalIntent": "Buff",
    "Icon": "Spell_Divination_Portent",
    "DisplayName": "hEssDaoX_WindDie_Name;1",
    "Description": "hEssDaoX_WindDie_Desc;1",
    "PreviewCursor": "Cast", "CastTextEvent": "Cast",
})

# --- Entangling Reach -------------------------------------------------------
RawSpell("Target_EssenceDao_Wood_Entangling_Reach_Cast", "Target", {
    "Level": "0", "SpellSchool": "Transmutation",
    "AreaRadius": "6", "TargetRadius": "24",
    "SpellRoll": "not SavingThrow(Ability.Strength, SourceSpellDC())",
    "SpellSuccess": "ApplyStatus(ENSNARED,100,10)",
    "SpellFail": "",
    "TargetConditions": "Character() and not Self()",
    "UseCosts": "ActionPoint:1;EssencePoint:1",
    "SpellFlags": "IsSpell;IsHarmful;HasSomaticComponent",
    "VerbalIntent": "Debuff", "TooltipAttackSave": "Strength",
    "Icon": "Spell_Conjuration_Entangle",
    "DisplayName": "hEssDaoX_EntanglingReach_Name;1",
    "Description": "hEssDaoX_EntanglingReach_Desc;1",
    "PreviewCursor": "Cast", "CastTextEvent": "Cast",
})

# Tide's Reflection III upgrades the reflection to a Water Myrmidon - BG3's own
# stronger elemental, so no new creature assets are needed.
RawSpell("Shout_EssenceDao_Water_SummonMyrmidon", "Shout", {
    "Level": "0", "SpellSchool": "Conjuration",
    "SpellProperties": "GROUND:Summon(b79527a1-a83d-4b23-82d5-a02b01638469,100,"
                       "Projectile_AiHelper_Summon_Strong,,'EssenceDaoCloneStack',"
                       "UNSUMMON_ABLE,SHADOWCURSE_SUMMON_CHECK)",
    "TargetConditions": "Self()",
    "UseCosts": "ActionPoint:1;EssencePoint:3",
    "SpellFlags": "IsSpell;HasSomaticComponent", "VerbalIntent": "Summon",
    "Icon": "Spell_Conjuration_ConjureElemental_Water",
    "DisplayName": "hEssDaoX_Myrmidon_Name;1",
    "Description": "hEssDaoX_Myrmidon_Desc;1",
    "PreviewCursor": "Cast", "CastTextEvent": "Cast",
})
