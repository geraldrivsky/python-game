from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from random import random


@dataclass
class CharacterStats:
    hp: int
    damage: int
    dodge_chance: float
    critical_chance: float
    critical_multiplier: float
    damage_reduction: float = 0.0


class Character(ABC):
    """Abstract base for all combat participants. SRP: pure combat mechanics only."""

    def __init__(
        self,
        hp: int,
        damage: int,
        dodge_chance: float,
        critical_chance: float,
        critical_multiplier: float,
    ) -> None:
        self.stats = CharacterStats(
            hp=hp,
            damage=damage,
            dodge_chance=dodge_chance,
            critical_chance=critical_chance,
            critical_multiplier=critical_multiplier,
        )

    @property
    @abstractmethod
    def name(self) -> str: ...

    def attack(self) -> int:
        s = self.stats
        mult = s.critical_multiplier if random() < s.critical_chance else 1
        return round(s.damage * mult)

    def defense(self, damage: int) -> dict:
        s = self.stats
        if random() < s.dodge_chance:
            return {"damage": 0, "is_dead": False}
        effective = max(1, round(damage * (1.0 - s.damage_reduction)))
        new_hp = max(0, s.hp - effective)
        self.stats = replace(s, hp=new_hp)
        return {"damage": effective, "is_dead": new_hp == 0}
