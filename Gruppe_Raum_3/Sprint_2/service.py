# Sprint_2/service.py

from datetime import datetime, date
from classe import Fahrplan
from adjazenzliste import (
    UHRZEITEN_BETRIEB_LINIE_U1,
    STATIONEN_U1,
    STATIONEN_REIHENFOLGE,
    MAX_VERSUCHE
)


def eingabe_station(alle_stationen: list[str]) -> str | None:
    """Fordert Benutzereingabe für eine Station und validiert sie"""
    for _ in range(MAX_VERSUCHE):
        s = input(f"Haltestelle eingeben aus {alle_stationen}: ").strip().upper()
        if s in alle_stationen:
            return s
        print("Ungültige Haltestelle. Bitte eine gültige Station eingeben.")
    return None


def eingabe_zeit() -> str | None:
    """Fordert Benutzereingabe für eine Uhrzeit und validiert das Format"""
    for _ in range(MAX_VERSUCHE):
        t = input("Gewünschte Zeit eingeben (HH:MM), z.B. 05:08: ").strip()
        try:
            datetime.strptime(t, "%H:%M")
            return t
        except ValueError:
            print("Ungültiges Format. Bitte so eingeben: HH:MM (z.B. 08:07).")
    return None


def erstelle_fahrplan() -> Fahrplan:
    """Erstellt ein Fahrplan-Objekt mit den Daten der Linie U1"""
    heute = date.today()

    start = datetime.combine(
        heute,
        datetime.strptime(UHRZEITEN_BETRIEB_LINIE_U1["start"], "%H:%M").time()
    )

    ende = datetime.combine(
        heute,
        datetime.strptime(UHRZEITEN_BETRIEB_LINIE_U1["ende"], "%H:%M").time()
    )

    return Fahrplan(
        startzeit=start,
        endzeit=ende,
        intervall=int(UHRZEITEN_BETRIEB_LINIE_U1["intervall_minuten"]),
        stationen=STATIONEN_U1,
        stationen_reihenfolge=STATIONEN_REIHENFOLGE
    )