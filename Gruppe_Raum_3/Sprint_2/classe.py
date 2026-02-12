# Sprint_2/classe.py

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


@dataclass
class Fahrplan:
    startzeit: datetime
    endzeit: datetime
    intervall: int
    stationen_reihenfolge: List[str]
    fahrtzeiten: List[int]
    haltezeiten: dict
    endhaltestellen: set

    def _idx(self, station: str) -> int:
        """Gibt den Index einer Station zurück"""
        return self.stationen_reihenfolge.index(station.upper())

    def _berechne_ankunft(self, zug_abfahrt: datetime, von_idx: int, bis_idx: int) -> datetime:
        """
        Berechnet Ankunftszeit an bis_idx.
        Haltezeiten der Zwischenstationen werden eingerechnet.
        Haltezeit der Startstation wird NICHT eingerechnet.
        Funktioniert für Hin- und Rückrichtung.
        """
        zeit = zug_abfahrt

        if von_idx < bis_idx:
            # Hinrichtung
            for i in range(von_idx, bis_idx):
                if i > von_idx:
                    zeit += timedelta(seconds=self.haltezeiten[self.stationen_reihenfolge[i]])
                zeit += timedelta(minutes=self.fahrtzeiten[i])
        else:
            # Rückrichtung
            for i in range(von_idx, bis_idx, -1):
                if i < von_idx:
                    zeit += timedelta(seconds=self.haltezeiten[self.stationen_reihenfolge[i]])
                zeit += timedelta(minutes=self.fahrtzeiten[i - 1])

        return zeit

    def _berechne_abfahrt(self, ankunft: datetime, station: str) -> datetime:
        """
        Abfahrtszeit an einer Station:
        - Endhaltestellen (LW Süd, Fürth Hbf): direkte Abfahrt, keine extra Haltezeit
        - Alle anderen Stationen: Ankunft + Haltezeit
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
        Findet die nächste Verbindung ab der gewünschten Zeit.

        Logik:
        - Ankunft an Startstation berechnen
        - Abfahrt = Ankunft + Haltezeit (außer Endhaltestellen)
        - Abfahrt auf frühere Minute abrunden
        - Wenn abgerundete Abfahrt >= gewünschte Zeit → diesen Zug nehmen

        Returns:
            (abfahrt_gerundet, ankunft_ziel_gerundet, ist_naechster_tag)
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
                # Ankunft an Startstation von Langwasser Süd
                ankunft_start = self._berechne_ankunft(zug_start, 0, start_idx)
            else:
                # Rückfahrt: bis Fürth Hbf, Wendezeit, dann zurück
                ankunft_fuerth = self._berechne_ankunft(zug_start, 0, fuerth_idx)
                abfahrt_rueck = ankunft_fuerth + timedelta(
                    seconds=self.haltezeiten[self.stationen_reihenfolge[fuerth_idx]]
                )
                ankunft_start = self._berechne_ankunft(abfahrt_rueck, fuerth_idx, start_idx)

            # Abfahrtszeit berechnen und abrunden
            abfahrt_start = self._berechne_abfahrt(ankunft_start, start)
            abfahrt_gerundet = self._runde_ab(abfahrt_start)

            if abfahrt_gerundet >= gewuenscht_dt:
                ankunft_ziel = self._berechne_ankunft(abfahrt_start, start_idx, ziel_idx)
                return abfahrt_gerundet, self._runde_ab(ankunft_ziel), False

            zug_start += timedelta(minutes=self.intervall)

        # Kein Zug heute mehr → ersten Zug morgen berechnen
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