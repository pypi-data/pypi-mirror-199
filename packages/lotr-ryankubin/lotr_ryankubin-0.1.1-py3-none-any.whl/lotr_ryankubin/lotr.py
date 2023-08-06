from lotr_ryankubin.connection import HTTPSConnection
from lotr_ryankubin.quote import Quote
from lotr_ryankubin.movie import Movie
from lotr_ryankubin.config import *


class Lotr:
    """
    Since we'll be working within the movies endpoint on the LOTR API, lets consolidate
    to one main place to interact with it, and manage our credentials/connection
    """

    def __init__(
        self,
        access_token=ACCESS_TOKEN,
        host=HOST_URL,
        version=API_VERSION,
        path=MOVIE_PATH,
    ):
        """
        Class that allows access to the API and provides the connection details for authentication
        :param: access_token: {int} access key to grant access to the API
        :param: host: {str} base API url
        :param: version: {str} API version
        :param: path: {str} primary API path
        """
        self.access_token = access_token
        self.host = host
        self.version = version
        self.path = path
        self.headers = {}
        self.endpoint = None
        self.http_instance = None
        self._validate_connection()

    def _validate_connection(self):
        if self.access_token is None or self.access_token == "":
            raise PermissionError("Access token required to view movies")
        self.endpoint = f"https://{self.host}/{self.version}/{self.path}"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

        self.http_instance = HTTPSConnection(
            endpoint=self.endpoint, headers=self.headers
        )
        # In lieue of an API endpoint that establishes connection or handles a handshake,
        # will use the movie endpoint to test authorization
        test_connection = self.http_instance.get(url=self.endpoint)
        if "success" in test_connection and test_connection["success"] is False:
            raise

    def movie(self, movie_id="", sort="", direction="dsc", movie_filter=""):
        """
        Explore the movies from the Lord of the Rings, including their awards, box office, and run time
        Become frustrated with audiences when you see that the Hobbit trilogy has a higher cume than the
        original
        :param movie_id: {str} Specific movie ID if looking for one movie in particular
        :param sort: {str} Sorting field, must match a Movie field
        :param direction: {str} Sorting direction, one of (asc, dsc) only
        :param movie_filter: {str} Filter to be applied to search.  Must match a Movie field,
        and supports (non)match, include/exclude, exists/does not exist, regex,
        and greater than/less than/equal to comparisons
        :return: Movie
        """
        return Movie(
            self.http_instance,
            movie_id=movie_id,
            sort=sort,
            direction=direction,
            movie_filter=movie_filter,
        )

    def quote(self, movie_id, sort="", direction="dsc", quote_filter="", limit=10):
        """
        Quotes include dialog from the movies, categorized by movie.  Use this to explore your favorite quotes!
        :param movie_id: {str} {required} Movie id for the quotes you wish to explore
        :param sort: {str} Sorting field, must match a Quote field
        :param direction: {str} Sorting direction, one of (asc, dsc) only
        :param quote_filter: {str} Filter to be applied to search.  Must match a Movie field,
        and supports (non)match, include/exclude, exists/does not exist, regex,
        and greater than/less than/equal to comparisons *NB* Currently not working
        :param limit: {int} Number of results to retrieve at one time
        :return: Quote
        """
        return Quote(
            self.http_instance,
            movie_id,
            sort=sort,
            direction=direction,
            quote_filter=quote_filter,
            limit=limit,
        )
