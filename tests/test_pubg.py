import pytest
import mock


@pytest.fixture
def mock_api():
    from mock_data import data
    from pubg import User, filter_game_data
    user = User('example')
    return filter_game_data(data, user)


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
    game_data, user = mock_api
    assert user.gamertag == 'example'
    assert game_data.duration == '30:53'
    assert game_data.date == 'Thu, Nov 15'
    assert game_data.map == 'Erangel'


# def test_dict(game_dict):
#     from pubg import filter_game_data
#     from inactive_api_pubg import game_one
#     filter_game_data(game_one)
#     assert game_dict['map'] == 'Erangel'