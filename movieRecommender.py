import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk   
from nltk.stem.porter import PorterStemmer   
from sklearn.metrics.pairwise import cosine_similarity
import pickle

#Methods:

def convert3(obj):
    myList = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            myList.append(i['name'])
            counter+=1
        else:
            break
    return myList

def convert(obj):
    myList = []
    for i in ast.literal_eval(obj):
        myList.append(i['name'])
    return myList

def fetch_director(obj):
    myList = []
    for i in ast.literal_eval(obj):
        if i['job'] == "Director":
            myList.append(i['name'])
            break
    return myList

def stem(text):
    myList = []
    for i in text.split():
        myList.append(ps.stem(i))
        
    return " ".join(myList)

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        print(new_df.iloc[i[0]].title)


# Reading the CSV files and loading them onto 'movies' and 'credits'
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

movies = movies.merge(credits,on='title')

# Changing the dataframe to includes ONLY these columns because these are bascially the only useful data to use to recommend movies
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]


movies.dropna(inplace=True)


movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['genres'] = movies['genres'].apply(convert)  


# Removing space between two words (ex.) Sam Worthington becomes SamWorthington
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ", "") for i in x])

# Creating a new column named 'tags' and adding elements of genres, keywords, cast, and crew in it
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Creating a new dataframe with columns containing the movie_id, title, and tags
new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()


ps = PorterStemmer()
new_df['tags'] = new_df['tags'].apply(stem)

similarity = cosine_similarity(vectors)

pickle.dump(new_df,open('movies.pkl', 'wb'))
pickle.dump(similarity,open('similarity.pkl', 'wb'))