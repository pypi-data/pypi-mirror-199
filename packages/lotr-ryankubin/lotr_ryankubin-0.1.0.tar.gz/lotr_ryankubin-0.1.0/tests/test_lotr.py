from tests.fixtures import *
from lotr_ryankubin.movie import Movie
from lotr_ryankubin.quote import Quote

import pytest


def test_connection_successful(blank_lotr):
    assert blank_lotr.http_instance.endpoint == "https://the-one-api.dev/v2/movie"


def test_bad_creds():
    with pytest.raises(Exception):
        l = Lotr(access_token="fubar")


def test_no_creds():
    with pytest.raises(Exception):
        l = Lotr()


def test_get_movie(blank_lotr):
    assert isinstance(blank_lotr.movie(), Movie)


def test_get_quote(blank_lotr):
    assert isinstance(blank_lotr.quote(movie_id=movie_id), Quote)
