import pytest

from lotr_ryankubin.lotr import Lotr


@pytest.fixture
def blank_lotr():
    """
    Returns a base connected Lotr
    Obviously terrible to have my credentials here
    """
    return Lotr(access_token='BzfZfw9Ti-TYlXBytdRT')


@pytest.fixture
def blank_movie(blank_lotr):
    """
    :return: All movies
    """
    return blank_lotr.movie()


@pytest.fixture
def movie_id():
    """
    :return: Movie id
    """
    return '5cd95395de30eff6ebccde5c'
