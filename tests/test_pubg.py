import pytest
import mock


@pytest.fixture
def mock_api():
    from mock_data import data
    from pubg import user, filter_game_data
    user.gamertag = 'example'
    return filter_game_data(data)


# @pytest.fixture
# def game_dict():
#     from pubg import game_data_dict
#     return game_data_dict


# def test_things_work():
#     """Test game_data_dict is empty before application is run."""
#     from pubg import game_data_dict
#     assert not game_data_dict


def test_more_things_work(mock_api):
    """Test function return correct class attributes."""
    from pubg import filter_game_data
    user, game = mock_api
    assert user.gamertag == 'example'
    assert game.duration == '30:53'
    assert game.date == 'Thu, Nov 15'
    assert game.game_map == 'Erangel'


# def test_dict(game_dict):
#     from pubg import filter_game_data
#     from inactive_api_pubg import game_one
#     filter_game_data(game_one)
#     assert game_dict['map'] == 'Erangel'