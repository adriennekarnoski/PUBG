"""Run terminal prompts to user."""
import requests
import os
from practice_data import data

url = "https://api.pubg.com/shards/xbox-na/matches/50e82100-bbfb-4499-be93-a8af7cb6d63c"
# url = "https://api.pubg.com/shards/xbox-na/samples"
# url = "https://api.pubg.com/shards/xbox-na/players?filter[playerNames]=ehhhdrienne"

api_key = os.environ.get('API_KEY')

header = {
  "Authorization": "Bearer " + api_key,
  "Accept": "application/vnd.api+json"
}

r = requests.get(url, headers=header)
response_dict = r.json()


average_dict = {
    'count': 0,
    'assists': 0,
    'damage': 0,
    'headshots': 0,
}
def filter_players(response_dict):
    """Begin the program."""
    players = response_dict['included']
    stats = players[0]['attributes']['stats']
