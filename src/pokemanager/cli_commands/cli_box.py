"""CLI commands for managing boxes."""

from argparse import Namespace

from pokemanager.data import Box
from pokemanager.main import AppData


def box(args: list[str]):
    """Manage boxes."""
    print("Managing boxes...")


def box_show(args: Namespace):
    """Show information about a box."""
    app_data = AppData()
    if args.name not in app_data.boxes:
        print(f"Box '{args.name}' not found.")
        return
    box: Box = app_data.boxes[args.name]
    print(f"Box Name: {box.name}")
    print(f"Players: {box.players}")
    print(f"Game: {box.game}")
    print(f"Gen: {box.gen}")
    print(f"Category: {box.category}")
    print(f"Number of Pokémon: {len(box.pc)}")
    if box.credentials:
        print(f"Credentials: {box.credentials}")
    if box.spreadsheet_url:
        print(f"Spreadsheet URL: {box.spreadsheet_url}")
    if box.worksheet_name:
        print(f"Worksheet Name: {box.worksheet_name}")


def box_list(args: Namespace):
    """List all boxes."""
    print("Listing all boxes...")
    for box_name, box in AppData().boxes.items():
        print(f"- {box_name}: {len(box.pc)} Pokémon")


def box_add(args: Namespace):
    """Add a new box."""
    print(f"Adding box: {args.name}")
    new_box = Box(name=args.name, game=args.game, category=args.category, pokemon=[])
    AppData.save_box(new_box)


def box_remove(args: Namespace):
    """Remove a box."""
    print(f"Removing box: {args.name}")
    AppData.delete_box(args.name)


def box_rename(args: Namespace):
    """Rename a box."""
    print(f"Renaming box from {args.old_name} to {args.new_name}")
    box = AppData().boxes[args.old_name]
    renamed_box = Box(
        name=args.new_name,
        game=box.game,
        category=box.category,
        pokemon=box.pc,
        players=box.players,
        credentials=box.credentials,
        spreadsheet_url=box.spreadsheet_url,
        worksheet_name=box.worksheet_name,
    )
    AppData.save_box(renamed_box)
    AppData.delete_box(args.old_name)


def box_config(args: Namespace):
    """Configure a box."""
    print(f"Configuring box {args.name}: setting {args.config_key} to {args.config_value}")
    raise NotImplementedError("Box config not implemented yet.")


def box_export(args: Namespace):
    """Export a box to a file."""
    print(f"Exporting box {args.name} to file {args.file_path.name}")
    raise NotImplementedError("Box export not implemented yet.")


def box_import(args: Namespace):
    """Import a box from a file."""
    print(f"Importing box from file {args.file_path.name}")
    raise NotImplementedError("Box import not implemented yet.")
