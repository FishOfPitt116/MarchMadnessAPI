"""
API Links:
    Postseason Tournaments - https://api.sportradar.us/ncaamb/trial/v4/en/tournaments/2021/PST/schedule.json?api_key=key
    2021 Tournament Info - http://api.sportradar.us/ncaamb/trial/v7/en/tournaments/6b1b9057-68b6-4705-9642-0d5e5f2c9dd1/schedule.json?api_key=key
"""

import json
import time
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
    seed: int

class Region(NamedTuple):
    name: str
    location: str
    rank: int
    teams: List[Team]

class RegionError(Exception):
    def __init__(self):
        super().__init__("Invalid region code.")

def _api_call(link: str) -> str:
    print("Making API call...")
    print(link)
    output = requests.get(link).json()
    time.sleep(1)   # Necessary b/c I'm limited to 1 call per second... sadge
    return output

def _get_madness_id(year: str):
    tourneys_json = _api_call(POSTSEASON_TOURNAMENTS_URL.format(year=year, key=api_key))
    for tournament in tourneys_json["tournaments"]:
        if tournament["name"] == "NCAA Men's Division I Basketball Tournament":
            return tournament["id"]
    return None

def find_team(year: str, school: str):
    madness_json = _api_call(PARTICIPANTS_URL.format(id=_get_madness_id(year), key=api_key))
    for bracket in madness_json["brackets"]:
        for team in bracket["participants"]:
            if school in [team["name"], team["market"]]:
                return Team(id=team["id"], name=team["name"], school=team["market"], seed=team["seed"])
    return None

def get_region(year: str, region: str):
    if region.lower() in ["midwest", "mw", "midwest region"]:
        region = "Midwest Regional"
    elif region.lower() in ["west", "w", "west region"]:
        region = "West Regional"
    elif region.lower() in ["east", "e", "east region"]:
        region = "East Regional"
    elif region.lower() in ["south", "s", "south region"]:
        region = "South Regional"
    else:
        raise RegionError
    madness_json = _api_call(PARTICIPANTS_URL.format(id=_get_madness_id(year), key=api_key))
    for bracket in madness_json["brackets"]:
        if bracket["name"] == region:
            teams = []
            for team in bracket["participants"]:
                teams.append(Team(id=team["id"], name=team["name"], school=team["market"], seed=team["seed"]))
            return Region(name=region, location=bracket["location"], rank=bracket["rank"], teams=teams)
    raise RegionError