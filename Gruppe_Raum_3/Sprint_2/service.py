# Sprint_2/service.py

from datetime import datetime, date
from adjazenzliste import (
    STATIONEN_U1,
    STATIONEN_REIHENFOLGE,
    HALTEZEITEN,
    ENDHALTESTELLEN,
    UHRZEITEN_BETRIEB_LINIE_U1
)
from classe import Fahrplan


def zeige_stationen():
    """Zeigt alle Stationen in 3 Spalten mit Nummerierung"""
    print("\n" + "=" * 80)
    print("VERFÜGBARE STATIONEN DER LINIE U1".center(80))
    print("=" * 80)

    zeilen = (len(STATIONEN_REIHENFOLGE) + 2) // 3
    for i in range(zeilen):
        zeile = ""
        for spalte in range(3):
            idx = i + spalte * zeilen
            if idx < len(STATIONEN_REIHENFOLGE):
                zeile += f"[{idx + 1:2d}] {STATIONEN_REIHENFOLGE[idx]:<24}"
        print(zeile)
    print("=" * 80)


def eingabe_station_mit_nummer(prompt: str, max_versuche: int = 3) -> str:
    """
    Eingabe einer Station per Nummer oder Name
    Returns: Stationsname in Großbuchstaben
    """
    for versuch in range(max_versuche):
        eingabe = input(f"\n{prompt} (Nummer oder Name): ").strip()

        # Nummer?
        if eingabe.isdigit():
            nummer = int(eingabe)
            if 1 <= nummer <= len(STATIONEN_REIHENFOLGE):
                return STATIONEN_REIHENFOLGE[nummer - 1]
            else:
                print(f"❌ Ungültige Nummer. Bitte zwischen 1 und {len(STATIONEN_REIHENFOLGE)} wählen.")
                continue

        # Name?
        eingabe_upper = eingabe.upper()
        if eingabe_upper in STATIONEN_REIHENFOLGE:
            return eingabe_upper
        else:
            print(f"❌ Station '{eingabe}' nicht gefunden.")

    print(f"\n❌ Maximale Anzahl Versuche ({max_versuche}) erreicht.")
    return None


def eingabe_zeit(max_versuche: int = 3) -> str:
    """Eingabe und Validierung der Uhrzeit im Format HH:MM"""
    for _ in range(max_versuche):
        t = input("\nGewünschte Abfahrtszeit (HH:MM), z.B. 05:08: ").strip()
        try:
            datetime.strptime(t, "%H:%M")
            return t
        except ValueError:
            print("❌ Ungültiges Format. Bitte HH:MM eingeben (z.B. 08:07).")
    return None


def erstelle_fahrplan() -> Fahrplan:
    """Factory-Funktion: Erstellt Fahrplan-Objekt"""
    heute = date.today()
    
    startzeit = datetime.combine(
        heute,
        datetime.strptime(UHRZEITEN_BETRIEB_LINIE_U1["start"], "%H:%M").time()
    )
    endzeit = datetime.combine(
        heute,
        datetime.strptime(UHRZEITEN_BETRIEB_LINIE_U1["ende"], "%H:%M").time()
    )
    
    return Fahrplan(
        startzeit=startzeit,
        endzeit=endzeit,
        intervall=int(UHRZEITEN_BETRIEB_LINIE_U1["intervall_minuten"]),
        stationen_reihenfolge=STATIONEN_REIHENFOLGE,
        stationen_graph=STATIONEN_U1,
        haltezeiten=HALTEZEITEN,
        endhaltestellen=ENDHALTESTELLEN
    )
