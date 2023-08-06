from lotr_ryankubin.query import *
from lotr_ryankubin.schemas import MOVIE_SCHEMA


class Movie:
    """
    Movie allows access to a filtered and sorted set of movies
    """

    def __init__(
        self, http_instance, movie_id="", sort="", direction="dsc", movie_filter=""
    ):
        """

        :param http_instance: {HTTPSConnection} communication facilitator
        :param movie_id: {str} Movie id for a specific LOTR movie
        :param sort: {str} Sorting field, must match a Quote field
        :param direction: {str} Sorting direction, one of (asc, dsc) only
        :param movie_filter: {str} Filter to be applied to search.  Must match a Movie field,
        and supports (non)match, include/exclude, exists/does not exist, regex,
        and greater than/less than/equal to comparisons
        """
        self.http_instance = http_instance
        self.movie_id = movie_id
        self.sort = sort
        self.direction = direction
        self.movie_filter = movie_filter

    def get_movies(self):
        """
        :return: Get movies, applying any sorting and filters
        """
        # Would love to use params as a dict here, but since filter input doesn't
        # want to know it's a filter, settling for a rougher option
        params = "?"
        params += query_sort(self.sort, self.direction, MOVIE_SCHEMA)

        if params and self.movie_filter:
            params += "&"
        params += query_filter(self.movie_filter, MOVIE_SCHEMA)
        return self.http_instance.get(self.http_instance.endpoint + params)

    def get_movie(self):
        """
        :return: Get movie based on id
        """
        return self.http_instance.get(f"{self.http_instance.endpoint}/{self.movie_id}")
