"""Run terminal prompts to user."""
import requests
import os
from practice_data import data
from statistics import mean
import json

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

personal_player_data = {}

game_data_dict = {}

# Use to get a random list of matches
# url = "https://api.pubg.com/shards/xbox-na/samples"

# Use to get information about a specific match
# url = "https://api.pubg.com/shards/xbox-na/matches/17d001b7-bddb-489c-8001-d7228578128f"

# url = 'https://api.playbattlegrounds.com/shards/xbox-na/players/account.a831af1196724930be51689635846ba2'

api_key = os.environ.get('API_KEY')

header = {
  "Authorization": "Bearer " + api_key,
  "Accept": "application/vnd.api+json"
}

# r = requests.get(url, headers=header)
# response_dict = r.json()

# response_dict['data']['relationships']['matches']['data'][0]['id']


# def make_api_call(type, data):
#     """Function to make api call and return response dictionary."""
#     if type == 'gamertag':
#         url = "https://api.pubg.com/shards/xbox-na/players?filter[playerNames]={}".format(data)
#     if type == 'match':
#         url = "https://api.pubg.com/shards/xbox-na/matches/{}".format(data)
#     r = requests.get(url, headers=header)
#     response_dict = r.json()
#     return response_dict


# def get_player_match_id():
#     """Function to get user gamertag and call make_api_call()."""
#     gamertag = input('Please enter your gamertag: ')
#     player_information_dict['gamertag'] = gamertag
#     response_matches = make_api_call('gamertag', gamertag)
#     match_id = response_matches['data'][0]['relationships']['matches']['data'][0]['id']
#     response_game_data = make_api_call('match', match_id)
#     return filter_player_data(response_game_data)


def filter_game_data(input):
    """Filter out information about the game."""
    game = input['data']['attributs']
    game_data_dict['dat']

def filter_player_data(input):
    """Function that takes in api response and filters out necessary data."""
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
    get_player_stats(player_stats_dict)


def get_player_stats(input_dict):
    """Print the average of dictionary values."""
    player_index = input_dict['name'].index(personal_player_data['gamertag'])
    for k, v in input_dict.items():
        personal_player_data[k] = v[player_index]
