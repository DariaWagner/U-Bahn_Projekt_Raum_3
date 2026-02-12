# Sprint_2/adjazenzliste.py

MAX_VERSUCHE = 3

# Betriebszeiten Linie U1
UHRZEITEN_BETRIEB_LINIE_U1 = {
    "start": "05:00",
    "ende": "23:00",
    "intervall_minuten": 10
}

# Reihenfolge der Stationen (Hinrichtung: Langwasser Süd → Fürth Hbf)
STATIONEN_REIHENFOLGE = [
    "LANGWASSER SÜD",
    "GEMEINSCHAFTSHAUS",
    "LANGWASSER MITTE",
    "SCHARFREITERING",
    "LANGWASSER NORD",
    "MESSE",
    "BAUERNFEINDSTRASSE",
    "HASENBUCK",
    "FRANKENSTRASSE",
    "MAFFEIPLATZ",
    "AUFSESSPLATZ",
    "HAUPTBAHNHOF",
    "LORENZKIRCHE",
    "WEISSER TURM",
    "PLÄRRER",
    "GOSTENHOF",
    "BÄRENSCHANZE",
    "MAXIMILIANSTRASSE",
    "EBERHARDSHOF",
    "MUGGENHOF",
    "STADTGRENZE",
    "JAKOBINENSTRASSE",
    "FÜRTH HBF"
]

# Fahrtzeiten in Minuten zwischen aufeinanderfolgenden Stationen (Hinrichtung)
# Index i = Fahrtzeit von Station i zu Station i+1
FAHRTZEITEN = [
    3,  # LANGWASSER SÜD     → GEMEINSCHAFTSHAUS
    2,  # GEMEINSCHAFTSHAUS  → LANGWASSER MITTE
    2,  # LANGWASSER MITTE   → SCHARFREITERING
    3,  # SCHARFREITERING    → LANGWASSER NORD
    2,  # LANGWASSER NORD    → MESSE
    3,  # MESSE              → BAUERNFEINDSTRASSE
    2,  # BAUERNFEINDSTRASSE → HASENBUCK
    2,  # HASENBUCK          → FRANKENSTRASSE
    2,  # FRANKENSTRASSE     → MAFFEIPLATZ
    1,  # MAFFEIPLATZ        → AUFSESSPLATZ
    2,  # AUFSESSPLATZ       → HAUPTBAHNHOF
    2,  # HAUPTBAHNHOF       → LORENZKIRCHE
    3,  # LORENZKIRCHE       → WEISSER TURM
    2,  # WEISSER TURM       → PLÄRRER
    2,  # PLÄRRER            → GOSTENHOF
    1,  # GOSTENHOF          → BÄRENSCHANZE
    2,  # BÄRENSCHANZE       → MAXIMILIANSTRASSE
    2,  # MAXIMILIANSTRASSE  → EBERHARDSHOF
    2,  # EBERHARDSHOF       → MUGGENHOF
    3,  # MUGGENHOF          → STADTGRENZE
    2,  # STADTGRENZE        → JAKOBINENSTRASSE
    3,  # JAKOBINENSTRASSE   → FÜRTH HBF
]

# Haltezeiten in Sekunden pro Station
# Standard: 30s | Hauptknoten (Hauptbahnhof, Plärrer): 60s | Endhaltestellen: 60s
HALTEZEITEN = {
    "LANGWASSER SÜD":     60,
    "GEMEINSCHAFTSHAUS":  30,
    "LANGWASSER MITTE":   30,
    "SCHARFREITERING":    30,
    "LANGWASSER NORD":    30,
    "MESSE":              30,
    "BAUERNFEINDSTRASSE": 30,
    "HASENBUCK":          30,
    "FRANKENSTRASSE":     30,
    "MAFFEIPLATZ":        30,
    "AUFSESSPLATZ":       30,
    "HAUPTBAHNHOF":       60,
    "LORENZKIRCHE":       30,
    "WEISSER TURM":       30,
    "PLÄRRER":            60,
    "GOSTENHOF":          30,
    "BÄRENSCHANZE":       30,
    "MAXIMILIANSTRASSE":  30,
    "EBERHARDSHOF":       30,
    "MUGGENHOF":          30,
    "STADTGRENZE":        30,
    "JAKOBINENSTRASSE":   30,
    "FÜRTH HBF":          60,
}

# Endhaltestellen - Züge starten hier ohne zusätzliche Haltezeit
ENDHALTESTELLEN = {"LANGWASSER SÜD", "FÜRTH HBF"}