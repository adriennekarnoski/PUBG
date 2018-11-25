"""Run terminal prompts to user."""
import requests
import os
from mock_data import data
from statistics import mean
import json
from datetime import datetime
import csv
import pandas
from terminaltables import SingleTable


class User(object):
    """Class for user to store data."""

    def __init__(self, gamertag=None, win_place=None, kill_place=None):
        """Initialize a User class."""
        self.gamertag = gamertag
        self.win_place = win_place
        self.kill_place = kill_place


class GameData(object):
    """Class for storing game data."""

    def __init__(self, date=None, mode=None, duration=None, game_map=None):
        """Initialize a GameData class."""
        self.date = date
        self.duration = duration
        self.mode = mode
        self.game_map = game_map


game = GameData()

user = User()


def make_api_call(type, data):
    """Function to make api call and return response dictionary."""
    api_key = os.environ.get('API_KEY')
    header = {
      "Authorization": "Bearer " + api_key,
      "Accept": "application/vnd.api+json"
    }
    if type == 'gamertag':
        url = "https://api.pubg.com/shards/xbox-na/players?filter[playerNames]={}".format(data)
    if type == 'match':
        url = "https://api.pubg.com/shards/xbox-na/matches/{}".format(data)
    r = requests.get(url, headers=header)
    response_dict = r.json()
    return response_dict


def get_player_match_id():
    """Function taking user gamertag to make api call to retun match ids."""
    gamertag = input('Please enter your gamertag: ')
    user.gamertag = gamertag
    if gamertag == 'example':
        filter_game_data(data)
    else:
        response_matches = make_api_call('gamertag', gamertag)
        get_last_game(response_matches)


def get_last_game(response_matches):
    """Take match ids and run api call on last match played."""
    try:
        match_id = response_matches['data'][0]['relationships']['matches']['data'][0]['id']
        response_game_data = make_api_call('match', match_id)
        filter_game_data(response_game_data)
    except IndexError:
        print("No matches for {} within the last 14 days".format(user.gamertag))


def filter_game_data(input_dict):
    """Filter out information about the game."""
    game_dict = input_dict['data']['attributes']
    time = datetime.strptime(game_dict['createdAt'], "%Y-%m-%dT%H:%M:%SZ")
    game.date = time.strftime('%a, %b %d')
    game.duration = seconds_to_minutes(game_dict['duration'])
    game.mode = game_dict['gameMode']
    if game_dict['mapName'] == 'Desert_Main':
        game.game_map = 'Miramar'
    if game_dict['mapName'] == 'Savage_Main':
        game.game_map = 'Sanhok'
    map_name = game_dict['mapName'].split('_')
    game.game_map = map_name[0]
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
    player_row = df.loc[df['name'] == user.gamertag]
    user.win_place = player_row['winPlace'].values[0]
    user.kill_place = player_row['killPlace'].values[0]
    player_data = player_row.values.tolist()[0]
    for i in range(len(player_data)):
        if player_data[i] == 0.0:
            player_data[i] = 0
        if type(player_data[i]) is float:
            player_data[i] = "{0:.2f}".format(player_data[i])
    player_data.remove(user.gamertag)
    average_values = create_average_list(df)
    top_ten_df = df.loc[df['winPlace'] <= 10]
    top_ten = create_average_list(top_ten_df)
    values_list = [player_data, average_values, top_ten]
    for i in range(len(values_list)):
        values_list[i].pop(8)
        values_list[i].pop(5)
    create_table(values_list[0], values_list[1], values_list[2])


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


def create_table(player, overall, top_ten):
    """Create a table for returning to the user."""
    labels = [
        'Kills',
        'Headshot Kills',
        'Assists',
        'DBNOs',
        'Longest Kill (m)',
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
    gamertag = user.gamertag
    data = [['', gamertag, 'OVERALL AVERAGE', 'TOP TEN AVERAGE']]
    player_score = 0
    for i in range(len(labels)):
        row = []
        row.append(labels[i])
        if i == 10:
            row.append(seconds_to_minutes(float(player[i])))
            row.append(seconds_to_minutes(float(overall[i])))
            row.append(seconds_to_minutes(float(top_ten[i])))
        else:
            row.append(player[i])
            row.append(overall[i])
            row.append(top_ten[i])
        data.append(row)
    table = SingleTable(data, 'PLAYER DATA')
    compare_response = compare_user(data[1:])
    return_to_user(compare_response, table)


def compare_user(input_list):
    """Compare user stats to the average game stats."""
    width = os.get_terminal_size().columns
    user_score = 0
    more_than = [0, 1, 2, 3, 5, 6, 11]
    for i in range(len(input_list)):
        if i in more_than:
            if input_list[i][1] > input_list[i][2]:
                user_score += 1
            if input_list[i][1] < input_list[i][2]:
                user_score -= 1
    if user_score > 0:
        blame = "EVERYONE"
    if user_score < 0:
        blame = "JUST YOU"
    if user_score == 0:
        blame = "TOO CLOSE TO TELL"
    response = " IT WAS {} ".format(blame)
    return response
    # for i in range(6):
    #     if i == 2:
    #         print(response.center(width))
    #     else:
    #         print('\n')


def return_to_user(compare_response, player_table):
    """Print table and other data for the user."""
    data = [[
        'DATE: {}'.format(game.date),
        'DURATION: {}'.format(game.duration),
        'MODE: {}'.format(game.mode),
        'MAP: {}'.format(game.game_map)]]
    game_table = SingleTable(data, 'MATCH ATTRIBUTES')
    print_list = [
        # '\n\n\n{}\n\n\n'.format(compare_response),
        '{0}{1}{2}'.format('\n' * 3, compare_response, '\n' * 3),
        game_table.table,
        player_table.table]
    # print(game_table.table)
    # print(player_table.table)
    # for i in range(6):
    #     if i == 2:
    #         print(compare_response)
    #     if i == 4:
    #         print(game_table.table)
    #     if i == 5:
    #         print(player_table.table)
    #     else:
    #         print('\n')
    for i in range(len(print_list)):
        print(print_list[i])


def seconds_to_minutes(seconds):
    """Function that takes seconds and converts to minutes."""
    seconds = "{0:.2f}".format(seconds / 60)
    minutes = seconds.split('.')
    if int(minutes[1]) >= 60:
        minutes[0] = int(minutes[0]) + 1
        minutes[1] = int(minutes[1]) - 60
    return '{}:{}'.format(minutes[0], minutes[1])


def run_pubg():
    """Opening function to run the program."""
    os.system('clear')
    opening_prompt = """
        Please make a selection:

        [1] Get stats on your last PUBG game played (Requires XBOX gamertag)
        [2] See an example using past data

        Enter selection:
    """
    user_input = input(opening_prompt)
    if user_input == '1':
        get_player_match_id()
    elif user_input == '2':
        user.gamertag = 'example'
        filter_game_data(data)
    else:
        print('OPTION NOT VALID')
        run_pubg()

if __name__ == "__main__":
    # run_pubg()
    get_player_match_id()