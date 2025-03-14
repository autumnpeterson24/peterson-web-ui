"""
Program: app.py
Author: Autumn Peterson
Date: 3/17/2025
Description:
    Fetching data from speedrun.com api (https://www.speedrun.com/api/v1/leaderboards/nd28z0ed/category/02qr00pk) and using the re library to parse information.
***Disclaimer:
    I used Chatpgpt.com helped me find the right tool I needed with the data that I was reading in. When it came to the timestamps, I couldn't get in readable times, and
    chatgpt.com helped me find the re library to convert the speedrun timestamps to be readable when displaying them.
    I also used the python black linter to clean up the code.
"""

import streamlit as st
import requests
import re


def fetch_player_name(player_id: str) -> str | None:
    """Fetch player name using their Speedrun.com ID and return a string of their username"""

    player_url = f"https://www.speedrun.com/api/v1/users/{player_id}"
    try:
        response = requests.get(
            player_url
        )  # fetching each player page to get their name
        if response.status_code == 200:
            return response.json()["data"]["names"][
                "international"
            ]  # get json data from speedrun.com api
        return (
            "Unknown Player"  # if there is no name then auto fill to be Unknown Player
        )

    except (
        requests.exceptions.Timeout
    ) as e:  # if the request takes too long it times out and returns none
        print("Request timed out!", e)
        return None

    except (
        requests.exceptions.RequestException
    ) as e:  # if there is a request exception a request error is thrown (like no internet connection)
        print("Request error:", e)
        return None


@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_leaderboard(category_id: str) -> list[dict] | None:
    """Fetches the times, places, and names of the players and saves them to a list of dicts to be used by streamlit within a dataframe"""

    url = (
        f"https://www.speedrun.com/api/v1/leaderboards/eldenring/category/{category_id}"
    )
    try:
        response = requests.get(url)

        if response.status_code == 200:  # make sure the response is good to go
            data = response.json()
            data_slice = data["data"]["runs"][:25]
            player_runs = []

            for run in data_slice:
                player_info = run["run"]["players"][0]
                if player_info["rel"] == "user":
                    player_name = fetch_player_name(player_info["id"])
                else:
                    player_name = player_info["name"]

                raw_time = run["run"]["times"]["primary"]

                # Convert ISO 8601 format to readable time chatgpt.com helped me with this conversion
                match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", raw_time)
                hours = int(match.group(1) or 0)
                minutes = int(match.group(2) or 0)
                seconds = int(match.group(3) or 0)

                formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

                run = dict(
                    Player_Name=player_name, Run_Time=formatted_time
                )  # create a dict for each run to add to the list
                player_runs.append(run)

            return player_runs

        else:
            print("Failed to fetch leaderboard:", response.status_code)

    except (
        requests.exceptions.Timeout
    ) as e:  # if the request takes too long it times out and returns none
        print("Request timed out!", e)
        return None

    except (
        requests.exceptions.RequestException
    ) as e:  # if there is a request exception a request error is thrown (like no internet connection)
        print("Request error:", e)
        return None
