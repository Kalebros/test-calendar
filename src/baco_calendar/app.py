# -*- coding: utf-8 -*-
"""
Main app Typer
"""

from typing import Annotated, Optional
from omegaconf import OmegaConf, DictConfig

import typer
from loguru import logger

from baco_calendar.calendardata.calendar import Calendar
from baco_calendar.calendardata.entry import CalendarEntry
from baco_calendar.calendardata.entrytype import EntryType

from baco_calendar.repositories.abstract import CalendarRepository
from baco_calendar.repositories.json.jsonrepository import JSONCalendarRepository



app = typer.Typer(
    name="baco-calendar",
    help="A calendar application for managing events and schedules.",
    no_args_is_help=True,
)

@app.command()
def launch(configuration: Annotated[str, typer.Option(..., help="Path to the configuration file")] = "") -> None:
    """
    Launch the baco-calendar application with the specified configuration.
    """
    config: Optional[DictConfig] = None
    if configuration == "":
        config = OmegaConf.create(
            {
                "bcalendar": {
                    "data-repository": {
                        "type": "json",
                        "configuration": {
                            "file-path": "repositories/calendar-data.json"
                        }
                    }
                }
            }
        )
        logger.info("Using default configuration")
    else:
        config = OmegaConf.load(configuration)
        logger.info(f"Using configuration from {configuration}")
    # Launch application with configuration
    repo_config = config.get("bcalendar", {}).get("data-repository", {})
    
    rep_json = JSONCalendarRepository()
    rep_json.configure(repo_config)
    rep_json.open()
    logger.info("baco-calendar launched successfully")
    new_calendar = Calendar(name="My Calendar")
    new_calendar.add_entry(CalendarEntry(entry_type=EntryType.WORK, entry_date="2024-01-01"))
    rep_json.save_calendar(new_calendar)
    rep_json.close()
    

    
    
@app.command()
def version() -> None:
    logger.info("baco-calendar version 1.0.0")

