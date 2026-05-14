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
        self._new_entries.append(entry)
    
    def update_entry(self, entry: CalendarEntry) -> None:
        """
        Update an existing entry in the calendar.
        """
        self._updated_entries.append(entry)
    
    def delete_entry(self, entry: CalendarEntry) -> None:
        """
        Delete an entry from the calendar.
        """
        self._deleted_entries.append(entry)
    
    def get_entries(self) -> list[CalendarEntry]:
        """
        Get a list of all calendar entries, including new, updated, and deleted entries.
        """
        return self._build_entry_list()
    
    def get_updated_entries(self) -> list[CalendarEntry]:
        """
        Get a list of all updated entries.
        """
        return deepcopy(self._updated_entries)
    
    def get_new_entries(self) -> list[CalendarEntry]:
        """
        Get a list of all new entries.
        """
        return deepcopy(self._new_entries)
    
    def get_deleted_entries(self) -> list[CalendarEntry]:
        """
        Get a list of all deleted entries.
        """
        return deepcopy(self._deleted_entries)
    
    def _build_entry_list(self) -> list[CalendarEntry]:
        """
        Build the list of calendar entries by applying new, updated, and deleted entries to the existing entries.
        """
        entries = deepcopy(self._entries)
        entries = [entry for entry in entries if entry not in self._deleted_entries]
        entries = [entry for entry in entries if entry not in self._updated_entries
                   and entry not in self._new_entries]
        entries.extend(deepcopy(self._updated_entries))
        entries.extend(deepcopy(self._new_entries))
        return entries
    
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