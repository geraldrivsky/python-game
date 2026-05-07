from models.character import Character
from models.monster_data import MonsterData


class Monster(Character):
    """A specific monster instance. SRP: narrative state + combat delegation."""

    def __init__(self, data: MonsterData) -> None:
        super().__init__(
            hp=data.hp,
            damage=data.damage,
            dodge_chance=data.dodge_chance,
            critical_chance=data.critical_chance,
            critical_multiplier=data.critical_multiplier,
        )
        self.data = data
        self.max_hp = data.hp
        self._action_idx = 0

    @property
    def name(self) -> str:
        return self.data.display_name

    def next_action(self) -> str:
        text = self.data.actions[self._action_idx % len(self.data.actions)]
        self._action_idx += 1
        return text

    def get_clue(self, round_num: int) -> str | None:
        if 1 <= round_num <= len(self.data.clues):
            return self.data.clues[round_num - 1]
        return None

    def get_geralt_thought(self, round_num: int, identified: bool) -> str | None:
        if identified:
            idx = (round_num - 4) % len(self.data.post_id_thoughts)
            return self.data.post_id_thoughts[idx]
        idx = min(round_num - 1, len(self.data.geralt_thoughts) - 1)
        return self.data.geralt_thoughts[idx]

    def hp_status(self) -> str:
        ratio = self.stats.hp / self.max_hp
        if ratio > 0.75:
            return "\033[92mПочти невредимо\033[0m"
        if ratio > 0.50:
            return "\033[93mРанено\033[0m"
        if ratio > 0.25:
            return "\033[91mТяжело ранено\033[0m"
        return "\033[91m\033[1mПри смерти\033[0m"
