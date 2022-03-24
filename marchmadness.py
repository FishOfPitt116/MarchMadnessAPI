"""
API Links:
    Postseason Tournaments - https://api.sportradar.us/ncaamb/trial/v4/en/tournaments/2021/PST/schedule.json?api_key=key
    2021 Tournament Info - http://api.sportradar.us/ncaamb/trial/v7/en/tournaments/6b1b9057-68b6-4705-9642-0d5e5f2c9dd1/schedule.json?api_key=key
"""

import json
from typing import List, Dict, Generator, NamedTuple, Optional, Tuple
import requests

POSTSEASON_TOURNAMENTS_URL = (
    "https://api.sportradar.us/ncaamb/trial/v7/en/tournaments/{year}/PST/schedule.json?api_key={key}"
) # use .format(year=num) to call
CONFERENCE_TOURNAMENTS_URL = (
    "https://api.sportradar.us/ncaamb/trial/v7/en/tournaments/{year}/PST/schedule.json?api_key={key}"
)
SPECIFIC_TOURNAMENT_URL = (
    "https://api.sportradar.us/ncaamb/trial/v7/en/tournaments/{id}/schedule.json?api_key={key}"
) # get id from postseason_tournaments_url to use here
PARTICIPANTS_URL = (
    "https://api.sportradar.us/ncaamb/trial/v7/en/tournaments/{id}/summary.json?api_key={key}"
)

with open(".secrets/keys.json") as f:
    api_key = json.load(f)["cbb_key"] # api_key now contains my api key

class Team(NamedTuple):
    id: str
    name: str
    school: str
    rank: int

class Region(NamedTuple):
    name: str
    location: str
    rank: int
    teams: List[Team]

def get_madness_id(year: str):
    tourneys_url = POSTSEASON_TOURNAMENTS_URL.format(year=year, key=api_key)
    tourneys_json = requests.get(tourneys_url).json()
    madness_id = tourneys_json["tournaments"][1]["id"]
    return madness_id

madness_2021_id = get_madness_id("2020")
print(madness_2021_id)
# madness_2021_url = PARTICIPANTS_URL.format(id=madness_2021_id, key=api_key)
# madness_2021 = requests.get(madness_2021_url)
# print(madness_2021)
# print(madness_2021.raise_for_status())