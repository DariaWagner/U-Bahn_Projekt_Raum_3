# Sprint_2/main.py

from service import erstelle_fahrplan, eingabe_zeit


if __name__ == "__main__":
    fahrplan = erstelle_fahrplan()
   
    print("=" * 60)
    print("Willkommen zum Fahrplan der U-Bahn Linie U1!")
    print("Langwasser Süd ↔ Fürth Hbf")
    print("=" * 60)
    
    start = None
    ziel = None
    
    while not start:
        start = input("\nGeben Sie die Starthaltestelle ein: ").strip().upper()
        if start not in fahrplan.stationen_reihenfolge:
            print("❌ Ungültige Haltestelle. Bitte versuchen Sie es erneut.")
            start = None
    
    while not ziel:
        ziel = input("Geben Sie die Zielhaltestelle ein: ").strip().upper()
        if ziel not in fahrplan.stationen_reihenfolge:
            print("❌ Ungültige Haltestelle. Bitte versuchen Sie es erneut.")
            ziel = None
        elif start == ziel:
            print("❌ Start und Ziel sind identisch. Bitte wählen Sie unterschiedliche Stationen.")
            ziel = None
    
    # Gewünschte Zeit abfragen
    gewuenscht = eingabe_zeit()
    if not gewuenscht:
        print("\n❌ Ungültige Zeiteingabe. Programm wird beendet.")
        exit()

    # Berechne nächste Abfahrt
    abfahrt = fahrplan.naechste_abfahrt(start, ziel, gewuenscht)
    
    print("\n" + "=" * 60)
    if abfahrt:
        print(f"✓ Nächste Abfahrt von {start} nach {ziel}:")
        print(f"  → {abfahrt.strftime('%H:%M')} Uhr")
    else:
        print("❌ Keine Verbindung gefunden (außerhalb der Betriebszeiten).")
    print("=" * 60)