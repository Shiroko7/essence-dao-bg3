# -*- coding: utf-8 -*-
"""Spec format for Essence techniques.

THE COST MODEL
--------------
The source system tracks two separate things, and conflating them breaks it:

  * a *learning budget* - calculateTotalPointsSpent() counts every ability you
    know against calculateEssencePoints(level). This is permanent.
  * a *usable pool*     - calculateEffectiveMaxPoints() is that same total minus
    the cost of every passive you know. Actives spend from it and get it back.

So two resources:

  EssenceAttunement  how much technique you may know. Every technique learned
                     reduces it. Refills on rest, but its *maximum* is already
                     reduced by what you know, so refilling only ever returns
                     your unspent budget.
  EssencePoint       what you spend to use active techniques. Refills on rest.
                     Passive techniques permanently reduce its maximum, which is
                     what "binding" essence means in the source system.

Hence a learned technique's passive carries:

  passive technique   ActionResource(EssenceAttunement,-N,0);
                      ActionResource(EssencePoint,-N,0)
  active technique    ActionResource(EssenceAttunement,-N,0);
                      UnlockSpell(<the active spell>)

and the learn-spell that grants it carries UseCosts "EssenceAttunement:N", which
is what makes BG3 grey out techniques you cannot afford. The engine does the
enforcement; we only declare the numbers.

TIER COSTS come straight from getTierCost(): initiate 1, adept 2, master 3.
"""

TIER_COST = {"initiate": 1, "adept": 2, "master": 3}
TIERS = ["Initiate", "Adept", "Master"]
PATHS = ["Water", "Fire", "Earth", "Metal", "Wood",
         "Poison", "Acid", "Lightning", "Wind"]

_REGISTRY = []
_STATUSES = []


class Status:
    """A custom status. `fields` are raw BG3 Status_BOOST fields."""

    def __init__(self, name, display, desc, fields=None, stype="BOOST"):
        self.name = name
        self.display = display
        self.desc = desc
        self.stype = stype
        self.fields = dict(fields or {})
        _STATUSES.append(self)

    @property
    def h_name(self):
        return f"hEssDaoS_{self.name}_Name"

    @property
    def h_desc(self):
        return f"hEssDaoS_{self.name}_Desc"


def S(name, display, desc, **kw):
    return Status(name, display, desc, **kw)


_RAW_SPELLS = []


def RawSpell(name, spell_type, fields):
    """A spell that is granted by a technique rather than learned directly.

    Used where one learned passive unlocks several castables - the Water Clone's
    detonate and swap, the Wind Die, and so on.
    """
    _RAW_SPELLS.append((name, spell_type, dict(fields)))


def all_raw_spells():
    return list(_RAW_SPELLS)


def all_statuses():
    return list(_STATUSES)


def _slug(name):
    out = []
    for ch in name:
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "_":
            out.append("_")
    return "".join(out).strip("_")


class Ability:
    """One technique. `fields` are raw BG3 stat fields, passed through verbatim."""

    def __init__(self, path, tier, name, blurb, *,
                 kind, spell_type=None, fields=None, boosts="",
                 passive_properties="", icon=None, grade="A", note=""):
        assert kind in ("passive", "active"), kind
        assert tier in TIER_COST, tier
        if kind == "active":
            assert spell_type in ("Target", "Shout", "Projectile", "Zone", "Rush"), spell_type
        self.path = path
        self.tier = tier
        self.name = name
        self.blurb = blurb              # player-facing description
        self.kind = kind
        self.spell_type = spell_type
        self.fields = dict(fields or {})
        self.boosts = boosts            # extra boosts on the learned passive
        self.passive_properties = passive_properties
        self.icon = icon or "PassiveFeature_Generic_Magical"
        self.grade = grade
        self.note = note
        self.slug = f"{path}_{_slug(name)}"
        _REGISTRY.append(self)

    # --- derived names -----------------------------------------------------
    @property
    def cost(self):
        return TIER_COST[self.tier]

    @property
    def passive_name(self):
        return f"EssenceDao_T_{self.slug}"

    @property
    def learn_name(self):
        return f"Shout_EssenceDao_Learn_{self.slug}"

    @property
    def spell_name(self):
        """The stat entry for the active itself (actives only)."""
        return f"{self.spell_type}_EssenceDao_{self.slug}"

    @property
    def container(self):
        return f"Shout_EssenceDao_{self.path}_{self.tier.capitalize()}"

    # --- localisation handles ---------------------------------------------
    @property
    def h_name(self):
        return f"hEssDao_{self.slug}_Name"

    @property
    def h_desc(self):
        return f"hEssDao_{self.slug}_Desc"

    @property
    def h_learn_name(self):
        return f"hEssDao_{self.slug}_LearnName"

    @property
    def h_learn_desc(self):
        return f"hEssDao_{self.slug}_LearnDesc"

    @property
    def h_release_name(self):
        return f"hEssDao_{self.slug}_RelName"

    @property
    def h_release_desc(self):
        return f"hEssDao_{self.slug}_RelDesc"

    def learned_boosts(self):
        parts = [f"ActionResource(EssenceAttunement,-{self.cost},0)"]
        if getattr(self, "is_reused_spell", False):
            # A granted BG3 spell is something you may cast, not bound essence -
            # it costs learning budget only, and carries its own UnlockSpell.
            pass
        elif self.kind == "passive":
            parts.append(f"ActionResource(EssencePoint,-{self.cost},0)")
        else:
            parts.append(f"UnlockSpell({self.spell_name})")
        if self.boosts:
            parts.append(self.boosts)
        return ";".join(parts)


def P(path, tier, name, blurb, **kw):
    """A passive technique - binds essence permanently.

    `fields` on a passive are raw PassiveData fields, which is how the
    StatsFunctorContext / Conditions / StatsFunctors triple gets expressed for
    passives that react to something rather than just granting a boost.
    """
    return Ability(path, tier, name, blurb, kind="passive", **kw)


def A(path, tier, name, blurb, spell_type="Target", **kw):
    """An active technique - costs EssencePoint each use."""
    return Ability(path, tier, name, blurb, kind="active", spell_type=spell_type, **kw)


def all_abilities():
    return list(_REGISTRY)
