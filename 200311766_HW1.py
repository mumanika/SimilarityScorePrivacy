import re, sys
import math, random
import numpy as np
import operator


#### BEGIN----- functions to read movie files and create db ----- ####

def add_ratings(db, chunks, num):
    if not chunks[0] in db:
        db[chunks[0]] = {}
    db[chunks[0]][num] = int(chunks[2])


def read_files(db, num):
    movie_file = "movies/" + num
    ratings = []
    fo = open(movie_file, "r")
    r = 0
    for line in fo:
        chunks = re.split(",", line)
        chunks[len(chunks) - 1] = chunks[len(chunks) - 1].strip()
        add_ratings(db, chunks, num)


#### END----- functions to read movie files and create db ----- ####

def score(w, p, aux, r):
    '''
    Inputs: weights of movies, max rating per moive, auxiliary information, and a record,
    Returns the corresponding score
    '''
    #### ----- your code here ----- ####

    pass


def compute_weights(db):
    '''
    Input: database of users
    Returns weights of all movies
    '''
    #### ----- your code here ----- ####

    ## you can use 10 base log

    pass


#### BEGIN----- additional functions ----- ####


#### END----- additional functions ----- ####

if __name__ == "__main__":
    db = {}
    files = ["03124", "06315", "07242", "16944", "17113",
             "10935", "11977", "03276", "14199", "08191",
             "06004", "01292", "15267", "03768", "02137"]

    for file in files:
        read_files(db, file)

    aux = {'14199': 4.5, '17113': 4.2, '06315': 4.0, '01292': 3.3,
           '11977': 4.2, '15267': 4.2, '08191': 3.8, '16944': 4.2,
           '07242': 3.9, '06004': 3.9, '03768': 3.5, '03124': 3.5}

    #### ----- your code here ----- ####

    def T(aux, r, dic, movie):
        return 1 - abs(aux-r)/(max(dic[movie]) - min(dic[movie]))

    weights = {}
    for movie in files:
        count = 0
        for user, ratings in db.items():
            count += list(ratings.keys()).count(movie)
        w = 1/math.log(count, 2)
        weights[movie] = w

    print("The weights that have been computed for the movies are:")
    for m,w in weights.items():
        print("{}\t{}".format(m,w))
    print("Minimum Weight: {}".format(min(weights.values())))
    print("Maximum Weight: {}".format(max(weights.values())))

    movie_ratings = {}
    for movie in aux.keys():
        movie_ratings[movie] = [aux[movie]]
    for user,ratings in db.items():
        for movie, rating in ratings.items():
            if movie in movie_ratings.keys():
                movie_ratings[movie].append(rating)

    supp_aux = len(aux.items())

    user_scores = {}
    for user, ratings in db.items():
        score = 0
        for movie, aux_rating in aux.items():
            if movie in ratings.keys():
                score += weights[movie]*T(aux_rating, ratings[movie], movie_ratings, movie)/supp_aux
            else:
                score += weights[movie]*T(aux_rating, 0, movie_ratings, movie)/supp_aux
        user_scores[user] = score

    similarity_scores = sorted(map(lambda x: x[1], user_scores.items()), reverse=True)
    print("The top 5 similarity scores are:")
    print(similarity_scores[:5])

    user, max = "", 0
    for u, score in user_scores.items():
        if score > max:
            user = u
            max = score

    print("The user ID with the highest similarity score is:")
    print(user, max)
    print("The movie ratings of this user along with the auxiliary database is:")
    for movie, rating in db[user].items():
        if movie in aux.keys():
            print(movie, rating, aux[movie])
        else:
            print(movie, rating)

    print("The difference between the highest and the second highest similarity scores are: {}".format(abs(similarity_scores[1] - similarity_scores[0])))

    M = 0
    for movie in aux.keys():
        M += weights[movie]/supp_aux
    print("The value of M for the auxiliary data set is: {}".format(M))













