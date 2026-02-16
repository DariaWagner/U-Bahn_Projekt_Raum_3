# Sprint_3/test.py
"""
Testfälle für Sprint 3
"""

from adjazenzliste import STATIONEN_REIHENFOLGE
from service import erstelle_netz
from classe import Station, Route, TarifRechner, RouteFinder


def test_fuzzy_matching():
    """Testet die Stationserkennung mit Fuzzy-Matching (US 3.1)"""
    print("=" * 80)
    print("TEST: FUZZY-MATCHING (User Story 3.1)".center(80))
    print("=" * 80)

    netz = erstelle_netz()

    test_cases = [
        ("Messe", "MESSE", "TF1: Exakte Übereinstimmung"),
        ("Fürth Hbf.", "FÜRTH HBF", "TF2: Mapping & Punkt (Hbf.)"),
        ("aufseßplatz", "AUFSESSPLATZ", "TF3: Kleinschreibung"),
        ("Aufsessplatz", "AUFSESSPLATZ", "TF4: ß-Ersetzung (ss→ß)"),
        ("Baerenchanze", "BÄRENSCHANZE", "TF5: Umlaute (ae→ä)"),
        ("Maffeiplat", "MAFFEIPLATZ", "TF6: Tippfehler 80%"),
        ("Jakobinenstrase", "JAKOBINENSTRASSE", "TF7: Tippfehler 80%"),
        ("  Gostenhof  ", "GOSTENHOF", "TF8: Leerzeichen (Trim)"),
        ("Langwasser Nord", "LANGWASSER NORD", "TF9: Langer Name"),
        ("Hauptbahnhof", "HAUPTBAHNHOF", "TF10: Eindeutigkeit"),
    ]

    erfolge = 0
    fehler = 0

    for eingabe, erwartet, beschreibung in test_cases:
        matches = netz.integrations(eingabe)

        if len(matches) == 1 and matches[0] == erwartet:
            print(f"✓ {beschreibung}")
            print(f"  Eingabe: '{eingabe}' → Erkannt: '{matches[0]}'")
            erfolge += 1
        else:
            print(f"✗ {beschreibung}")
            print(f"  Eingabe: '{eingabe}' → Erkannt: {matches}")
            print(f"  Erwartet: '{erwartet}'")
            fehler += 1
        print()

    # Negative Tests
    print("-" * 80)
    print("NEGATIVE TESTS:")
    print("-" * 80)

    negative_tests = [
        ("Wasser", "TF11: Zu ungenau (<80%)"),
        ("Flughafen", "TF12: Linienfremd (existiert nicht auf U1)"),
    ]

    for eingabe, beschreibung in negative_tests:
        matches = netz.integrations(eingabe)

        if len(matches) == 0:
            print(f"✓ {beschreibung}")
            print(f"  Eingabe: '{eingabe}' → Keine Treffer (korrekt)")
            erfolge += 1
        else:
            print(f"✗ {beschreibung}")
            print(f"  Eingabe: '{eingabe}' → Treffer: {matches}")
            fehler += 1
        print()

    print("=" * 80)
    print(f"ERGEBNIS: {erfolge} erfolgreich, {fehler} fehlgeschlagen")
    print("=" * 80)


def test_ticketkategorien():
    """Testet die Ticketkategorisierung"""
    print("\n" + "=" * 80)
    print("TEST: TICKETKATEGORISIERUNG".center(80))
    print("=" * 80)

    test_cases = [
        (1, "kurz"), (2, "kurz"), (3, "kurz"),
        (4, "mittel"), (5, "mittel"), (8, "mittel"),
        (9, "lang"), (15, "lang"), (22, "lang"),
    ]

    erfolge = 0
    fehler = 0

    for anzahl, erwartet in test_cases:
        result = TarifRechner.ticketkategorie(anzahl)

        if result == erwartet:
            print(f"✓ {anzahl} Stationen → {result}")
            erfolge += 1
        else:
            print(f"✗ {anzahl} Stationen → {result} (erwartet: {erwartet})")
            fehler += 1

    print("\n" + "=" * 80)
    print(f"ERGEBNIS: {erfolge} erfolgreich, {fehler} fehlgeschlagen")
    print("=" * 80)


def test_route_berechnung():
    """Testet die Routenberechnung"""
    print("\n" + "=" * 80)
    print("TEST: ROUTENBERECHNUNG".center(80))
    print("=" * 80)

    netz = erstelle_netz()
    route_finder = RouteFinder(netz, STATIONEN_REIHENFOLGE)

    test_cases = [
        ("LANGWASSER SÜD", "FÜRTH HBF", 22, "Komplette Strecke"),
        ("MESSE", "PLÄRRER", 9, "Hinrichtung Mitte"),
        ("PLÄRRER", "MESSE", 9, "Rückrichtung Mitte"),
        ("HAUPTBAHNHOF", "LORENZKIRCHE", 1, "Kurze Strecke"),
    ]

    erfolge = 0
    fehler = 0

    for start, ziel, erwartet_stops, beschreibung in test_cases:
        route = route_finder.shortlist_routes(start, ziel)

        if route and route.stops_count == erwartet_stops:
            print(f"✓ {beschreibung}")
            print(f"  {start} → {ziel}: {route.stops_count} Stationen")
            erfolge += 1
        else:
            print(f"✗ {beschreibung}")
            if route:
                print(f"  {start} → {ziel}: {route.stops_count} (erwartet: {erwartet_stops})")
            else:
                print(f"  Keine Route gefunden")
            fehler += 1
        print()

    print("=" * 80)
    print(f"ERGEBNIS: {erfolge} erfolgreich, {fehler} fehlgeschlagen")
    print("=" * 80)


def test_preisberechnung():
    """Testet die Preisberechnung (US 3.2)"""
    print("\n" + "=" * 80)
    print("TEST: PREISBERECHNUNG (User Story 3.2)".center(80))
    print("=" * 80)

    # Test-Routen
    route_kurz = Route([Station(f"S{i}", i) for i in range(1, 4)])  # 2 Stationen
    route_mittel = Route([Station(f"S{i}", i) for i in range(1, 9)])  # 7 Stationen
    route_lang = Route([Station(f"S{i}", i) for i in range(1, 11)])  # 9 Stationen

    test_cases = [
        (route_kurz, True, False, False, 1.65, "Kurz-Einzel, Karte"),
        (route_kurz, True, True, False, 1.32, "Kurz-Einzel, Sozial, Karte"),
        (route_kurz, True, False, True, 1.90, "Kurz-Einzel, Bar"),
        (route_kurz, False, False, False, 5.00, "Kurz-Mehr, Karte"),
        (route_mittel, True, False, False, 2.20, "Mittel-Einzel, Karte"),
        (route_mittel, False, True, False, 5.60, "Mittel-Mehr, Sozial, Karte"),
        (route_lang, True, False, False, 3.30, "Lang-Einzel, Karte"),
        (route_lang, False, False, True, 11.50, "Lang-Mehr, Bar"),
    ]

    erfolge = 0
    fehler = 0

    for route, ist_einzel, sozial, bar, erwartet, beschreibung in test_cases:
        pb = TarifRechner.berechne(route, ist_einzel, sozial, bar)
        preis = TarifRechner.anzahl_tarifen(pb)

        if abs(preis - erwartet) < 0.01:
            print(f"✓ {beschreibung}")
            print(f"  Berechnet: {preis:.2f} € (erwartet: {erwartet:.2f} €)")
            erfolge += 1
        else:
            print(f"✗ {beschreibung}")
            print(f"  Berechnet: {preis:.2f} € (erwartet: {erwartet:.2f} €)")
            fehler += 1
        print()

    print("=" * 80)
    print(f"ERGEBNIS: {erfolge} erfolgreich, {fehler} fehlgeschlagen")
    print("=" * 80)


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + "SPRINT 3 - TESTAUSFÜHRUNG".center(78) + "║")
    print("╚" + "═" * 78 + "╝")

    test_fuzzy_matching()
    test_ticketkategorien()
    test_route_berechnung()
    test_preisberechnung()

    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + "ALLE TESTS ABGESCHLOSSEN".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    print()
