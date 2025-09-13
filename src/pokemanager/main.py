"""Main."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import gspread

from pokemanager.utils import combinations


@dataclass(frozen=True)
class Pokemon:
    """A Pokémon with its types."""

    party: bool
    met: str
    name: str
    nickname: str
    type1: str
    type2: str | None = None
    lost: bool = False
    dead: bool = False


@dataclass(frozen=True)
class PkBox:
    """A PC box containing Pokémon."""

    player: str
    pokemons: list[Pokemon]

    def get_active_pokemons(self) -> list[Pokemon]:
        """Get all active Pokémon (not lost or dead)."""
        return [pk for pk in self.pokemons if not (pk.lost or pk.dead)]


def parse_pokemon_sheet(data: list[list[str]]) -> PkBox:
    """Parse a Pokémon sheet into a PC box."""
    pokemons: list[Pokemon] = []
    player = data[0][3]
    for row in data[3:]:
        if row[1] == "":
            continue
        pokemon = Pokemon(
            party=True if row[0] == "TRUE" else False,
            met=row[1],
            name=row[4],
            nickname=row[5],
            type1=row[2],
            type2=row[3] if row[3] != "" else None,
            lost=True if row[6] == "TRUE" else False,
            dead=True if row[7] == "TRUE" else False,
        )
        pokemons.append(pokemon)
    return PkBox(player=player, pokemons=pokemons)


@dataclass(frozen=True)
class Soul:
    """A soul in a soullocke."""

    name: str
    nickname: str
    type1: str
    type2: str | None = None
    lost: bool = False
    dead: bool = False


@dataclass(frozen=True)
class Soullink:
    """A soullink between two Pokémon."""

    party: bool
    met: str
    p1: Soul
    p2: Soul

    def is_lost(self) -> bool:
        """Check if either soul is lost."""
        return self.p1.lost or self.p2.lost

    def is_dead(self) -> bool:
        """Check if either soul is dead."""
        return self.p1.dead or self.p2.dead

    def is_lost_or_dead(self) -> bool:
        """Check if either soul is lost or dead."""
        return self.is_dead() or self.is_lost()

    def get_data(self) -> list[Any]:
        """Get soullink data as a list."""
        return [
            self.party,
            self.met,
            self.p1.type1,
            self.p1.type2,
            self.p1.name,
            self.p1.nickname,
            self.p1.lost,
            self.p1.dead,
            self.p2.type1,
            self.p2.type2,
            self.p2.name,
            self.p2.nickname,
            self.p2.lost,
            self.p2.dead,
        ]


@dataclass(frozen=True)
class SlBox:
    """A soullocke box containing soullinks."""

    player1: str
    player2: str
    soullinks: list[Soullink]

    def get_active_soullinks(self) -> list[Soullink]:
        """Get all active soullinks (not lost or dead)."""
        return [sl for sl in self.soullinks if not sl.is_lost_or_dead()]

    def get_data(self) -> list[list[Any]]:
        """Get soullocke box data as a list of lists."""
        return [
            ["parties", "valid?", "p1", "", "", "", "Totals:", "", "", "", "", "", "Totals:", ""],
            ["", "", "", "", "", "", "losts", "deaths", "", "", "", "", "losts", "deaths"],
            ["Party", "Met", "Type 1", "Type 2", "Pokémon", "Nickname", "Lost", "Dead",
                "Type 1", "Type 2", "Pokémon", "Nickname", "Lost", "Dead"]
        ] + [sl.get_data() for sl in self.soullinks]


def validate_soullocke_team(soullinks: list[Soullink]) -> bool:
    """Validate a soullocke team of 6 or fewer soullinks.

    Returns True if team is valid, otherwise returns False.

    A valid team has no duplicate types, but allows one duplicate if removing one member
    results in a team with all unique types.
    """
    if len(soullinks) > 6:
        return False
    for i in range(len(soullinks)):
        valid = True
        sub_team = soullinks[:i] + soullinks[i+1:]
        seen_types: list[str] = []
        for sl in sub_team:
            if sl.p1.type1 in seen_types or sl.p2.type1 in seen_types:
                valid = False
                break
            seen_types.extend([sl.p1.type1, sl.p2.type1])
        if valid:
            return True
    return False


def parse_soullocke_sheet(data: list[list[str]]) -> SlBox:
    """Parse a soullocke sheet into a Soullocke box."""
    soullinks: list[Soullink] = []
    player1 = data[0][2]
    player2 = data[0][8]
    for row in data[3:]:
        if row[1] == "":
            continue
        p1_soul = Soul(
            name=row[4],
            nickname=row[5],
            type1=row[2],
            type2=row[3] if row[3] != "" else None,
            lost=True if row[6] == "TRUE" else False,
            dead=True if row[7] == "TRUE" else False,
        )
        p2_soul = Soul(
            name=row[10],
            nickname=row[11],
            type1=row[8],
            type2=row[9] if row[9] != "" else None,
            lost=True if row[12] == "TRUE" else False,
            dead=True if row[13] == "TRUE" else False,
        )
        soullink = Soullink(
            party=True if row[0] == "TRUE" else False,
            met=row[1],
            p1=p1_soul,
            p2=p2_soul,
        )
        soullinks.append(soullink)
    return SlBox(player1=player1, player2=player2, soullinks=soullinks)


if __name__ == "__main__":
    service_account_json = Path(R"C:\Users\Ethan\AppData\Roaming\gspread\pokemanager-472012-509deb432125.json")
    # print(*["a", "b", "c"])
    print()
    gc = gspread.service_account(service_account_json)
    sh = gc.open_by_key("1pGHZDsfM1_DWxVWdA_oE1w3R5cMM9xpMyUeBVsBxf3I")
    ws = sh.worksheet("Pokémon Tracker")
    data: list[list[str]] = ws.get_all_values()
    # print(*data, sep="\n")  # Example operation: print all values in the worksheet
    # print()

    soullocke_data: SlBox = parse_soullocke_sheet(data)

    # print(data[0:3], sep="\n")
    # print()
    print(f"{soullocke_data.player1=}")
    print(f"{soullocke_data.player2=}")
    print()
    print(*soullocke_data.get_active_soullinks(), sep="\n")
    print()

    all_active = soullocke_data.get_active_soullinks()
    all_combos: list[list[Soullink]] = combinations(all_active, 6)
    valid_combos = list(filter(validate_soullocke_team, all_combos))
    invalid_combos = list(filter(lambda x: not validate_soullocke_team(x), all_combos))
    print(f"{len(all_active)=}")
    print(f"{len(all_combos)=}")
    print(f"{len(valid_combos)=}")
    print(f"{len(invalid_combos)=}")
    print()
    # print(f"{valid_combos[0]=}")
    # print()
    # print(f"{invalid_combos[0]=}")
    # print()
    data_out = [[poke for sl in team for poke in (sl.p1.name, sl.p2.name)] for team in valid_combos]
    print(*data_out[:3], sep="\n")

    # short_data = [[row[5], row[11]] for row in data]

    worksheet = sh.worksheet("Team Builder")
    padded_data_out = gspread.utils.fill_gaps(data_out, worksheet.row_count, 12)
    worksheet.update(padded_data_out, "A:L")
    print("Updated Team Builder A:L")

    # print(len(combinations(short_data, 6)))
    # print()
