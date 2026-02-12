# Sprint_2/main.py

from service import (
    erstelle_fahrplan,
    eingabe_zeit,
    zeige_stationen,
    eingabe_station_mit_nummer
)


if __name__ == "__main__":
    fahrplan = erstelle_fahrplan()

    print("\n" + "=" * 80)
    print("WILLKOMMEN ZUM FAHRPLAN DER U-BAHN LINIE U1!".center(80))
    print("Langwasser Süd ↔ Fürth Hbf".center(80))
    print("=" * 80)

    # Alle Stationen anzeigen
    zeige_stationen(fahrplan)

    # Eingabe Start
    start = eingabe_station_mit_nummer(fahrplan, "Geben Sie die Starthaltestelle ein")
    print(f"✓ Start: {start}")

    # Eingabe Ziel
    while True:
        ziel = eingabe_station_mit_nummer(fahrplan, "Geben Sie die Zielhaltestelle ein")
        if start == ziel:
            print("❌ Start und Ziel sind identisch. Bitte wählen Sie eine andere Station.")
        else:
            print(f"✓ Ziel: {ziel}")
            break

    # Zeitabfrage
    gewuenscht = eingabe_zeit()
    if not gewuenscht:
        print("\n❌ Ungültige Zeiteingabe. Programm wird beendet.")
        exit()

    # Berechnung
    abfahrt, ankunft, ist_naechster_tag = fahrplan.naechste_abfahrt(start, ziel, gewuenscht)

    print("\n" + "=" * 80)
    if abfahrt and ankunft:
        print("✓ NÄCHSTE VERBINDUNG".center(80))
        print("-" * 80)

        if ist_naechster_tag:
            print("⚠ ACHTUNG: Betriebsschluss erreicht!".center(80))
            print("Nächste Verbindung erst morgen:".center(80))
            print("-" * 80)

        print(f"  Von:      {start}")
        print(f"  Nach:     {ziel}")
        print(f"  Abfahrt:  {abfahrt.strftime('%H:%M')} Uhr")
        print(f"  Ankunft:  {ankunft.strftime('%H:%M')} Uhr")
    else:
        print("❌ Keine Verbindung gefunden.".center(80))
    print("=" * 80 + "\n")