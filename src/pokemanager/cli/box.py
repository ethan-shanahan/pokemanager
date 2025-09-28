from json import load as json_load
from pathlib import Path
from typing import Literal, Optional, get_args

from click import Choice, File, argument, command, group, option, pass_obj

from pokemanager.cli.utils import CLIRuntime
from pokemanager.const import GAMEMODES
from pokemanager.utils import URL, Database


@group
@pass_obj
def box(rt: CLIRuntime):
    """Box management commands."""
    rt.verb("Boxing...")


@command
@pass_obj
def setup(rt: CLIRuntime):
    """Setup a new box."""
    rt.verb("Setting up...")


@command
@argument("box_name")
@argument("gamemode", type=Choice(get_args(GAMEMODES)))
@argument("credentials", envvar="PKM_CRED", type=File("rb"))
@argument("spreadsheet_url", envvar="PKM_SS_URL", type=URL)
@argument("worksheet_from", envvar="PKM_WS_FROM")
@argument("worksheet_to", envvar="PKM_WS_TO")
@pass_obj
def fetch(
    rt: CLIRuntime,
    box_name: str,
    gamemode: GAMEMODES,
    credentials: File,
    spreadsheet_url: URL,
    worksheet_from: str,
    worksheet_to: str,
) -> None:
    """Fetch a box from a Google Sheets spreadsheet."""
    rt.verb("Fetching...")
    database = Database(
        credentials=json_load(credentials),
        spreadsheet_url=spreadsheet_url,
        worksheet_from=worksheet_from,
        worksheet_to=worksheet_to,
    )
    new_box = rt.fetch_box(box_name=box_name, gamemode=gamemode, database=database)
    rt.save_box(new_box)


@command
@argument("box_name")
@option("-k", "--kind", type=Choice(("default",)), default="default")
@option("-w", "--worksheet-to", default=None)
@pass_obj
def report(rt: CLIRuntime, box_name: str, kind: Literal["default"], worksheet_to: Optional[str]) -> None:
    """Report on a box, uploading to a Google Sheets worksheet."""
    rt.verb("Reporting...")
    rt.report_box(box_name, kind, worksheet_to)


box.add_command(setup)
box.add_command(fetch)
box.add_command(report)
