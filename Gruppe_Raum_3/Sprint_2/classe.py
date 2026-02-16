# Sprint_2/classe.py

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict


@dataclass
class Fahrplan:
    """
    Repräsentiert den Fahrplan der U-Bahn Linie U1
    Sprint 2: Bidirektionaler Verkehr mit variablen Haltezeiten
    """
    startzeit: datetime
    endzeit: datetime
    intervall: int
    stationen_reihenfolge: List[str]
    stationen_graph: Dict  # STATIONEN_U1 aus adjazenzliste.py
    haltezeiten: Dict[str, int]
    endhaltestellen: set

    def _idx(self, station: str) -> int:
        """Gibt den Index einer Station zurück"""
        return self.stationen_reihenfolge.index(station.upper())

    def _berechne_ankunft(self, zug_abfahrt: datetime, von_idx: int, bis_idx: int) -> datetime:
        """
        Berechnet Ankunftszeit an bis_idx
        Berücksichtigt Fahrtzeiten aus STATIONEN_U1 und Haltezeiten
        """
        zeit = zug_abfahrt

        if von_idx < bis_idx:
            # Hinrichtung
            for i in range(von_idx, bis_idx):
                # Haltezeit an Zwischenstation (nicht am Start)
                if i > von_idx:
                    zeit += timedelta(seconds=self.haltezeiten[self.stationen_reihenfolge[i]])
                
                # Fahrtzeit aus STATIONEN_U1
                station_name = self.stationen_reihenfolge[i]
                fahrtzeit = self.stationen_graph[station_name][0]["fahrtzeit"]
                if fahrtzeit:
                    zeit += timedelta(minutes=fahrtzeit)
        else:
            # Rückrichtung
            for i in range(von_idx, bis_idx, -1):
                # Haltezeit an Zwischenstation
                if i < von_idx:
                    zeit += timedelta(seconds=self.haltezeiten[self.stationen_reihenfolge[i]])
                
                # Fahrtzeit (gleiche Zeit rückwärts)
                station_name = self.stationen_reihenfolge[i - 1]
                fahrtzeit = self.stationen_graph[station_name][0]["fahrtzeit"]
                if fahrtzeit:
                    zeit += timedelta(minutes=fahrtzeit)

        return zeit

    def _berechne_abfahrt(self, ankunft: datetime, station: str) -> datetime:
        """
        Berechnet Abfahrtszeit an einer Station
        Endhaltestellen: Abfahrt = Ankunft (keine zusätzliche Haltezeit)
        Andere Stationen: Abfahrt = Ankunft + Haltezeit
        """
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

        # Durchlaufe alle Züge des Tages
        while zug_start <= self.endzeit:
            if ist_hinrichtung:
                # Direkte Hinfahrt
                ankunft_start = self._berechne_ankunft(zug_start, 0, start_idx)
            else:
                # Rückfahrt: erst nach Fürth Hbf, dann zurück
                ankunft_fuerth = self._berechne_ankunft(zug_start, 0, fuerth_idx)
                wendezeit = timedelta(seconds=self.haltezeiten[self.stationen_reihenfolge[fuerth_idx]])
                abfahrt_rueck = ankunft_fuerth + wendezeit
                ankunft_start = self._berechne_ankunft(abfahrt_rueck, fuerth_idx, start_idx)

            abfahrt_start = self._berechne_abfahrt(ankunft_start, start)
            abfahrt_gerundet = self._runde_ab(abfahrt_start)

            # Prüfe ob dieser Zug passt
            if abfahrt_gerundet >= gewuenscht_dt:
                ankunft_ziel = self._berechne_ankunft(abfahrt_start, start_idx, ziel_idx)
                return abfahrt_gerundet, self._runde_ab(ankunft_ziel), False

            zug_start += timedelta(minutes=self.intervall)

        # Kein Zug mehr heute → nächster Tag
        naechster_tag = self.startzeit + timedelta(days=1)

        if ist_hinrichtung:
            ankunft_start = self._berechne_ankunft(naechster_tag, 0, start_idx)
        else:
            ankunft_fuerth = self._berechne_ankunft(naechster_tag, 0, fuerth_idx)
            wendezeit = timedelta(seconds=self.haltezeiten[self.stationen_reihenfolge[fuerth_idx]])
            abfahrt_rueck = ankunft_fuerth + wendezeit
            ankunft_start = self._berechne_ankunft(abfahrt_rueck, fuerth_idx, start_idx)

        abfahrt_start = self._berechne_abfahrt(ankunft_start, start)
        abfahrt_morgen = self._runde_ab(abfahrt_start)
        ankunft_ziel = self._berechne_ankunft(abfahrt_start, start_idx, ziel_idx)
        
        return abfahrt_morgen, self._runde_ab(ankunft_ziel), True
