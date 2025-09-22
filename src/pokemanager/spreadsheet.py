"""Fetch a box from a Google Sheet."""

from pathlib import Path
from typing import Any, Generator, Literal

import gspread

from pokemanager.const import TYPE
from pokemanager.data import Box, Pokemon, Soul, Soullink, SoullinkPC, StandardPC
from pokemanager.utils import URL


def fetch(
    credentials: Path,
    spreadsheet_url: URL,
    worksheet_name: str,
    category: Literal["standard", "soullink"],
    box_name: str,
) -> Box:
    """Fetch a box from Google Sheets."""
    gspread_connection = gspread.service_account(credentials)
    spreadsheet = gspread_connection.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(worksheet_name)
    raw_data: list[list[str]] = worksheet.get_all_values()
    header: list[list[str]] = raw_data[:3]
    data: list[list[str]] = raw_data[3:]
    return Box(
        name=box_name,
        **parse_header(header),
        category=category,
        credentials=credentials,
        spreadsheet_url=spreadsheet_url,
        worksheet_name=worksheet_name,
        pokemon=parse_data(data, category),
    )


def parse_header(header_data: list[list[str]]) -> dict[str, Any]:
    return {"game": "X", "players": ["Player 1", "Player 2"]}


def parse_data(data: list[list[str]], category: Literal["standard", "soullink"]) -> StandardPC | SoullinkPC:
    match category:
        case "standard":
            return StandardPC(parse_standard(data))
        case "soullink":
            return SoullinkPC(parse_soullink(data))


def parse_standard(data: list[list[str]]) -> Generator[Pokemon]:
    return (
        Pokemon(
            name="",
            nickname="",
            elected_type="Bug",
            auxiliary_type="Dark",
            lost=False,
            dead=False,
        )
        for ln in ()  # data
        if ln[1] != ""
    )


def parse_soullink(data: list[list[str]]) -> Generator[Soullink]:
    return (
        Soullink(
            party=True if ln[0] == "TRUE" else False,
            met=ln[1],
            p1=Soul(
                name=ln[4],
                nickname=ln[5],
                elected_type=ln[2],
                auxiliary_type=ln[3] if ln[3] in TYPE else None,
                lost=True if ln[6] == "TRUE" else False,
                dead=True if ln[7] == "TRUE" else False,
            ),
            p2=Soul(
                name=ln[10],
                nickname=ln[11],
                elected_type=ln[8],
                auxiliary_type=ln[9] if ln[9] in TYPE else None,
                lost=True if ln[12] == "TRUE" else False,
                dead=True if ln[13] == "TRUE" else False,
            ),
        )
        for ln in data
        if ln[1] != ""
    )


def report(
    box: Box,
    worksheet_name: str,
):
    if not all(bool(config) for config in (box.category, box.credentials, box.spreadsheet_url)):
        raise ValueError(f"Please configure box: {box.name}")
    gspread_connection = gspread.service_account(box.credentials)
    spreadsheet = gspread_connection.open_by_url(box.spreadsheet_url)
    worksheet = spreadsheet.worksheet(worksheet_name)
    if box.category == "standard":
        raise NotImplementedError("Standard Pokemon are not supported yet.")
    else:
        info: list[list[str | float]] = [
            [sum(pk.score for sl in team for pk in (sl.p1, sl.p2))]
            + [pkname for sl in team for pkname in (sl.p1.name, sl.p2.name)]
            for team in box.pc.get_teams()
        ]
    worksheet.update(gspread.utils.fill_gaps(info, worksheet.row_count, 13), "A:M")
