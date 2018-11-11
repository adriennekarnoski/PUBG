import pytest


def test_files_work():
    from pubg import checking_files
    thing = checking_files()
    assert thing == 'yes'
