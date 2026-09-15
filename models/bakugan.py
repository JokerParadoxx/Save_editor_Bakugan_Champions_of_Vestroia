# Constantes de Facciones y Especies de Bakugan
FACTIONS = {
    0: "Pyrus (Fuego 🔥)",
    1: "Aquos (Agua 💧)",
    2: "Ventus (Viento 🍃)",
    3: "Haos (Luz ⚡)",
    4: "Darkus (Oscuridad 🌑)",
    5: "Aurelus (Oro ✨)"
}

FACTION_NAMES = ["Pyrus", "Aquos", "Ventus", "Haos", "Darkus", "Aurelus"]

BAKUGAN_SPECIES = [
    "Dragonoid", "Nillious", "Hydorous", "Trox", "Pegatrix", "Howlkor",
    "Cyndeous", "Fangzor", "Mantonoid", "Serpenteeze", "Skorporos", "Webam",
    "Hydranoid", "Maxotaur", "Gorthor", "Kraaken", "Zentaur", "Tretorous",
    "Pharol", "Auxillataur", "Gillator"
]


class BakuganData:
    """Modelo que representa un Bakugan individual"""

    def __init__(self, index, nickname="Bakugan", species_id=0, faction_id=0, level=1, b_power=500, evo_form=0):
        self.index = index
        self.nickname = nickname
        self.species_id = species_id % len(BAKUGAN_SPECIES)
        self.faction_id = faction_id % len(FACTIONS)
        self.level = max(1, min(100, level))
        self.b_power = max(100, min(9999, b_power))
        self.evo_form = evo_form

    @property
    def species_name(self):
        return BAKUGAN_SPECIES[self.species_id]

    @property
    def faction_name(self):
        return FACTIONS[self.faction_id]

    def __repr__(self):
        return f"<Bakugan #{self.index+1}: {self.nickname} ({self.species_name} - {self.faction_name}) Lvl {self.level} BP {self.b_power}>"
