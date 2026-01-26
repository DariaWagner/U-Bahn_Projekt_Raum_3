# Bereit zum Dienst, Meisterin.


from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date, timedelta
from math import ceil
from typing import Optional, Dict, Any, List


@dataclass
class Fahrplan:
    startzeit: datetime
    endzeit: datetime
    intervall: int                 # Minuten
    stationen: Dict[str, List[Dict[str, Any]]]

    def berechne_fahrtzeit_von_start(self, station: str) -> Optional[int]:
        """
        Summiert die Fahrtzeiten von A bis zur gewünschten Station.
        Rückgabe in Minuten, oder None wenn Station ungültig/nicht erreichbar.
        """
        station = station.strip().upper()
        if station not in self.stationen:
            return None

        if station == "A":
            return 0

        aktuelle_station = "A"
        gesamt = 0

        # Linie ist hier nur vorwärts A->B->C->D
        while aktuelle_station is not None and aktuelle_station != station:
            verbindungen = self.stationen.get(aktuelle_station, [])
            if not verbindungen:
                return None

            v = verbindungen[0]
            nachher = v.get("nachher")
            fahrtzeit = v.get("fahrtzeit")

            if nachher is None or fahrtzeit is None:
                return None

            gesamt += int(fahrtzeit)
            aktuelle_station = str(nachher)

        return gesamt if aktuelle_station == station else None

    def berechne_fahrtzeit(self, start: str, ziel: str) -> Optional[int]:
        """
        Extra-Methode passend zum UML: Fahrtzeit von 'start' nach 'ziel'.
        In Sprint 1 reicht die Richtung A->...; deshalb hier simpel:
        Wir rechnen über die Start-Offsets.
        """
        start = start.strip().upper()
        ziel = ziel.strip().upper()

        off_start = self.berechne_fahrtzeit_von_start(start)
        off_ziel = self.berechne_fahrtzeit_von_start(ziel)
        if off_start is None or off_ziel is None:
            return None

        diff = off_ziel - off_start
        return diff if diff >= 0 else None  # rückwärts ist im Modell nicht vorgesehen

    def naechste_abfahrt(self, station: str, aktuelle_zeit: str) -> Optional[datetime]:
        """
        Gibt die nächste tatsächliche Abfahrtszeit an der Station zurück,
        die >= gewünschter Zeit ist. Oder None, wenn keine Bahn mehr fährt.
        """
        station = station.strip().upper()
        offset = self.berechne_fahrtzeit_von_start(station)
        if offset is None:
            return None

        try:
            gewuenscht_dt = datetime.combine(
                self.startzeit.date(),
                datetime.strptime(aktuelle_zeit.strip(), "%H:%M").time()
            )
        except ValueError:
            return None

        offset_td = timedelta(minutes=offset)

        erste_station_abfahrt = self.startzeit + offset_td
        letzte_station_abfahrt = self.endzeit + offset_td  # letzter Zug startet 23:00 an A

        # Wenn gewünschte Zeit nach der letzten möglichen Abfahrt liegt -> keine Bahn mehr
        if gewuenscht_dt > letzte_station_abfahrt:
            return None

        # Wenn gewünschte Zeit vor der ersten Abfahrt liegt -> erste Abfahrt nehmen
        if gewuenscht_dt <= erste_station_abfahrt:
            return erste_station_abfahrt

        # Sonst: auf nächstes Intervall aufrunden
        delta_min = (gewuenscht_dt - erste_station_abfahrt).total_seconds() / 60.0
        n = ceil(delta_min / self.intervall)
        kandidat = erste_station_abfahrt + timedelta(minutes=n * self.intervall)

        # Sicherheitscheck: darf nicht nach letzter Abfahrt liegen
        if kandidat > letzte_station_abfahrt:
            return None

        return kandidat
