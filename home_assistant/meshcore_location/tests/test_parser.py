"""Basic parser tests that do not require Home Assistant."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


PARSER_PATH = (
    Path(__file__).parents[3]
    / "custom_components"
    / "meshcore_location"
    / "parser.py"
)
SPEC = spec_from_file_location("meshcore_location_parser", PARSER_PATH)
assert SPEC is not None and SPEC.loader is not None
PARSER = module_from_spec(SPEC)
sys.modules[SPEC.name] = PARSER
SPEC.loader.exec_module(PARSER)
find_participants = PARSER.find_participants
parse_location = PARSER.parse_location


MESSAGE = (
    "<Tracking_Private> Tracker_Node_A: test :: "
    "10:19:35 4.16V 19.9C 5% "
    "https://maps.google.com/?q=52.417405,13.363181"
)


def test_finds_participant() -> None:
    """Find a sender from a MeshCore channel line."""
    assert find_participants([MESSAGE]) == ["Tracker_Node_A"]


def test_ignores_icon_attributes_as_participants() -> None:
    """Do not offer Home Assistant icon values as MeshCore participants."""
    assert find_participants(["mdi:message", MESSAGE]) == ["Tracker_Node_A"]


def test_reads_location_and_attributes() -> None:
    """Read GPS and optional telemetry from a matching message."""
    location = parse_location([MESSAGE], "Tracker_Node_A")
    assert location is not None
    assert location.latitude == 52.417405
    assert location.longitude == 13.363181
    assert location.battery_voltage == 4.16
    assert location.temperature == 19.9
    assert location.light_percent == 5.0


def test_finds_multiple_channel_participants_from_history() -> None:
    """Offer each tracker sender found across saved channel messages."""
    history = [
        "<Tracking_Private> Tracker_Node_B: test :: "
        "https://maps.google.com/?q=52.417086,13.362911",
        MESSAGE,
        "<Tracking_Private> Tracker_Node_C: test :: "
        "https://maps.google.com/?q=52.416946,13.363433",
        "mdi:message",
    ]
    assert find_participants(history) == [
        "Tracker_Node_A",
        "Tracker_Node_B",
        "Tracker_Node_C",
    ]
    tracker_c = parse_location(history, "Tracker_Node_C")
    assert tracker_c is not None
    assert tracker_c.latitude == 52.416946
    assert tracker_c.longitude == 13.363433


def test_reads_activity_entry_text_when_name_is_prefixed() -> None:
    """Accept the shape rendered by a Home Assistant activity entry."""
    logbook_text = (
        "Tracking_Private Messages: <Tracking_Private> Tracker_Node_C: test :: "
        "https://maps.google.com/?q=52.416946,13.363433"
    )
    assert find_participants([logbook_text]) == ["Tracker_Node_C"]
