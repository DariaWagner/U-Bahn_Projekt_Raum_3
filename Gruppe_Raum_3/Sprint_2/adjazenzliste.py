# Sprint_2/adjazenzliste.py
"""
Adjazenzliste für U-Bahn Linie U1 (Nürnberg)
Format: Station -> [{"vorher": ..., "nachher": ..., "linie": ..., "fahrtzeit": ..., "umsteigezeit": ...}]
Sprint 2: Bidirektionaler Verkehr mit variablen Haltezeiten (umsteigezeit)
"""

# ============================================================================
# KONSTANTEN
# ============================================================================

MAX_VERSUCHE = 3

# ============================================================================
# BETRIEBSZEITEN LINIE U1
# ============================================================================

UHRZEITEN_BETRIEB_LINIE_U1 = {
    "start": "05:00",
    "ende": "23:00",
    "intervall_minuten": 10
}

# ============================================================================
# ADJAZENZLISTE (nur Richtung: Langwasser Süd → Fürth Hbf)
# ============================================================================

STATIONEN_U1 = {
    "LANGWASSER SÜD": [{
        "vorher": None,
        "nachher": "GEMEINSCHAFTSHAUS",
        "linie": "U1",
        "fahrtzeit": 3,
        "umsteigezeit": 60  # Endhaltestelle
    }],
    "GEMEINSCHAFTSHAUS": [{
        "vorher": "LANGWASSER SÜD",
        "nachher": "LANGWASSER MITTE",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "LANGWASSER MITTE": [{
        "vorher": "GEMEINSCHAFTSHAUS",
        "nachher": "SCHARFREITERING",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "SCHARFREITERING": [{
        "vorher": "LANGWASSER MITTE",
        "nachher": "LANGWASSER NORD",
        "linie": "U1",
        "fahrtzeit": 3,
        "umsteigezeit": 30
    }],
    "LANGWASSER NORD": [{
        "vorher": "SCHARFREITERING",
        "nachher": "MESSE",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "MESSE": [{
        "vorher": "LANGWASSER NORD",
        "nachher": "BAUERNFEINDSTRASSE",
        "linie": "U1",
        "fahrtzeit": 3,
        "umsteigezeit": 30
    }],
    "BAUERNFEINDSTRASSE": [{
        "vorher": "MESSE",
        "nachher": "HASENBUCK",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "HASENBUCK": [{
        "vorher": "BAUERNFEINDSTRASSE",
        "nachher": "FRANKENSTRASSE",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "FRANKENSTRASSE": [{
        "vorher": "HASENBUCK",
        "nachher": "MAFFEIPLATZ",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "MAFFEIPLATZ": [{
        "vorher": "FRANKENSTRASSE",
        "nachher": "AUFSESSPLATZ",
        "linie": "U1",
        "fahrtzeit": 1,
        "umsteigezeit": 30
    }],
    "AUFSESSPLATZ": [{
        "vorher": "MAFFEIPLATZ",
        "nachher": "HAUPTBAHNHOF",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "HAUPTBAHNHOF": [{
        "vorher": "AUFSESSPLATZ",
        "nachher": "LORENZKIRCHE",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 60  # Hauptknoten
    }],
    "LORENZKIRCHE": [{
        "vorher": "HAUPTBAHNHOF",
        "nachher": "WEISSER TURM",
        "linie": "U1",
        "fahrtzeit": 3,
        "umsteigezeit": 30
    }],
    "WEISSER TURM": [{
        "vorher": "LORENZKIRCHE",
        "nachher": "PLÄRRER",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "PLÄRRER": [{
        "vorher": "WEISSER TURM",
        "nachher": "GOSTENHOF",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 60  # Hauptknoten
    }],
    "GOSTENHOF": [{
        "vorher": "PLÄRRER",
        "nachher": "BÄRENSCHANZE",
        "linie": "U1",
        "fahrtzeit": 1,
        "umsteigezeit": 30
    }],
    "BÄRENSCHANZE": [{
        "vorher": "GOSTENHOF",
        "nachher": "MAXIMILIANSTRASSE",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "MAXIMILIANSTRASSE": [{
        "vorher": "BÄRENSCHANZE",
        "nachher": "EBERHARDSHOF",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "EBERHARDSHOF": [{
        "vorher": "MAXIMILIANSTRASSE",
        "nachher": "MUGGENHOF",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "MUGGENHOF": [{
        "vorher": "EBERHARDSHOF",
        "nachher": "STADTGRENZE",
        "linie": "U1",
        "fahrtzeit": 3,
        "umsteigezeit": 30
    }],
    "STADTGRENZE": [{
        "vorher": "MUGGENHOF",
        "nachher": "JAKOBINENSTRASSE",
        "linie": "U1",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    "JAKOBINENSTRASSE": [{
        "vorher": "STADTGRENZE",
        "nachher": "FÜRTH HBF",
        "linie": "U1",
        "fahrtzeit": 3,
        "umsteigezeit": 30
    }],
    "FÜRTH HBF": [{
        "vorher": "JAKOBINENSTRASSE",
        "nachher": None,
        "linie": "U1",
        "fahrtzeit": None,
        "umsteigezeit": 60  # Endhaltestelle
    }]
}

# ============================================================================
# HILFSLISTEN (für Kompatibilität)
# ============================================================================

# Reihenfolge der Stationen
STATIONEN_REIHENFOLGE = list(STATIONEN_U1.keys())

# Fahrtzeiten als Liste (für Sprint 2 Kompatibilität)
FAHRTZEITEN = [
    station[0]["fahrtzeit"] for station in STATIONEN_U1.values() if station[0]["fahrtzeit"]
]

# Haltezeiten in Sekunden (umsteigezeit)
HALTEZEITEN = {
    station_name: station[0]["umsteigezeit"]
    for station_name, station in STATIONEN_U1.items()
}

# Endhaltestellen
ENDHALTESTELLEN = {"LANGWASSER SÜD", "FÜRTH HBF"}
