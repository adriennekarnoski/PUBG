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
from terminaltables import SingleTable


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
    """Function taking user gamertag to make api call to retun match ids."""
    user_gamertag = input('Please enter your gamertag: ')
    gamertag = user_gamertag
    response_matches = make_api_call('gamertag', gamertag)
    try:
        match_id = response_matches['data'][0]['relationships']['matches']['data'][0]['id']
        response_game_data = make_api_call('match', match_id)
        filter_game_data(response_game_data)
    except IndexError:
        print("No matches for {} within the last 14 days".format(gamertag))


def print_game_data(game_data_dict):
    """Function to print game data."""
    response = """
        {}'s Last Match

        Game Duration: {}
        Date: {}
        Map: {}""".format(
            gamertag,
            game_data_dict['duration'],
            game_data_dict['date'],
            game_data_dict['map']
            )
    print(response)


def filter_game_data(input_dict):
    """Filter out information about the game."""
    game_data_dict = {}
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
    print_game_data(game_data_dict)
    create_dataframe(input_dict)


def create_dataframe(input_dict):
    """Function that takes in api response and creates a pandas dataframe."""
    d = {
        'kills': [],
        'headshotKills': [],
        'assists': [],
        'DBNOs': [],
        'longestKill': [],
        'killPlace': [],
        'killPoints': [],
        'damageDealt': [],
        'winPlace': [],
        'walkDistance': [],
        'rideDistance': [],
        'swimDistance': [],
        'timeSurvived': [],
        'winPoints': [],
        'boosts': [],
        'heals': [],
        'revives': [],
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


def get_data_from_dataframe(df):
    """Get all necessary data from dataframe."""
    player_data = df.loc[df['name'] == gamertag].values.tolist()[0]
    for i in range(len(player_data)):
        if player_data[i] == 0.0:
            player_data[i] = 0
        if type(player_data[i]) is float:
            player_data[i] = "{0:.2f}".format(player_data[i])
    player_data.remove(gamertag)
    player_data.pop(8)
    average_values = create_average_list(df)
    average_values.pop(8)
    top_ten_df = df.loc[df['winPlace'] <= 10]
    top_ten = create_average_list(top_ten_df)
    top_ten.pop(8)
    print_table(player_data, average_values, top_ten)


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


def print_table(player, overall, top_ten):
    """Return all data to user in a table."""
    labels = [
        'Kills',
        'Headshot Kills',
        'Assists',
        'DBNOs',
        'Longest Kill (m)',
        'Kill Place',
        'Kill Points',
        'Damage Dealt',
        'Walk Distance (m)',
        'Ride Distance (m)',
        'Swim Distance (m)',
        'Time Survived',
        'Win Points',
        'Boosts',
        'Heals',
        'Revives',
        'Weapons Acquired']
    data = [['', gamertag.upper(), 'OVERALL AVERAGE', 'TOP TEN AVERAGE']]
    player_score = 0
    distance_list = [4, 8, 9, 10]
    for i in range(len(labels)):
        row = []
        row.append(labels[i])
        if i == 11:
            row.append(seconds_to_minutes(float(player[i])))
            row.append(seconds_to_minutes(float(overall[i])))
            row.append(seconds_to_minutes(float(top_ten[i])))
        else:
            row.append(player[i])
            row.append(overall[i])
            row.append(top_ten[i])
        data.append(row)
    table = SingleTable(data)
    print(table.table)


def seconds_to_minutes(seconds):
    """Function that takes seconds and converts to minutes."""
    seconds = "{0:.2f}".format(seconds / 60)
    minutes = seconds.split('.')
    if int(minutes[1]) >= 60:
        minutes[0] = int(minutes[0]) + 1
        minutes[1] = int(minutes[1]) - 60
    return '{}:{}'.format(minutes[0], minutes[1])


def run_pubg():
    """."""
    opening_prompt = """
        Please make a selection:

        [1] Get stats on your last PUBG game played (Requires XBOX gamertag)
        [2] See an example using past data

        Enter selection:
    """
    user_input = input(opening_prompt)
    if user_input == '1':
        get_player_match_id()
    if user_input == '2':
        os.system('clear')
        filter_game_data(data)
    else:
        os.system('clear')
        print('OPTION NOT VALID')
        run_pubg()

if __name__ == "__main__":
    run_pubg()