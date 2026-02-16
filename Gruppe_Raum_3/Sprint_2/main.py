# Sprint_2/main.py

from service import (
    zeige_stationen,
    eingabe_station_mit_nummer,
    eingabe_zeit,
    erstelle_fahrplan
)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("WILLKOMMEN ZUM FAHRPLAN DER U-BAHN LINIE U1!".center(80))
    print("Langwasser Süd ↔ Fürth Hbf".center(80))
    print("=" * 80)

    # Stationen anzeigen
    zeige_stationen()

    # Start eingeben
    start = eingabe_station_mit_nummer("Geben Sie die Starthaltestelle ein")
    if not start:
        exit(1)
    print(f"✓ Start: {start}")

    # Ziel eingeben (≠ Start)
    while True:
        ziel = eingabe_station_mit_nummer("Geben Sie die Zielhaltestelle ein")
        if not ziel:
            exit(1)
        if start == ziel:
            print("❌ Start und Ziel sind identisch. Bitte andere Station wählen.")
        else:
            print(f"✓ Ziel: {ziel}")
            break

    # Zeit eingeben
    gewuenscht = eingabe_zeit()
    if not gewuenscht:
        print("\n❌ Ungültige Zeiteingabe. Programm wird beendet.")
        exit(1)

    # Fahrplan erstellen und nächste Abfahrt berechnen
    fahrplan = erstelle_fahrplan()
    abfahrt, ankunft, ist_morgen = fahrplan.naechste_abfahrt(start, ziel, gewuenscht)

    # Ausgabe
    print("\n" + "=" * 80)
    print("VERBINDUNG GEFUNDEN".center(80))
    print("=" * 80)

    if ist_morgen:
        print("⚠ ACHTUNG: Betriebsschluss erreicht!".center(80))
        print("Nächste Verbindung erst morgen:".center(80))
        print("-" * 80)

    print(f"  Von:     {start}")
    print(f"  Nach:    {ziel}")
    print(f"  Abfahrt: {abfahrt.strftime('%H:%M')} Uhr")
    print(f"  Ankunft: {ankunft.strftime('%H:%M')} Uhr")
    print("=" * 80)

    print("\nVielen Dank für Ihre Fahrt mit der U-Bahn Nürnberg!")
