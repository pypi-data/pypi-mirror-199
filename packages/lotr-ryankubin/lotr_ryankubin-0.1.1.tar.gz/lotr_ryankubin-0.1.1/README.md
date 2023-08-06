## LOTR SDK
***
If you've ever wanted to have every piece of dialogue from every lord of the rings movie at your fingertips, boy do I have the SDK for you.  With this package, you'll be able to access information on all 6 (yes, even the hobbit trilogy) movies, and every quote therein.

### Prerequisites
You'll need python 3 installed.

### Setup and Installation
To get started, you'll need to install the lotr_ryankubin package

```
pip install lotr_ryankubin
```

## How to use it
The key to the whole interaction is to create a `Lotr` object.  You'll need to initialize this with your access token, which you can obtain by registering [here](https://the-one-api.dev/).
Once you have your token, initialize your connection
```
from lotr_ryankubin.lotr import Lotr
l = Lotr(access_token='your_token_here')
```
If there is any issue authenticating, this will raise an unauthorized error, and you'll need to check your token to confirm it is correct.

From here, you now have access to the two main functions: movies and quotes. When you call a get, the return for all will be in JSON.  Both are able to apply filters and sorts, in the format:
Sort:
```
sort=<field_name>
direction = asc|dsc
```
Filter:
```
movie_filter=<fieldname><filterlogic>
```
Where filterlogic can be a regular expression, a comparison, existance, etc.  Review the docs above to see the different formats and available options.

To fetch all movies:
```
m = l.movie()
m.get_movies()
```

To fetch movies with an academy award:
```
fancy_m = l.movie(movie_filter='academyAwardWins>0')
fancy_m.get_movies()
```

To fetch all quotes:
```
q = l.quote(movie_id=<movie_id>)
q.get_quotes()
```

Quotes are paginated by default, you can iterate through them by next(), previous(), or setting the limit or offset manually on the quote object
```
q.next()
q.previous()

q.limit = 100
q.next()
