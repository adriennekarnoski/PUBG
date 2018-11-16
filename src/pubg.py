"""Run terminal prompts to user."""
import requests
import os
from practice_data import data
from statistics import mean
import json
from datetime import datetime
import csv
import pandas

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

personal_player_data = {}

game_data_dict = {
    'gamertag': 'example'
}


api_key = os.environ.get('API_KEY')

header = {
  "Authorization": "Bearer " + api_key,
  "Accept": "application/vnd.api+json"
}


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
    """Function to get user gamertag and call make api call to retun match ids."""
    gamertag = input('Please enter your gamertag: ')
    game_data_dict['gamertag'] = gamertag
    response_matches = make_api_call('gamertag', gamertag)
    try:
        match_id = response_matches['data'][0]['relationships']['matches']['data'][0]['id']
        response_game_data = make_api_call('match', match_id)
        filter_game_data(response_game_data)
    except IndexError:
        print("No matches within the last 14 days")


def print_game_data():
    """Function to print game data."""
    response = """
        {}'s Last Match

        Game Duration: {}
        Date: {}
        Map: {}""".format(
            game_data_dict['gamertag'],
            game_data_dict['duration'],
            game_data_dict['date'],
            game_data_dict['map']
            )
    print(response)


def print_player_data(input_list):
    """Function to print the user's personal data."""
    response = """

        PERSONAL STATS

        Win Place: {0[4]}
        Win Points: {0[5]}
        Death By: {0[2]}
        Time Survived: {0[8]}

        Kills: {0[6]}
        Assists: {0[0]}
        Damage Dealt: {0[1]}
        Headshots: {0[3]}
        Longest Kill: {0[7]} meters
        Weapons Acquired: {0[9]}""".format(input_list)
    print(response)


def print_other_players_data(input_list):
    """Function to print the other player's data."""
    response = """

        OVERALL STATS

        Average Kills: {0[0]}
        Average Headshots: {0[1]}
        Average Survival Time: {0[2]}

        Most Kills: {0[3]}
        Most Headshots: {0[4]}
        Highest Damage: {0[5]}
        Longest Kill: {0[6]} meters """.format(input_list)
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
    with open('pubg_stats.csv', mode='w') as csv_file:
        fieldnames = [
            'assists',
            'damage',
            'death',
            'headshots',
            'win_place',
            'win_points',
            'kills',
            'longest_kill',
            'time_survived',
            'weapons',
            'name'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        player_list = input_dict['included']
        for i in range(len(player_list)):
            if player_list[i]['type'] == 'participant':
                stats = player_list[i]['attributes']['stats']
                writer.writerow(
                    {
                        'assists': stats['assists'],
                        'damage': stats['damageDealt'],
                        'death': stats['deathType'],
                        'headshots': stats['headshotKills'],
                        'win_place': stats['winPlace'],
                        'win_points': stats['winPoints'],
                        'kills': stats['kills'],
                        'longest_kill': stats['longestKill'],
                        'time_survived': stats['timeSurvived'],
                        'weapons': stats['weaponsAcquired'],
                        'name': stats['name']
                    }
                )
    get_dataframe_data()


def get_dataframe_data():
    """Create a pandas dataframe and get desired values."""
    get_average = ['kills', 'headshots', 'time_survived']
    get_max = ['kills', 'headshots', 'damage', 'longest_kill']
    overall_data_list = []
    df = pandas.read_csv('pubg_stats.csv')
    df_player_row = df.loc[df['name'] == game_data_dict['gamertag']].values.tolist()
    for i in range(len(get_average)):
        overall_data_list.append(df[get_average[i]].mean())
    for i in range(len(get_max)):
        overall_data_list.append(df[get_max[i]].max())
    player_data = edit_player_data(df_player_row[0])
    overall_data = edit_overall_game_data(overall_data_list)
    print_game_data()
    print_player_data(player_data)
    print_other_players_data(overall_data)


def edit_player_data(input_list):
    """Edit player values for easier reading before returning to the user."""
    input_list[1] = "{0:.2f}".format(input_list[1])
    input_list[8] = seconds_to_minutes(input_list[8])
    input_list[7] = "{0:.2f}".format(input_list[7])
    if input_list[2] == 'byplayer':
        input_list[2] = 'Player'
    else:
        input_list[2] = input_list[2].title()
    return input_list


def edit_overall_game_data(input_list):
    """Edit format of overall average game data."""
    input_list[0] = int(round(input_list[0]))
    input_list[1] = int(round(input_list[1]))
    input_list[2] = seconds_to_minutes(input_list[2])
    input_list[5] = "{0:.2f}".format(input_list[5])
    input_list[6] = "{0:.2f}".format(input_list[6])
    return input_list


def return_to_user(player_data, overall_data):
    """Function to ."""
    print_game_data()
    print_player_data(player_data)
    print_other_players_data(overall_data)


def seconds_to_minutes(seconds):
    """Function that takes seconds and converts to minutes."""
    seconds = "{0:.2f}".format(seconds / 60)
    minutes = seconds.split('.')
    if int(minutes[1]) >= 60:
        minutes[0] = int(minutes[0]) + 1
        minutes[1] = int(minutes[1]) - 60
    return '{} minutes and {} seconds'.format(minutes[0], minutes[1])

if __name__ == "__main__":
    get_player_match_id()