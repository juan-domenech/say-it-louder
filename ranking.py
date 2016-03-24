
def basic_ranking(movies):
    movies_new = []

    # We are interested only in movies and tv series titles
    for movie in movies:
        if movie['kind'] == 'movie' or movie['kind'] == 'tv series':
            movies_new.append(movie)

    # Discard year = 0 or 2155 (Movie in development)
    movies_temp = []
    for movie in movies_new:
        if movie['year'] != 0 and movie['year'] != 2155:
            movies_temp.append(movie)

    # Field reorder
    movies_temp = []
    for movie in movies_new:
        temp = {}
        temp['title'] = movie['title']
        temp['year'] = movie['year']
        temp['movieID'] = movie['movieID']
        movies_temp.append(temp)
    movies_new = movies_temp

    # Sorting
    movies_new = sorted(movies_new)

    # Reverse
    movies_new = movies_new[::-1]

    # Limit to 40 matches
    return movies_new[0:40]
