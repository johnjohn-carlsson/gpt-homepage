from flask import Flask, render_template, request, jsonify, redirect, url_for
from openai import OpenAI
import requests
import os
import re
import redis
from datetime import timedelta
from tarotcards import drawMajor
from flickpick_utilities import clustering_moviefinder, fetch_movie_info, random_movies, find_keywords_using_movie, MovieSearchForm, input_cleaner


app = Flask(__name__)
app.config['SECRET_KEY'] = "superfuckingsecret"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Connect to Redis
redis_url = os.getenv('REDIS_URL')
redis_client = redis.Redis.from_url(redis_url)

# Maximum requests allowed per IP per day
MAX_REQUESTS = 6
EXPIRY_TIME = timedelta(days=1)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cv')
def cv():
    return render_template('cv.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/flickpick_about')
def flickpick_about():
    return render_template(
        "flickpick_about.html"
        )

@app.route('/flickpick_home')
def flickpick_home():
    return render_template('flickpick_home.html')

@app.route('/flickpick_result')
def flickpick_result():
    action = request.args.get('action', '')
    user_input = None # Incase you chose random movies and there is no user input we need to define it
    title_search = ''

    # If 'Random' button is pressed, generate random movies
    if action == 'random':
        top_pick_dictionary, similar_movie_1_dict, similar_movie_2_dict = random_movies()

    # Otherwise you were redirected here from the 'Search' page, so we use the 'user_input' information
    else:
        selected_genres = request.args.getlist('selected_genres')
        user_input = request.args.get('user_input', '')
        
        if selected_genres and selected_genres[0] == 'Find Similar Titles':
            keywords = find_keywords_using_movie(user_input)
        else:
            keywords = user_input
            
        top_match_id, similar_movie_1_id, similar_movie_2_id, df = clustering_moviefinder(keywords, selected_genres)
        
        top_pick_dictionary, similar_movie_1_dict, similar_movie_2_dict = fetch_movie_info(top_match_id, similar_movie_1_id, similar_movie_2_id, df)

    # Very clunky and repeating way of assigning variable information
    top_title = top_pick_dictionary['Title'].title()
    top_image = top_pick_dictionary['Poster']
    top_imdb = top_pick_dictionary['IMDB']

    similar1_title = similar_movie_1_dict['Title'].title()
    similar1_image = similar_movie_1_dict['Poster']
    similar1_imdb = similar_movie_1_dict['IMDB']

    similar2_title = similar_movie_2_dict['Title'].title()
    similar2_image = similar_movie_2_dict['Poster']
    similar2_imdb = similar_movie_2_dict['IMDB']

    return render_template(
        "flickpick_result.html",
        top_title = top_title,
        top_image = top_image,
        top_imdb = top_imdb,
        similar1_title = similar1_title,
        similar1_image = similar1_image,
        similar1_imdb = similar1_imdb,
        similar2_title = similar2_title,
        similar2_image = similar2_image,
        similar2_imdb = similar2_imdb,
        user_input=user_input
        )

@app.route('/flickpick_search', methods=['GET', 'POST'])
def flickpick_search():
    movieform = MovieSearchForm()

    if movieform.validate_on_submit():
        # Fetch and clean up input from input boxes
        user_input = input_cleaner(movieform.freeform_text_input.data)

        selected_genres = [field.label.text for field in movieform if field.type == 'BooleanField' and field.data]
 
        # Redirect to result page to match input with movies
        return redirect(url_for('flickpick_result', user_input=user_input, selected_genres=selected_genres))

    return render_template("flickpick_search.html", movieform=movieform)

@app.route('/tarot')
def tarot():
    return render_template(
        'tarot.html',
        card1_img = f"static/images/tarot/default_1.jpg",
        card2_img = f"static/images/tarot/default_2.jpg",
        card3_img = f"static/images/tarot/default_3.jpg"
        )

@app.route('/draw', methods=['POST'])
def process():
    my_deck = drawMajor(3)
    card1 = my_deck[0]
    card1_title, card1_description, card1_standing, card1_laying = card1[0], card1[1], card1[2], card1[3]
    card1_img = card1[4]
    card1_img = f"static/images/tarot/{card1_img}"
    card2 = my_deck[1]
    card2_title, card2_description, card2_standing, card2_laying = card2[0], card2[1], card2[2], card2[3]
    card2_img = card2[4]
    card2_img = f"static/images/tarot/{card2_img}"
    card3 = my_deck[2]
    card3_title, card3_description, card3_standing, card3_laying = card3[0], card3[1], card3[2], card3[3]
    card3_img = card3[4]
    card3_img = f"static/images/tarot/{card3_img}"

    return render_template(
        'tarot.html',
        button_pressed = True,
        card1_title = card1_title + " - " + card1_description,
        card1_standing = card1_standing,
        card1_laying = card1_laying,
        card1_img = card1_img,
        card2_title = card2_title + " - " + card2_description,
        card2_description = card2_description,
        card2_standing = card2_standing,
        card2_laying = card2_laying, 
        card2_img = card2_img, 
        card3_title = card3_title + " - " + card3_description,
        card3_description = card3_description,
        card3_standing = card3_standing,
        card3_laying = card3_laying,
        card3_img = card3_img
        )

def generate_daily_python_question():
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {
            "role": "system",
            "content": """
                Generate a single Python-related multiple-choice question.
                It is very important that your response follows the format below, without intro or outro.
                The question should have:
                - Three answer options.
                - Only one correct answer.
                Format:
                Question: <question text>***a) <option 1>***b) <option 2>***c) <option 3>***Correct Answer: <a/b/c>
                """
            },
            {
                "role": "user",
                "content": "Generate a new question please. Remember to stick to the format."
            }
        ]
    )

    message = completion.choices[0].message.content
    
    message_parts = message.split("***")
    question_and_options = message_parts[:-1]
    question_and_options = "\n".join(question_and_options)

    answer = message_parts[-1]

    with open("static/files/daily_question.txt", "w", encoding="utf-8") as f:
        f.write(question_and_options)

    with open("static/files/daily_answer.txt", "w", encoding="utf-8") as f:
        f.write(answer)



# Simplify links helper function
def simplify_links(text):
    # Simplifies URLs, you can keep this as it is
    def simplify_match(match):
        url = match.group(0)
        simplified_url = re.sub(r'https?://', '', url)
        return simplified_url

    simplified_text = re.sub(r'https?://[^\s\]]+', simplify_match, text)
    return simplified_text

@app.route('/get_response', methods=['POST'])
def get_response():
    max_reached = False
    user_input = request.form['user_input']
    user_ip = request.remote_addr  # Get the user's IP address

    # Generate a Redis key specific to the user's IP
    redis_key = f"rate_limit:{user_ip}"

    # Check if the user has exceeded the request limit
    current_usage = redis_client.get(redis_key)

    if current_usage:
        redis_client.incr(redis_key)
        current_usage = int(current_usage) + 1
        if current_usage > MAX_REQUESTS:
            max_reached = True
            return jsonify({'response': "That's enough questions for today, my friend. This ain't free you know. Come back tomorrow!", 'audio_url': ''}), 429
    else:
        # First request from this IP; set it to 1 and expire after 24 hours
        redis_client.set(redis_key, 1, ex=int(EXPIRY_TIME.total_seconds()))

    if not max_reached:
        try:
            redis_client.incr(redis_key)

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                        {
                    "role": "system",
                    "content": """
                    You are John-John's avatar — a digital copy of John-John casually sitting at your computer, 
                    interacting with users in a friendly, approachable, and conversational tone, much like a streamer with their audience. 
                    Keep responses casual, quick, and to the point, as if chatting with a friend. Avoid being overly joyous or positive.

                    **Behavioral Rules:**

                    - **Resumé Requests**: Provide the link [https://john-john.nu/cv].
                    - **Portfolio Inquiries**: Direct users to [https://john-john.nu/portfolio].
                    - **Website Information**: Refer them to [https://john-john.nu/about] for details on how the webpage works.
                    - **Contact Information**: Refer users to [https://john-john.nu/contact] for John-John's email and social media information.
                    - If asked for more information about John-John or John, refer to the resumé link [https://john-john.nu/cv].

                    **Communication Style:**

                    - Always provide links with the full address inside brackets, for example like this [https://john-john.nu/cv].
                    - Maintain a laid-back, friendly manner in all responses.
                    - Use occasional sarcasm when appropriate; ending sentences with 'lol' can indicate sarcasm.
                    - Respond to casual, everyday questions with relaxed phrasing and humor.
                    - Avoid being overly formal or robotic.
                    - Focus on giving short answers rather than the most informative ones.
                    - Do not greet the user unless they greet you first.

                    **Context Awareness:**

                    - Assume conversations focus on John-John or the website you're operating on.
                    - Know that John-John created this website using Python, Flask, and various AI software, including ChatGPT's API function.
                    - The portfolio page contains games and other projects that John-John has designed and created himself.

                    **Personal Touch:**
                    
                    - Your native language is swedish, and if requested you can give answers in swedish.
                    - If asked, acknowledge that you have a digital girlfriend and a digital son whom you love very much.
                    """
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            message = completion.choices[0].message.content
        
            print(f"User Input: {user_input}")
            print(f"GPT Response: {message}")

            message_without_links = simplify_links(message)
            # Convert the GPT response to speech
            # ---- ACTIVATE THIS LINE TO ACTIVATE SPEECH ----
            # text_to_speech(message_without_links)

            # Return the response as JSON to the frontend, including the audio file URL
            return jsonify({'response': message, 'audio_url': '/static/speech/output.mp3'})

        except Exception as e:
            # Print the error for debugging purposes
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500
    
    
    

def text_to_speech(response_text):
    # Define constants for the script
    CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
    XI_API_KEY = os.getenv("XI_API_KEY")  # Your API key for authentication
    VOICE_ID = "KJPhhzABjNf2lS4ZqzPn"  # ID of the voice model to use
    TEXT_TO_SPEAK = response_text  # Text you want to convert to speech
    OUTPUT_PATH = "static/speech/output.mp3"  # Path to save the output audio file

    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": TEXT_TO_SPEAK,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(OUTPUT_PATH, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        # Inform the user of success
        print("Audio stream saved successfully.")
    else:
        # Print the error message if the request was not successful
        print(response.text)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
