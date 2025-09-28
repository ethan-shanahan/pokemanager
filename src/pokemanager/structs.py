"""Data structures for Pokemon and Boxes."""

import pickle
from dataclasses import InitVar, dataclass, field
from itertools import combinations
from typing import Generator, Iterable, NamedTuple, Optional, TypeVar, get_args

from pokemanager.const import GAME_TO_GEN, GAMEMODES, GAMES, SCORES, TYPE
from pokemanager.utils import Database, all_equal


class BaseStats(NamedTuple):
    """A named tuple representing a Pokemon's base stats."""

    hp: Optional[int] = None
    attack: Optional[int] = None
    defence: Optional[int] = None
    special_attack: Optional[int] = None
    special_defence: Optional[int] = None
    speed: Optional[int] = None

    @property
    def total(self) -> int:
        """Calculate the base stat total."""
        if all(
            map(
                lambda attr: attr is not None,
                (self.hp, self.attack, self.defence, self.special_attack, self.special_defence, self.speed),
            )
        ):
            return sum((self.hp, self.attack, self.defence, self.special_attack, self.special_defence, self.speed))  # type: ignore
        else:
            raise RuntimeError("Cannot calculate base stat total since base stats are undefined.")


@dataclass
class Pokemon:
    """A class representing a Pokemon."""

    name: str
    nickname: str
    primary_type: InitVar[TYPE]
    secondary_type: InitVar[Optional[TYPE]] = None
    primary: TYPE = field(init=False)
    secondary: TYPE = field(init=False)
    score: float = field(init=False)
    lost: bool = False
    dead: bool = False
    party: bool = False
    met: str = "?"
    stats: BaseStats = field(default_factory=BaseStats)

    def __post_init__(self, primary_type: TYPE, secondary_type: Optional[TYPE]) -> None:
        """Calculate and assign the pokemon's base stat total."""
        self.primary = primary_type

        if secondary_type is not None and secondary_type in get_args(TYPE):
            self.secondary = secondary_type
        else:
            self.secondary = primary_type

        self.score = SCORES[frozenset((self.primary, self.secondary))]


class Soullink:
    """A tuple of Pokemon that are linked in a Soullocke."""

    # __slots__ = ("dead", "lost", "met", "nickname", "party", "score")

    def __init__(self, link: Iterable[Pokemon]) -> None:
        """Initialise the Soullink."""
        self._link = tuple(link)
        if len(self._link) < 2:
            raise RuntimeError("Fewer than 2 pokemon were given to a soullink.")
        self.nickname: str = " & ".join(pk.nickname for pk in self._link)
        self.elected_types: tuple[TYPE, ...] = tuple(pk.primary for pk in self._link)
        self.score: float = sum(pk.score for pk in self._link)
        self.lost: bool = any(pk.lost for pk in self._link)
        self.dead: bool = any(pk.dead for pk in self._link)
        self.party: bool = any(pk.party for pk in self._link)
        if not all_equal(pk.met for pk in self._link):
            raise RuntimeError("Not all pokemon in a soullink were met at the same location.")
        self.met: str = self._link[0].met

    @property
    def active(self) -> bool:
        """Check if the soullink is active (not lost or dead)."""
        return not any((self.lost, self.dead))

    def __len__(self):
        """Allows len(instance)."""
        return len(self._link)

    def __iter__(self):
        """Allows iteration (for item in instance)."""
        return iter(self._link)

    def __getitem__(self, index: int):
        """Allows indexing (instance[0]) and slicing (instance[:2])."""
        return self._link[index]


BoxEntry = TypeVar("BoxEntry", Pokemon, Soullink)


class Box(list[BoxEntry]):
    """A box of Pokemon or Soullinks."""

    def __init__(
        self,
        entries: Iterable[BoxEntry],
        name: str,
        gamemode: GAMEMODES,
        game: GAMES,
        players: tuple[str, ...] = tuple(),
        database: Database = Database(),
    ) -> None:
        """Initialise the box."""
        super().__init__(entries)
        if gamemode == "standard" and not all(isinstance(entry, Pokemon) for entry in self):
            raise RuntimeError("Non-pokemon were given when gamemode is standard.")
        elif gamemode == "soullocke" and not all(isinstance(entry, Soullink) for entry in self):
            raise RuntimeError("Non-soullinks were given when gamemode is soullocke.")
        self.name = name
        self.gamemode = gamemode
        self.game = game
        self.gen = GAME_TO_GEN[game]
        self.players = players
        self.database = database

    def get_active(self) -> Generator[BoxEntry]:
        """Get all active Soullinks (not lost or dead)."""
        raise NotImplementedError("Base Box class must be subclassed.")

    def get_teams(self) -> Generator[tuple[BoxEntry, ...]]:
        """Get all valid teams of 6 Soullinks (or fewer if a team can't be filled)."""
        raise NotImplementedError("Base Box class must be subclassed.")

    def report(self, kind: Optional[str] = "default") -> list[list[str]]:
        """Generate a report of all valid teams of Soullinks."""
        raise NotImplementedError("Base Box class must be subclassed.")


class StandardBox(Box[Pokemon]):
    """A box of Pokemon."""

    pass


class SoullockeBox(Box[Soullink]):
    """A box of Soullinks."""

    def get_active(self) -> Generator[Soullink]:
        """Get all active Soullinks (not lost or dead)."""
        return (entry for entry in self if entry.active)

    def get_teams(self) -> Generator[tuple[Soullink, ...]]:
        """Get all valid teams of 6 Soullinks (or fewer if a team can't be filled)."""
        return (
            team for team in combinations(self.get_active(), max(len([self.get_active()]), 6)) if validate_team(team)
        )

    def report(self, kind: Optional[str] = "default") -> list[list[str]]:
        """Generate a report of all valid teams of Soullinks."""
        if kind != "default":
            raise NotImplementedError("Only one report kind is implemented yet.")
        return [
            [str(sum(sl.score for sl in team))] + [pk.name for sl in team for pk in sl] for team in self.get_teams()
        ]


def validate_team(team: tuple[Soullink, ...]) -> bool:
    """Validate that a team of Soullinks is valid."""
    if len(team) > 6:
        return False
    for i in range(len(team)):
        valid = True
        sub_team = team[:i] + team[i + 1 :]
        seen_types: list[TYPE] = []
        for sl in sub_team:
            if sl.elected_types[0] in seen_types or sl.elected_types[1] in seen_types:
                valid = False
                break
            seen_types.extend(sl.elected_types)
        if valid:
            return True
    return False


if __name__ == "__main__":
    pass
