# -*- coding: utf-8 -*-
"""
Calendar data management module for baco-calendar.
"""

from typing import Optional

from copy import deepcopy

from .entry import CalendarEntry
from .entrytype import EntryType
from .period import EntryPeriod

class Calendar:
    """
    Represents a calendar with multiple entries.
    """

    def __init__(self, name: str, identifier: Optional[str] = None) -> None:
        self._identifier: Optional[str] = identifier
        self._name: str = name
        self._entries: list[CalendarEntry] = []

        self._new_entries: list[CalendarEntry] = []
        self._updated_entries: list[CalendarEntry] = []
        self._deleted_entries: list[CalendarEntry] = []

    @property
    def identifier(self) -> Optional[str]:
        """
        Get the unique identifier of the calendar.
        """
        return self._identifier
    
    @identifier.setter
    def identifier(self, value: str) -> None:
        """
        Set the unique identifier of the calendar.
        """
        self._identifier = value
    
    @property
    def name(self) -> str:
        """
        Get the name of the calendar.
        """
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the calendar.
        """
        self._name = value
    
    def add_entry(self, entry: CalendarEntry) -> None:
        """
        Add a new entry to the calendar.
        """
        if entry.entry_date not in [e.entry_date for e in self._entries]:
            self._entries.append(entry)
            self._new_entries.append(entry)
    
    def update_entry(self, entry: CalendarEntry) -> None:
        """
        Update an existing entry in the calendar.
        """
        actual_entry = next((e for e in self._entries if e.entry_date == entry.entry_date), None)
        if actual_entry is not None:
            self._entries.remove(actual_entry)
            self._entries.append(entry)
            self._updated_entries.append(entry)
        else:
            self._new_entries.append(entry)
            self._entries.append(entry)

    def delete_entry(self, entry: CalendarEntry) -> None:
        """
        Delete an entry from the calendar.
        """
        actual_entry = next((e for e in self._entries if e.entry_date == entry.entry_date), None)
        if actual_entry is not None:
            self._entries.remove(actual_entry)
            self._deleted_entries.append(actual_entry)

    def get_entries(self) -> list[CalendarEntry]:
        """
        Get a list of all calendar entries, including new, updated, and deleted entries.
        """
        return Calendar._order_entries(self._entries)
    
    def get_updated_entries(self) -> list[CalendarEntry]:
        """
        Get a list of all updated entries.
        """
        return Calendar._order_entries(self._updated_entries)
    
    def get_new_entries(self) -> list[CalendarEntry]:
        """
        Get a list of all new entries.
        """
        return Calendar._order_entries(self._new_entries)
    
    def get_deleted_entries(self) -> list[CalendarEntry]:
        """
        Get a list of all deleted entries.
        """
        return Calendar._order_entries(self._deleted_entries)
        
    def to_dict(self) -> dict:
        """
        Convert the calendar to a dictionary representation.
        """
        return {
            "identifier": self._identifier,
            "name": self._name,
            "entries": [entry.model_dump() for entry in self.get_entries()]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Calendar":
        """
        Create a Calendar instance from a dictionary representation.
        """
        calendar = cls(name=data["name"], identifier=data.get("identifier"))
        for entry_data in data.get("entries", []):
            entry = CalendarEntry.model_validate(entry_data)
            calendar._entries.append(entry)
        return calendar
    
    def clean_up_entries(self) -> None:
        """
        Clear the lists of new, updated, and deleted entries after they have been processed.
        """
        self._new_entries.clear()
        self._updated_entries.clear()
        self._deleted_entries.clear()
    
    @classmethod
    def _order_entries(cls, entries: list[CalendarEntry]) -> list[CalendarEntry]:
        """
        Order the entries by their date.
        """
        result = deepcopy(entries)
        result.sort(key=lambda e: e.entry_date)
        return result