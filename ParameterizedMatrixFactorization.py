import csv
from scipy.sparse.linalg import svds
import numpy as np
import pandas as pd

movies_list = []
users_list = []
ratings_list = []

def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations = 5):
	#sorting users predictions
	user_row_number = userID - 1
	sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending = False)

	#get user data and merge in movie information
	user_data = original_ratings_df[original_ratings_df.UserID == (userID)]
	user_full = (user_data.merge(movies_df, how = 'left', left_on = 'MovieID', right_on = 'MovieID').sort_values(['Rating'], ascending=False))

	print 'User {0} has already rated {1} movies.'.format(userID, user_full.shape[0])
	print 'Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations)
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
	recommendations = (movies_df[~movies_df['MovieID'].isin(user_full['MovieID'])].merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',left_on = 'MovieID',right_on = 'MovieID').rename(columns = {user_row_number: 'Predictions'}).sort_values('Predictions', ascending = False).iloc[:num_recommendations, :-1])

	return user_full, recommendations



def init():	
	ratings_list = [i.strip().split("::") for i in open('/home/ashwin/Documents/smai project/ml-1m/ratings.dat', 'r').readlines()]
	users_list = [i.strip().split("::") for i in open('/home/ashwin/Documents/smai project/ml-1m/users.dat', 'r').readlines()] 
	movies_list = [i.strip().split("::") for i in open('/home/ashwin/Documents/smai project/ml-1m/movies.dat', 'r').readlines()] 

	ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'MovieID', 'Rating', 'Timestamp'], dtype = int)
	movies_df = pd.DataFrame(movies_list, columns = ['MovieID', 'Title', 'Genres'])
	movies_df['MovieID'] = movies_df['MovieID'].apply(pd.to_numeric, errors = 'ignore')
	
	movies_df.head()
	#movies_df.head()
	ratings_df.head()
	R_df = ratings_df.pivot(index = 'UserID', columns = 'MovieID', values = 'Rating').fillna(0)
	#print R_df.head()

	R = R_df.as_matrix()
	user_ratings_mean = np.mean(R, axis = 1)
	R_demeaned = R - user_ratings_mean.reshape(-1, 1)
	U, sigma, Vt = svds(R_demeaned, k = 80)
#parameters between range 20 to 100 given optimal results

	sigma = np.diag(sigma)

	#print R_demeaned.shape
	print U.shape
	print Vt.shape
	print sigma

	all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
	preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)

	already_rated, predictions = recommend_movies(preds_df, 837, movies_df, ratings_df, 10)

	print predictions
		


init()



import requests
import json

response = requests.get('http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)')
print response.url.split('/')[-2]

# Get base url filepath structure. w185 corresponds to size of movie poster.
headers = {'Accept': 'application/json'}
payload = {'api_key': 'Plz insert your key here '}
response = requests.get("http://api.themoviedb.org/3/configuration", params=payload, headers=headers)
response = json.loads(response.text)
base_url = response['images']['base_url'] + 'w185'

def get_poster(imdb_url, base_url):
    # Get IMDB movie ID
    response = requests.get(imdb_url)
    movie_id = response.url.split('/')[-2]
    
    # Query themoviedb.org API for movie poster path.
    movie_url = 'http://api.themoviedb.org/3/movie/{:}/images'.format(movie_id)
    headers = {'Accept': 'application/json'}
    payload = {'api_key': 'INSERT API_KEY HERE'} 
    response = requests.get(movie_url, params=payload, headers=headers)
    try:
        file_path = json.loads(response.text)['posters'][0]['file_path']
    except:
        # IMDB movie ID is sometimes no good. Need to get correct one.
        movie_title = imdb_url.split('?')[-1].split('(')[0]
        payload['query'] = movie_title
        response = requests.get('http://api.themoviedb.org/3/search/movie', params=payload, headers=headers)
        movie_id = json.loads(response.text)['results'][0]['id']
        payload.pop('query', None)
        movie_url = 'http://api.themoviedb.org/3/movie/{:}/images'.format(movie_id)
        response = requests.get(movie_url, params=payload, headers=headers)
        file_path = json.loads(response.text)['posters'][0]['file_path']
        
    return base_url + file_path
    
    
toy_story = 'http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)'

# Load in movie data
idx_to_movie = {}
with open('ml-100k/u.item', 'r') as f:
    for line in f.readlines():
        info = line.split('|')
        idx_to_movie[int(info[0])-1] = info[4]
        
def top_k_movies(similarity, mapper, movie_idx, k=6):
    return [mapper[x] for x in np.argsort(similarity[movie_idx,:])[:-k-1:-1]]
    
idx = 0 # Toy Story
movies = top_k_movies(item_similarity, idx_to_movie, idx)


