# Sprint_2/classe.py

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


@dataclass
class Fahrplan:
    startzeit: datetime
    endzeit: datetime
    intervall: int
    stationen: Dict[str, List[Dict[str, Any]]]
    stationen_reihenfolge: List[str]

    def finde_linear_weg(self, start: str, ziel: str) -> Optional[List[str]]:
        """Findet den Weg zwischen zwei Stationen in beide Richtungen"""
        start = start.upper()
        ziel = ziel.upper()

        if start not in self.stationen_reihenfolge:
            return None
        if ziel not in self.stationen_reihenfolge:
            return None

        i1 = self.stationen_reihenfolge.index(start)
        i2 = self.stationen_reihenfolge.index(ziel)

        if i1 <= i2:
            # Hinrichtung: Langwasser Süd → Fürth Hbf
            return self.stationen_reihenfolge[i1:i2 + 1]
        else:
            # Rückrichtung: Fürth Hbf → Langwasser Süd
            return list(reversed(self.stationen_reihenfolge[i2:i1 + 1]))

    def berechne_reisezeit(self, weg: List[str]) -> timedelta:
        """Berechnet die Reisezeit entlang eines Weges"""
        gesamt = timedelta()

        for i in range(len(weg) - 1):
            aktuelle = weg[i]
            naechste = weg[i + 1]

            # Suche nach der Verbindung in der bidirektionalen Adjazenzliste
            for v in self.stationen[aktuelle]:
                if v["nachher"] == naechste:
                    gesamt += timedelta(minutes=v["fahrtzeit"])
                    if i < len(weg) - 2:  # Keine Haltezeit am Ziel
                        gesamt += timedelta(seconds=v["haltezeit"])
                    break

        return gesamt

    def dauer_gesamt_hinweg(self) -> timedelta:
        """Berechnet die Gesamtdauer für die komplette Hinfahrt"""
        return self.berechne_reisezeit(self.stationen_reihenfolge)

    def naechste_abfahrt(self, start: str, ziel: str, gewuenscht: str) -> Optional[datetime]:
        """Findet die nächste Abfahrt nach gewünschter Zeit (berücksichtigt Hin- und Rückfahrt)"""
        weg = self.finde_linear_weg(start, ziel)
        if not weg:
            return None

        gewuenscht_dt = datetime.combine(
            self.startzeit.date(),
            datetime.strptime(gewuenscht, "%H:%M").time()
        )

        # Prüfe ob Hinrichtung oder Rückrichtung
        i_start = self.stationen_reihenfolge.index(start.upper())
        i_ziel = self.stationen_reihenfolge.index(ziel.upper())
        ist_hinrichtung = i_start < i_ziel

        zug_start = self.startzeit

        while zug_start <= self.endzeit:
            if ist_hinrichtung:
                # HINFAHRT: Zug startet in Langwasser Süd
                offset = self.berechne_reisezeit(
                    self.finde_linear_weg(self.stationen_reihenfolge[0], start)
                )
                ankunft_start = zug_start + offset

                if ankunft_start >= gewuenscht_dt:
                    return ankunft_start.replace(second=0)
            else:
                # RÜCKFAHRT: Zug muss erst Fürth Hbf erreichen, wenden, dann zurück
                # Zeit bis Fürth Hbf + 60 Sek Wendezeit
                zeit_bis_fuerth = self.dauer_gesamt_hinweg()
                start_rueckfahrt = zug_start + zeit_bis_fuerth + timedelta(seconds=60)

                # Zeit von Fürth Hbf bis zur Startstation
                offset_rueck = self.berechne_reisezeit(
                    self.finde_linear_weg(self.stationen_reihenfolge[-1], start)
                )
                ankunft_start = start_rueckfahrt + offset_rueck

                if ankunft_start >= gewuenscht_dt:
                    return ankunft_start.replace(second=0)

            # Nächster Zug
            zug_start += timedelta(minutes=self.intervall)

        return None