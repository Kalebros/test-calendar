# -*- coding: utf-8 -*-
"""
JSON file-based calendar repository implementation for baco-calendar.
"""

import pytest
from baco_calendar.calendardata.calendar import Calendar
from baco_calendar.calendardata.entry import CalendarEntry
from baco_calendar.calendardata.entrytype import EntryType
from baco_calendar.repositories.json.jsonrepository import JSONCalendarRepository

@pytest.fixture(name="sample_calendar")
def fixture_sample_calendar() -> Calendar:
    """
    Fixture to create a sample calendar for testing.
    """
    calendar = Calendar(name="Test Calendar", identifier="test_calendar")
    entry1 = CalendarEntry(entry_type=EntryType.WORK, entry_date="2024-01-01")
    entry2 = CalendarEntry(entry_type=EntryType.FESTIVE, entry_date="2024-01-02")
    calendar.add_entry(entry1)
    calendar.add_entry(entry2)
    yield calendar
    calendar = Calendar(name="Test Calendar", identifier="test_calendar")
    entry1 = CalendarEntry(entry_type=EntryType.WORK, entry_date="2024-01-01")
    entry2 = CalendarEntry(entry_type=EntryType.FESTIVE, entry_date="2024-01-02")
    calendar.add_entry(entry1)
    calendar.add_entry(entry2)

@pytest.fixture(name="json_repo_config")
def fixture_json_repo_config(tmp_path) -> dict:
    """
    Fixture to create a sample configuration for JSONCalendarRepository.
    """
    file_path = tmp_path / "calendars.json"
    return {
        "type": "JSON",
        "file_path": str(file_path)
    }

def test_json_repository_configuration(json_repo_config: dict) -> None:
    """
    Test that the JSONCalendarRepository can be configured correctly.
    """
    repo = JSONCalendarRepository()
    repo.configure(json_repo_config)
    assert repo._configuration == json_repo_config
    assert not repo._is_open
    assert repo.get_configuration() == json_repo_config

def test_json_repository_open_close(json_repo_config: dict) -> None:
    """
    Test that the JSONCalendarRepository can be opened and closed correctly.
    """
    repo = JSONCalendarRepository()
    repo.configure(json_repo_config)
    repo.open()
    assert repo._is_open
    repo.close()
    assert not repo._is_open

def test_json_repository_save_and_get_calendar(sample_calendar: Calendar, json_repo_config: dict) -> None:
    """
    Test that a calendar can be saved and retrieved from the JSONCalendarRepository.
    """
    repo = JSONCalendarRepository()
    repo.configure(json_repo_config)
    repo.open()
    assert repo.get_calendar(sample_calendar.identifier) is None
    assert len(repo.list_calendars()) == 0

    assert sample_calendar.identifier == "test_calendar"
    saved_calendar = repo.save_calendar(sample_calendar)
    assert saved_calendar is not None

    retrieved_calendar = repo.get_calendar(sample_calendar.identifier)
    assert retrieved_calendar is not None
    assert retrieved_calendar.name == sample_calendar.name
    assert retrieved_calendar.identifier == sample_calendar.identifier
    assert len(retrieved_calendar.get_entries()) == len(sample_calendar.get_entries())
    assert retrieved_calendar.get_entries()[0].entry_type == sample_calendar.get_entries()[0].entry_type
    assert retrieved_calendar.get_entries()[0].entry_date == sample_calendar.get_entries()[0].entry_date
    assert retrieved_calendar.get_entries()[1].entry_type == sample_calendar.get_entries()[1].entry_type
    assert retrieved_calendar.get_entries()[1].entry_date == sample_calendar.get_entries()[1].entry_date
    repo.close()

def test_json_repository_list_open_calendars(sample_calendar: Calendar, json_repo_config: dict) -> None:
    """
    Test that the list_calendars method returns the correct calendars when the repository is open.
    """
    repo = JSONCalendarRepository()
    repo.configure(json_repo_config)
    repo.open()
    assert len(repo.list_calendars()) == 0

    repo.save_calendar(sample_calendar)
    calendars = repo.list_calendars()
    assert len(calendars) == 1
    assert calendars[0].identifier == sample_calendar.identifier
    repo.close()
