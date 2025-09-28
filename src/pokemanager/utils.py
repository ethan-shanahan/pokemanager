"""Utility functions and classes for the pokemanager package."""

from dataclasses import dataclass
from itertools import groupby
from re import sub
from typing import Any, Iterable, Literal, Mapping, Optional
from unicodedata import normalize

from gspread import Worksheet, service_account_from_dict


def all_equal(iterable: Iterable[Any]):
    """Returns True if all the elements are equal to each other."""
    return next((g := groupby(iterable)), True) and not next(g, False)


def slugify(value: Any, allow_unicode: bool = False):
    """Slugify a string.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = normalize("NFKC", value)
    else:
        value = normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = sub(r"[^\w\s-]", "", value.lower())
    return sub(r"[-\s]+", "-", value).strip("-_")


class URL(str):
    """A string that is validated to be a URL."""

    def __new__(cls, string: str = ""):
        """Verifies that the provided string is a url."""
        if string and type(string) is not str:
            raise TypeError('Unexpected type for URL: "%s"' % type(string))
        if string and not (string.startswith("http://") or string.startswith("https://")):
            raise ValueError('Passed string value "%s" is not an "http*://" URL' % (string,))

        return str.__new__(cls, string)


@dataclass
class Database:
    """A class representing a database connection."""

    credentials: Optional[Mapping[str, Any]] = None
    spreadsheet_url: Optional[URL] = None
    worksheet_from: Optional[str] = None
    worksheet_to: Optional[str] = None

    def get_worksheet(self, from_or_to: Literal["from", "to"], worksheet: Optional[str] = None) -> Worksheet:
        """Fetch all values from the specified worksheet."""
        match from_or_to:
            case "from":
                if worksheet is None:
                    worksheet = self.worksheet_from
            case "to":
                if worksheet is None:
                    worksheet = self.worksheet_to
        if self.credentials is None:
            raise RuntimeError("Credentials are undefined.")
        if self.spreadsheet_url is None:
            raise RuntimeError("Spreadsheet URL is undefined.")
        if worksheet is None:
            raise RuntimeError(
                f"The worksheet to {'read from' if from_or_to == 'from' else 'write to'} must be specified."
            )

        gspread_connection = service_account_from_dict(self.credentials)
        spreadsheet = gspread_connection.open_by_url(self.spreadsheet_url)
        return spreadsheet.worksheet(worksheet)
