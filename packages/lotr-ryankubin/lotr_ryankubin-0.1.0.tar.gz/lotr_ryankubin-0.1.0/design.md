Design considerations

First time committing to pypi, caused some changes in structure

Lotr as the main connection object is kind of an awkward name, but fits the bill as needed

Did not take into consideration API rate limiting as I was somewhat constrained on time

/movie/{id}/quote endpoint didn't seem to be accepting filters; couldn't get it working in any context, but left the option in if it was a mistake on my part

Obviously a million more tests could be done, along with better specification on asserted Exceptions

Plaintext credentials in fixtures is awful, but again with time constraints I felt it was fine as is

Separation of movies and quotes seemed natural, as an expanded version would likely interface directly into the quotes endpoint instead

Overall it was a fun project, thanks!