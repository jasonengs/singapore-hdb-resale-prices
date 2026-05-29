import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

FONT_AWESOME_KIT = os.getenv("FONT_AWESOME_KIT")

FLAT_TYPE_COLORS = {
    "flat_type": {
        "1 Room": {"color": {"base": "#00A6F4", "tint": "#74D4FF"}},
        "2 Room": {"color": {"base": "#FD9A00", "tint": "#FFB86A"}},
        "3 Room": {"color": {"base": "#00C950", "tint": "#7BF1A8"}},
        "4 Room": {"color": {"base": "#FB2C36", "tint": "#FFA2A2"}},
        "5 Room": {"color": {"base": "#AD46FF", "tint": "#DAB2FF"}},
        "Executive": {"color": {"base": "#d4522a", "tint": "#ffa88f"}},
        "Multi-Generation": {"color": {"base": "#F6339A", "tint": "#FDA5D5"}},
    }
}
# Change name
PRIMARY_BASE_COLOR = FLAT_TYPE_COLORS["flat_type"]["1 Room"]["color"]["base"]
PRIMARY_TINT_COLOR = FLAT_TYPE_COLORS["flat_type"]["1 Room"]["color"]["tint"]
SECONDARY_BASE_COLOR = FLAT_TYPE_COLORS["flat_type"]["2 Room"]["color"]["base"]
SECONDARY_TINT_COLOR = FLAT_TYPE_COLORS["flat_type"]["2 Room"]["color"]["tint"]
COLOR_SCALE = [
    [0.0, "#f0f9ff"],
    [0.2, "#DFF2FE"],
    [0.4, "#b8e6fe"],
    [0.6, "#74d4ff"],
    [0.8, "#00bcff"],
    [1.0, "#00a6f4"],
]

NEUTRAL_COLOR = "#ffffff"

TICK_FONT = dict(size=11, color="#6a7282")

HOVER_LABEL_FONT = dict(size=13, color="#101828")
