# Sprint_2/service.py

from datetime import datetime, date
from classe import Fahrplan
from adjazenzliste import (
    UHRZEITEN_BETRIEB_LINIE_U1,
    STATIONEN_REIHENFOLGE,
    FAHRTZEITEN,
    HALTEZEITEN,
    ENDHALTESTELLEN,
    MAX_VERSUCHE
)


def zeige_stationen(fahrplan: Fahrplan) -> None:
    """Zeigt alle Stationen in drei Spalten mit Nummerierung"""
    stationen = fahrplan.stationen_reihenfolge
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


def eingabe_station_mit_nummer(fahrplan: Fahrplan, prompt: str) -> str:
    """Erlaubt Eingabe per Nummer oder Stationsname"""
    stationen = fahrplan.stationen_reihenfolge

    while True:
        eingabe = input(f"\n{prompt} (Nummer oder Name): ").strip()

        if eingabe.isdigit():
            nummer = int(eingabe)
            if 1 <= nummer <= len(stationen):
                return stationen[nummer - 1]
            else:
                print(f"❌ Ungültige Nummer. Bitte zwischen 1 und {len(stationen)} wählen.")
        else:
            eingabe_upper = eingabe.upper()
            if eingabe_upper in stationen:
                return eingabe_upper
            else:
                print("❌ Ungültige Station. Bitte Nummer oder vollständigen Namen eingeben.")


def eingabe_zeit() -> str | None:
    """Fordert Benutzereingabe für eine Uhrzeit und validiert das Format"""
    for _ in range(MAX_VERSUCHE):
        t = input("\nGewünschte Abfahrtszeit eingeben (HH:MM), z.B. 05:08: ").strip()
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
        stationen_reihenfolge=STATIONEN_REIHENFOLGE,
        fahrtzeiten=FAHRTZEITEN,
        haltezeiten=HALTEZEITEN,
        endhaltestellen=ENDHALTESTELLEN
    )