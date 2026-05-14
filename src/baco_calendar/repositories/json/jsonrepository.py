# -*- coding: utf-8 -*-
"""
JSON file-based calendar repository implementation for baco-calendar.
"""

from datetime import date
import json
from typing import Dict, Any, Optional, List
from pathlib import Path

from baco_calendar.calendardata.calendar import Calendar
from baco_calendar.calendardata.entry import CalendarEntry
from baco_calendar.repositories.abstract import CalendarRepository
from baco_calendar.exceptions.calendarerror import CalendarConfigurationError, CalendarNotFoundError, CalendarRepositoryError

from loguru import logger

class JSONCalendarRepository(CalendarRepository):
    """
    Calendar repository implementation that uses JSON files for storage.
    """

    def __init__(self) -> None:
        self._configuration: Optional[Dict[str, Any]] = None
        self._calendars: Dict[str, Calendar] = {}
        self._is_open: bool = False
    
    @classmethod
    def _generate_identifier(cls) -> str:
        """
        Generate a unique identifier for a new calendar.
        """
        import uuid
        return str(uuid.uuid4())
    
    def configure(self, configuration: Dict[str, Any]) -> None:
        """
        Configure the repository with the given settings.
        """
        logger.info("Configuring JSONCalendarRepository with provided configuration.")
        if self._is_open:
            raise CalendarRepositoryError("Cannot configure repository while it is open. Please close it first.")
        
        if configuration.get('type', '').upper() != 'JSON':
            raise CalendarConfigurationError("Invalid configuration type for JSONCalendarRepository")
        
        self._configuration = configuration
        if self._configuration.get('configuration', {}).get('file-path') is None:
            raise CalendarConfigurationError("Missing 'file-path' in configuration for JSONCalendarRepository")
        
    def open(self) -> None:
        """
        Open the repository for operations.
        """
        logger.info("Opening JSONCalendarRepository.")
        if self._configuration is None:
            raise CalendarConfigurationError("Repository configuration is not set. Please configure the repository before opening.")
        

        file_path = Path(self._configuration['configuration']['file-path'])
        if file_path.exists() and not file_path.is_file():
            raise CalendarConfigurationError(f"Configured file path '{file_path}' is not a valid file.")
        if file_path.exists():
            try:
                with file_path.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                    for cal_data in data.get('calendars', []):
                        calendar = Calendar(name=cal_data['name'], identifier=cal_data['identifier'])
                        for entry_data in cal_data.get('entries', []):
                            entry = CalendarEntry(
                                entry_type=entry_data['entry_type'],
                                entry_date=date.fromisoformat(entry_data['entry_date'])
                            )
                            calendar._entries.append(entry)
                        self._calendars[calendar.identifier] = calendar
                self._is_open = True
            except json.JSONDecodeError as e:
                raise CalendarRepositoryError(f"Failed to parse JSON calendar repository file: {str(e)}")
        else:
            logger.info("JSON calendar repository file does not exist. Starting with an empty repository.")
            self._calendars = {}
            self._is_open = True
    
    def close(self) -> None:
        """
        Close the repository and release any resources.
        """
        logger.info("Closing JSONCalendarRepository.")

        file_path = Path(self._configuration['configuration']['file-path'])
        try:
            for calendar in self._calendars.values():
                calendar.get_entries()
            with file_path.open('w', encoding='utf-8') as f:
                data = {
                    'calendars': [
                        JSONCalendarRepository._parse_calendar_to_json(cal.to_dict()) for cal in self._calendars.values()
                    ]
                }
                json.dump(data, f, indent=4)
            self._calendars = {}
            self._is_open = False
        except Exception as e:
            raise CalendarRepositoryError(f"Failed to write to JSON calendar repository file: {str(e)}")
        
        self._calendars = {}
        self._is_open = False
    
    def get_configuration(self) -> Dict[str, Any]:
        """
        Retrieve the current configuration of the repository.
        """
        if self._configuration is None:
            raise CalendarConfigurationError("Repository configuration is not set.")
        return self._configuration
    
    def get_calendar(self, identifier: str) -> Optional[Calendar]:
        """
        Retrieve a calendar by its identifier.
        """
        if not self._is_open:
            raise CalendarRepositoryError("Repository is not open. Please open the repository before accessing calendars.")
        
        calendar = self._calendars.get(identifier)
        return calendar
        
    def list_calendars(self) -> List[Calendar]:
        """
        List all available calendars in the repository.
        """
        if not self._is_open:
            raise CalendarRepositoryError("Repository is not open. Please open the repository before accessing calendars.")
        
        return list(self._calendars.values())
    
    def save_calendar(self, calendar: Calendar) -> Calendar | None:
        """
        Add a new calendar to the repository.
        """
        if not self._is_open:
            raise CalendarRepositoryError("Repository is not open. Please open the repository before adding calendars.")
        
        if calendar.identifier in self._calendars:
            raise CalendarRepositoryError(f"A calendar with identifier '{calendar.identifier}' already exists in the repository.")
        
        if calendar.identifier is None:
            calendar.identifier = self._generate_identifier()
        
        self._calendars[calendar.identifier] = calendar
        return calendar
    
    def delete_calendar(self, identifier: str) -> None:
        """
        Delete a calendar from the repository by its identifier.
        """
        if not self._is_open:
            raise CalendarRepositoryError("Repository is not open. Please open the repository before deleting calendars.")
        
        if identifier not in self._calendars:
            raise CalendarNotFoundError(f"Calendar with identifier '{identifier}' not found in the repository.")
        
        del self._calendars[identifier]
    
    @classmethod
    def _parse_calendar_to_json(cls, raw_calendar_data: dict) -> dict:
        """
        Convert a Calendar object to a JSON-serializable dictionary.
        """
        for entry in raw_calendar_data.get('entries', []):
            if isinstance(entry.get('entry_date'), date):
                entry['entry_date'] = entry['entry_date'].isoformat()
        return raw_calendar_data
