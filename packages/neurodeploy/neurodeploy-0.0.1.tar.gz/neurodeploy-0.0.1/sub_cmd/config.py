#!/usr/bin/python
from typing import Optional
import typer

import process.nd_config as config


config_app = typer.Typer()


@config_app.callback()
def config_callback():
    print("Save cli config")


@config_app.command("update")
def update_config():
    """
    #update config
    """
    config.save_config()
