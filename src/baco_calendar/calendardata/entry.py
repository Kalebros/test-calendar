# -*- coding: utf-8 -*-
"""
Calendar entry definitions.
"""

from pydantic import BaseModel, Field
from datetime import date
from baco_calendar.calendardata.entrytype import EntryType

from baco_calendar.calendardata.period import EntryPeriod

class CalendarEntry(BaseModel):
    """
    Represents a calendar entry with a specific type.
    """
    entry_type: EntryType = EntryType.WORK
    entry_date: date
    periods: list[EntryPeriod] = Field(default_factory=list)

