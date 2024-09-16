from journal import prompt, generate_prompt, sentimental, write_in_journal, get_daterange, print_analysis
from unittest.mock import Mock
import csv
import pytest
import tempfile


def test_sentimental():
    assert sentimental("I had a great day") == "Positive"
    assert sentimental("I feel terrible") == "Negative"


def test_write_in_journal():
    file = open("journal.csv", "r")
    with open("journal.csv", "r") as file:
        write_in_journal("2022-11-29", "abc", "Neutral")
        reader = csv.DictReader(file)
        for row in reader:
            if row["text"] == "abc":
                assert row["date"] == "2022-11-29"


def test_get_daterange():
    assert get_daterange(7) == ['2024-02-18', '2024-02-19', '2024-02-20', '2024-02-21', '2024-02-22', '2024-02-23', '2024-02-24', '2024-02-25']




