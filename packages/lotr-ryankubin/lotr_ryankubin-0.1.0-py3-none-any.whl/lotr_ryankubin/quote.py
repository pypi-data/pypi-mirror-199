from lotr_ryankubin.query import *
from lotr_ryankubin.schemas import QUOTE_SCHEMA


class Quote:
    """
    Quote allows access to a filtered and sorted set of quotes by movie (original LOTR only)
    """

    def __init__(
        self,
        http_instance,
        movie_id,
        quote_id="",
        sort="",
        direction="dsc",
        quote_filter="",
        limit=10,
    ):
        """
        :param http_instance: {HTTPSConnection} communication facilitator
        :param movie_id: {str} {required} Movie id for the quotes you wish to explore
        :param sort: {str} Sorting field, must match a Quote field
        :param direction: {str} Sorting direction, one of (asc, dsc) only
        :param quote_filter: {str} Filter to be applied to search.  Must match a Movie field,
        and supports (non)match, include/exclude, exists/does not exist, regex,
        and greater than/less than/equal to comparisons *NB* Currently not working
        :param limit: {int} Number of results to retrieve at one time
        """
        self.http_instance = http_instance
        self.movie_id = movie_id
        self.quote_id = quote_id
        self.sort = sort
        self.direction = direction
        self.quote_filter = quote_filter
        self.endpoint = f"{self.http_instance.endpoint}/{movie_id}/quote"
        self.limit = limit
        # using offset rather than provided page to allow users to change their limit
        # while maintaining place
        self.offset = 0

    def get_quotes(self, offset=0):
        """
        :param  offset: {int} -- starting point to begin list of quotes if more than the limit
        :return Quotes, applying limit, offset, sorting, and filters
        """
        # Would love to use params as a dict here, but since filter input doesn't
        # want to know it's a filter, settling for a rougher option
        params = f"?offset={offset}&limit={self.limit}"
        if self.sort:
            params += "&"
            params += query_sort(self.sort, self.direction, QUOTE_SCHEMA)

        # I can't seem to get the API to recognize filters; it doesn't fail, but it doesn't apply
        # properly either.  Sorting is working ok, and filters work for movies.
        if self.quote_filter:
            params += "&"
            params += query_filter(self.quote_filter, QUOTE_SCHEMA)
        print(params)
        if not offset:
            self.offset = self.limit
        else:
            self.offset += self.limit

        return self.http_instance.get(self.endpoint + params)

    def next(self):
        """
        :return: Get next set of results from the query
        """
        next_quotes = self.get_quotes(self.offset)
        return next_quotes

    def previous(self):
        """
        :return: Get the previously set of results from the query
        """
        previous_quotes = self.offset - self.limit * 2
        if previous_quotes > 0:
            self.offset = previous_quotes
            return self.get_quotes(self.offset)
        else:
            return self.get_quotes()
