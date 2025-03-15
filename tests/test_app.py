"""
Program: test_app.py
Author: Autumn Peterson
Description:
    Testing for the Elden Ring streamlit app.py
"""

import pytest
import elden_fetch


@pytest.fixture
def zip_leaderboard() -> list[dict]:
    """Creating the leaderboard of top 50 speedruns"""
    zip_id = "02qr00pk"
    leaderboard = elden_fetch.fetch_leaderboard(zip_id)
    return leaderboard


@pytest.fixture
def gods_leaderboard() -> list[dict]:
    """Creating the leaderboard of top 50 speedruns"""
    gods_id = "mke64ljd"
    leaderboard = elden_fetch.fetch_leaderboard(gods_id)
    return leaderboard


@pytest.fixture
def consort_leaderboard() -> list[dict]:
    """Creating the leaderboard of top 50 speedruns"""
    consort_id = "jdr4mmn2"
    leaderboard = elden_fetch.fetch_leaderboard(consort_id)
    return leaderboard


def test_elden_fetch_zip(zip_leaderboard: list[dict]) -> None:
    """Testing that request went through and the leaderboard is type list not None from the Any% Zip speedrun"""
    assert type(zip_leaderboard) == list


def test_elden_fetch_gods(gods_leaderboard: list[dict]) -> None:
    """Testing that request went through and the leaderboard is type list not None from the All Gods speedrun"""
    assert type(gods_leaderboard) == list


def test_elden_fetch_consort(consort_leaderboard: list[dict]) -> None:
    """Testing that request went through and the leaderboard is type list not None from the Defeat Consort speedrun"""
    assert type(consort_leaderboard) == list
