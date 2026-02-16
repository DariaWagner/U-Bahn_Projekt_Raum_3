# Sprint_3/classe.py
"""
Klassen für Sprint 3 - Reiseinformationen und Tariflogik
Nur Sprint 3 relevante Klassen aus Klassendiagramm
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, date
from typing import List, Optional, Tuple, Dict
from difflib import SequenceMatcher


# ============================================================================
# STATION
# ============================================================================

@dataclass
class Station:
    """Repräsentiert eine einzelne Haltestelle"""
    name: str
    number: int

    def display_name(self) -> str:
        """Gibt den Namen für die Anzeige zurück"""
        return self.name


# ============================================================================
# ROUTE
# ============================================================================

@dataclass
class Route:
    """Repräsentiert eine Route zwischen zwei Stationen"""
    stations: List[Station]
    stops_count: int
    to_string: str

    def __init__(self, stations: List[Station]):
        self.stations = stations
        self.stops_count = len(stations) - 1
        self.to_string = " → ".join([s.name for s in stations])


# ============================================================================
# ZEITRECHNER (Verkürzte Version - Sprint 2 Logik)
# ============================================================================

class Zeitrechner:
    """Berechnet Ankunfts- und Abfahrtszeiten"""
    
    def __init__(self, stationen_reihenfolge: List[str], stationen_graph: Dict, 
                 haltezeiten: Dict[str, int], endhaltestellen: set):
        self.stationen_reihenfolge = stationen_reihenfolge
        self.stationen_graph = stationen_graph
        self.haltezeiten = haltezeiten
        self.endhaltestellen = endhaltestellen
    
    def _fahrtzeit_holen(self, station_idx: int) -> int:
        """Holt Fahrtzeit aus Graph"""
        station_name = self.stationen_reihenfolge[station_idx]
        return self.stationen_graph[station_name][0]["fahrtzeit"] or 0
    
    def _haltezeit_addieren(self, zeit: datetime, station_idx: int) -> datetime:
        """Addiert Haltezeit"""
        station_name = self.stationen_reihenfolge[station_idx]
        return zeit + timedelta(seconds=self.haltezeiten[station_name])
    
    def berechne_ankunft(self, zug_abfahrt: datetime, von_idx: int, bis_idx: int) -> datetime:
        """Berechnet Ankunftszeit"""
        zeit = zug_abfahrt
        
        if von_idx < bis_idx:
            # Hinrichtung
            for i in range(von_idx, bis_idx):
                if i > von_idx:
                    zeit = self._haltezeit_addieren(zeit, i)
                zeit += timedelta(minutes=self._fahrtzeit_holen(i))
        else:
            # Rückrichtung
            for i in range(von_idx, bis_idx, -1):
                if i < von_idx:
                    zeit = self._haltezeit_addieren(zeit, i)
                zeit += timedelta(minutes=self._fahrtzeit_holen(i - 1))
        
        return zeit
    
    def berechne_abfahrt(self, ankunft: datetime, station: str) -> datetime:
        """Berechnet Abfahrtszeit"""
        if station in self.endhaltestellen:
            return ankunft
        return ankunft + timedelta(seconds=self.haltezeiten[station])
    
    @staticmethod
    def runde_ab(dt: datetime) -> datetime:
        """Rundet auf volle Minute ab"""
        return dt.replace(second=0, microsecond=0)


# ============================================================================
# FAHRPLAN BERECHNER (Verkürzte Version - Sprint 2 Logik)
# ============================================================================

class FahrplanBerechner:
    """Findet nächste Verbindung"""
    
    def __init__(self, startzeit: datetime, endzeit: datetime, intervall: int,
                 zeitrechner: Zeitrechner, stationen_reihenfolge: List[str]):
        self.startzeit = startzeit
        self.endzeit = endzeit
        self.intervall = intervall
        self.zeitrechner = zeitrechner
        self.stationen_reihenfolge = stationen_reihenfolge
    
    def _idx(self, station: str) -> int:
        """Gibt Stationsindex zurück"""
        return self.stationen_reihenfolge.index(station.upper())
    
    def _berechne_ankunft_an_start(self, zug_start: datetime, start_idx: int, ist_hinrichtung: bool) -> datetime:
        """Berechnet wann Zug an Startstation ankommt"""
        if ist_hinrichtung:
            return self.zeitrechner.berechne_ankunft(zug_start, 0, start_idx)
        
        # Rückrichtung: erst nach Fürth, dann zurück
        fuerth_idx = len(self.stationen_reihenfolge) - 1
        ankunft_fuerth = self.zeitrechner.berechne_ankunft(zug_start, 0, fuerth_idx)
        wendezeit = timedelta(seconds=self.zeitrechner.haltezeiten[self.stationen_reihenfolge[fuerth_idx]])
        abfahrt_rueck = ankunft_fuerth + wendezeit
        return self.zeitrechner.berechne_ankunft(abfahrt_rueck, fuerth_idx, start_idx)
    
    def _finde_verbindung_heute(self, start_idx: int, ziel_idx: int, start: str, 
                                gewuenscht_dt: datetime, ist_hinrichtung: bool) -> Optional[Tuple[datetime, datetime]]:
        """Sucht Verbindung für heute"""
        zug_start = self.startzeit
        
        while zug_start <= self.endzeit:
            ankunft_start = self._berechne_ankunft_an_start(zug_start, start_idx, ist_hinrichtung)
            abfahrt_start = self.zeitrechner.berechne_abfahrt(ankunft_start, start)
            abfahrt_gerundet = Zeitrechner.runde_ab(abfahrt_start)
            
            if abfahrt_gerundet >= gewuenscht_dt:
                ankunft_ziel = self.zeitrechner.berechne_ankunft(abfahrt_start, start_idx, ziel_idx)
                return abfahrt_gerundet, Zeitrechner.runde_ab(ankunft_ziel)
            
            zug_start += timedelta(minutes=self.intervall)
        
        return None
    
    def naechste_abfahrt(self, start: str, ziel: str, gewuenscht: str) -> Tuple[Optional[datetime], Optional[datetime], bool]:
        """Findet nächste Verbindung"""
        start = start.upper()
        ziel = ziel.upper()
        
        gewuenscht_dt = datetime.combine(self.startzeit.date(), datetime.strptime(gewuenscht, "%H:%M").time())
        start_idx = self._idx(start)
        ziel_idx = self._idx(ziel)
        ist_hinrichtung = start_idx < ziel_idx
        
        # Suche heute
        verbindung = self._finde_verbindung_heute(start_idx, ziel_idx, start, gewuenscht_dt, ist_hinrichtung)
        if verbindung:
            return verbindung[0], verbindung[1], False
        
        # Nächster Tag
        naechster_tag = self.startzeit + timedelta(days=1)
        ankunft_start = self._berechne_ankunft_an_start(naechster_tag, start_idx, ist_hinrichtung)
        abfahrt_start = self.zeitrechner.berechne_abfahrt(ankunft_start, start)
        abfahrt_morgen = Zeitrechner.runde_ab(abfahrt_start)
        ankunft_ziel = self.zeitrechner.berechne_ankunft(abfahrt_start, start_idx, ziel_idx)
        
        return abfahrt_morgen, Zeitrechner.runde_ab(ankunft_ziel), True


# ============================================================================
# UBAHN NETZ (User Story 3.1: Fuzzy-Matching)
# ============================================================================

class UbahnNetz:
    """
    Verwaltet Stationen und bietet Fuzzy-Matching
    User Story 3.1: Robuste Eingabeverarbeitung
    """

    def __init__(self):
        self.adjacency: Dict[str, List[str]] = {}
        self.station_numbers: Dict[str, int] = {}
        self.stations_by_number: Dict[int, str] = {}
        self.station_list_raw: List[str] = []

    def add_station(self, name: str, number: int):
        """Fügt eine Station zum Netz hinzu"""
        normalized = self._normalize(name)
        self.adjacency[normalized] = [name]
        self.station_numbers[normalized] = number
        self.stations_by_number[number] = name
        self.station_list_raw.append(name)

        # Erweiterte Namen für Abkürzungen
        expanded = self._apply_abbreviations(normalized)
        if expanded != normalized and expanded not in self.adjacency:
            self.adjacency[expanded] = [name]
            self.station_numbers[expanded] = number

    def _normalize(self, text: str) -> str:
        """
        Normalisiert Text für Fuzzy-Matching
        - Kleinschreibung, Trimmen
        - Bindestriche → Leerzeichen
        - Umlaute: ä→ae, ö→oe, ü→ue, ß→ss
        """
        text = text.strip().lower()
        text = text.replace("-", " ")
        text = text.replace("ä", "ae").replace("ö", "oe")
        text = text.replace("ü", "ue").replace("ß", "ss")
        return text

    def _apply_abbreviations(self, text: str) -> str:
        """
        Ersetzt Abkürzungen durch Vollwörter
        Hbf./hbf → hauptbahnhof
        Str./str → strasse
        Fr./fr → friedrich
        """
        abbr_map = {
            "hbf": "hauptbahnhof",
            "hbf.": "hauptbahnhof",
            "str": "strasse",
            "str.": "strasse",
            "fr": "friedrich",
            "fr.": "friedrich",
        }

        text = text.replace(".", "")
        words = text.split()
        result = []

        for word in words:
            if word in abbr_map:
                result.append(abbr_map[word])
            elif word + "." in abbr_map:
                result.append(abbr_map[word + "."])
            else:
                result.append(word)

        return " ".join(result)

    def _similarity(self, a: str, b: str) -> float:
        """Berechnet Ähnlichkeit zwischen zwei Strings (0.0 - 1.0)"""
        return SequenceMatcher(None, a, b).ratio()

    def has_station(self, name: str) -> bool:
        """Prüft ob Station existiert (mit Fuzzy-Matching)"""
        normalized = self._normalize(name)
        normalized = self._apply_abbreviations(normalized)

        if normalized in self.adjacency:
            return True

        for station_norm in self.adjacency.keys():
            if self._similarity(normalized, station_norm) >= 0.8:
                return True

        return False

    def integrations(self, name: str) -> List[str]:
        """
        Findet passende Stationen (Fuzzy-Matching, 80% Schwellwert)
        Returns: Liste der Stationsnamen (leer bei keinem Match)
        """
        normalized = self._normalize(name)
        normalized = self._apply_abbreviations(normalized)

        matches = []

        # Exakte Übereinstimmung hat Priorität
        if normalized in self.adjacency:
            return self.adjacency[normalized]

        # Fuzzy-Matching
        for station_norm, station_names in self.adjacency.items():
            similarity = self._similarity(normalized, station_norm)
            if similarity >= 0.8:
                matches.append((similarity, station_names[0]))

        # Sortiere nach Ähnlichkeit
        matches.sort(key=lambda x: x[0], reverse=True)

        return [name for _, name in matches]

    def station_by_number(self, num: int) -> Optional[str]:
        """Gibt Station anhand der Nummer zurück"""
        return self.stations_by_number.get(num)

    def station_list(self) -> List[str]:
        """Gibt alle Stationsnamen zurück"""
        return self.station_list_raw


# ============================================================================
# ROUTE FINDER
# ============================================================================

class RouteFinder:
    """Findet Routen zwischen Stationen"""

    def __init__(self, netz: UbahnNetz, stationen_reihenfolge: List[str]):
        self.netz = netz
        self.stationen_reihenfolge = stationen_reihenfolge
        self.stationen: List[Station] = [
            Station(name=name, number=i + 1)
            for i, name in enumerate(stationen_reihenfolge)
        ]

    def find_all_routes(self, start: str, ziel: str) -> List[Route]:
        """Findet alle Routen"""
        start = start.upper()
        ziel = ziel.upper()

        try:
            start_idx = self.stationen_reihenfolge.index(start)
            ziel_idx = self.stationen_reihenfolge.index(ziel)
        except ValueError:
            return []

        if start_idx < ziel_idx:
            stations = self.stationen[start_idx:ziel_idx + 1]
        else:
            stations = list(reversed(self.stationen[ziel_idx:start_idx + 1]))

        return [Route(stations)]

    def shortlist_routes(self, start: str, ziel: str) -> Optional[Route]:
        """Gibt die beste Route zurück"""
        routes = self.find_all_routes(start, ziel)
        return routes[0] if routes else None


# ============================================================================
# PREISBERECHNUNG (User Story 3.2) - VERWENDET KOLLEGEN ticket.py
# ============================================================================

# Import von Kollegen-Modul (NICHT ÄNDERN!)
try:
    from ticket import (
        TicketKategorie, TicketArt, Zahlart, Ticketpreis, erstelle_ticket
    )
    
    # Adapter-Klasse für Kompatibilität mit bestehendem Code
    class PreisBerechnung:
        """Adapter für Ticketpreis von Kollegen"""
        def __init__(self, ticketpreis: Ticketpreis):
            self.ticketpreis = ticketpreis
            self.ticketkategorie = ticketpreis.kategorie.name.lower()
            self.basispreis = ticketpreis.berechne_basispreis()
            self.ist_einzelticket = (ticketpreis.art == TicketArt.EINZEL)
            self.mehrfahrt = (ticketpreis.art == TicketArt.MEHRFAHRT)
            self.sozialrabatt = ticketpreis.hat_sozialrabatt
            self.barzahlung = (ticketpreis.zahlart == Zahlart.BAR)
            self.zuschlag_ticketart_prozent = 10.0
            self.rabatt_prozent = 20.0
            self.zuschlag_bar_prozent = 15.0
            self.anzahl_tarifen = 1 if self.ist_einzelticket else 4
    
    class TarifRechner:
        """Adapter für Ticketpreis-Berechnung von Kollegen"""
        
        PREISE_EINZEL = {"kurz": 1.50, "mittel": 2.00, "lang": 3.00}
        PREISE_MEHR = {"kurz": 5.00, "mittel": 7.00, "lang": 10.00}
        
        @staticmethod
        def ticketkategorie(anzahl_stationen: int) -> str:
            """Bestimmt Ticketkategorie"""
            kategorie = Ticketpreis.bestimme_kategorie(anzahl_stationen)
            return kategorie.name.lower()
        
        @staticmethod
        def berechne(route: Route, ist_einzelticket: bool, sozialrabatt: bool, barzahlung: bool) -> PreisBerechnung:
            """Erstellt PreisBerechnung"""
            ticketpreis = erstelle_ticket(
                anzahl_stationen=route.stops_count,
                ist_mehrfahrt=not ist_einzelticket,
                ist_barzahlung=barzahlung,
                hat_sozialrabatt=sozialrabatt
            )
            return PreisBerechnung(ticketpreis)
        
        @staticmethod
        def anzahl_tarifen(pb: PreisBerechnung) -> float:
            """Berechnet Endpreis"""
            return pb.ticketpreis.berechne_endpreis()

except ImportError:
    # Fallback: Original-Implementation falls ticket.py nicht vorhanden
    @dataclass
    class PreisBerechnung:
        """Original PreisBerechnung"""
        ticketkategorie: str
        basispreis: float
        mehrfahrt: bool
        ist_einzelticket: bool
        sozialrabatt: bool
        barzahlung: bool
        zuschlag_ticketart_prozent: float
        rabatt_prozent: float
        zuschlag_bar_prozent: float
        anzahl_tarifen: int

    class TarifRechner:
        """Original TarifRechner"""
        PREISE_EINZEL = {"kurz": 1.50, "mittel": 2.00, "lang": 3.00}
        PREISE_MEHR = {"kurz": 5.00, "mittel": 7.00, "lang": 10.00}

        @staticmethod
        def ticketkategorie(anzahl_stationen: int) -> str:
            if anzahl_stationen <= 3:
                return "kurz"
            elif anzahl_stationen <= 8:
                return "mittel"
            else:
                return "lang"

        @staticmethod
        def berechne(route: Route, ist_einzelticket: bool, sozialrabatt: bool, barzahlung: bool) -> PreisBerechnung:
            kategorie = TarifRechner.ticketkategorie(route.stops_count)
            if ist_einzelticket:
                basispreis = TarifRechner.PREISE_EINZEL[kategorie]
                anzahl = 1
            else:
                basispreis = TarifRechner.PREISE_MEHR[kategorie]
                anzahl = 4

            return PreisBerechnung(
                ticketkategorie=kategorie,
                basispreis=basispreis,
                mehrfahrt=not ist_einzelticket,
                ist_einzelticket=ist_einzelticket,
                sozialrabatt=sozialrabatt,
                barzahlung=barzahlung,
                zuschlag_ticketart_prozent=10.0,
                rabatt_prozent=20.0,
                zuschlag_bar_prozent=15.0,
                anzahl_tarifen=anzahl
            )

        @staticmethod
        def anzahl_tarifen(pb: PreisBerechnung) -> float:
            preis = pb.basispreis
            if pb.ist_einzelticket:
                preis += preis * (pb.zuschlag_ticketart_prozent / 100.0)
            if pb.sozialrabatt:
                preis -= preis * (pb.rabatt_prozent / 100.0)
            if pb.barzahlung:
                preis += preis * (pb.zuschlag_bar_prozent / 100.0)
            return round(preis, 2)


# ============================================================================
# TICKET
# ============================================================================

@dataclass
class Ticket:
    """Repräsentiert ein Ticket"""
    ticket_id: str
    kaufzeit: datetime
    gueltigkeit_date: str
    route: Route
    preis: PreisBerechnung

    def apply_validity_rules(self) -> None:
        """Setzt Gültigkeitsdatum"""
        self.gueltigkeit_date = self.kaufzeit.strftime("%d.%m.%Y")


# ============================================================================
# CONSOLE UI (User Story 3.3)
# ============================================================================

class ConsoleUI:
    """
    Konsolenbasierte Benutzeroberfläche
    User Story 3.3: Reiseinformationen anzeigen
    """

    def __init__(self, netz: UbahnNetz, route_finder: RouteFinder, fahrplan_berechner):
        self.netz = netz
        self.route_finder = route_finder
        self.fahrplan = fahrplan_berechner
        self.MAX_VERSUCHE = 3

    def zeige_stationen(self):
        """Zeigt alle Stationen in 3 Spalten"""
        stationen = self.netz.station_list()
        print("\n" + "=" * 80)
        print("VERFÜGBARE STATIONEN DER LINIE U1".center(80))
        print("=" * 80)

        zeilen = (len(stationen) + 2) // 3
        for i in range(zeilen):
            zeile = ""
            for spalte in range(3):
                idx = i + spalte * zeilen
                if idx < len(stationen):
                    zeile += f"[{idx + 1:2d}] {stationen[idx]:<24}"
            print(zeile)
        print("=" * 80)

    def eingabe_station_mit_nummer(self, prompt: str) -> Optional[str]:
        """Eingabe mit Nummer oder Name inkl. Fuzzy-Matching"""
        for versuch in range(self.MAX_VERSUCHE):
            eingabe = input(f"\n{prompt} (Nummer oder Name): ").strip()

            if eingabe.isdigit():
                nummer = int(eingabe)
                station = self.netz.station_by_number(nummer)
                if station:
                    return station
                else:
                    anzahl = len(self.netz.station_list())
                    print(f"❌ Ungültige Nummer. Bitte zwischen 1 und {anzahl} wählen.")
                    continue

            matches = self.netz.integrations(eingabe)

            if len(matches) == 0:
                print(f"❌ Station '{eingabe}' nicht gefunden.")
            elif len(matches) == 1:
                return matches[0]
            else:
                print(f"⚠ Mehrere Stationen gefunden für '{eingabe}':")
                for i, match in enumerate(matches, 1):
                    print(f"  [{i}] {match}")

                auswahl = input("Bitte Nummer wählen: ").strip()
                if auswahl.isdigit() and 1 <= int(auswahl) <= len(matches):
                    return matches[int(auswahl) - 1]
                else:
                    print("❌ Ungültige Auswahl.")

        print(f"\n❌ Maximale Anzahl Versuche ({self.MAX_VERSUCHE}) erreicht.")
        return None

    def eingabe_zeit(self) -> Optional[str]:
        """Eingabe und Validierung der Uhrzeit"""
        for _ in range(self.MAX_VERSUCHE):
            t = input("\nGewünschte Abfahrtszeit (HH:MM), z.B. 05:08: ").strip()
            try:
                datetime.strptime(t, "%H:%M")
                return t
            except ValueError:
                print("❌ Ungültiges Format. Bitte HH:MM eingeben.")
        return None

    def eingabe_ja_nein(self, prompt: str) -> bool:
        """Ja/Nein Abfrage"""
        while True:
            antwort = input(f"{prompt} (j/n): ").strip().lower()
            if antwort in ["j", "ja", "y", "yes"]:
                return True
            elif antwort in ["n", "nein", "no"]:
                return False
            else:
                print("❌ Bitte 'j' für Ja oder 'n' für Nein eingeben.")

    def zeige_zusammenfassung(
        self, start: str, ziel: str, abfahrt: datetime, ankunft: datetime,
        route: Route, preis_berechnung: PreisBerechnung, endpreis: float, ist_morgen: bool
    ):
        """Zeigt finale Reisezusammenfassung"""
        print("\n" + "=" * 80)
        print("REISEZUSAMMENFASSUNG".center(80))
        print("=" * 80)

        if ist_morgen:
            print("⚠ ACHTUNG: Betriebsschluss erreicht!".center(80))
            print("Nächste Verbindung erst morgen:".center(80))
            print("-" * 80)

        print(f"  Zeitstempel:      {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"  Von:              {start}")
        print(f"  Nach:             {ziel}")
        print(f"  Route:            {route.to_string}")
        print(f"  Anzahl Stationen: {route.stops_count}")
        print(f"  Abfahrt:          {abfahrt.strftime('%H:%M')} Uhr")
        print(f"  Ankunft:          {ankunft.strftime('%H:%M')} Uhr")
        print("-" * 80)
        print(f"  Ticketkategorie:  {preis_berechnung.ticketkategorie.capitalize()}")
        art = "Einzelticket" if preis_berechnung.ist_einzelticket else "Mehrfahrtenticket (4 Fahrten)"
        print(f"  Ticketart:        {art}")
        print(f"  Basispreis:       {preis_berechnung.basispreis:.2f} €")

        if preis_berechnung.ist_einzelticket:
            print(f"  + Einzelticket:   +{preis_berechnung.zuschlag_ticketart_prozent:.0f}%")

        if preis_berechnung.sozialrabatt:
            print(f"  - Sozialrabatt:   -{preis_berechnung.rabatt_prozent:.0f}%")

        if preis_berechnung.barzahlung:
            print(f"  + Barzahlung:     +{preis_berechnung.zuschlag_bar_prozent:.0f}%")

        print("-" * 80)
        print(f"  ENDPREIS:         {endpreis:.2f} €")
        print("=" * 80)

    def main(self):
        """Hauptablauf des Ticketautomaten"""
        print("\n" + "=" * 80)
        print("WILLKOMMEN ZUM FAHRPLAN DER U-BAHN LINIE U1!".center(80))
        print("Langwasser Süd ↔ Fürth Hbf".center(80))
        print("=" * 80)

        self.zeige_stationen()

        start = self.eingabe_station_mit_nummer("Geben Sie die Starthaltestelle ein")
        if not start:
            return
        print(f"✓ Start: {start}")

        while True:
            ziel = self.eingabe_station_mit_nummer("Geben Sie die Zielhaltestelle ein")
            if not ziel:
                return
            if start.upper() == ziel.upper():
                print("❌ Start und Ziel sind identisch.")
            else:
                print(f"✓ Ziel: {ziel}")
                break

        gewuenscht = self.eingabe_zeit()
        if not gewuenscht:
            print("\n❌ Ungültige Zeiteingabe.")
            return

        route = self.route_finder.shortlist_routes(start, ziel)
        if not route:
            print("❌ Keine Route gefunden.")
            return

        abfahrt, ankunft, ist_morgen = self.fahrplan.naechste_abfahrt(start, ziel, gewuenscht)
        if not abfahrt:
            print("❌ Keine Verbindung gefunden.")
            return

        print("\n" + "-" * 80)
        print("TICKETAUSWAHL")
        print("-" * 80)
        ist_einzelticket = self.eingabe_ja_nein("Einzelticket? (Nein = Mehrfahrtenticket)")
        sozialrabatt = self.eingabe_ja_nein("Sozialrabatt berechtigt?")
        barzahlung = self.eingabe_ja_nein("Barzahlung? (Nein = Kartenzahlung)")

        preis_berechnung = TarifRechner.berechne(route, ist_einzelticket, sozialrabatt, barzahlung)
        endpreis = TarifRechner.anzahl_tarifen(preis_berechnung)

        self.zeige_zusammenfassung(start, ziel, abfahrt, ankunft, route, preis_berechnung, endpreis, ist_morgen)

        print("\nVielen Dank für Ihre Fahrt mit der U-Bahn Nürnberg!")
