# -*- coding: utf-8 -*-
"""
Main app Typer
"""

from typing import Annotated, Optional
from omegaconf import OmegaConf, DictConfig

import typer
from loguru import logger


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
    
    
@app.command()
def version() -> None:
    logger.info("baco-calendar version 1.0.0")

