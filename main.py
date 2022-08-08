import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv('.env')

SHEETY_BEARER_TOKEN = os.environ['sheety_bearer_token']
SHEETY_ENDPOINT = os.environ['sheety_endpoint']
NUTRITIONIX_APP_ID = os.environ['nutritionix_app_id']
NUTRITIONIX_APP_KEY = os.environ['nutritionix_app_key']
GENDER = os.environ['GENDER']
WEIGHT_KG = os.environ['WEIGHT_KG']
HEIGHT_CM = os.environ['HEIGHT_CM']
AGE = os.environ['AGE']


# Adds authentication to the Sheety endpoint to secure it
sheety_headers = {"Authorization": SHEETY_BEARER_TOKEN}

# API key and app id from Nutritionix API website
headers = {
    'x-app-id': NUTRITIONIX_APP_ID,
    'x-app-key': NUTRITIONIX_APP_KEY
}

app_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = SHEETY_ENDPOINT

text = input('Tell me which exercises you did: ')
# e.g ran 2km cycled 3hours

parameters = {
    "query": text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Mkes a request with the required parameters
response = requests.post(url=app_endpoint, json=parameters, headers=headers)
answer = response.json()['exercises']

# Gets the current date and time
date = datetime.datetime.now()
time_now = date.time()

# Formats the answer into columns
for i in answer:
    sheety_params = {
        'workout': {
            'date': date.strftime('%Y%m%d'),
            'time': time_now.strftime('%X'),
            'exercise': i['name'].title(),
            'duration': i['duration_min'],
            'calories': i['nf_calories']
        }
    }

    # Generates a new row of data in your Google sheet for each of the exercises gotten from the Nutritionix API
    update = requests.post(url=sheety_endpoint, json=sheety_params, headers=sheety_headers)
    print(update.text)

