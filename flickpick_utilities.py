from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import nltk
from nltk.stem import WordNetLemmatizer
import csv
import random


genres  = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 
           'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 
           'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 
           'Thriller', 'TV Movie', 'War', 'Western']

class MovieSearchForm(FlaskForm):
    freeform_text_input = StringField('Describe your ideal movie:')
    similar_titles = BooleanField('Find Similar Titles')
    submit = SubmitField('Pick my Flick')


def genre_list(movie_search_form, genres):
    fields = {genre: BooleanField(label=genre) for genre in genres}
    return type('MovieSearchForm', (movie_search_form,), fields)

MovieSearchForm = genre_list(MovieSearchForm, genres)

# ----------------------------------------------------------------------

def input_cleaner(user_input:str):

    # Remove blankspace and capitalizations from input
    user_input_without_whitespace = user_input.strip()
    clean_user_input = user_input_without_whitespace.lower()

    return clean_user_input

# ----------------------------------------------------------------------

nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
pd.set_option("display.max_colwidth", 10000)


# Standardize text for vectorization
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text
    
def lemmatize_text(text):
    words = text.split()
    lemmatized_text = ""
    for word in words:
        lemmatized_text = f'{lemmatized_text}{lemmatizer.lemmatize(word)} '
    return lemmatized_text

csv_location = 'static/documents/filtered_movie_dataset.csv'

# Function to find and return movie IDs
def clustering_moviefinder(input_text: str, requested_genres_list=None):
    
    # Fetch raw data
    df = pd.read_csv(csv_location)

    # Filter the DataFrame by requested genres if any are specified
    if requested_genres_list:
        for genre in requested_genres_list:
            if genre != "Find Similar Titles":
                df = df[df['genres'].str.contains(genre, case=False, na=False)].reset_index(drop=True)


    # Create vector from keywords
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['keywords'])

    # Create KNN model
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=3, n_jobs=-1)
    model_knn.fit(X)

    # Fetch and vectorize input
    processed_input = preprocess_text(input_text)
    processed_input = lemmatize_text(processed_input)
    
    input_vector = vectorizer.transform([processed_input])

    # Find nearest neighbors (the best fit and the next three best fits)
    distances, indices = model_knn.kneighbors(input_vector, n_neighbors=3)
    
    best_fit = indices[0][0]
    similar_movie_1 = indices[0][1]
    similar_movie_2 = indices[0][2]

    return best_fit, similar_movie_1, similar_movie_2, df

# Function to find and return movie information given movie IDs
def fetch_movie_info(top_movie, similar_1_id, similar_2_id, df):
    # TOP MOVIE INFO
    top_title = df.iloc[top_movie]["title"]
    top_poster_path = df.iloc[top_movie]["poster_path"]
    top_imdb_id = df.iloc[top_movie]["imdb_id"]
    top_movie_id = df.iloc[top_movie]["id"]

    top_movie_dictionary = {
        "Title": top_title,
        "Poster": f"https://image.tmdb.org/t/p/w1280{top_poster_path}",
        "IMDB": f"https://www.imdb.com/title/{top_imdb_id}",
        "Keywords": df.iloc[top_movie]["keywords"],
    }

    if pd.isna(top_poster_path) or top_poster_path == "":
        top_movie_dictionary["Poster"] = (
            "https://www.malaco.com/wp-content/uploads/2016/06/no-photo-available-black-profile-300x300.jpg"
        )
    if pd.isna(top_imdb_id) or top_imdb_id == "":
        if pd.isna(top_movie_id) or top_movie_id == "":
            top_movie_dictionary["IMDB"] = f"https://www.google.com/search?q={top_title} movie"
        else:
            top_movie_dictionary["IMDB"] = f"https://www.themoviedb.org/movie/{top_movie_id}"

    # SIMILAR MOVIE 1 INFO
    similar_1_title = df.iloc[similar_1_id]["title"]
    similar_1_poster_path = df.iloc[similar_1_id]["poster_path"]
    similar_1_imdb_id = df.iloc[similar_1_id]["imdb_id"]
    similar_1_movie_id = df.iloc[similar_1_id]["id"]

    similar_movie_1_dict = {
        "Title": similar_1_title,
        "Poster": f"https://image.tmdb.org/t/p/w1280{similar_1_poster_path}",
        "IMDB": f"https://www.imdb.com/title/{similar_1_imdb_id}",
        "Keywords": df.iloc[similar_1_id]["keywords"],
    }

    if pd.isna(similar_1_poster_path) or similar_1_poster_path == "":
        similar_movie_1_dict["Poster"] = (
            "https://www.malaco.com/wp-content/uploads/2016/06/no-photo-available-black-profile-300x300.jpg"
        )
    if pd.isna(similar_1_imdb_id) or similar_1_imdb_id == "":
        if pd.isna(similar_1_movie_id) or similar_1_movie_id == "":
            similar_movie_1_dict["IMDB"] = f"https://www.google.com/search?q={similar_1_title} movie"
        else:
            similar_movie_1_dict["IMDB"] = f"https://www.themoviedb.org/movie/{similar_1_movie_id}"

    # SIMILAR MOVIE 2 INFO
    similar_2_title = df.iloc[similar_2_id]["title"]
    similar_2_poster_path = df.iloc[similar_2_id]["poster_path"]
    similar_2_imdb_id = df.iloc[similar_2_id]["imdb_id"]
    similar_2_movie_id = df.iloc[similar_2_id]["id"]

    similar_movie_2_dict = {
        "Title": similar_2_title,
        "Poster": f"https://image.tmdb.org/t/p/w1280{similar_2_poster_path}",
        "IMDB": f"https://www.imdb.com/title/{similar_2_imdb_id}",
        "Keywords": df.iloc[similar_2_id]["keywords"],
    }

    if pd.isna(similar_2_poster_path) or similar_2_poster_path == "":
        similar_movie_2_dict["Poster"] = (
            "https://www.malaco.com/wp-content/uploads/2016/06/no-photo-available-black-profile-300x300.jpg"
        )
    if pd.isna(similar_2_imdb_id) or similar_2_imdb_id == "":
        if pd.isna(similar_2_movie_id) or similar_2_movie_id == "":
            similar_movie_2_dict["IMDB"] = f"https://www.google.com/search?q={similar_2_title} movie"
        else:
            similar_movie_2_dict["IMDB"] = f"https://www.themoviedb.org/movie/{similar_2_movie_id}"

    return top_movie_dictionary, similar_movie_1_dict, similar_movie_2_dict

# Function to find and return random movie information
def random_movies():
    with open(csv_location, newline="", mode="r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        all_rows = list(reader)

        for n in range(2):
            if n == 0:
                row = random.choice(all_rows)

                title = row[0]
                poster_path = row[3]
                imdb_id = row[5]
                movie_id = row[4]

                similar_movie_1_dict = {
                    "Title": title,
                    "Poster": f"https://image.tmdb.org/t/p/w1280{poster_path}",
                    "IMDB": f"https://www.imdb.com/title/{imdb_id}",
                }

                if not poster_path:
                    similar_movie_1_dict[
                        "Poster"
                    ] = "https://www.malaco.com/wp-content/uploads/2016/06/no-photo-available-black-profile-300x300.jpg"
                if not imdb_id:
                    if not movie_id:
                        similar_movie_1_dict["IMDB"] = f"https://www.google.com/search?q={title} movie"
                    else:
                        similar_movie_1_dict["IMDB"] = f"https://www.themoviedb.org/movie/{movie_id}"

            elif n == 1:
                row = random.choice(all_rows)

                title = row[0]
                poster_path = row[3]
                imdb_id = row[5]
                movie_id = row[4]

                similar_movie_2_dict = {
                    "Title": title,
                    "Poster": f"https://image.tmdb.org/t/p/w1280{poster_path}",
                    "IMDB": f"https://www.imdb.com/title/{imdb_id}",
                }

                if not poster_path:
                    similar_movie_2_dict[
                        "Poster"
                    ] = "https://www.malaco.com/wp-content/uploads/2016/06/no-photo-available-black-profile-300x300.jpg"
                if not imdb_id:
                    if not movie_id:
                        similar_movie_2_dict["IMDB"] = f"https://www.google.com/search?q={title} movie"
                    else:
                        similar_movie_2_dict["IMDB"] = f"https://www.themoviedb.org/movie/{movie_id}"

        row = random.choice(all_rows)

        title = row[0]
        poster_path = row[3]
        imdb_id = row[5]
        movie_id = row[4]

        top_movie_dictionary = {
            "Title": title,
            "Poster": f"https://image.tmdb.org/t/p/w1280{poster_path}",
            "IMDB": f"https://www.imdb.com/title/{imdb_id}",
        }

        if not poster_path:
            top_movie_dictionary[
                "Poster"
            ] = "https://www.malaco.com/wp-content/uploads/2016/06/no-photo-available-black-profile-300x300.jpg"
        if not imdb_id:
            if not movie_id:
                top_movie_dictionary["IMDB"] = f"https://www.google.com/search?q={title} movie"
            else:
                top_movie_dictionary["IMDB"] = f"https://www.themoviedb.org/movie/{movie_id}"

    return top_movie_dictionary, similar_movie_1_dict, similar_movie_2_dict

def find_keywords_using_movie(input_text: str):
    df = pd.read_csv(csv_location)
    
    movie = df.loc[df['title'] == input_text]
    keywords = movie['keywords'].to_string(index=False)
    
    return keywords