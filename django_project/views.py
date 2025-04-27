from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the movie data (only once)
movies = pd.read_csv("netflix_titles.csv")
movies = movies.drop(['show_id', 'director', 'cast', 'country', 'date_added',
                      'rating', 'release_year', 'duration', 'listed_in'], axis=1)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['description'])
cos_theta = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_movies_by_description(movie_title, num_recommendations=5):
    try:
        idx = movies[movies['title'] == movie_title].index[0]
        sim_scores = list(enumerate(cos_theta[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations + 1]
        movie_indices = [i[0] for i in sim_scores]
        return movies['title'].iloc[movie_indices].tolist()
    except IndexError:
        return None

def index(request):
    titles = sorted(movies['title'].dropna().unique())
    return render(request, 'index.html', {'titles': titles})

def recommend(request):
    if request.method == 'POST':
        selected_movie = request.POST.get('movie')
        recommendations = recommend_movies_by_description(selected_movie)
        return render(request, 'result.html', {
            'selected_movie': selected_movie,
            'recommendations': recommendations
        })
    return render(request, 'recommender/index.html')
    