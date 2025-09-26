"""CLI commands for managing Pokémon."""

from argparse import Namespace

from pokemanager.data import Box, Pokemon, Soullink
from pokemanager.main import AppData


def pokemon(commands: list[str]):
    """Manage Pokémon."""
    print("Managing Pokémon...")


def pokemon_add(commands: Namespace):
    """Add a Pokémon to a box."""
    print(f"Adding Pokémon to box {commands.box_name} with data: {commands.pokemon_data}")


def pokemon_remove(commands: Namespace):
    """Remove a Pokémon from a box."""
    print(f"Removing Pokémon with ID {commands.pokemon_id} from box {commands.box_name}")


def pokemon_move(commands: Namespace):
    """Move a Pokémon from one box to another."""
    print(
        f"Moving Pokémon with ID {commands.pokemon_id} from box {commands.from_box_name} to box {commands.to_box_name}"
    )


def pokemon_list(args: Namespace):
    """List all Pokémon in a box."""
    print(f"Listing all Pokémon in box {args.box_name}")
    app_data = AppData()
    if args.box_name not in app_data.boxes:
        print(f"Box '{args.box_name}' not found.")
        return
    for entry in app_data.boxes[args.box_name].pc:
        print(f"- {entry.name}")


def pokemon_show(args: Namespace):
    """Show information about a Pokémon."""
    print(f"Showing Pokémon {args.name} in box {args.box_name}")
    app_data = AppData()
    if args.box_name not in app_data.boxes:
        print(f"Box '{args.box_name}' not found.")
        return
    for entry in app_data.boxes[args.box_name].pc:
        if entry.name == args.name:
            if isinstance(entry, Pokemon):
                raise NotImplementedError
            else:
                print(f"Soullink: {entry.name}")
                print(f"- {entry.p1.name}:")
                print(f"  - type1: {entry.p1.type1.name}:")
                print(f"  - type2: {entry.p1.type2}:")
                print(f"  - score: {entry.p1.score}:")
                print(f"- {entry.p2.name}:")
                print(f"  - type1: {entry.p2.type1.name}:")
                print(f"  - type2: {entry.p2.type2}:")
                print(f"  - score: {entry.p2.score}:")
            break


def pokemon_find(commands: Namespace):
    """Find Pokémon across all boxes based on criteria."""
    print(f"Finding Pokémon with criteria: {commands.search_criteria}")


def pokemon_export(commands: Namespace):
    """Export Pokémon from a box to a file."""
    print(
        f"Exporting Pokémon with ID {commands.pokemon_id} from box {commands.box_name} to file {commands.file_path.name}"  # noqa: E501
    )


def pokemon_import(commands: Namespace):
    """Import Pokémon from a file to a box."""
    print(f"Importing Pokémon from file {commands.file_path.name} to box {commands.box_name}")


def pokemon_edit(commands: Namespace):
    """Edit a Pokémon's data in a box."""
    print(
        f"Editing Pokémon with ID {commands.pokemon_id} in box {commands.box_name} to new data: {commands.new_pokemon_data}"  # noqa: E501
    )
