"""Run terminal prompts to user."""
import requests
import os
from practice_data import data

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


average_dict = {
    'assists': 0,
    'damage': 0,
    'headshots': 0,
    'kill_place': 0,
    'kill_points': 0,
    'kills': 0,
    'longest_kill': 0,
}


def filter_players(input):
    """Begin the program."""
    count = 0
    player_list = input['included']
    for i in range(len(player_list)):
        if player_list[i]['type'] == 'participant':
            stats = player_list[i]['attributes']['stats']
            count += 1
            average_dict['assists'] += stats['assists']
            average_dict['damage'] += stats['damageDealt']
            average_dict['headshots'] += stats['headshotKills']
            average_dict['kill_place'] += stats['killPlace']
            average_dict['kill_points'] += stats['killPoints']
            average_dict['kills'] += stats['kills']
            average_dict['longest_kill'] += stats['longestKill']
    find_average(average_dict, count)
    return count


def find_average(input_dict, count):
    """Find the average of dictionary values."""
    for key in input_dict:
        input_dict[key] = input_dict[key] / count
