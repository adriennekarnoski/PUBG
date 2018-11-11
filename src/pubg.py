"""Run terminal prompts to user."""
import requests
import os
from practice_data import data
from statistics import mean
import json
from datetime import datetime
import csv

player_stats_dict = {
    'assists': [],
    'damage': [],
    'death': [],
    'headshots': [],
    'win_place': [],
    'win_points': [],
    'kills': [],
    'longest_kill': [],
    'time_survived': [],
    'weapons': [],
    'name': []
}

personal_player_data = {
    'gamertag': 'Bambo007'
}

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


def to_csv(input_dict):
    with open('pubg_stats.csv', mode='w') as csv_file:
        fieldnames = ['kills', 'headshots', 'name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        player_list = input_dict['included']
        for i in range(len(player_list)):
            if player_list[i]['type'] == 'participant':
                stats = player_list[i]['attributes']['stats']
                writer.writerow(
                    {
                        'kills': stats['kills'],
                        'headshots': stats['headshotKills'],
                        'name': stats['name']
                    }
                )


def make_api_call(type, data):
    """Function to make api call and return response dictionary."""
    if type == 'gamertag':
        url = "https://api.pubg.com/shards/xbox-na/players?filter[playerNames]={}".format(data)
    if type == 'match':
        url = "https://api.pubg.com/shards/xbox-na/matches/{}".format(data)
    r = requests.get(url, headers=header)
    response_dict = r.json()
    return response_dict


def get_player_match_id():
    """Function to get user gamertag and call make_api_call()."""
    url = "https://api.pubg.com/shards/xbox/matches/2035e7be-0781-4e04-8e39-dd3db0f2823c"
    r = requests.get(url, headers=header)
    response_dict = r.json()
    print(response_dict)


def respond_to_user():
    """Return all information to the user."""
    response = """
        {}'s Last Match

        Game Duration: {}
        Date: {}
        Map: {}


        PERSONAL STATS

        Win Place: {}
        Win Points: {}
        Death By: {}
        Time Survived: {}

        Kills: {}
        Assists: {}
        Damage Dealt: {}
        Headshots: {}
        Longest Kill: {} meters
        Weapons Acquired: {}""".format(
        personal_player_data['gamertag'],
        game_data_dict['duration'],
        game_data_dict['date'],
        game_data_dict['map'],
        personal_player_data['win_place'],
        personal_player_data['win_points'],
        personal_player_data['death'],
        personal_player_data['time_survived'],
        personal_player_data['kills'],
        personal_player_data['assists'],
        personal_player_data['damage'],
        personal_player_data['headshots'],
        personal_player_data['longest_kill'],
        personal_player_data['weapons']
    )
    print(response)
    other_players()


def other_players():
    """Information on other players in the game."""
    average_kills = round(mean(player_stats_dict['kills']))
    average_headshots = round(mean(player_stats_dict['headshots']))
    average_time_survived = seconds_to_minutes(mean(player_stats_dict['time_survived']))
    longest_kill_rounded = "{0:.2f}".format(max(player_stats_dict['longest_kill']))
    response = """

        OVERALL STATS

        Average Kills: {}
        Average Headshots: {}
        Average Survival Time: {}

        Most Kills: {}
        Most Headshots: {}
        Highest Damage: {}
        Longest Kill: {} meters """.format(
            average_kills,
            average_headshots,
            average_time_survived,
            max(player_stats_dict['kills']),
            max(player_stats_dict['headshots']),
            max(player_stats_dict['damage']),
            longest_kill_rounded
        )
    print(response)


def filter_game_data(input_dict):
    """Filter out information about the game."""
    game = input_dict['data']['attributes']
    game_time = game['createdAt']
    f = "%Y-%m-%dT%H:%M:%SZ"
    time = datetime.strptime(game_time, f)
    edited_time = time.strftime('%a, %b %d')
    game_data_dict['date'] = edited_time
    game_duration = game['duration']
    game_data_dict['duration'] = seconds_to_minutes(game_duration)
    if game['mapName'] == 'Desert_Main':
        game_data_dict['map'] = 'Miramar'
    if game['mapName'] == 'Savage_Main':
        game_data_dict['map'] = 'Sanhok'
    map_name = game['mapName'].split('_')
    game_data_dict['map'] = map_name[0]
    filter_player_data(input_dict)


def filter_player_data(input_dict):
    """Function that takes in api response and filters out necessary data."""
    count = 0
    player_list = input_dict['included']
    for i in range(len(player_list)):
        if player_list[i]['type'] == 'participant':
            stats = player_list[i]['attributes']['stats']
            count += 1
            player_stats_dict['assists'].append(stats['assists'])
            player_stats_dict['damage'].append(stats['damageDealt'])
            player_stats_dict['death'].append(stats['deathType'])
            player_stats_dict['headshots'].append(stats['headshotKills'])
            player_stats_dict['win_place'].append(stats['winPlace'])
            player_stats_dict['win_points'].append(stats['winPoints'])
            player_stats_dict['kills'].append(stats['kills'])
            player_stats_dict['longest_kill'].append(stats['longestKill'])
            player_stats_dict['time_survived'].append(stats['timeSurvived'])
            player_stats_dict['weapons'].append(stats['weaponsAcquired'])
            player_stats_dict['name'].append(stats['name'])
    get_player_stats(player_stats_dict)


def get_player_stats(input_dict):
    """Print the average of dictionary values."""
    player_index = input_dict['name'].index(personal_player_data['gamertag'])
    for k, v in input_dict.items():
        personal_player_data[k] = v[player_index]
    edit_player_dict_values(personal_player_data)


def edit_player_dict_values(input):
    """Change the layout of various values in player dictionary."""
    if personal_player_data['death'] is 'byplayer':
        personal_player_data['death'] = 'Player'
    else:
        personal_player_data['death'] = personal_player_data['death'].title()
    player_survived = personal_player_data['time_survived']
    personal_player_data['time_survived'] = seconds_to_minutes(player_survived)
    longest_kill = personal_player_data['longest_kill']
    personal_player_data['longest_kill'] = "{0:.2f}".format(longest_kill)
    respond_to_user()


def seconds_to_minutes(seconds):
    """Function that takes seconds and converts to minutes."""
    seconds = "{0:.2f}".format(seconds / 60)
    minutes = seconds.split('.')
    if int(minutes[1]) >= 60:
        minutes[0] = int(minutes[0]) + 1
        minutes[1] = int(minutes[1]) - 60
    return '{} minutes and {} seconds'.format(minutes[0], minutes[1])

# if __name__ == "__main__":
#     get_player_match_id()