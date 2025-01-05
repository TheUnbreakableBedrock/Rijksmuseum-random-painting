from fastapi import FastAPI
from dotenv import load_dotenv

import requests
import csv
import random
import os
import json
import datetime

# Load secret .env file
load_dotenv()

# load api key from .env file
API_KEY = os.getenv("MY_API_KEY")

# start api application
app = FastAPI()

def validateJSON(jsonData):
    if jsonData["artObject"]["webImage"] != None:
        return True
    else:
        return False

def get_posts(id):
    # Define the API endpoint URL
    url = f'https://www.rijksmuseum.nl/api/nl/collection/{id}?key={API_KEY}'

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

# function to get a random id from a collection csv
def get_random_id():
    # set filename variable for easy filename change
    filename = '202001-rma-csv-collection-cleaned.csv'

    # open file and count lines
    with open(filename) as f:
        lines = sum(1 for line in f)
        line_number = random.randrange(lines)

    # read line at random line number
    with open(filename) as f:
        reader = csv.reader(f)
        chosen_row = next(row for row_number, row in enumerate(reader)
                          if row_number == line_number)

    return chosen_row[0]

# combine functions to supply api response for chosen id
def get_random_post():
    id = get_random_id()
    print(id)
    return get_posts(id)

# expose endpoint for data
@app.get("/random-painting")
async def read_root():
    while True:
        response = get_random_post()
        if validateJSON(response):
            return response