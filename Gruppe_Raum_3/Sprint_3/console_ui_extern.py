# console_ui.py

from typing import Optional, List


class ConsoleUI:
    """
    Konsolen-Benutzeroberfläche für das U-Bahn-Ticket-System
    Handhabt alle Benutzerinteraktionen über die Konsole
    """

    def __init__(self, stationen_reihenfolge: List[str]):
        """
        Initialisiert die ConsoleUI

        Args:
            stationen_reihenfolge: Liste aller verfügbaren Stationen
        """
        self.stationen_reihenfolge = stationen_reihenfolge

    def ask_yes_no(self, frage: str) -> bool:
        """
        Stellt eine Ja/Nein-Frage an den Benutzer

        Args:
            frage: Die zu stellende Frage

        Returns:
            True für Ja, False für Nein
        """
        while True:
            antwort = input(f"{frage} (j/n): ").strip().lower()
            if antwort in ['j', 'ja', 'y', 'yes']:
                return True
            elif antwort in ['n', 'nein', 'no']:
                return False
            else:
                print("❌ Bitte geben Sie 'j' für Ja oder 'n' für Nein ein.")

    def ask_amount(self, prompt: str) -> float:
        """
        Fragt nach einem Geldbetrag

        Args:
            prompt: Die Eingabeaufforderung

        Returns:
            Der eingegebene Betrag als float
        """
        while True:
            try:
                betrag_str = input(f"{prompt}: ").strip().replace(',', '.')
                betrag = float(betrag_str)
                if betrag < 0:
                    print("❌ Der Betrag darf nicht negativ sein.")
                    continue
                return betrag
            except ValueError:
                print("❌ Bitte geben Sie einen gültigen Betrag ein (z.B. 10.50)")

    def choose_start_station(self, ziel: Optional[str] = None) -> str:
        """
        Lässt den Benutzer eine Startstation wählen

        Args:
            ziel: Optional die Zielstation (für Validierung)

        Returns:
            Der Name der gewählten Station (uppercase)
        """
        print("\n📍 Verfügbare Stationen:")

        for i, station in enumerate(self.stationen_reihenfolge, 1):
            print(f"  {i}. {station}")

        while True:
            try:
                auswahl = input("\nWählen Sie die Startstation (Nummer oder Name): ").strip()

                # Versuche als Nummer
                if auswahl.isdigit():
                    index = int(auswahl) - 1
                    if 0 <= index < len(self.stationen_reihenfolge):
                        station = self.stationen_reihenfolge[index]
                        if ziel and station.upper() == ziel.upper():
                            print("❌ Start- und Zielstation dürfen nicht identisch sein.")
                            continue
                        return station
                    else:
                        print(f"❌ Bitte wählen Sie eine Nummer zwischen 1 und {len(self.stationen_reihenfolge)}.")
                        continue

                # Versuche als Name
                station_upper = auswahl.upper()
                if station_upper in self.stationen_reihenfolge:
                    if ziel and station_upper == ziel.upper():
                        print("❌ Start- und Zielstation dürfen nicht identisch sein.")
                        continue
                    return station_upper
                else:
                    print(f"❌ Station '{auswahl}' nicht gefunden. Bitte versuchen Sie es erneut.")

            except ValueError:
                print("❌ Ungültige Eingabe. Bitte geben Sie eine Nummer oder einen Stationsnamen ein.")

    def choose_destination_station(self, start: str) -> str:
        """
        Lässt den Benutzer eine Zielstation wählen

        Args:
            start: Die Startstation (für Validierung)

        Returns:
            Der Name der gewählten Zielstation (uppercase)
        """
        print("\n🎯 Verfügbare Zielstationen:")

        for i, station in enumerate(self.stationen_reihenfolge, 1):
            if station.upper() != start.upper():
                print(f"  {i}. {station}")

        while True:
            try:
                auswahl = input("\nWählen Sie die Zielstation (Nummer oder Name): ").strip()

                # Versuche als Nummer
                if auswahl.isdigit():
                    index = int(auswahl) - 1
                    if 0 <= index < len(self.stationen_reihenfolge):
                        station = self.stationen_reihenfolge[index]
                        if station.upper() == start.upper():
                            print("❌ Start- und Zielstation dürfen nicht identisch sein.")
                            continue
                        return station
                    else:
                        print(f"❌ Bitte wählen Sie eine Nummer zwischen 1 und {len(self.stationen_reihenfolge)}.")
                        continue

                # Versuche als Name
                station_upper = auswahl.upper()
                if station_upper in self.stationen_reihenfolge:
                    if station_upper == start.upper():
                        print("❌ Start- und Zielstation dürfen nicht identisch sein.")
                        continue
                    return station_upper
                else:
                    print(f"❌ Station '{auswahl}' nicht gefunden. Bitte versuchen Sie es erneut.")

            except ValueError:
                print("❌ Ungültige Eingabe. Bitte geben Sie eine Nummer oder einen Stationsnamen ein.")

    def display_welcome(self):
        """Zeigt die Willkommensnachricht an"""
        print("\n" + "="*60)
        print("🚇 Willkommen beim U-Bahn Ticket-Automaten (Linie U3)")
        print("="*60)

    def display_ticket_info(self, ticket_info: dict):
        """
        Zeigt Ticket-Informationen an

        Args:
            ticket_info: Dictionary mit Ticket-Informationen
        """
        print("\n" + "="*60)
        print("🎫 TICKET-INFORMATION")
        print("="*60)

        for key, value in ticket_info.items():
            print(f"{key}: {value}")

        print("="*60)
