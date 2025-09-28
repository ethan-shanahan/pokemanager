"""Utilities for the CLI."""

from typing import Any

from click import Context, Group, echo

from pokemanager.runtime import Runtime
from pokemanager.structs import SoullockeBox, StandardBox


class CLIRuntime(Runtime):
    """Runtime context for CLI commands."""

    def __init__(self, verbosity: int) -> None:
        """Initialise Runtime."""
        super().__init__()
        self.verbosity = verbosity

    def save_box(self, box: str | StandardBox | SoullockeBox) -> None:
        """Save a box to the appdata directory."""
        self.verb(f"Saving box: {box if isinstance(box, str) else box.name}")
        return super().save_box(box)

    def delete_box(self, box: str | StandardBox | SoullockeBox) -> None:
        """Delete a box from the appdata directory."""
        self.verb(f"Deleting box: {box if isinstance(box, str) else box.name}")
        return super().delete_box(box)

    def verb(self, message: Any) -> None:
        """Print message if verbosity is at least 1."""
        if self.verbosity >= 1:
            echo(message)

    def vverb(self, message: Any) -> None:
        """Print message if verbosity is at least 2."""
        if self.verbosity >= 2:
            echo(message)

    def vvverb(self, message: Any) -> None:
        """Print message if verbosity is at least 3."""
        if self.verbosity >= 3:
            echo(message)


class MainGroup(Group):
    def get_command(self, ctx: Context, cmd_name: str):
        if (cmd := super().get_command(ctx, cmd_name)) is not None:
            return cmd

        # Custom Aliases:
        match cmd_name:
            case "ss":
                return Group.get_command(self, ctx, "spreadsheet")
            case _:
                return None

    # def resolve_command(self, ctx: Context, args: list[str]):
    #     # always return the full command name
    #     _, cmd, args = super().resolve_command(ctx, args)
    #     return cmd.name, cmd, args
