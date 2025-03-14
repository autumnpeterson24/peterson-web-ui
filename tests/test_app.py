"""
Program: test_app.py
Author: Autumn Peterson
Description:
    Testing for the Elden Ring streamlit app.py
"""

import pytest
import elden_fetch


@pytest.fixture
def zip_leaderboard() -> dict:
    """Creating the leaderboard of top 50 speedruns"""
    zip_id = "02qr00pk"
    leaderboard = elden_fetch.fetch_leaderboard(zip_id)
    return leaderboard


@pytest.fixture
def gods_leaderboard() -> dict:
    """Creating the leaderboard of top 50 speedruns"""
    gods_id = "mke64ljd"
    leaderboard = elden_fetch.fetch_leaderboard(gods_id)
    return leaderboard


@pytest.fixture
def consort_leaderboard() -> dict:
    """Creating the leaderboard of top 50 speedruns"""
    consort_id = "jdr4mmn2"
    leaderboard = elden_fetch.fetch_leaderboard(consort_id)
    return leaderboard


def test_elden_fetch_zip(zip_leaderboard: dict) -> None:
    """Testing that all 25 slices from the Zip speedrun was recieved from the request"""
    assert len(zip_leaderboard) == 25


def test_elden_fetch_gods(gods_leaderboard: dict) -> None:
    """Testing that all 5 slices from the All Gods speedrun was recieved from the request"""
    assert len(gods_leaderboard) == 5


def test_elden_fetch_consort(consort_leaderboard: dict) -> None:
    """Testing that all 12 slices from the Defeat Consort speedrun was recieved from the request"""
    assert len(consort_leaderboard) == 12
