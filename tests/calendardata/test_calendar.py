# -*- coding: utf-8 -*-
"""
Tests for the Calendar class in the calendardata module.
"""

from datetime import datetime

import pytest

from baco_calendar.calendardata.calendar import Calendar
from baco_calendar.calendardata.entry import CalendarEntry
from baco_calendar.calendardata.entrytype import EntryType


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

def test_calendar_initialization(sample_calendar: Calendar) -> None:
    """
    Test that the calendar is initialized correctly.
    """
    assert sample_calendar.name == "Test Calendar"
    assert sample_calendar.identifier == "test_calendar"
    assert len(sample_calendar._new_entries) == 2

def test_calendar_add_entry(sample_calendar: Calendar) -> None:
    """
    Test adding a new entry to the calendar.
    """
    new_entry = CalendarEntry(entry_type=EntryType.VACATION, entry_date="2024-01-03")
    sample_calendar.add_entry(new_entry)
    assert len(sample_calendar._new_entries) == 3
    assert sample_calendar._new_entries[-1] == new_entry

def test_calendar_entry_types(sample_calendar: Calendar) -> None:
    """
    Test that the entry types are correctly assigned.
    """
    assert sample_calendar._new_entries[0].entry_type == EntryType.WORK
    assert sample_calendar._new_entries[1].entry_type == EntryType.FESTIVE

def test_calendar_entry_dates(sample_calendar: Calendar) -> None:
    """
    Test that the entry dates are correctly assigned.
    """
    assert sample_calendar._new_entries[0].entry_date == datetime.strptime("2024-01-01", "%Y-%m-%d").date()
    assert sample_calendar._new_entries[1].entry_date == datetime.strptime("2024-01-02", "%Y-%m-%d").date()

def test_calendar_entry_periods(sample_calendar: Calendar) -> None:
    """
    Test that the entry periods are correctly initialized.
    """
    assert sample_calendar._new_entries[0].periods == []
    assert sample_calendar._new_entries[1].periods == []

def test_calendar_entry_modification(sample_calendar: Calendar) -> None:
    """
    Test modifying an existing entry in the calendar.
    """
    modified_entry = CalendarEntry(entry_type=EntryType.COMPENSATED, entry_date="2024-01-01")
    sample_calendar.update_entry(modified_entry)
    assert len(sample_calendar._updated_entries) == 1
    assert sample_calendar._updated_entries[0] == modified_entry
    
    entries = sample_calendar.get_entries()
    assert len(entries) == 2
    assert entries[0].entry_type == EntryType.COMPENSATED
    assert entries[0].entry_date == datetime.strptime("2024-01-01", "%Y-%m-%d").date()
    assert entries[1].entry_type == EntryType.FESTIVE
    assert entries[1].entry_date == datetime.strptime("2024-01-02", "%Y-%m-%d").date()

    assert len(sample_calendar._updated_entries) == 1
    assert sample_calendar._updated_entries[0] == modified_entry

def test_calendar_entry_deletion(sample_calendar: Calendar) -> None:
    """
    Test deleting an existing entry from the calendar.
    """
    entry_to_delete = CalendarEntry(entry_type=EntryType.WORK, entry_date="2024-01-01")
    sample_calendar.delete_entry(entry_to_delete)
    assert len(sample_calendar._deleted_entries) == 1
    assert sample_calendar._deleted_entries[0] == entry_to_delete
    
    entries = sample_calendar.get_entries()
    assert len(entries) == 1
    assert entries[0].entry_type == EntryType.FESTIVE
    assert entries[0].entry_date == datetime.strptime("2024-01-02", "%Y-%m-%d").date()

    assert len(sample_calendar._deleted_entries) == 1
    assert sample_calendar._deleted_entries[0] == entry_to_delete

def test_calendar_cleanup_entries(sample_calendar: Calendar) -> None:
    """
    Test cleaning up the new, updated, and deleted entries in the calendar.
    """
    sample_calendar.clean_up_entries()
    assert len(sample_calendar._new_entries) == 0
    assert len(sample_calendar._updated_entries) == 0
    assert len(sample_calendar._deleted_entries) == 0
