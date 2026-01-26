import config

# Konstanten definieren
ZEIT_FORMAT = "%H:%M"
intervall_default = config.INTERVALL_DEFAULT  # in Minuten


# Klasse Fahrplan erstellen mit startzeit: datetime, endzeit: dateime, intervall, stationen: adjacency list
class Fahrplan:
    def __init__(self, startzeit, endzeit, intervall, stationen):
        self.startzeit = startzeit
        self.endzeit = endzeit
        self.intervall = intervall
        self.stationen = stationen
# Fahrzeit berechnen von Startstation zu Zielstation 