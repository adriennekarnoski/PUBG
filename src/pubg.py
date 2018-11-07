"""Run terminal prompts to user."""
import requests
import os
from practice_data import data
from statistics import mean
import json
from datetime import datetime

player_stats_dict = {
    'assists': [],
    'damage': [],
    'death': [],
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

def run_stats(input):
    filter_game_data(input)
    filter_player_data(input)
    response = """
        {}'s Last Match

        Total Game Duration: {}
        Date: {}
        Map: {}

        Kill Place: {}
        Kill Points: {}
        Death By: {}

        Kills: {}
        Assists: {}
        Total Damage Dealt: {}
        Headshots: {}
        Longest Kill: {} """.format(
        personal_player_data['gamertag'],
        game_data_dict['duration'],
        game_data_dict['date'],
        game_data_dict['map'],
        personal_player_data['kill_place'],
        personal_player_data['kill_points'],
        personal_player_data['death'],
        personal_player_data['kills'],
        personal_player_data['assists'],
        personal_player_data['damage'],
        personal_player_data['headshots'],
        personal_player_data['longest_kill']
    )
    print(response)


def filter_game_data(input):
    """Filter out information about the game."""
    game = input['data']['attributes']
    game_time = game['createdAt']
    f = "%Y-%m-%dT%H:%M:%SZ"
    time = datetime.strptime(game_time, f)
    s = time.strftime('%a, %b %d')
    game_data_dict['date'] = s
    seconds = "{0:.2f}".format(game['duration'] / 60)
    minutes = seconds.split('.')
    game_data_dict['duration'] = '{} minutes and {} seconds'.format(minutes[0], minutes[1])
    if game['mapName'] == 'Desert_Main':
        game_data_dict['map'] = 'Miramar'
    if game['mapName'] == 'Savage_Main':
        game_data_dict['map'] = 'Sanhok'
    map_name = game['mapName'].split('_')
    game_data_dict['map'] = map_name[0]


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
            player_stats_dict['death'].append(stats['deathType'])
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
    if personal_player_data['death'] is 'byplayer':
        personal_player_data['death'] = 'By Player'
    else:
        personal_player_data['death'] = personal_player_data['death'].title()
