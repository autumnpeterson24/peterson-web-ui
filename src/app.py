"""
Program: app.py
Author: Autumn Peterson
Date: 3/17/2025
Description:
    Streamlit front-end for Elden Ring Speedruns. Contains the creation of the dataframe to hold the leaderboard for Elden Ring Speedruns
    as well as a bar graph that measures the amount of occurences certain players show up on the leaderboard. All data is fetched from speedrun.com.
***Disclaimer: chatgpt.com was super helpful when it came to figuring out how to use all the really cool features that streamlit allows like importing pandas and using
    a dataframe. It takes a lot of time away from having to pour through documentation. I also figured out that using a config.toml allows for the website
    to be different colors.
    I also used the python black linter to clean up the code.

    App url: https://autumnpeterson24-peterson-web-ui-srcapp-rstjyv.streamlit.app/
"""

import streamlit as st
import elden_fetch as ef
import pandas as pd  # to use dataframe and display data
import altair as alt  # to use in the creation of the chart
import streamlit as st
from pathlib import Path

# Elden Ring's category ID for Any% Zip and All Gods Speedruns =========================
zip_id = "02qr00pk"
gods_id = "mke64ljd"
consort_id = "jdr4mmn2"
# ========================================================================================

# Inject Google Font and CSS =============================================================
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinzel&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

def local_css(file_name: str)->None:
    """ Read in the css style format from assets to use for the API """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/styles.css") # load in the styles

# Categories for both dataframe and chart to use ========================================
st.sidebar.title("Select Run Category")
categories = {"Any% Zip": zip_id, "Two Gods": gods_id, "Defeat Consort": consort_id}

selected_category = st.sidebar.radio(
    "Choose a Category", list(categories.keys())
)  # create a category selector as a sidebar
# =======================================================================================


def fetch_chart_data() -> list[dict] | None:
    """Fetches data from all three categories to be used for the chart data"""
    all_leaderboards = []
    for c in categories.values():
        leaderboard = ef.fetch_leaderboard(c)
        if (
            leaderboard == None
        ):  # checking to see if the request came through if None then return None
            return None  # it is an exception error at this point

        all_leaderboards.extend(leaderboard)
    return all_leaderboards


def create_leaderboards() -> None:
    """Creating the leaderboad as a pandas dataframe for nicely organized data for each speedrun category, Any% Zip, All Gods, and Defeat Consort"""
    leaderboard = ef.fetch_leaderboard(categories[selected_category])
    if (
        leaderboard == None
    ):  # checking to see if the request came through if None then write error message to website and return None
        st.write("An error occurred when connecting...")
        return None

    st.header(
        f"{selected_category} Leaderboard"
    )  # header for labeling which run over the dataframe

    if len(leaderboard) >= 10:
        top_10_toggle = st.toggle(
            "Only show top 10", value=True
        )  # create a toggle to ony show top ten

        if top_10_toggle:
            leaderboard = leaderboard[
                :10
            ]  # only grab the top ten if the toggle is enabled

    leaderboard_df = pd.DataFrame(
        leaderboard
    )  # using dataframe instead of table for extra features and highlighting names when hovering over

    medals = ["🥇", "🥈", "🥉"]  # medal emojis!
    leaderboard_df.index = [
        medals[i] if i < 3 else str(i + 1) for i in range(len(leaderboard_df))
    ]  # replace the top three indexes of dataframe to have medal emojis

    leaderboard_df = leaderboard_df.reset_index().rename(
        columns={"index": "Place"}
    )  # rename the index colum to be Place of player

    st.dataframe(
        leaderboard_df, hide_index=True
    )  # create the dataframe of all the top runs


def create_chart() -> None:
    """Creating the chart that tracks the appearances of each speedrunner and how many times they appear on the leaderboard"""
    combined = fetch_chart_data()
    if (
        combined == None
    ):  # checking to see if the request came through if None then return None
        return None

    combined_df = pd.DataFrame(combined)
    player_count = (
        combined_df["Player_Name"].value_counts().reset_index()
    )  # counting occurences of players on leaderboard across 3 seperate speedruns
    player_count.columns = ["Player", "Appearances"]

    player_count["Appearances"] = player_count["Appearances"].astype(int)

    top_5 = player_count.head(5)  # returns the first 5 most occuring players

    show_chart = st.checkbox(
        "Show Most Recurring Players Across All Speedrun Categories"
    )  # have a checkbox toggle for if you want to see the most reoccuring players on the leaderboard

    if show_chart:  # show the bar chart if the checkbox is checked
        st.subheader(
            "Top 5 Most Recurring Players"
        )  # chart for displaying the most occuring players

        chart = (
            alt.Chart(top_5)
            .mark_bar(color="goldenrod")
            .encode(
                x=alt.X(
                    "Appearances:Q",
                    title="Number of Times on Leaderboard",
                    axis=alt.Axis(format="d"),
                ),
                y=alt.Y("Player:N", sort="-x", title="Player Name"),
            )
            .properties(width=700, height=400)
        )

        st.altair_chart(chart)


def display_category_details() -> None:
    """Fetch and display category description and rules"""
    category_details = ef.fetch_category_details(categories[selected_category])

    if category_details:
        st.header(f"{category_details['name']} Speedrun Details & Info")
        st.write(f"**Description Link:** {category_details['description']}")
        st.write(f"**Rules:** {category_details['rules']}")
    else:
        st.write("Failed to load category details.")


# Create Leaderboard and Charts ======================================================================
st.title("Elden Ring Speedruns")
display_category_details()
create_leaderboards()
create_chart()
