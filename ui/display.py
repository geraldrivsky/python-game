from time import sleep

from engine.turn_result import TurnResult
from models.witcher import Witcher
from models.monster import Monster
from models.oils import OILS
from ui.constants import W, STYLE_NAMES, POTION_META


def line(ch: str = "═") -> None:
    print(ch * W)


def sep(ch: str = "─") -> None:
    print(ch * W)


def hp_bar(current: int, maximum: int = 100, width: int = 22) -> str:
    current = max(0, current)
    filled  = round(current / maximum * width)
    ratio   = current / maximum
    col     = "\033[92m" if ratio > 0.5 else "\033[93m" if ratio > 0.25 else "\033[91m"
    bar     = "█" * filled + "░" * (width - filled)
    return f"{col}[{bar}]\033[0m"


def print_status(witcher: Witcher, monster: Monster, round_num: int) -> None:
    sep()
    print(f"  Геральт  {hp_bar(witcher.stats.hp)} {witcher.stats.hp}/100 HP")
    print(f"  Тварь    {monster.hp_status()}")
    sep()
    oil_label = OILS[witcher.current_oil].name if witcher.current_oil else "не нанесено"
    avail     = [POTION_META[k][0] for k in POTION_META if k not in witcher.potions_used]
    print(f"  Стиль:   {STYLE_NAMES[witcher.current_style]}")
    print(f"  Масло:   {oil_label}")
    print(f"  Зелья:   {', '.join(avail) if avail else 'все выпиты'}")
    sep()


def print_result(r: TurnResult) -> None:
    # Monster action flavour text
    print(f"\n  \033[2m{r.monster_action}\033[0m\n")

    # Clue box
    if r.clue:
        _print_clue_box(r.clue)

    # Identification reveal
    if r.is_identification:
        print(f"  \033[96m{'!'*3} ИДЕНТИФИКАЦИЯ: {r.identified_name}\033[0m")
        sep()
        for sent in (r.identified_text or "").split(". "):
            if sent.strip():
                print(f"  {sent.strip()}.")
        if r.oil_tip:
            print(f"\n  \033[93m► {r.oil_tip}\033[0m")
        sep()
        print()

    # Geralt's inner monologue
    if r.geralt_thought:
        print(f"  \033[90m«{r.geralt_thought}»\033[0m\n")

    # Geralt's hits
    if r.witcher_hits:
        for i, h in enumerate(r.witcher_hits, 1):
            prefix = f"  [Удар {i}] " if len(r.witcher_hits) > 1 else "  "
            if h["dodged"]:
                print(f"{prefix}Геральт замахивается — тварь уклоняется.")
            else:
                crit  = " \033[93m[КРИТ!]\033[0m" if h["crit"] else ""
                bonus = " \033[96m[МАСЛО]\033[0m" if r.used_oil_bonus else ""
                print(f"{prefix}Геральт наносит \033[93m{h['damage']}\033[0m урона.{crit}{bonus}")
    else:
        print("  Геральт готовится, не атакуя в этот ход.")

    # Monster's counter
    sleep(0.25)
    if r.witcher_dodged:
        print("  Тварь бросается — Геральт уклоняется!")
    else:
        print(f"  Тварь наносит \033[91m{r.monster_damage}\033[0m урона.")


def print_ending(winner: str, monster: Monster, identified: bool, used_correct_oil: bool) -> None:
    print()
    line()
    if winner == "witcher":
        if identified and used_correct_oil:
            print(f"  \033[92mПОБЕДА.\033[0m Геральт медленно опустил меч.")
            print(f"  {monster.data.display_name} — {monster.data.category.value}.")
            print( "  Правильное масло. Правильная тактика.")
            print( "  Знание — половина победы ведьмака.")
        elif used_correct_oil:
            print( "  \033[92mПОБЕДА.\033[0m Геральт выжил.")
            print( "  Правильное масло сработало — хотя он и не знал почему.")
        else:
            print( "  \033[92mПОБЕДА.\033[0m Но какой ценой.")
            print(f"  Это был {monster.data.display_name} [{monster.data.category.value}].")
            print(f"  {monster.data.oil_tip}")
            print( "  В следующий раз — разобраться раньше.")
    else:
        print( "  \033[91mСМЕРТЬ.\033[0m Геральт пал.")
        if not identified:
            print( "  Он так и не узнал, что убило его.")
            print(f"  Это был {monster.data.display_name} [{monster.data.category.value}].")
            print(f"  {monster.data.oil_tip}")
        print( "  Монстр растворился в темноте леса.")
    line()


# ── Internal helpers ─────────────────────────────────────────────

def _print_clue_box(text: str) -> None:
    print(f"  ┌{'─'*(W-4)}┐")
    words = text.split()
    line_buf: list[str] = []
    lines: list[str] = []
    for w in words:
        if len(" ".join(line_buf + [w])) > W - 8:
            lines.append(" ".join(line_buf))
            line_buf = [w]
        else:
            line_buf.append(w)
    if line_buf:
        lines.append(" ".join(line_buf))
    for ln in lines:
        print(f"  │ \033[93m{ln:<{W-6}}\033[0m │")
    print(f"  └{'─'*(W-4)}┘\n")
