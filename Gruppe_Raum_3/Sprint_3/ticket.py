# Sprint_2/ticket.py

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TicketKategorie(Enum):
    """Ticket-Kategorien basierend auf Anzahl der Stationen"""
    KURZ = "Kurzticket"      # 1-3 Stationen
    MITTEL = "Mittelticket"  # 4-8 Stationen
    LANG = "Langticket"      # 9+ Stationen


class TicketArt(Enum):
    """Art des Tickets"""
    EINZEL = "Einzelticket"
    MEHRFAHRT = "Mehrfahrtenticket"  # 4 Fahrten


class Zahlart(Enum):
    """Zahlungsmethode"""
    BAR = "Barzahlung"
    BARGELDLOS = "Bargeldlose Zahlung"


@dataclass
class Ticketpreis:
    """Speichert alle Preisinformationen für ein Ticket"""
    kategorie: TicketKategorie
    art: TicketArt
    zahlart: Zahlart
    hat_sozialrabatt: bool
    anzahl_stationen: int
    
    # Basispreise gemäß Spezifikation
    _BASISPREISE_EINZEL = {
        TicketKategorie.KURZ: 1.50,
        TicketKategorie.MITTEL: 2.00,
        TicketKategorie.LANG: 3.00
    }
    
    _BASISPREISE_MEHRFAHRT = {
        TicketKategorie.KURZ: 5.00,
        TicketKategorie.MITTEL: 7.00,
        TicketKategorie.LANG: 10.00
    }
    
    # Zuschläge und Rabatte
    _EINZELTICKET_ZUSCHLAG = 0.10  # +10%
    _SOZIALRABATT = 0.20           # -20%
    _BAR_ZUSCHLAG = 0.15           # +15%
    
    @staticmethod
    def bestimme_kategorie(anzahl_stationen: int) -> TicketKategorie:
        """Bestimmt die Ticket-Kategorie basierend auf der Anzahl der Stationen"""
        if anzahl_stationen <= 3:
            return TicketKategorie.KURZ
        elif anzahl_stationen <= 8:
            return TicketKategorie.MITTEL
        else:
            return TicketKategorie.LANG
    
    def berechne_basispreis(self) -> float:
        """Berechnet den Basispreis ohne Zuschläge/Rabatte"""
        if self.art == TicketArt.EINZEL:
            return self._BASISPREISE_EINZEL[self.kategorie]
        else:
            return self._BASISPREISE_MEHRFAHRT[self.kategorie]
    
    def berechne_endpreis(self) -> float:
        """
        Berechnet den Endpreis mit allen Zuschlägen und Rabatten
        
        Berechnungsreihenfolge:
        1. Basispreis
        2. + Ticketart-Zuschlag (nur Einzelticket)
        3. - Sozialrabatt (falls berechtigt)
        4. + Zahlart-Zuschlag (nur Barzahlung)
        """
        preis = self.berechne_basispreis()
        
        # Schritt 1: Ticketart-Zuschlag für Einzeltickets
        if self.art == TicketArt.EINZEL:
            preis += preis * self._EINZELTICKET_ZUSCHLAG
        
        # Schritt 2: Sozialrabatt anwenden
        if self.hat_sozialrabatt:
            preis -= preis * self._SOZIALRABATT
        
        # Schritt 3: Zahlart-Zuschlag für Barzahlung
        if self.zahlart == Zahlart.BAR:
            preis += preis * self._BAR_ZUSCHLAG
        
        return round(preis, 2)
    
    def erstelle_preisaufschluesselung(self) -> dict:
        """Erstellt eine detaillierte Aufschlüsselung der Preisberechnung"""
        aufschluesselung = {
            "basispreis": self.berechne_basispreis(),
            "zuschlaege": [],
            "rabatte": [],
            "endpreis": self.berechne_endpreis()
        }
        
        # Ticketart-Zuschlag
        if self.art == TicketArt.EINZEL:
            betrag = self.berechne_basispreis() * self._EINZELTICKET_ZUSCHLAG
            aufschluesselung["zuschlaege"].append({
                "beschreibung": "Einzelticket-Zuschlag (+10%)",
                "betrag": round(betrag, 2)
            })
        
        # Sozialrabatt
        if self.hat_sozialrabatt:
            # Rabatt auf Preis nach Ticketart-Zuschlag
            basis = self.berechne_basispreis()
            if self.art == TicketArt.EINZEL:
                basis += basis * self._EINZELTICKET_ZUSCHLAG
            betrag = basis * self._SOZIALRABATT
            aufschluesselung["rabatte"].append({
                "beschreibung": "Sozialrabatt (-20%)",
                "betrag": round(betrag, 2)
            })
        
        # Zahlart-Zuschlag
        if self.zahlart == Zahlart.BAR:
            # Zuschlag auf Preis nach allen vorherigen Schritten
            basis = self.berechne_basispreis()
            if self.art == TicketArt.EINZEL:
                basis += basis * self._EINZELTICKET_ZUSCHLAG
            if self.hat_sozialrabatt:
                basis -= basis * self._SOZIALRABATT
            betrag = basis * self._BAR_ZUSCHLAG
            aufschluesselung["zuschlaege"].append({
                "beschreibung": "Barzahlungs-Zuschlag (+15%)",
                "betrag": round(betrag, 2)
            })
        
        return aufschluesselung
    
    def __str__(self) -> str:
        """String-Repräsentation für Ausgabe"""
        return (f"{self.kategorie.value} | {self.art.value} | "
                f"{self.zahlart.value} | "
                f"Sozialrabatt: {'Ja' if self.hat_sozialrabatt else 'Nein'}")


def erstelle_ticket(anzahl_stationen: int, 
                    ist_mehrfahrt: bool,
                    ist_barzahlung: bool,
                    hat_sozialrabatt: bool) -> Ticketpreis:
    """
    Factory-Funktion zum Erstellen eines Ticketpreis-Objekts
    
    Args:
        anzahl_stationen: Anzahl der zu fahrenden Stationen
        ist_mehrfahrt: True für Mehrfahrtenticket, False für Einzelticket
        ist_barzahlung: True für Barzahlung, False für bargeldlose Zahlung
        hat_sozialrabatt: True wenn Sozialrabatt berechtigt
    
    Returns:
        Ticketpreis-Objekt mit berechneten Preisen
    """
    kategorie = Ticketpreis.bestimme_kategorie(anzahl_stationen)
    art = TicketArt.MEHRFAHRT if ist_mehrfahrt else TicketArt.EINZEL
    zahlart = Zahlart.BAR if ist_barzahlung else Zahlart.BARGELDLOS
    
    return Ticketpreis(
        kategorie=kategorie,
        art=art,
        zahlart=zahlart,
        hat_sozialrabatt=hat_sozialrabatt,
        anzahl_stationen=anzahl_stationen
    )
