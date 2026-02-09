# U-Bahn Fahrplanauskunft - Linie U1

Ein Python-basiertes Fahrplanauskunftssystem für die Nürnberger U-Bahn Linie U1 (Langwasser Süd ↔ Fürth Hbf).

## Projektbeschreibung

Dieses Projekt implementiert eine Fahrplanauskunft für die U-Bahn Linie U1 mit 23 Stationen. Das System berechnet Abfahrtszeiten unter Berücksichtigung von:

- Bidirektionalem Verkehr (Hin- und Rückfahrt)
- Variablen Haltezeiten an verschiedenen Stationstypen
- Taktfahrplan mit 10-Minuten-Intervall
- Wendezeiten an Endhaltestellen

## Features

- ✅ **23 Stationen**: Vollständige Strecke von Langwasser Süd bis Fürth Hbf
- ✅ **Bidirektionaler Verkehr**: Fahrt in beide Richtungen möglich
- ✅ **Variable Haltezeiten**:
  - Standard: 30 Sekunden
  - Hauptknoten (Hauptbahnhof, Plärrer): 60 Sekunden
  - Endhaltestellen: 60 Sekunden
- ✅ **Taktfahrplan**: Alle 10 Minuten (05:00 - 23:00 Uhr)
- ✅ **Eingabevalidierung**: Benutzerfreundliche Fehlerbehandlung

## 🛠️ Technische Details

### Projektstruktur

```
Sprint_2/
├── main.py              # Hauptprogramm mit Benutzerinteraktion
├── classe.py            # Fahrplan-Datenklasse und Geschäftslogik
├── service.py           # Service-Funktionen für Eingaben
└── adjazenzliste.py     # Stationsdaten und Konfiguration
```

### Datenmodell

**Adjazenzliste**: Bidirektionale Graphenstruktur mit:

- Stationsnamen
- Fahrtzeiten (in Minuten)
- Haltezeiten (in Sekunden)

**Fahrplan-Klasse**: Verwaltet:

- Betriebszeiten (Start/Ende)
- Taktintervall
- Wegfindung
- Reisezeitberechnung

## 💻 Installation & Verwendung

### Voraussetzungen

- Python 3.10 oder höher

### Installation

```bash
# Repository klonen
git clone <repository-url>
cd Sprint_2

# Keine zusätzlichen Dependencies erforderlich (nutzt nur Python Standard Library)
```

### Ausführung

```bash
python main.py
```

### Beispiel-Interaktion

```
============================================================
Willkommen zum Fahrplan der U-Bahn Linie U1!
Langwasser Süd ↔ Fürth Hbf
============================================================

Geben Sie die Starthaltestelle ein: LANGWASSER MITTE
Geben Sie die Zielhaltestelle ein: MESSE
Gewünschte Zeit eingeben (HH:MM), z.B. 05:08: 05:01

============================================================
✓ Nächste Abfahrt von LANGWASSER MITTE nach MESSE:
  → 05:06 Uhr
============================================================
```

## Berechnungsbeispiel

**Szenario**: Fahrt von Langwasser Mitte zur Messe um 05:01 Uhr

| Zeit         | Station              | Aktion              |
| ------------ | -------------------- | ------------------- |
| 05:00:00     | Langwasser Süd       | Zugstart            |
| 05:03:00     | Gemeinschaftshaus    | Ankunft             |
| 05:03:30     | Gemeinschaftshaus    | Abfahrt (+30s Halt) |
| 05:05:30     | Langwasser Mitte     | Ankunft             |
| **05:06:00** | **Langwasser Mitte** | **Abfahrt**         |
| 05:08:00     | Messe                | Ankunft             |

**Ergebnis**: Nächste Abfahrt um **05:06 Uhr**

## Architektur

### Komponenten

1. **adjazenzliste.py**: Datenhaltung
   - Stationsreihenfolge
   - Bidirektionale Verbindungen
   - Betriebszeiten

2. **classe.py**: Kernlogik
   - `finde_linear_weg()`: Wegfindung in beide Richtungen
   - `berechne_reisezeit()`: Zeitberechnung mit Haltezeiten
   - `naechste_abfahrt()`: Findet nächsten verfügbaren Zug

3. **service.py**: Hilfsfunktionen
   - Eingabevalidierung
   - Fahrplan-Initialisierung

4. **main.py**: Benutzeroberfläche
   - Interaktive Eingaben
   - Ausgabeformatierung

## User Stories (Sprint 2)

- **US 2.1** (Fahrgast): Variable Haltezeiten für Ein-/Ausstieg ✅
- **US 2.2** (Fahrgast): Bidirektionaler Verkehr ✅
- **US 2.3** (Verkehrsbetrieb): Reale U1-Streckenstruktur ✅

## 🔧 Technologien

- **Python 3.10+**
- **Dataclasses**: Für typsichere Datenmodelle
- **datetime/timedelta**: Für präzise Zeitberechnungen
- **Type Hints**: Für bessere Code-Dokumentation

## Abnahmekriterien

- [x] Datenstruktur für U1 (23 Stationen)
- [x] Eingabe: Start, Ziel, gewünschte Zeit
- [x] Verarbeitung: Haltezeiten berücksichtigt
- [x] Verarbeitung: Beide Fahrtrichtungen unterstützt
- [x] Ausgabe: Minutengenaue Abfahrtszeit

## Zukünftige Erweiterungen

- [ ] Ankunftszeit zusätzlich zur Abfahrtszeit anzeigen
- [ ] Gesamtreisedauer berechnen
- [ ] Umsteigeverbindungen zu anderen Linien
- [ ] Echtzeitverspätungen
- [ ] Weboberfläche (GUI)
- [ ] API-Endpoint für externe Anwendungen

## Autor

**Daria Wagner**  
Retraining: Data & Process Analytics  
Projekt: Portfolio für Praktikumsbewerbung (Juni 2026)

## Lizenz

Dieses Projekt wurde zu Lernzwecken erstellt.
