"""App data management."""

from os import getenv
from pathlib import Path
from pickle import dump as pickle_dump
from pickle import load as pickle_load
from sys import platform
from tomllib import load as toml_load
from typing import Any, AnyStr, Generator, Iterable, Mapping, Optional

from gspread import Worksheet, service_account, service_account_from_dict
from gspread.utils import fill_gaps

from pokemanager.const import GAMEMODES
from pokemanager.structs import Pokemon, Soullink, SoullockeBox, StandardBox
from pokemanager.utils import URL, Database, slugify


class Runtime(dict[str, StandardBox | SoullockeBox]):
    """Runtime data."""

    def __init__(self) -> None:
        """Initialise runtime data."""
        if not self.config_file.exists():
            self.make_default_config()
        with self.config_file.open("rb") as f:
            config: dict[str, str] = toml_load(f)
        self.appdata_path = Path(config.get("appdata_path", self.default_appdata_path)).expanduser().resolve()

        super().__init__()
        for box_file in self.appdata_path.joinpath("boxes").glob("*.pkl"):
            with box_file.open("rb") as f:
                box: StandardBox | SoullockeBox = pickle_load(f)
                self[box.name] = box

    @property
    def config_file(self) -> Path:
        """Get the config file path."""
        if platform.startswith("win"):
            return Path(getenv("LOCALAPPDATA", "~\\AppData\\Local") + "\\pokemanager.toml").expanduser().resolve()
        elif platform.startswith("linux"):
            return Path(getenv("XDG_CONFIG_HOME", "~/.config") + "/pokemanager.toml").expanduser().resolve()
        elif platform.startswith("darwin"):
            return Path("~/Library/Application Support/pokemanager/config.toml").expanduser().resolve()
        else:
            raise NotImplementedError(f"Unsupported platform: {platform}")

    def make_default_config(self):
        """Create a default configuration file."""
        with self.config_file.open("w", encoding="utf-8") as f:
            f.writelines(
                (
                    "# pokemanager configuration file\n",
                    "# created by pokemanager\n",
                    "\n",
                    f"appdata = '{self.default_appdata_path}'\n",
                )
            )

    @property
    def default_appdata_path(self) -> Path:
        """Get the default appdata path."""
        if platform.startswith("win"):
            return Path(getenv("APPDATA", "~\\AppData\\Roaming") + "\\pokemanager").expanduser().resolve()
        elif platform.startswith("linux"):
            return Path(getenv("XDG_DATA_HOME", "~/.local/share") + "/pokemanager").expanduser().resolve()
        elif platform.startswith("darwin"):
            return Path("~/Library/Application Support/pokemanager").expanduser().resolve()
        else:
            raise NotImplementedError(f"Unsupported platform: {platform}")

    def save_box(self, box: str | StandardBox | SoullockeBox) -> None:
        """Save a box to the appdata directory."""
        if isinstance(box, str):
            box = self[box]
        box_path: Path = self.appdata_path.joinpath("boxes", f"{slugify(box.name)}.pkl")
        box_path.parent.mkdir(parents=True, exist_ok=True)
        with box_path.open("wb") as f:
            pickle_dump(box, f)

    def delete_box(self, box: str | StandardBox | SoullockeBox) -> None:
        """Delete a box from the appdata directory."""
        if isinstance(box, str):
            box = self[box]
        box_path: Path = self.appdata_path.joinpath("boxes", f"{slugify(box.name)}.pkl")
        if box_path.exists():
            box_path.unlink()

    def fetch_box(self, box_name: str, gamemode: GAMEMODES, database: Database) -> StandardBox | SoullockeBox:
        """Fetch a box from a Google Sheets spreadsheet."""
        if box_name in self:
            raise RuntimeError(f"Box '{box_name}' already exists.")
        raw_data: list[list[str]] = database.get_worksheet("from").get_all_values()
        header: list[list[str]] = raw_data[:3]
        data: list[list[str]] = raw_data[3:]
        match gamemode:
            case "standard":
                raise NotImplementedError("The standard gamemode is not implemented yet.")
                Box = StandardBox
                parsed_header: dict[str, Any] = {"game": "X", "players": (header[0][2], header[0][8])}
                parsed_data: Iterable[Pokemon] = (Pokemon() for ln in data if ln[1] != "")
            case "soullocke":
                box = SoullockeBox
                parsed_header: dict[str, Any] = {"game": "X", "players": (header[0][2], header[0][8])}
                parsed_data: Iterable[Soullink] = (
                    Soullink(
                        (
                            Pokemon(
                                name=ln[4],
                                nickname=ln[5],
                                primary_type=ln[2],
                                secondary_type=ln[3],
                                lost=True if ln[6] == "TRUE" else False,
                                dead=True if ln[7] == "TRUE" else False,
                                party=True if ln[0] == "TRUE" else False,
                                met=ln[1],
                            ),
                            Pokemon(
                                name=ln[10],
                                nickname=ln[11],
                                primary_type=ln[8],
                                secondary_type=ln[9],
                                lost=True if ln[12] == "TRUE" else False,
                                dead=True if ln[13] == "TRUE" else False,
                                party=True if ln[0] == "TRUE" else False,
                                met=ln[1],
                            ),
                        )
                    )
                    for ln in data
                    if ln[1] != ""
                )

        self[box_name] = box(parsed_data, name=box_name, gamemode=gamemode, **parsed_header, database=database)
        return self[box_name]

    def report_box(
        self, box: str | StandardBox | SoullockeBox, kind: Optional[str] = None, worksheet_to: Optional[str] = None
    ):
        if isinstance(box, str):
            box = self[box]
        worksheet: Worksheet = box.database.get_worksheet("to", worksheet_to)
        worksheet.update(fill_gaps(box.report(kind), worksheet.row_count, worksheet.col_count))


if __name__ == "__main__":
    runtime = Runtime()
    print(runtime.appdata_path)
