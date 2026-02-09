# Sprint_2/adjazenzliste.py

MAX_VERSUCHE = 3

# Betriebszeiten Linie U1
UHRZEITEN_BETRIEB_LINIE_U1 = {
    "start": "05:00",
    "ende": "23:00",
    "intervall_minuten": 10
}

# Reihenfolge der Stationen (Hinrichtung)
# Langwasser Süd → Fürth Hbf
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
'''
 Adjazenzliste mit:
 - Fahrtzeit (in Minuten)
 - Haltezeit (in Sekunden)

 Haltezeiten:
 Standard: 30 Sekunden
 Hauptknoten: Hauptbahnhof, Plärrer → 60 Sekunden
 Endhaltestellen: Langwasser Süd, Fürth Hbf → 60 Sekunden

 BIDIREKTIONALE Adjazenzliste - jede Station hat Verbindungen in beide Richtungen
'''
STATIONEN_U1 = {
    "LANGWASSER SÜD": [
        {"nachher": "GEMEINSCHAFTSHAUS", "fahrtzeit": 3, "haltezeit": 60}
    ],

    "GEMEINSCHAFTSHAUS": [
        {"nachher": "LANGWASSER SÜD", "fahrtzeit": 3, "haltezeit": 30},
        {"nachher": "LANGWASSER MITTE", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "LANGWASSER MITTE": [
        {"nachher": "GEMEINSCHAFTSHAUS", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "SCHARFREITERING", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "SCHARFREITERING": [
        {"nachher": "LANGWASSER MITTE", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "LANGWASSER NORD", "fahrtzeit": 3, "haltezeit": 30}
    ],

    "LANGWASSER NORD": [
        {"nachher": "SCHARFREITERING", "fahrtzeit": 3, "haltezeit": 30},
        {"nachher": "MESSE", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "MESSE": [
        {"nachher": "LANGWASSER NORD", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "BAUERNFEINDSTRASSE", "fahrtzeit": 3, "haltezeit": 30}
    ],

    "BAUERNFEINDSTRASSE": [
        {"nachher": "MESSE", "fahrtzeit": 3, "haltezeit": 30},
        {"nachher": "HASENBUCK", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "HASENBUCK": [
        {"nachher": "BAUERNFEINDSTRASSE", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "FRANKENSTRASSE", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "FRANKENSTRASSE": [
        {"nachher": "HASENBUCK", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "MAFFEIPLATZ", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "MAFFEIPLATZ": [
        {"nachher": "FRANKENSTRASSE", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "AUFSESSPLATZ", "fahrtzeit": 1, "haltezeit": 30}
    ],

    "AUFSESSPLATZ": [
        {"nachher": "MAFFEIPLATZ", "fahrtzeit": 1, "haltezeit": 30},
        {"nachher": "HAUPTBAHNHOF", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "HAUPTBAHNHOF": [
        {"nachher": "AUFSESSPLATZ", "fahrtzeit": 2, "haltezeit": 60},
        {"nachher": "LORENZKIRCHE", "fahrtzeit": 2, "haltezeit": 60}
    ],

    "LORENZKIRCHE": [
        {"nachher": "HAUPTBAHNHOF", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "WEISSER TURM", "fahrtzeit": 3, "haltezeit": 30}
    ],

    "WEISSER TURM": [
        {"nachher": "LORENZKIRCHE", "fahrtzeit": 3, "haltezeit": 30},
        {"nachher": "PLÄRRER", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "PLÄRRER": [
        {"nachher": "WEISSER TURM", "fahrtzeit": 2, "haltezeit": 60},
        {"nachher": "GOSTENHOF", "fahrtzeit": 2, "haltezeit": 60}
    ],

    "GOSTENHOF": [
        {"nachher": "PLÄRRER", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "BÄRENSCHANZE", "fahrtzeit": 1, "haltezeit": 30}
    ],

    "BÄRENSCHANZE": [
        {"nachher": "GOSTENHOF", "fahrtzeit": 1, "haltezeit": 30},
        {"nachher": "MAXIMILIANSTRASSE", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "MAXIMILIANSTRASSE": [
        {"nachher": "BÄRENSCHANZE", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "EBERHARDSHOF", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "EBERHARDSHOF": [
        {"nachher": "MAXIMILIANSTRASSE", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "MUGGENHOF", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "MUGGENHOF": [
        {"nachher": "EBERHARDSHOF", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "STADTGRENZE", "fahrtzeit": 3, "haltezeit": 30}
    ],

    "STADTGRENZE": [
        {"nachher": "MUGGENHOF", "fahrtzeit": 3, "haltezeit": 30},
        {"nachher": "JAKOBINENSTRASSE", "fahrtzeit": 2, "haltezeit": 30}
    ],

    "JAKOBINENSTRASSE": [
        {"nachher": "STADTGRENZE", "fahrtzeit": 2, "haltezeit": 30},
        {"nachher": "FÜRTH HBF", "fahrtzeit": 3, "haltezeit": 30}
    ],

    "FÜRTH HBF": [
        {"nachher": "JAKOBINENSTRASSE", "fahrtzeit": 3, "haltezeit": 60}
    ]
}