# -*- coding: utf-8 -*-
"""
Entry type definitions for calendar records.
"""

from enum import StrEnum

class EntryType(StrEnum):
    """
    Enumeration of possible entry types for calendar records.

    Current types are:
        - WORK: Normal work day
        - FESTIVE: Local or national festivity
        - VACATION: Vacation day
        - COMPENSATED: Compensated day, same as festive
        - WEEKEND: Weekdend day, no work, no vacation, no compensated.
    """
    
    WORK = "work"
    FESTIVE = "festive"
    VACATION = "vacation"
    COMPENSATED = "compensated"
    WEEKEND = "weekend"
