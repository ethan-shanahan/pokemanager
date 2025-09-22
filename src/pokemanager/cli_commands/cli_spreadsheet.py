"""CLI commands for fetching data from Google Sheets."""

from argparse import Namespace

from pokemanager.data import Box
from pokemanager.main import AppData
from pokemanager.spreadsheet import fetch, report


def spreadsheet_fetch(args: Namespace):
    """Fetch a box from Google Sheets."""
    print("Fetching box...")
    print(f"Google Sheet URL: {args.spreadsheet_url}")
    new_box: Box = fetch(args.credentials, args.spreadsheet_url, args.worksheet_name, args.category, args.box_name)
    AppData.save_box(new_box)


def spreadsheet_report(args: Namespace):
    """Report box information to Google Sheets."""
    app_data = AppData()
    if args.box_name not in app_data.boxes:
        print(f"Box '{args.box_name}' not found.")
        return
    report(app_data.boxes[args.box_name], args.worksheet_name)
