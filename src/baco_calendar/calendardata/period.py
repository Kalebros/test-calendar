# -*- coding: utf-8 -*-
"""
Period definitions for calendar records.
"""

from pydantic import BaseModel

class EntryPeriod(BaseModel):
    """
    Represents a period of calendar entries, defined by a start and end date.
    """
    time_marker: str
    description: str