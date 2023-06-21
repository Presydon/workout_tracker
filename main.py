import requests
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

APP_ID = os.getenv('APP_ID')
API_KEY = os.getenv('API_KEY')
USER_ID = os.getenv('USER_ID')
bearer_api = os.getenv('bearer_api')

nutrition_endpoint = 'https://trackapi.nutritionix.com/v2'

header = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

query = input("Tell me which exercise you did: ")
exercise_endpoint = f'{nutrition_endpoint}/natural/exercise'
exercise_config = {
    'query': query,
    'gender': 'male',
    'weight_kg': 70,
    'height_cm': 185,
    'age': 27,
}

response = requests.post(url=exercise_endpoint, headers=header, json=exercise_config)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheety_endpoint = 'https://api.sheety.co/4b59f028be4d1b6a58744b3fa96ac943/copyOfMyWorkouts/workouts'

bearer_header = {
    'Authorization': f'Bearer {bearer_api}'
}

for exercise in result['exercises']:
    sheet_inputs = {
        'workout': {
            'date': today_date,
            'time': now_time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories'],
        }
    }

    sheet_response = requests.post(url=sheety_endpoint, json=sheet_inputs, headers=bearer_header)
    print(sheet_response.status_code)
    print(sheet_response.text)


