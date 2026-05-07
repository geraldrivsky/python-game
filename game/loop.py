import random
from time import sleep

from engine.battle import BattleEngine
from models.witcher import Witcher
from models.monster import Monster
from models.monster_data import MONSTERS
from models.oils import OILS
from ui.constants import W, POTION_META, STYLE_DESCRIPTIONS
from ui.display import print_status, print_result, print_ending, line
from ui.input import ask, oil_menu, potion_menu, style_menu
from ui.intro import show_intro


class GameLoop:
    """Orchestrates the full game session. SRP: coordinates subsystems, owns no domain logic."""

    def run(self) -> None:
        show_intro()
        witcher, monster, engine = self._init_game()
        self._game_loop(witcher, monster, engine)
        self._show_ending(witcher, monster, engine)

    # ── Initialisation ────────────────────────────────────────────

    def _init_game(self) -> tuple[Witcher, Monster, BattleEngine]:
        print()
        line()
        print("  Всё, что вы можете сделать сейчас — отомстить.")
        print("  Геральт не знает, что это за тварь. Нужно разобраться в бою.")
        line()
        witcher = Witcher()
        monster = Monster(random.choice(list(MONSTERS.values())))
        engine  = BattleEngine(witcher, monster)
        return witcher, monster, engine

    # ── Main loop ─────────────────────────────────────────────────

    def _game_loop(self, witcher: Witcher, monster: Monster, engine: BattleEngine) -> None:
        while not engine.is_over:
            print(f"\n{'═'*W}")
            print(f"  Раунд {engine.round_num + 1}")
            print_status(witcher, monster, engine.round_num)

            print("  Действие Геральта:")
            print("    1. Атаковать")
            print("    2. Нанести масло на меч")
            print("    3. Выпить зелье")
            print("    4. Сменить стиль боя")

            result = self._dispatch(ask(">", ("1", "2", "3", "4")), witcher, engine)
            print()
            print_result(result)
            sleep(0.3)

    def _dispatch(self, choice: str, witcher: Witcher, engine: BattleEngine):
        if choice == "1":
            return engine.attack()

        if choice == "2":
            oil_key = oil_menu(witcher)
            if oil_key:
                print(f"\n  Геральт наносит {OILS[oil_key].name} на серебряный меч.")
                return engine.prepare_oil(oil_key)

        elif choice == "3":
            pot_key = potion_menu(witcher)
            if pot_key:
                print(f"\n  Геральт выпивает {POTION_META[pot_key][0]}.")
                return engine.prepare_potion(pot_key)

        elif choice == "4":
            new_style = style_menu(witcher)
            if new_style:
                name = next(n for k, n, _ in STYLE_DESCRIPTIONS if k == new_style)
                print(f"\n  Геральт переходит в {name}.")
                return engine.prepare_style(new_style)

        print("  Геральт медлит.")
        return engine.prepare_style(witcher.current_style)

    # ── Ending ────────────────────────────────────────────────────

    def _show_ending(self, witcher: Witcher, monster: Monster, engine: BattleEngine) -> None:
        print_ending(
            winner=engine.winner or "monster",
            monster=monster,
            identified=engine.identified,
            used_correct_oil=witcher.current_oil == monster.data.oil_weakness,
        )
