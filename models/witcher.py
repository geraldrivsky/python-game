from dataclasses import replace

from models.character import Character


class Witcher(Character):
    """Geralt of Rivia. SRP: manages Witcher-specific state (oil, style, potions)."""

    _BASE_DAMAGE = 20
    _BASE_DODGE  = 0.20
    _BASE_CRIT   = 0.10

    def __init__(self) -> None:
        super().__init__(
            hp=100,
            damage=self._BASE_DAMAGE,
            dodge_chance=self._BASE_DODGE,
            critical_chance=self._BASE_CRIT,
            critical_multiplier=2.0,
        )
        self._dmg_mult  = 1.0
        self._dodge_bon = 0.0
        self._crit_bon  = 0.0

        self.current_oil: str | None = None
        self.current_style: str = "wolf"
        self.hits_per_round: int = 1
        self.potions_used: set[str] = set()

    @property
    def name(self) -> str:
        return "Геральт"

    # ── Style / oil / potion ─────────────────────────────────────

    def set_style(self, style: str) -> None:
        """style: 'wolf' | 'cat' | 'bear'"""
        self.current_style = style
        self._recalc()

    def apply_oil(self, oil_key: str) -> None:
        self.current_oil = oil_key

    def drink(self, potion_key: str) -> bool:
        """Returns False if already consumed."""
        if potion_key in self.potions_used:
            return False
        self.potions_used.add(potion_key)

        if potion_key == "swallow":
            self.stats = replace(self.stats, hp=self.stats.hp + 50)
        elif potion_key == "thunder":
            self._dmg_mult *= 1.30
            self._recalc()
        elif potion_key == "blizzard":
            self._dodge_bon += 0.20
            self._crit_bon  += 0.15
            self._recalc()
        elif potion_key == "bear":
            self.stats = replace(self.stats, damage_reduction=0.25)

        return True

    # ── Internal stat recalculation ──────────────────────────────

    def _recalc(self) -> None:
        dmg   = round(self._BASE_DAMAGE * self._dmg_mult)
        dodge = self._BASE_DODGE + self._dodge_bon
        crit  = self._BASE_CRIT  + self._crit_bon
        hits  = 1

        if self.current_style == "cat":
            dmg   = round(dmg * 0.65)
            dodge = min(0.90, dodge + 0.15)
            crit  = min(0.90, crit  + 0.05)
            hits  = 2
        elif self.current_style == "bear":
            dmg   = round(dmg * 1.45)
            dodge = max(0.0,  dodge - 0.15)

        self.stats = replace(self.stats, damage=dmg, dodge_chance=dodge, critical_chance=crit)
        self.hits_per_round = hits
