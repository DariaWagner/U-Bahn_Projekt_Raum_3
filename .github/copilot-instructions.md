# Copilot Instructions for U-Bahn Projekt Teil 2 (OOP)

## Project Overview

This is an educational OOP project modeling a subway (U-Bahn) system. The project continues from `25FIDP_Kurzstrecke` and focuses on object-oriented design patterns. It simulates a transit system with stations, schedules, and route planning.

## Architecture

The codebase follows **Separation of Concerns** principle with distinct modules:

### Core Structure (Gruppe_Raum_3/Sprint_1/)

- **`Sprint_1_Adjazenzliste.py`**: Data layer - adjacency list representation of the transit network
  - `STATIONEN`: Dict mapping station names to connections (form: `{"A": [{"vorher": None, "nachher": "B", "fahrtzeit": 2}]}`)
  - `UHRZEITEN_BETRIEB_LINIE_TEST`: Operating hours and interval (e.g., 5:00-23:00, 10-min intervals)
  - `MAX_VERSUCHE`: Input retry limit (3)

- **`Sprint_1_classe.py`**: Domain model - `Fahrplan` dataclass encapsulates schedule logic
  - `berechne_fahrtzeit_von_start()`: Cumulative travel time from station A to target
  - `berechne_fahrtzeit()`: Travel duration between two stations
  - `naechste_abfahrt()`: Next departure given current time
  - Uses `datetime` for time calculations, all station names uppercase

- **`Sprint_1_main.py`**: Presentation layer - user interaction and I/O
  - Input validation loops: `eingabe_station()` and `eingabe_zeit()` with retry logic
  - `baue_fahrplan()`: Initializes Fahrplan from adjacency list

## Key Conventions

- **Language**: German naming conventions (Stationen, Fahrplan, Fahrtzeit, etc.)
- **Time Format**: 24-hour format "HH:MM", handled via `datetime.strptime()`
- **Station IDs**: Single uppercase letters (A, B, C, D)
- **Graph Representation**: Linear adjacency list (A→B→C→D); unidirectional only in Sprint 1
- **Validation**: All input methods include try-except for time parsing and membership checks
- **Return Types**: Methods return `Optional[...]` when values may be invalid (e.g., unreachable stations)

## Common Workflows

- **Adding a new station**: Update `STATIONEN` dict and `UHRZEITEN_BETRIEB_LINIE_TEST` in Adjazenzliste
- **Modifying schedule logic**: Edit `Fahrplan` methods; verify offset calculations in `berechne_fahrtzeit()`
- **Changing UI flow**: Modify `main()` function; input methods are separate for testability

## Type Hints & Patterns

- Use `@dataclass` for domain models (see `Fahrplan` - no `__init__` needed)
- Type hints on all parameters and returns: `str`, `Optional[int]`, `Dict[str, List[Dict[str, Any]]]`
- Private methods prefixed with `_` (unused in current code but follows Python conventions)
- String normalization: `.strip().upper()` on all user input

## Integration Points

- No external dependencies beyond Python stdlib (`datetime`, `dataclasses`)
- Data flows: Adjazenzliste → Fahrplan → main() → user
- Error handling: Return `None` for invalid states (unreachable stations, times outside operating hours)

## Testing Considerations

- `MAX_VERSUCHE` limits user attempts before exit (useful for testing input boundaries)
- `berechne_fahrtzeit_von_start()` validates station existence before calculation
- Schedule operates in 10-minute intervals; verify time calculations match interval boundaries
