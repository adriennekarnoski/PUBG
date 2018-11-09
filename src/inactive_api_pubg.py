"""File to run program without active API call."""
from practice_data import data
from pubg import filter_game_data


def run_pubg_without_api():
    """Function to run pubg program without calling API.
    Use for testing and building without going over API rate limit."""
    filter_game_data(data)

if __name__ == "__main__":
    run_pubg_without_api()