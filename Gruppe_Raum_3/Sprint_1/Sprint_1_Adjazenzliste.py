# Bereit zum Dienst, Meisterin.

# Adjazenzliste (nur Richtung A -> B -> C -> D)
STATIONEN = {
    "A": [{"vorher": None, "nachher": "B", "linie": None, "fahrtzeit": 2, "umsteigezeit": None}],
    "B": [{"vorher": "A", "nachher": "C", "linie": None, "fahrtzeit": 3, "umsteigezeit": None}],
    "C": [{"vorher": "B", "nachher": "D", "linie": None, "fahrtzeit": 1, "umsteigezeit": None}],
    "D": [{"vorher": "C", "nachher": None, "linie": None, "fahrtzeit": None, "umsteigezeit": None}],
}

# Betriebszeiten und Takt
UHRZEITEN_BETRIEB_LINIE_TEST = {
    "start": "05:00",
    "ende": "23:00",
    "intervall_minuten": 10
}

# Max. Versuche bei falscher Eingabe
MAX_VERSUCHE = 3
