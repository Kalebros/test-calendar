# -*- coding: utf-8 -*-
"""
Abstract repository interface for calendar data management.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from omegaconf import DictConfig

from baco_calendar.calendardata.calendar import Calendar


class CalendarRepository(ABC):
    """
    Abstract base class for calendar data repositories.
    """

    @abstractmethod
    def configure(self, configuration: Dict[str, Any] | DictConfig ) -> None:
        """
        Configure the repository with the given settings.
        """
        pass

    @abstractmethod
    def open(self) -> None:
        """
        Open the repository for operations.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close the repository and release any resources.
        """
        pass

    @abstractmethod
    def get_configuration(self) -> Dict[str, Any]:
        """
        Retrieve the current configuration of the repository.
        """
        pass

    @abstractmethod
    def get_calendar(self, identifier: str) -> Optional[Calendar]:
        """
        Retrieve a calendar by its identifier.
        """
        pass

    @abstractmethod
    def list_calendars(self) -> List[Calendar]:
        """
        List all available calendars in the repository.
        """
        pass

    @abstractmethod
    def save_calendar(self, calendar: Calendar) -> Calendar | None:
        """
        Save a calendar to the repository.
        """
        pass

    @abstractmethod
    def delete_calendar(self, identifier: str) -> None:
        """
        Delete a calendar from the repository by its identifier.
        """
        pass