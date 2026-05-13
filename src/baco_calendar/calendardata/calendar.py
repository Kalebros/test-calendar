# -*- coding: utf-8 -*-
"""
Calendar data management module for baco-calendar.
"""

from typing import Optional

from .entry import CalendarEntry
from .entrytype import EntryType
from .period import EntryPeriod

from pydantic import BaseModel, Field

class Calendar(BaseModel):
    """
    Represents a calendar with multiple entries.
    """
    identifier: Optional[str] = None
    name: str
    description: str
    entries: list[CalendarEntry] = Field(default_factory=list)
