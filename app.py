import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get_gifs')
def get_gifs():

    #get searched query from the frontend. if no query, it will use cat as a default query
    search_query = request.args.get('search_query')
    
    #tenor api key from .env
    api_key = os.environ.get('api_key')
    
    #number of gif data per page from .env
    limit = os.environ.get('limit')
    
    #tenor app name from .env
    ckey =  os.environ.get('ckey')
    
    #using try/except to avoid breaking code, if endpoint throws api limit error.
    try:
        #tenor api endpoint to search gif
        endpoint = f"https://tenor.googleapis.com/v2/search?q={search_query}&key={api_key}&client_key={ckey}&limit={limit}"
        
        #used requests library for get post http request
        fetch = requests.get(endpoint)

        # Extract preview GIFs from the response
        preview_gifs = [{'id': each.get('id'), 'title': each.get('title'), 'gif': each.get('media_formats').get('gif').get('url')} for each in fetch.json().get('results')]
        
        # Return JSON response
        return jsonify({'preview_gifs': preview_gifs})
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/', methods=['GET', 'POST'])
def get_data():
    #checking if method is post or not
    if request.method == 'POST':
        selected_gif_url = request.form.get('selected_gif_url') #you can store this gif url in db and use it wherever you want. 
        return jsonify({'GIF': selected_gif_url})
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(os.environ.get('debug'))
