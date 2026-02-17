# Sprint 3: Reiseinformationen und Tariflogik

## Übersicht

Sprint 3 erweitert das U-Bahn Fahrplanauskunftssystem um:

- **US 3.1**: Fuzzy-Matching für Stationseingaben (80% Schwellwert)
- **US 3.2**: Preisberechnung mit Rabatten und Zuschlägen
- **US 3.3**: Vollständige Reisezusammenfassung mit Ankunftszeit

**WICHTIG**: Implementiert sind NUR die für Sprint 3 notwendigen Klassen aus dem Klassendiagramm.

## Implementierte Klassen (aus Klassendiagramm)

```
✓ Station            - Haltestelle
✓ Route              - Strecke zwischen Stationen
✓ UbahnNetz          - Stationsverwaltung mit Fuzzy-Matching
✓ RouteFinder        - Routensuche
✓ PreisBerechnung    - Preisparameter
✓ TarifRechner       - Preisberechnung
✓ Ticket             - Ticketobjekt
✓ ConsoleUI          - Benutzeroberfläche
```

**Nicht implementiert (zukünftige Sprints):**

- TicketAutomatApp
- PaymentStrategy, CashPayment, CardPayment
- TicketPrinter
- QRCodeService

## Projektstruktur

```
Sprint_3/
├── classe.py                   # 8 Klassen für Sprint 3
├── service.py                  # FahrplanBerechner + Konfiguration
├── main.py                     # Nur main()
├── test.py                     # Automatisierte Tests
├── README.md                   # Diese Datei
└── UML_Diagramm_Sprint3.txt    # ASCII UML (nur Sprint 3)
```

## User Stories

### US 3.1: Robuste Eingabeverarbeitung

**Normalisierung:**

- Leerzeichen trimmen
- Kleinschreibung
- Umlaute: ä→ae, ö→oe, ü→ue, ß→ss
- Bindestriche → Leerzeichen

**Mapping von Abkürzungen:**

- `Hbf` / `Hbf.` → `Hauptbahnhof`
- `Str` / `Str.` → `Straße`
- `Fr` / `Fr.` → `Friedrich`

**Fuzzy-Matching:**

- Mindestens 80% Übereinstimmung
- Verwendet `difflib.SequenceMatcher`

**Beispiele:**

```
"Fürth Hbf."       → FÜRTH HBF
"aufseßplatz"      → AUFSESSPLATZ
"Baerenchanze"     → BÄRENSCHANZE
"Maffeiplat"       → MAFFEIPLATZ (80%)
```

**Implementiert in:** `UbahnNetz`

### US 3.2: Rabattsystem

**Ticketkategorien:**

- Kurz: 1-3 Stationen
- Mittel: 4-8 Stationen
- Lang: 9+ Stationen

**Basispreise:**

```
Einzelticket:       Kurz 1,50€ | Mittel 2,00€ | Lang 3,00€
Mehrfahrtenticket:  Kurz 5,00€ | Mittel 7,00€ | Lang 10,00€
```

**Konditionen:**

- Einzelticket: +10%
- Sozialrabatt: -20%
- Barzahlung: +15%

**Berechnungsformel:**

```
1. Basispreis wählen
2. + Einzelticket (+10%) wenn Einzelticket
3. - Sozialrabatt (-20%) wenn berechtigt
4. + Bar-Zuschlag (+15%) wenn Barzahlung
```

**Implementiert in:** `TarifRechner`, `PreisBerechnung`

### US 3.3: Reiseinformationen

Zeigt vollständige Informationen:

- Zeitstempel
- Start/Ziel/Route
- Abfahrts- und Ankunftszeit
- Ticketkategorie und -art
- Preisaufschlüsselung
- Endpreis

**Implementiert in:** `ConsoleUI.zeige_zusammenfassung()`

## Installation & Verwendung

### Voraussetzungen

- Python 3.10+
- Keine externen Dependencies

### Ausführung

**Hauptprogramm:**

```bash
python main.py
```

**Tests:**

```bash
python test.py
```

**Erwartete Ausgabe:**

```
✓ Fuzzy-Matching: 12/12 Tests
✓ Ticketkategorisierung: 9/9 Tests
✓ Routenberechnung: 5/5 Tests
✓ Preisberechnung: 8/8 Tests
```

## Testfälle (aus Backlog)

### Fuzzy-Matching Tests (US 3.1)

| Nr  | Eingabe           | Erwartet         | Status |
| --- | ----------------- | ---------------- | ------ |
| 1   | `Messe`           | MESSE            | ✓      |
| 2   | `Fürth Hbf.`      | FÜRTH HBF        | ✓      |
| 3   | `aufseßplatz`     | AUFSESSPLATZ     | ✓      |
| 4   | `Aufsessplatz`    | AUFSESSPLATZ     | ✓      |
| 5   | `Baerenchanze`    | BÄRENSCHANZE     | ✓      |
| 6   | `Maffeiplat`      | MAFFEIPLATZ      | ✓      |
| 7   | `Jakobinenstrase` | JAKOBINENSTRASSE | ✓      |
| 8   | `  Gostenhof  `   | GOSTENHOF        | ✓      |
| 9   | `Langwasser Nord` | LANGWASSER NORD  | ✓      |
| 10  | `Hauptbahnhof`    | HAUPTBAHNHOF     | ✓      |
| 11  | `Wasser`          | Fehler           | ✓      |
| 12  | `Flughafen`       | Fehler           | ✓      |

### Preisberechnung Tests (US 3.2)

| Route  | Typ    | Rabatt | Zahlung | Preis  | Status |
| ------ | ------ | ------ | ------- | ------ | ------ |
| Kurz   | Einzel | Nein   | Karte   | 1,65€  | ✓      |
| Kurz   | Einzel | Ja     | Karte   | 1,32€  | ✓      |
| Kurz   | Einzel | Nein   | Bar     | 1,90€  | ✓      |
| Kurz   | Mehr   | Nein   | Karte   | 5,00€  | ✓      |
| Mittel | Einzel | Nein   | Karte   | 2,20€  | ✓      |
| Mittel | Mehr   | Ja     | Karte   | 5,60€  | ✓      |
| Lang   | Einzel | Nein   | Karte   | 3,30€  | ✓      |
| Lang   | Mehr   | Nein   | Bar     | 11,50€ | ✓      |

## Klassenstruktur

### Kernklassen

**Station** (Dataclass)

- `name: str`
- `number: int`
- Methode: `display_name()`

**Route** (Dataclass)

- `stations: List[Station]`
- `stops_count: int`
- `to_string: str`

**UbahnNetz** (US 3.1)

- Fuzzy-Matching Logik
- Methoden: `integrations()`, `has_station()`, `station_by_number()`

**RouteFinder**

- Routensuche zwischen Stationen
- Methoden: `find_all_routes()`, `shortlist_routes()`

**TarifRechner** (US 3.2)

- Statische Methoden für Preisberechnung
- `ticketkategorie()`, `berechne()`, `anzahl_tarifen()`

**PreisBerechnung** (Dataclass, US 3.2)

- Alle Preisparameter
- Zuschläge, Rabatte, Kategorien

**Ticket** (Dataclass)

- Ticketobjekt mit Route und Preis
- Methode: `apply_validity_rules()`

**ConsoleUI** (US 3.3)

- Benutzeroberfläche
- Methoden: `zeige_stationen()`, `eingabe_station_mit_nummer()`, `zeige_zusammenfassung()`, `main()`

### Service Layer

**FahrplanBerechner**

- Sprint 2 Zeitberechnung
- Methode: `naechste_abfahrt()`

**Factory-Funktionen**

- `erstelle_netz()` → UbahnNetz
- `erstelle_console_ui()` → ConsoleUI

## Architektur

```
main.py
   └─ erstelle_console_ui()  [service.py]
        ├─ netz = UbahnNetz()
        ├─ route_finder = RouteFinder(netz)
        ├─ fahrplan = FahrplanBerechner()
        └─ ConsoleUI(netz, route_finder, fahrplan)
              └─ main()
```

## Abnahmekriterien

- [x] Stationseingaben mit 80% Genauigkeit erkannt
- [x] Abkürzungen (Hbf., Str.) korrekt verarbeitet
- [x] Ankunftszeit korrekt berechnet
- [x] Preisberechnung für alle Kombinationen korrekt
- [x] Abschließende Übersicht mit allen Infos

## Unterschiede zum Klassendiagramm

**Was implementiert ist:**

- Alle Sprint 3 relevanten Klassen
- Fuzzy-Matching (US 3.1)
- Preisberechnung (US 3.2)
- Reisezusammenfassung (US 3.3)

**Was NICHT implementiert ist (zukünftig):**

- Payment-Klassen (CashPayment, CardPayment)
- TicketAutomatApp (Hauptklasse für gesamtes System)
- TicketPrinter (Ticket-Druck)
- QRCodeService (QR-Code Generierung)

Diese Klassen werden in späteren Sprints hinzugefügt.

## Entwicklungshinweise

### Erweiterung für weitere Linien

```python
# Aktuell: nur U1 in service.py
STATIONEN_REIHENFOLGE = ["LANGWASSER SÜD", ..., "FÜRTH HBF"]

# Zukünftig: mehrere Linien
LINIEN = {
    "U1": ["LANGWASSER SÜD", ..., "FÜRTH HBF"],
    "U2": ["RÖTHENBACH", ..., "FLUGHAFEN"],
    "U3": ["NORDWESTRING", ..., "GUSTAV-ADOLF-STRASSE"]
}
```

### Integration mit Payment-System (zukünftig)

```python
# Sprint 4/5: PaymentStrategy hinzufügen
from payment import CashPayment, CardPayment

payment_method = CashPayment() if barzahlung else CardPayment()
result = payment_method.pay(endpreis)
```

## Technische Details

**Fuzzy-Matching Algorithmus:**

```python
similarity = SequenceMatcher(None, eingabe, station).ratio()
if similarity >= 0.8:  # 80% Schwellwert
    match_gefunden()
```

**Preisberechnung:**

```python
preis = basispreis
if einzelticket:
    preis *= 1.10  # +10%
if sozialrabatt:
    preis *= 0.80  # -20%
if barzahlung:
    preis *= 1.15  # +15%
```

## Autor

**Sprint 3**

**Daria Wagner,**  
**Markus Badura,**
**Okan Cakir,**
**Sven Gräfe,**
**Omar Hamza,**
**Ishak Khalil,**
**Stefan Meiß**

---

**Basierend auf dem Klassendiagramm**  
**Implementiert: Sprint 3 Klassen**
