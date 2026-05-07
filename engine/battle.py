from typing import Optional

from engine.interfaces import ICombatant, IIdentifiable
from engine.turn_result import TurnResult
from models.witcher import Witcher
from models.monster import Monster


class BattleEngine:
    """Manages turn sequencing and victory conditions. SRP: pure battle logic, no UI."""

    def __init__(self, witcher: Witcher, monster: Monster) -> None:
        self._witcher = witcher
        self._monster = monster
        self.round_num = 0
        self.identified = False
        self.is_over = False
        self.winner: Optional[str] = None

    # ── Public interface ─────────────────────────────────────────

    def attack(self) -> TurnResult:
        """Full combat round: Geralt attacks, monster responds."""
        self.round_num += 1
        w, m = self._witcher, self._monster

        hits: list[dict] = []
        used_oil_bonus = False

        for _ in range(w.hits_per_round):
            raw_dmg = w.attack()

            oil_bonus = False
            if w.current_oil and w.current_oil == m.data.oil_weakness:
                raw_dmg = round(raw_dmg * m.data.oil_multiplier)
                oil_bonus = True
                used_oil_bonus = True

            result = m.defense(raw_dmg)
            crit = (
                raw_dmg > round(w.stats.damage * m.data.oil_multiplier * 0.9)
                if oil_bonus
                else raw_dmg > w.stats.damage
            )
            hits.append({"damage": result["damage"], "dodged": result["damage"] == 0, "crit": crit})

            if m.stats.hp <= 0:
                break

        monster_result = {"damage": 0, "is_dead": False}
        monster_action = m.next_action()
        if m.stats.hp > 0:
            monster_result = w.defense(m.attack())

        return self._build_result(
            hits=hits,
            monster_action=monster_action,
            monster_damage=monster_result["damage"],
            witcher_dodged=monster_result["damage"] == 0,
            used_oil_bonus=used_oil_bonus,
        )

    def prepare_oil(self, oil_key: str) -> TurnResult:
        """Apply oil. Monster attacks while Geralt prepares."""
        self._witcher.apply_oil(oil_key)
        return self._monster_turn()

    def prepare_potion(self, potion_key: str) -> TurnResult:
        """Drink potion. Monster attacks while Geralt prepares."""
        self._witcher.drink(potion_key)
        return self._monster_turn()

    def prepare_style(self, style: str) -> TurnResult:
        """Switch style (or stall). Monster attacks while Geralt prepares."""
        self._witcher.set_style(style)
        return self._monster_turn()

    # ── Internal ─────────────────────────────────────────────────

    def _monster_turn(self) -> TurnResult:
        self.round_num += 1
        m, w = self._monster, self._witcher
        monster_action = m.next_action()
        result = w.defense(m.attack())
        return self._build_result(
            hits=[],
            monster_action=monster_action,
            monster_damage=result["damage"],
            witcher_dodged=result["damage"] == 0,
            used_oil_bonus=False,
        )

    def _build_result(
        self,
        hits: list,
        monster_action: str,
        monster_damage: int,
        witcher_dodged: bool,
        used_oil_bonus: bool,
    ) -> TurnResult:
        w, m = self._witcher, self._monster
        rn = self.round_num

        clue = m.get_clue(rn) if not self.identified else None
        is_id = False
        id_text: Optional[str] = None
        id_name: Optional[str] = None
        oil_tip: Optional[str] = None

        if rn >= 4 and not self.identified:
            self.identified = True
            is_id = True
            id_text = m.data.identified_text
            id_name = m.data.display_name
            oil_tip = m.data.oil_tip
            clue = m.get_clue(4)

        thought = m.get_geralt_thought(rn, self.identified)

        if w.stats.hp <= 0:
            self.is_over = True
            self.winner = "monster"
        elif m.stats.hp <= 0:
            self.is_over = True
            self.winner = "witcher"

        return TurnResult(
            round_num=rn,
            witcher_hits=hits,
            monster_action=monster_action,
            monster_damage=monster_damage,
            witcher_dodged=witcher_dodged,
            clue=clue,
            is_identification=is_id,
            identified_text=id_text,
            identified_name=id_name,
            oil_tip=oil_tip,
            geralt_thought=thought,
            witcher_hp=w.stats.hp,
            monster_hp=m.stats.hp,
            monster_hp_status=m.hp_status(),
            is_over=self.is_over,
            winner=self.winner,
            used_oil_bonus=used_oil_bonus,
        )
