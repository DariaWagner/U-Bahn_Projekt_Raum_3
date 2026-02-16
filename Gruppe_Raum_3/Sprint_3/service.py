# Sprint_3/service.py
"""
Service-Layer für Sprint 3
Nutzt adjazenzliste.py für Konfiguration
"""

from datetime import datetime, timedelta, date
from typing import Tuple, Optional
from adjazenzliste import (
    STATIONEN_U1,
    STATIONEN_REIHENFOLGE,
    HALTEZEITEN,
    ENDHALTESTELLEN,
    UHRZEITEN_BETRIEB_LINIE_U1
)
from classe import UbahnNetz, RouteFinder, ConsoleUI


# ============================================================================
# FAHRPLAN-BERECHNER (Sprint 2 Logik)
# ============================================================================

class FahrplanBerechner:
    """
    Enthält die Zeitberechnung aus Sprint 2
    Nutzt STATIONEN_U1 aus adjazenzliste.py
    """

    def __init__(self):
        heute = date.today()
        self.startzeit = datetime.combine(
            heute, datetime.strptime(UHRZEITEN_BETRIEB_LINIE_U1["start"], "%H:%M").time()
        )
        self.endzeit = datetime.combine(
            heute, datetime.strptime(UHRZEITEN_BETRIEB_LINIE_U1["ende"], "%H:%M").time()
        )
        self.intervall = int(UHRZEITEN_BETRIEB_LINIE_U1["intervall_minuten"])
        self.stationen_reihenfolge = STATIONEN_REIHENFOLGE
        self.stationen_graph = STATIONEN_U1
        self.haltezeiten = HALTEZEITEN
        self.endhaltestellen = ENDHALTESTELLEN

    def _idx(self, station: str) -> int:
        """Gibt den Index einer Station zurück"""
        return self.stationen_reihenfolge.index(station.upper())

    def _berechne_ankunft(self, zug_abfahrt: datetime, von_idx: int, bis_idx: int) -> datetime:
        """Berechnet Ankunftszeit an bis_idx"""
        zeit = zug_abfahrt

        if von_idx < bis_idx:
            # Hinrichtung
            for i in range(von_idx, bis_idx):
                if i > von_idx:
                    zeit += timedelta(seconds=self.haltezeiten[self.stationen_reihenfolge[i]])
                
                # Hole Fahrzeit aus STATIONEN_U1
                station_name = self.stationen_reihenfolge[i]
                station_info = self.stationen_graph[station_name][0]
                fahrzeit = station_info["fahrtzeit"]
                if fahrzeit:
                    zeit += timedelta(minutes=fahrzeit)
        else:
            # Rückrichtung
            for i in range(von_idx, bis_idx, -1):
                if i < von_idx:
                    zeit += timedelta(seconds=self.haltezeiten[self.stationen_reihenfolge[i]])
                
                # Rückrichtung: nutze die gleiche Fahrzeit
                station_name = self.stationen_reihenfolge[i - 1]
                station_info = self.stationen_graph[station_name][0]
                fahrzeit = station_info["fahrtzeit"]
                if fahrzeit:
                    zeit += timedelta(minutes=fahrzeit)

        return zeit

    def _berechne_abfahrt(self, ankunft: datetime, station: str) -> datetime:
        """Abfahrtszeit an einer Station"""
        if station in self.endhaltestellen:
            return ankunft
        return ankunft + timedelta(seconds=self.haltezeiten[station])

    def _runde_ab(self, dt: datetime) -> datetime:
        """Rundet auf die frühere volle Minute ab"""
        return dt.replace(second=0, microsecond=0)

    def naechste_abfahrt(
        self, start: str, ziel: str, gewuenscht: str
    ) -> Tuple[Optional[datetime], Optional[datetime], bool]:
        """
        Findet die nächste Verbindung
        Returns: (abfahrt, ankunft, ist_naechster_tag)
        """
        start = start.upper()
        ziel = ziel.upper()

        gewuenscht_dt = datetime.combine(
            self.startzeit.date(),
            datetime.strptime(gewuenscht, "%H:%M").time()
        )

        start_idx = self._idx(start)
        ziel_idx = self._idx(ziel)
        ist_hinrichtung = start_idx < ziel_idx
        fuerth_idx = len(self.stationen_reihenfolge) - 1

        zug_start = self.startzeit

        while zug_start <= self.endzeit:
            if ist_hinrichtung:
                ankunft_start = self._berechne_ankunft(zug_start, 0, start_idx)
            else:
                ankunft_fuerth = self._berechne_ankunft(zug_start, 0, fuerth_idx)
                abfahrt_rueck = ankunft_fuerth + timedelta(
                    seconds=self.haltezeiten[self.stationen_reihenfolge[fuerth_idx]]
                )
                ankunft_start = self._berechne_ankunft(abfahrt_rueck, fuerth_idx, start_idx)

            abfahrt_start = self._berechne_abfahrt(ankunft_start, start)
            abfahrt_gerundet = self._runde_ab(abfahrt_start)

            if abfahrt_gerundet >= gewuenscht_dt:
                ankunft_ziel = self._berechne_ankunft(abfahrt_start, start_idx, ziel_idx)
                return abfahrt_gerundet, self._runde_ab(ankunft_ziel), False

            zug_start += timedelta(minutes=self.intervall)

        # Nächster Tag
        naechster_tag = self.startzeit + timedelta(days=1)

        if ist_hinrichtung:
            ankunft_start = self._berechne_ankunft(naechster_tag, 0, start_idx)
        else:
            ankunft_fuerth = self._berechne_ankunft(naechster_tag, 0, fuerth_idx)
            abfahrt_rueck = ankunft_fuerth + timedelta(
                seconds=self.haltezeiten[self.stationen_reihenfolge[fuerth_idx]]
            )
            ankunft_start = self._berechne_ankunft(abfahrt_rueck, fuerth_idx, start_idx)

        abfahrt_start = self._berechne_abfahrt(ankunft_start, start)
        abfahrt_morgen = self._runde_ab(abfahrt_start)
        ankunft_ziel = self._berechne_ankunft(abfahrt_start, start_idx, ziel_idx)
        return abfahrt_morgen, self._runde_ab(ankunft_ziel), True


# ============================================================================
# FACTORY-FUNKTIONEN
# ============================================================================

def erstelle_netz() -> UbahnNetz:
    """Erstellt UbahnNetz mit allen Stationen"""
    netz = UbahnNetz()
    for i, name in enumerate(STATIONEN_REIHENFOLGE, start=1):
        netz.add_station(name, i)
    return netz


def erstelle_console_ui() -> ConsoleUI:
    """Erstellt die komplette ConsoleUI für Sprint 3"""
    netz = erstelle_netz()
    route_finder = RouteFinder(netz, STATIONEN_REIHENFOLGE)
    fahrplan = FahrplanBerechner()

    return ConsoleUI(netz, route_finder, fahrplan)
