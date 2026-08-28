# -*- coding: utf-8 -*-
"""One-off pass applying the syntax corrections the Toolkit reported.

Every change here is a direct response to a logged error, with the correct form
taken from Larian's own shipped stats:

  Advantage(SavingThrow, Ability.Wisdom)  ->  Advantage(SavingThrow,Wisdom)
      "Unknown ability 'Ability.Wisdom'"
  Disadvantage(AbilityCheck, Ability.X)   ->  Disadvantage(Ability,X)
      "invalid boost description 'AbilityCheck,Ability.X'"
  StatusGroups SG_Buff / SG_Debuff        ->  dropped
      "Invalid attribute flag 'SG_Buff' for modifier StatusGroups"
      (the valid list is SG_Condition, SG_Poisoned, SG_Restrained, ...)
  StatsFunctorContext OnSavingThrowFailed ->  OnDamaged
      "Invalid attribute flag 'OnSavingThrowFailed'" - there is no
      saving-throw-failed context, so the trigger changes meaning slightly
  Proficiency(History)                    ->  ProficiencyBonus(Skill,History)
      "invalid boost description 'History' for boost 'Proficiency'"
      (Proficiency is for weapons and tools; skills use ProficiencyBonus)
  StatusImmunity(ENTANGLED)               ->  dropped, not a real status
  DealDamage(...,ProficiencyBonus*2,...)  ->  no arithmetic; halved to the flat value
  Die(NONE,Necrotic)                      ->  not a functor; lethal damage instead

Run once; the changes are then part of build/defs/*.py.
"""
import glob, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = (glob.glob(os.path.join(ROOT, "build", "defs", "*.py"))
         + [os.path.join(ROOT, "build", "gen_abilities.py"),
            os.path.join(ROOT, "build", "gen_interrupts.py")])

REGEX = [
    (r'(Advantage|Disadvantage)\((SavingThrow|Skill),\s*Ability\.(\w+)\)', r'\1(\2,\3)'),
    (r'(Advantage|Disadvantage)\(AbilityCheck,\s*Ability\.(\w+)\)', r'\1(Ability,\2)'),
    (r'Proficiency\((History|Medicine|Nature|Survival|Athletics|Stealth|Perception)\)',
     r'ProficiencyBonus(Skill,\1)'),
]

LITERAL = [
    ('"StatusGroups": "SG_Buff",', ''),
    ('"StatusGroups": "SG_Debuff",', ''),
    ('"StatusGroups": "SG_Debuff;SG_Condition"', '"StatusGroups": "SG_Condition"'),
    ('"StatusGroups": "SG_Debuff;SG_Poisoned"', '"StatusGroups": "SG_Poisoned"'),
    ('"StatusGroups": "SG_Condition;SG_Incapacitated"', '"StatusGroups": "SG_Incapacitated"'),
    ('data "StatusGroups" "SG_Buff"', 'data "StatusGroups" "SG_RemoveOnRespec"'),
    ('"StatsFunctorContext": "OnSavingThrowFailed"', '"StatsFunctorContext": "OnDamaged"'),
    ('StatusImmunity(ENTANGLED);StatusImmunity(WEB)', 'StatusImmunity(WEB)'),
    ('DealDamage(SOURCE,ProficiencyBonus*2,Poison)', 'DealDamage(SOURCE,ProficiencyBonus,Poison)'),
    ('"OnApplyFunctors": "Die(NONE,Necrotic)"', '"OnApplyFunctors": "DealDamage(999,Necrotic,Magical)"'),
    # Reroll functors: the real signature is Reroll(threshold, bool)
    ('RerollSavingThrow(1,true)', 'Reroll(1,true)'),
    ('RerollAttackRoll(1,true)', 'Reroll(Attack,1,true)'),
]

changed = 0
for path in FILES:
    if not os.path.isfile(path):
        continue
    text = original = io.open(path, encoding="utf-8").read()
    for pat, rep in REGEX:
        text = re.sub(pat, rep, text)
    for a, b in LITERAL:
        text = text.replace(a, b)
    if text != original:
        io.open(path, "w", encoding="utf-8", newline="\n").write(text)
        changed += 1
        print(f"  fixed {os.path.relpath(path, ROOT)}")

print(f"\n{changed} files updated")

# report anything still using a shape the Toolkit rejected
print("\n=== residual suspicious patterns ===")
bad = {
    "Ability. prefix": r'Ability\.\w+',
    "SG_Buff / SG_Debuff": r'SG_(Buff|Debuff)',
    "AbilityCheck boost": r'(Advantage|Disadvantage)\(AbilityCheck',
    "arithmetic in functor": r'DealDamage\([^)]*\*\d',
}
for label, pat in bad.items():
    hits = []
    for path in FILES:
        if os.path.isfile(path):
            for m in re.finditer(pat, io.open(path, encoding="utf-8").read()):
                hits.append(os.path.basename(path))
    print(f"  {label:<24} {len(hits)} remaining"
          + (f"  ({', '.join(sorted(set(hits))[:4])})" if hits else ""))
