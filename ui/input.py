from models.witcher import Witcher
from models.oils import OILS
from ui.constants import POTION_META, STYLE_DESCRIPTIONS


def ask(prompt: str, valid: tuple | list) -> str:
    while True:
        v = input(f"\n  {prompt} ").strip()
        if v in valid:
            return v
        print(f"  Введите одно из: {', '.join(str(x) for x in valid)}")


def oil_menu(witcher: Witcher) -> str | None:
    """Show oil selection. Returns chosen oil key or None if cancelled."""
    print()
    for i, (key, oil) in enumerate(OILS.items(), 1):
        active = " ◄ активно" if witcher.current_oil == key else ""
        print(f"    {i}. {oil.name}{active}")
        print(f"       \033[2m{oil.targets}\033[0m")
        print(f"       \033[2m{oil.lore}\033[0m")
    print(f"    {len(OILS)+1}. Отмена")

    choice = ask(">", [str(i) for i in range(1, len(OILS) + 2)])
    if int(choice) > len(OILS):
        return None
    return list(OILS.keys())[int(choice) - 1]


def potion_menu(witcher: Witcher) -> str | None:
    """Show potion selection. Returns chosen potion key or None if cancelled/empty."""
    avail = [(k, *POTION_META[k]) for k in POTION_META if k not in witcher.potions_used]
    if not avail:
        print("  Зелий не осталось.")
        return None

    print()
    for i, (key, name, desc) in enumerate(avail, 1):
        print(f"    {i}. {name} — {desc}")
    print(f"    {len(avail)+1}. Отмена")

    choice = ask(">", [str(i) for i in range(1, len(avail) + 2)])
    if int(choice) > len(avail):
        return None
    return avail[int(choice) - 1][0]


def style_menu(witcher: Witcher) -> str | None:
    """Show style selection. Returns chosen style key or None if cancelled."""
    print()
    for i, (key, name, desc) in enumerate(STYLE_DESCRIPTIONS, 1):
        active = " ◄ текущий" if witcher.current_style == key else ""
        print(f"    {i}. {name}{active}")
        print(f"       \033[2m{desc}\033[0m")
    print(f"    4. Отмена")

    choice = ask(">", ("1", "2", "3", "4"))
    if choice == "4":
        return None
    return STYLE_DESCRIPTIONS[int(choice) - 1][0]
