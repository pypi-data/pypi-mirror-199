import os, sys
import logging
import pathlib
import requests
from P4 import P4, P4Exception
from .utils import console_handler, abort, check_version
from pathlib import Path

log = logging.getLogger(__name__)
help_string = """A utility for managing Unknown projects"""

base_path = pathlib.Path(os.path.dirname(__file__))
commands_folder = base_path / "commands"

from typer import Typer, Context, Argument, Option, echo, secho, confirm, prompt

app = Typer(add_completion=False)

@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def cli(
    ctx: Context,
    #verbose: str = Option(None, "-v", "--verbose", help="Verbose logging: info or debug"),
    #output: str = Option("text", "-o", "--output", help="Output text or json"),
):
    """
    This tool handles the initial setup of Perforce Projects.
    It creates workspaces for you according to naming conventions and sets up a virtual drive.
    Please run the 'project setup' command to get started.
    """
    # by default we log out to console WARN and higher but can view info with -v
    #if verbose:
    #    console_handler.setLevel(getattr(logging, verbose.upper()))
    p4 = P4()
    try:
        p4.connect()
        ignore_file = "s:\\sn2-main\\.p4ignore.txt".lower()
        cfg = Path(p4.env('P4CONFIG'))
        if p4.ignore_file.lower() != ignore_file:
            secho(f"Your p4ignore file should be set to '{ignore_file}', not '{p4.ignore_file}'.", fg="yellow")
            y = confirm(f"Would you like to change the setting in your {cfg} file?")
            if y:
                _lines = []
                lines = []
                with cfg.open() as f:
                    _lines = f.readlines()
                for l in _lines:
                    if not l.upper().startswith("P4IGNORE"):
                        lines.append(l)
                lines.append(f"P4IGNORE={ignore_file}\n")
                with cfg.open("w") as f:
                    f.writelines(lines)
            secho("Your p4config file now contains the following:")
            with cfg.open() as f:
                lines = f.readlines()
                for l in lines:
                    secho(f"{l.strip()}")
            secho("\nYou're all set. Please run your command again.", fg="green")
            exit(0)

    except Exception as e:
        raise
    
    check_version()


from unknowncli.commands import project
from unknowncli.commands import task

app.add_typer(project.app, name="project", help="Manage initial project setup")
app.add_typer(task.app, name="task", help="Manage perforce task streams")
