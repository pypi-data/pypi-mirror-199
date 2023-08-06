from tests.fixtures import *


def test_bad_filter(blank_movie):
    with pytest.raises(Exception):
        blank_movie.movie_filter = ">=10"
        blank_movie.get_movies()


def test_good_filter(blank_movie):
    blank_movie.movie_filter = "academyAwardWins>0"
    assert blank_movie.get_movies()["total"] == 6


def test_bad_sort(blank_movie):
    with pytest.raises(Exception):
        blank_movie.sort = "not_a_field"
        blank_movie.get_movies()


def test_good_sort(blank_movie):
    blank_movie.sort = "name"
    assert blank_movie.get_movies()["docs"][0]["name"] == "The Unexpected Journey"
