"""."""

from dataclasses import InitVar, dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Generic, Literal, Optional, TypeVar

from pokemanager.const import GAME_TO_GEN, GAMES, GENS, SCORES, TYPE, Dual, Type
from pokemanager.utils import URL


@dataclass(frozen=True)
class Soul:
    """A Pokémon Soul."""

    name: str
    nickname: str
    elected_type: InitVar[TYPE]
    auxiliary_type: InitVar[Optional[TYPE]] = None
    type1: Type = field(init=False)
    type2: Optional[Type] = field(init=False)
    lost: bool = False
    dead: bool = False
    score: float = field(init=False)

    def __post_init__(self, elected_type: TYPE, auxiliary_type: Optional[TYPE]):
        """Set type1, type2, and score after initialization."""
        object.__setattr__(self, "type1", Type[elected_type])
        if auxiliary_type is None:
            object.__setattr__(self, "type2", None)
            object.__setattr__(self, "score", SCORES[frozenset((elected_type,))])
        else:
            object.__setattr__(self, "type2", Type[auxiliary_type])
            object.__setattr__(self, "score", SCORES[frozenset((elected_type, auxiliary_type))])


@dataclass(frozen=True)
class Pokemon:
    """A Pokémon."""

    party: bool = field(init=False)
    met: str = field(init=False)
    name: str
    nickname: str
    elected_type: InitVar[TYPE]
    auxiliary_type: InitVar[Optional[TYPE]] = None
    type1: Type = field(init=False)
    type2: Optional[Type] = field(init=False)
    lost: bool = False
    dead: bool = False
    score: float = field(init=False)

    def __post_init__(self, elected_type: TYPE, auxiliary_type: Optional[TYPE]):
        """Set dual and score after initialization."""
        object.__setattr__(self, "type1", Type[elected_type])
        if auxiliary_type is None:
            object.__setattr__(self, "type2", None)
            object.__setattr__(self, "score", SCORES[frozenset((elected_type,))])
        else:
            object.__setattr__(self, "type2", Type[auxiliary_type])
            object.__setattr__(self, "score", SCORES[frozenset((elected_type, auxiliary_type))])

    def is_lost_or_dead(self) -> bool:
        """Check if pokemon is lost or dead."""
        return self.lost or self.dead


@dataclass(frozen=True)
class Soullink:
    """A soullink between two Pokémon souls."""

    party: bool
    met: str
    p1: Soul
    p2: Soul
    name: str = field(init=False)

    def __post_init__(self) -> None:
        """Initialise the name of the soullink."""
        object.__setattr__(self, "name", f"{self.p1.name} & {self.p2.name}")

    def is_lost(self) -> bool:
        """Check if either soul is lost."""
        return self.p1.lost or self.p2.lost

    def is_dead(self) -> bool:
        """Check if either soul is dead."""
        return self.p1.dead or self.p2.dead

    def is_lost_or_dead(self) -> bool:
        """Check if either soul is lost or dead."""
        return self.is_dead() or self.is_lost()

    def get_data(self) -> list[bool | str]:
        """Get soullink data as a list."""
        return [
            self.party,
            self.met,
            self.p1.type1.name,
            self.p1.type2.name if self.p1.type2 else "",
            self.p1.name,
            self.p1.nickname,
            self.p1.lost,
            self.p1.dead,
            self.p2.type1.name,
            self.p2.type2.name if self.p2.type2 else "",
            self.p2.name,
            self.p2.nickname,
            self.p2.lost,
            self.p2.dead,
        ]


class StandardPC(list[Pokemon]):
    """A PC containing Pokémon."""

    def get_active(self) -> "StandardPC":
        """Get all active Pokémon (not lost or dead)."""
        return StandardPC(pk for pk in self if not pk.is_lost_or_dead())


class SoullinkPC(list[Soullink]):
    """A PC containing Soullinks."""

    def get_active(self) -> "SoullinkPC":
        """Get all active Soullinks (not lost or dead)."""
        return SoullinkPC(sl for sl in self if not sl.is_lost_or_dead())

    def get_teams(self) -> list["SoullinkPC"]:
        return [SoullinkPC(team) for team in combinations(self.get_active(), 6) if SoullinkPC(team).validate_as_team()]

    def validate_as_team(self) -> bool:
        if len(self) > 6:
            return False
        for i in range(len(self)):
            valid = True
            sub_team = self[:i] + self[i + 1 :]
            seen_types: list[Type] = []
            for sl in sub_team:
                if sl.p1.type1 in seen_types or sl.p2.type1 in seen_types:
                    valid = False
                    break
                seen_types.extend([sl.p1.type1, sl.p2.type1])
            if valid:
                return True
        return False


@dataclass(frozen=True)
class Box:
    """A box containing Pokémon."""

    name: str
    game: GAMES
    gen: GENS = field(init=False)
    category: Literal["standard", "soullink"]
    pokemon: InitVar[list[Pokemon] | list[Soullink]]
    players: tuple[str, ...] = ()
    credentials: Optional[Path] = None
    spreadsheet_url: Optional[URL] = None
    worksheet_name: Optional[str] = None
    pc: StandardPC | SoullinkPC = field(init=False)

    def __post_init__(self, pokemon: list[Pokemon] | list[Soullink]) -> None:
        """Initialise the box's generation and PC."""
        object.__setattr__(self, "gen", GAME_TO_GEN[self.game])
        match self.category:
            case "standard":
                object.__setattr__(self, "pc", StandardPC(pokemon))
            case "soullink":
                object.__setattr__(self, "pc", SoullinkPC(pokemon))
