"""Run terminal prompts to user."""
import requests
import os
# from mock_api_response import data
from mock_data import data
from statistics import mean
import json
from datetime import datetime
import csv
import pandas

table_data = []

gamertag = 'example'

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
        # filter_game_data(response_game_data)
        save_to_file(response_game_data)
    except IndexError:
        print("No matches within the last 14 days")


# def save_to_file(input_data):
#     with open('data.py', 'w') as outfile:
#         json.dump(input_data, outfile)


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
    time = datetime.strptime(game['createdAt'], "%Y-%m-%dT%H:%M:%SZ")
    game_data_dict['date'] = time.strftime('%a, %b %d')
    game_data_dict['duration'] = seconds_to_minutes(game['duration'])
    if game['mapName'] == 'Desert_Main':
        game_data_dict['map'] = 'Miramar'
    if game['mapName'] == 'Savage_Main':
        game_data_dict['map'] = 'Sanhok'
    map_name = game['mapName'].split('_')
    game_data_dict['map'] = map_name[0]
    filter_player_data(input_dict)


# def filter_player_data(input_dict):
#     """Function that takes in api response and filters out necessary data."""
#     with open('pubg_stats.csv', mode='w') as csv_file:
#         fieldnames = [
#             'DBNOs',
#             'assists',
#             'boosts',
#             'damage',
#             'death',
#             'headshots',
#             'heals',
#             'win_place',
#             'win_points',
#             'kills',
#             'revives',
#             'ride_distance',
#             'swim_distance',
#             'walk_distance',
#             'longest_kill',
#             'time_survived',
#             'weapons',
#             'name'
#         ]
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         writer.writeheader()
#         player_list = input_dict['included']
#         for i in range(len(player_list)):
#             if player_list[i]['type'] == 'participant':
#                 stats = player_list[i]['attributes']['stats']
#                 writer.writerow(
#                     {
#                         'DBNOs': stats['DBNOs'],
#                         'assists': stats['assists'],
#                         'boosts': stats['boosts'],
#                         'damage': stats['damageDealt'],
#                         'death': stats['deathType'],
#                         'headshots': stats['headshotKills'],
#                         'heals': stats['heals'],
#                         'win_place': stats['winPlace'],
#                         'win_points': stats['winPoints'],
#                         'kills': stats['kills'],
#                         'revives': stats['revives'],
#                         'ride_distance': stats['rideDistance'],
#                         'swim_distance': stats['swimDistance'],
#                         'walk_distance': stats['walkDistance'],
#                         'longest_kill': stats['longestKill'],
#                         'time_survived': stats['timeSurvived'],
#                         'weapons': stats['weaponsAcquired'],
#                         'name': stats['name']
#                     }
#                 )
#     get_dataframe_data()


def create_dataframe(input_dict):
    """Function that takes in api response and filters out necessary data."""
    d = {
        'DBNOs': [],
        'assists': [],
        'boosts': [],
        'damageDealt': [],
        'headshotKills': [],
        'heals': [],
        'winPlace': [],
        'winPoints': [],
        'kills': [],
        'revives': [],
        'rideDistance': [],
        'swimDistance': [],
        'walkDistance': [],
        'longestKill': [],
        'timeSurvived': [],
        'weaponsAcquired': [],
        'name': []
    }
    player_list = input_dict['included']
    for i in range(len(player_list)):
        if player_list[i]['type'] == 'participant':
            stats = player_list[i]['attributes']['stats']
            for key, value in stats.items():
                if key in d:
                    d[key].append(value)
    df = pandas.DataFrame(d)
    get_data_from_dataframe(df)
    # return df


# def get_dataframe_data():
#     """Create a pandas dataframe and get desired values."""
#     get_average = ['kills', 'headshots', 'time_survived']
#     get_max = ['kills', 'headshots', 'damage', 'longest_kill']
#     overall_data_list = []
#     df = pandas.read_csv('pubg_stats.csv')
#     df_player_row = df.loc[df['name'] == game_data_dict['gamertag']].values.tolist()
#     for i in range(len(get_average)):
#         overall_data_list.append(df[get_average[i]].mean())
#     for i in range(len(get_max)):
#         overall_data_list.append(df[get_max[i]].max())
#     player_data = edit_player_data(df_player_row[0])
#     overall_data = edit_overall_game_data(overall_data_list)
#     return_to_user(player_data, overall_data)


def get_data_from_dataframe(df):
    """Create a pandas dataframe and get desired values."""
    player_data = df.loc[df['name'] == gamertag].values.tolist()[0]
    for i in range(len(player_data)):
        if player_data[i] == 0.0:
            player_data[i] = 0
        if type(player_data[i]) is float:
            player_data[i] = "{0:.2f}".format(player_data[i])
    player_data.remove(gamertag)
    df.drop(columns=['name'])
    average_values = create_average_list(df)
    top_ten_df = df.loc[df['winPlace'] <= 10]
    top_ten = create_average_list(top_ten_df)
    print_dataframe(player_data, average_values, top_ten)
    # df = pandas.read_csv('pubg_stats.csv')
    # df_player_row = df.loc[df['name'] == game_data_dict['gamertag']].values.tolist()
    # for i in range(len(get_average)):
    #     overall_data_list.append(df[get_average[i]].mean())
    # for i in range(len(get_max)):
    #     overall_data_list.append(df[get_max[i]].max())
    # player_data = edit_player_data(df_player_row[0])
    # overall_data = edit_overall_game_data(overall_data_list)
    # return_to_user(player_data, overall_data)


def create_average_list(df):
    """Find the average of columns in a dataframe."""
    output_list = []
    for column in df:
        if df[column].dtype == 'int64':
            output_list.append(int(round(df[column].mean())))
        elif df[column].dtype == 'float64':
            average = df[column].mean()
            output_list.append("{0:.2f}".format(average))
    return output_list


def print_dataframe(player, overall, top_ten):
    """."""
    output_df = pandas.DataFrame.from_dict(
        dict([
            (gamertag, player),
            ('All Players', overall),
            ('Top 10', top_ten),
        ]))
    print(output_df)

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


def helper_function():
    """Function to run application without API call."""
    game_data_dict['gamertag'] = 'example'
    filter_game_data(data)

# if __name__ == "__main__":
#     helper_function()