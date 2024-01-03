"""This python module tests the python module project_2."""
from unittest.mock import patch
import pytest
from _pytest.monkeypatch import MonkeyPatch
import cowsay
import pandas as pd
from colorama import Fore
from wadsup.final_project_bu import (
    check,
    user_input,
    preferences,
    determine_winner,
    stats,
    your_destiny,
    youtube,
    countdown,
)


def test_check_yes():
    """Function tests user input 'yes' and 'YEs.'"""
    assert (
        check("yes", "Tonno")
        == "\nYour on the right site Tonno!\nWadsup helps you to decide which Dutch Wadden island is "
        "your island.\nwadsup uses CS50 (common sense 50 \U0001F609) to detect your destination."
    )
    assert (
        check("YEs", "Tonno")
        == "\nYour on the right site Tonno!\nWadsup helps you to decide which Dutch Wadden island is "
        "your island.\nwadsup uses CS50 (common sense 50 \U0001F609) to detect your destination."
    )


def test_check_no():
    """Function tests user input 'n'."""
    with pytest.raises(SystemExit):
        check("n", "Tonno")


def test_user_input():
    """Function tests storing user input in a list."""
    monkeypatch = MonkeyPatch()
    # fictional userinput '1', '2', '3' and assign to variable "inpt" (class list_iterator)
    inpt = iter(["1", "2", "3"])
    # patch fictional user input
    monkeypatch.setattr("builtins.input", lambda _: next(inpt))
    result = user_input()
    assert result == ["1", "2", "3"]


#  pd_df_islands if the chosen user inputs lead to the correct outcomes
def test_preferences():
    """This function tests if user input calculates the right score."""
    assert preferences("5", "5", "5") == {
        "Texel": 24,
        "Vlieland": 20,
        "Terschelling": 14,
        "Ameland": 18,
        "Schiermonnikoog": 22,
    }


# Use with pytest.raises to pd_df_islands functions
# sys.exit: https://docs.pytest.org/en/7.1.x/how-to/assert.html
def test_your_destiny():
    """Function prints winning island using cowsay."""
    assert your_destiny("Tonno", "Ameland") == cowsay.tux(
        Fore.GREEN + "Tonno" + "\n" + Fore.GREEN + "Ameland" + " is your destiny! "
    )


def test_your_destiny_wrong_island():
    """Function tests input 'wrong' island."""
    with pytest.raises(SystemExit):
        your_destiny("Tonno", "Sicilie")


def test_determine_winner_one_winner():
    """Function tests one winner."""
    assert (
        determine_winner(
            {
                "Texel": 24,
                "Vlieland": 23,
                "Terschelling": 16,
                "Ameland": 20,
                "Schiermonnikoog": 25,
            }
        )
        == "Schiermonnikoog"
    )


def test_determine_winner_multiple_winner():
    """Funtion tests if winner is in list of islands with the same score."""
    assert determine_winner(
        {
            "Texel": 25,
            "Vlieland": 23,
            "Terschelling": 24,
            "Ameland": 25,
            "Schiermonnikoog": 25,
        }
    ) in ["Texel", "Ameland", "Schiermonnikoog"]


def test_stats():
    """Testing if pandas dataframe is created, mean and median."""

    # Unpacking stats
    pd_df_islands, mean, median = stats(
        {
            "Texel": 18,
            "Vlieland": 9,
            "Terschelling": 10,
            "Ameland": 14,
            "Schiermonnikoog": 11,
        }
    )
    assert isinstance(pd_df_islands, pd.core.frame.DataFrame) and (
        mean == 12.4,
        median == 11,
    )


#
def test_countdown():
    """Function tests if None is returned."""
    assert countdown(5) is None


@patch("project_2.YouTube")
def test_youtube(mock_youtube):
    """docstring"""
    # mock_youtube.return_value.title = "Ameland Video Title"
    mock_youtube.return_value.thumbnail_url = "http://youtube.com/ameland_thumbnail.jpg"
    assert youtube("Ameland") == (
        "Thumbnail URL:",
        "http://youtube.com/ameland_thumbnail.jpg",
    )
