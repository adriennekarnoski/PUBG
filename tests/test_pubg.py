import pytest


@pytest.fixture
def mock_api():
    from pubg import game_data_dict, helper_function
    helper_function()


@pytest.fixture
def game_dict():
    from pubg import game_data_dict
    return game_data_dict


def test_things_work():
    """Test game_data_dict is empty before application is run."""
    from pubg import game_data_dict
    assert not game_data_dict


def test_more_things_work(mock_api):
    from pubg import game_data_dict
    assert game_data_dict


def test_dict(game_dict):
    from pubg import filter_game_data
    from inactive_api_pubg import game_one
    filter_game_data(game_one)
    assert game_dict['map'] == 'Erangel'