from time import sleep

from scripts.printing_text import text_parts, slow_print, dramatic_pause, paragraph_pause
from ui.constants import W


def show_intro() -> None:
    """Display the opening narrative. SRP: intro presentation only."""
    _DRAMATIC_INDICES = {12, 16, 21, 30, 32, 40, 46, 48, 51}

    print("═" * W)
    print("  ПОТЕРЯННЫЙ СОЛДАТИК")
    print("═" * W)

    skip = input("\n  Вступление: [Enter] читать  |  [s] пропустить: ").strip().lower() == "s"
    if skip:
        return

    is_slow = False
    for i, part in enumerate(text_parts):
        if part == " ":
            is_slow = not is_slow
            continue
        if part == "":
            paragraph_pause()
            continue
        if i in _DRAMATIC_INDICES:
            dramatic_pause()
        slow_print(part, delay=0.075 if is_slow else 0.039)
        if part and i < len(text_parts) - 1 and text_parts[i + 1] != "":
            sleep(0.2)

    sleep(1.5)
