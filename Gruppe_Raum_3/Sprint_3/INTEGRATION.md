# Integration mit Kollegen-Modulen

## Übersicht

Dieses Projekt ist modular aufgebaut und kann mit verschiedenen U-Bahn Adjazenzlisten arbeiten.

## Kollegen-Module (NICHT ÄNDERN!)

### 1. `ticket.py` (von Kollegen)

Enthält die Preisberechnung mit Enums:

- `TicketKategorie` (KURZ, MITTEL, LANG)
- `TicketArt` (EINZEL, MEHRFAHRT)
- `Zahlart` (BAR, BARGELDLOS)
- `Ticketpreis` - Hauptklasse für Preisberechnung
- `erstelle_ticket()` - Factory-Funktion

**Verwendung in Sprint 3:**

- `classe.py` importiert `ticket.py`
- Adapter-Klassen `PreisBerechnung` und `TarifRechner`
- Fallback auf Original-Implementation wenn `ticket.py` nicht vorhanden

### 2. `console_ui_extern.py` (von Kollegen)

Enthält UI-Funktionen:

- `ask_yes_no()` - Ja/Nein Fragen
- `ask_amount()` - Geldbetrag abfragen
- `choose_start_station()` - Startstation wählen
- `choose_destination_station()` - Zielstation wählen

**Hinweis:** Aktuell wird die interne `ConsoleUI` Klasse verwendet.

## Adjazenzliste-Format

### Standard-Format (Sprint 1 kompatibel)

```python
STATIONEN_U1 = {
    "STATION_NAME": [{
        "vorher": "VORHERIGE_STATION",  # oder None
        "nachher": "NÄCHSTE_STATION",   # oder None
        "linie": "U1",                  # Linien-ID
        "fahrtzeit": 3,                 # Minuten (oder None)
        "umsteigezeit": 30              # Sekunden
    }]
}
```

### Beispiel: U1 (Nürnberg)

```python
"LANGWASSER SÜD": [{
    "vorher": None,
    "nachher": "GEMEINSCHAFTSHAUS",
    "linie": "U1",
    "fahrtzeit": 3,
    "umsteigezeit": 60  # Endhaltestelle
}],
"HAUPTBAHNHOF": [{
    "vorher": "AUFSESSPLATZ",
    "nachher": "LORENZKIRCHE",
    "linie": "U1",
    "fahrtzeit": 2,
    "umsteigezeit": 60  # Hauptknoten
}]
```

## Neue U-Bahn Linie hinzufügen

### Schritt 1: Erstelle neue `adjazenzliste_UX.py`

```python
# adjazenzliste_u2.py

MAX_VERSUCHE = 3

UHRZEITEN_BETRIEB_LINIE_U2 = {
    "start": "05:00",
    "ende": "23:30",
    "intervall_minuten": 8
}

STATIONEN_U2 = {
    "RÖTHENBACH": [{
        "vorher": None,
        "nachher": "HOHE MARTER",
        "linie": "U2",
        "fahrtzeit": 3,
        "umsteigezeit": 60
    }],
    "HOHE MARTER": [{
        "vorher": "RÖTHENBACH",
        "nachher": "ZIEGELSTEIN",
        "linie": "U2",
        "fahrtzeit": 2,
        "umsteigezeit": 30
    }],
    # ... weitere Stationen
}

STATIONEN_REIHENFOLGE = list(STATIONEN_U2.keys())

HALTEZEITEN = {
    station_name: station[0]["umsteigezeit"]
    for station_name, station in STATIONEN_U2.items()
}

ENDHALTESTELLEN = {"RÖTHENBACH", "FLUGHAFEN"}
```

### Schritt 2: Passe `service.py` an

```python
# Ändere Imports
from adjazenzliste_u2 import (
    STATIONEN_U2 as STATIONEN_U1,  # Alias!
    STATIONEN_REIHENFOLGE,
    HALTEZEITEN,
    ENDHALTESTELLEN,
    UHRZEITEN_BETRIEB_LINIE_U2 as UHRZEITEN_BETRIEB_LINIE_U1
)
```

**Fertig!** Alle anderen Dateien bleiben unverändert.

## Unterstützte Linien

### Aktuell implementiert:

- ✅ **U1** (Langwasser Süd ↔ Fürth Hbf) - 23 Stationen

### Einfach hinzuzufügen:

- **U2** (Röthenbach ↔ Flughafen)
- **U3** (Gustav-Adolf-Straße ↔ Nordwestring)
- Beliebige andere lineare U-Bahn Strecken

## Wichtige Regeln

### 1. Adjazenzliste muss haben:

- ✅ `vorher` - Vorherige Station (oder None)
- ✅ `nachher` - Nächste Station (oder None)
- ✅ `linie` - Linien-ID (String)
- ✅ `fahrtzeit` - Fahrzeit in Minuten (int oder None)
- ✅ `umsteigezeit` - Haltezeit in Sekunden (int)

### 2. Pflicht-Konstanten:

- `UHRZEITEN_BETRIEB_LINIE_XX` (dict mit start/ende/intervall)
- `STATIONEN_REIHENFOLGE` (List[str])
- `HALTEZEITEN` (Dict[str, int])
- `ENDHALTESTELLEN` (Set[str])

### 3. Namenskonvention:

- Stationsnamen: **GROSSBUCHSTABEN**
- Endhaltestellen: `umsteigezeit = 60`
- Hauptknoten: `umsteigezeit = 60`
- Normale Stationen: `umsteigezeit = 30`

## Adapter-Pattern

Das System verwendet Adapter um mit verschiedenen Implementierungen zu arbeiten:

```
ticket.py (Kollegen)
    ↓
PreisBerechnung (Adapter)
    ↓
TarifRechner (Adapter)
    ↓
ConsoleUI
```

## Testing

Teste nach Änderungen immer:

```bash
cd Sprint_3
python3 test.py
```

Erwartete Ausgabe:

```
✓ Fuzzy-Matching: 12/12
✓ Ticketkategorien: 9/9
✓ Routenberechnung: 4/4
✓ Preisberechnung: 8/8
```

## Troubleshooting

**Problem:** `ImportError: cannot import name 'TicketKategorie'`

- **Lösung:** `ticket.py` fehlt → Fallback wird automatisch verwendet

**Problem:** Falsche Preise

- **Lösung:** Prüfe ob `ticket.py` die gleichen Preise hat wie Spezifikation

**Problem:** Station nicht gefunden

- **Lösung:** Prüfe ob Station in `STATIONEN_REIHENFOLGE` ist (GROSSBUCHSTABEN!)

## Beispiel: Komplette U2 Integration

```python
# adjazenzliste_u2.py
STATIONEN_U2 = {
    "RÖTHENBACH": [{"vorher": None, "nachher": "HOHE MARTER",
                    "linie": "U2", "fahrtzeit": 3, "umsteigezeit": 60}],
    # ... 20 weitere Stationen
    "FLUGHAFEN": [{"vorher": "NORDOSTBAHNHOF", "nachher": None,
                   "linie": "U2", "fahrtzeit": None, "umsteigezeit": 60}]
}

# service.py
from adjazenzliste_u2 import STATIONEN_U2 as STATIONEN_U1, ...

# main.py
print("U-BAHN LINIE U2: Röthenbach ↔ Flughafen")
```

**Funktioniert sofort!** ✅

## Autor

Sprint 3
Daria Wagner
Markus Badura
Okan Cakir
Sven Gräfe
Omar Hamza
Ishak Khalil
Stefan Meiß
