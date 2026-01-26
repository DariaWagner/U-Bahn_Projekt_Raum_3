# Bereit zum Dienst, Meisterin.

from datetime import datetime, date

import Sprint_1_Adjazenzliste
from Sprint_1_classe import Fahrplan


def baue_fahrplan() -> Fahrplan:
    heute = date.today()

    start = datetime.combine(heute, datetime.strptime(Sprint_1_Adjazenzliste.UHRZEITEN_BETRIEB_LINIE_TEST["start"], "%H:%M").time())
    ende = datetime.combine(heute, datetime.strptime(Sprint_1_Adjazenzliste.UHRZEITEN_BETRIEB_LINIE_TEST["ende"], "%H:%M").time())
    intervall = int(Sprint_1_Adjazenzliste.UHRZEITEN_BETRIEB_LINIE_TEST["intervall_minuten"])

    return Fahrplan(
        startzeit=start,
        endzeit=ende,
        intervall=intervall,
        stationen=Sprint_1_Adjazenzliste.STATIONEN
    )

def eingabe_station(alle_stationen: list[str]) -> str | None:
    for _ in range(Sprint_1_Adjazenzliste.MAX_VERSUCHE):
        s = input(f"Haltestelle eingeben {alle_stationen}: ").strip().upper()
        if s in alle_stationen:
            return s
        print("Ungültige Haltestelle. Bitte A, B, C oder D eingeben.")
    return None


def eingabe_zeit() -> str | None:
    for _ in range(Sprint_1_Adjazenzliste.MAX_VERSUCHE):
        t = input("Gewünschte Zeit eingeben (HH:MM), z.B. 05:08: ").strip()
        try:
            datetime.strptime(t, "%H:%M")
            return t
        except ValueError:
            print("Ungültiges Format. Bitte so eingeben: HH:MM (z.B. 08:07).")
    return None


def main():
    fahrplan = baue_fahrplan()
    alle_stationen = sorted(list(Sprint_1_Adjazenzliste.STATIONEN.keys()))

    print("\n--- U-Test Fahrplanauskunft (Sprint 1) ---")
    print("Strecke: A -> B (2min) -> C (3min) -> D (1min)")
    print("Takt: alle 10 Minuten | erste Abfahrt A: 05:00 | letzte Abfahrt A: 23:00\n")

    station = eingabe_station(alle_stationen)
    if station is None:
        print("Zu viele falsche Eingaben. Programm endet.")
        return

    zeit = eingabe_zeit()
    if zeit is None:
        print("Zu viele falsche Eingaben. Programm endet.")
        return

    naechste = fahrplan.naechste_abfahrt(station, zeit)
    if naechste is None:
        print(f"Keine Bahn mehr an Station {station} nach {zeit}.")
    else:
        print(f"Die nächste Bahn fährt um {naechste.strftime('%H:%M')} Uhr an Station {station} ab.")


if __name__ == "__main__":
    main()
