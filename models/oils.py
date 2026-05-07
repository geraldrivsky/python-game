from dataclasses import dataclass
from enum import Enum


class OilType(Enum):
    NECROPHAGE = "necrophage"
    RELICT     = "relict"
    INSECTOID  = "insectoid"
    CURSED     = "cursed"


@dataclass(frozen=True)
class Oil:
    type: OilType
    name: str
    targets: str
    lore: str


OILS: dict[str, Oil] = {
    "necrophage": Oil(
        OilType.NECROPHAGE,
        "Масло некрофагов",
        "Трупоеды: гули, альгули, утопцы, гнильцы",
        "Настоянное на чемерице и вороньем глазе. Разъедает хитиновые пластины трупоедов.",
    ),
    "relict": Oil(
        OilType.RELICT,
        "Реликтовое масло",
        "Реликты: леший, сильваны, зерриканские лошадки",
        "Основа — смола серебристого тиса. Проникает сквозь кору-кожу древних духов.",
    ),
    "insectoid": Oil(
        OilType.INSECTOID,
        "Масло насекомоидных",
        "Насекомоидные: кикиморы, арахноморфы, эндреги",
        "Едкий состав на основе кислоты болотника. Растворяет хитин насекомоидных.",
    ),
    "cursed": Oil(
        OilType.CURSED,
        "Масло проклятых",
        "Проклятые существа: оборотни, плакальщицы, нагльфары",
        "Замешано на лунном серебре. Жжёт тех, чей облик искажён проклятием.",
    ),
}
