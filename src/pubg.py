"""Run terminal prompts to user."""
import requests
import os
from practice_data import data
from statistics import mean
import json


# Use to get a random list of matches
# url = "https://api.pubg.com/shards/xbox-na/samples"

# Use to get information about a specific match
url = "https://api.pubg.com/shards/xbox-na/matches/17d001b7-bddb-489c-8001-d7228578128f"

#Use to find my matches
# url = "https://api.pubg.com/shards/xbox-na/players?filter[playerNames]=ehhhdrienne"

api_key = os.environ.get('API_KEY')

header = {
  "Authorization": "Bearer " + api_key,
  "Accept": "application/vnd.api+json"
}

r = requests.get(url, headers=header)
response_dict = r.json()


player_stats_dict = {
    'assists': [],
    'damage': [],
    'headshots': [],
    'kill_place': [],
    'kill_points': [],
    'kills': [],
    'longest_kill': [],
    'name': []
}


def filter_player_data(input):
    """Begin the program."""
    count = 0
    player_list = input['included']
    for i in range(len(player_list)):
        if player_list[i]['type'] == 'participant':
            stats = player_list[i]['attributes']['stats']
            count += 1
            player_stats_dict['assists'].append(stats['assists'])
            player_stats_dict['damage'].append(stats['damageDealt'])
            player_stats_dict['headshots'].append(stats['headshotKills'])
            player_stats_dict['kill_place'].append(stats['killPlace'])
            player_stats_dict['kill_points'].append(stats['killPoints'])
            player_stats_dict['kills'].append(stats['kills'])
            player_stats_dict['longest_kill'].append(stats['longestKill'])
            player_stats_dict['name'].append(stats['name'])
    # print_average(player_stats_dict)


# def print_average(input_dict):
#     """Print the average of dictionary values."""
#     for k, v in input_dict.items():
#         print("Average {}: {}".format(k, mean(v)))
