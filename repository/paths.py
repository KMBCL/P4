from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_BASE_ROOT = f"{BASE_DIR.parent}/database"

PLAYER_DIR = Path(f"{DATA_BASE_ROOT}/players.json")
TOURNAMENT_DIR = Path(f"{DATA_BASE_ROOT}/tournaments.json")
MENU_DIR = Path(f"{DATA_BASE_ROOT}/menu.json")
