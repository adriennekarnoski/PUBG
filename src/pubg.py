"""Run terminal prompts to user."""
import requests
import os
from practice_data import data
from statistics import mean

# url = "https://api.pubg.com/shards/xbox-na/matches/50e82100-bbfb-4499-be93-a8af7cb6d63c"
# url = "https://api.pubg.com/shards/xbox-na/samples"
# url = "https://api.pubg.com/shards/xbox-na/players?filter[playerNames]=ehhhdrienne"

# api_key = os.environ.get('API_KEY')

# header = {
#   "Authorization": "Bearer " + api_key,
#   "Accept": "application/vnd.api+json"
# }

# r = requests.get(url, headers=header)
# response_dict = r.json()


player_stats_dict = {
    'assists': [],
    'damage': [],
    'headshots': [],
    'kill_place': [],
    'kill_points': [],
    'kills': [],
    'longest_kill': [],
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
    print(mean(player_stats_dict['kills']))
    # find_average(average_dict, count)


def find_average(input_dict, count):
    """Find the average of dictionary values."""
    for key in input_dict:
        input_dict[key] = input_dict[key] / count
