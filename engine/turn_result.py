from dataclasses import dataclass
from typing import Optional


@dataclass
class TurnResult:
    round_num: int
    witcher_hits: list[dict]
    monster_action: str
    monster_damage: int
    witcher_dodged: bool
    clue: Optional[str]
    is_identification: bool
    identified_text: Optional[str]
    identified_name: Optional[str]
    oil_tip: Optional[str]
    geralt_thought: Optional[str]
    witcher_hp: int
    monster_hp: int
    monster_hp_status: str
    is_over: bool
    winner: Optional[str]       # "witcher" | "monster"
    used_oil_bonus: bool
