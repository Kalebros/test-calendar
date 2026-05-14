# -*- coding: utf-8 -*-

from enum import IntEnum

class CalendarErrorCode(IntEnum):
    """
    Enumeration of calendar error codes.
    """
    CALENDAR_NOT_FOUND = 310
    CONFIGURATION_ERROR = 311
    REPOSITORY_ERROR = 312

class CalendarError(Exception):
    """
    Base exception class for calendar-related errors.
    """
    def __init__(self, code: int, msg: str) -> None:
        super().__init__(msg)
        self.message = msg
        self.internal_code = code

    def __repr__(self) -> str:
        return f"CalendarError(code={self.internal_code}, message='{self.message}')"

class CalendarNotFoundError(CalendarError):
    """
    Exception raised when a calendar is not found in the repository.
    """
    def __init__(self,msg: str = 'Calendar by identifier not found') -> None:
        super().__init__(CalendarErrorCode.CALENDAR_NOT_FOUND, msg)

class CalendarConfigurationError(CalendarError):
    """
    Exception raised for errors in calendar repository configuration.
    """
    def __init__(self, msg: str = 'Invalid calendar repository configuration.') -> None:
        super().__init__(CalendarErrorCode.CONFIGURATION_ERROR, msg)

class CalendarRepositoryError(CalendarError):
    """
    Exception raised for general errors in calendar repository operations.
    """
    def __init__(self, msg: str = 'General calendar repository error') -> None:
        super().__init__(CalendarErrorCode.REPOSITORY_ERROR, msg)