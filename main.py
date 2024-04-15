
import requests
from datetime import datetime
import os
#updates this google sheet: https://docs.google.com/spreadsheets/d/1N6tz8NlNDcBLYncJVP6o2qa1qNvrbRlcw4eyC-j7-R8/edit#gid=0
#uses Sheety API to update google sheet, Bearer Auth in Sheety settings: https://sheety.co/docs/authentication.html
#

# #set as environment variables
# APP_ID = "69c7957c"
# API_KEY = "d4364cc6b4c426a4f5ff4bc566896a4b"
# BEARER_TOKEN="Oina2^fAOisA03Kn*6a"


exercise_input=input("What exercise did you do today?")

headers={
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters={
    "query":exercise_input,
    "weight_kg": 58,
    "height_cm": 170.18,
    "age": 32,
}

exercise_endpoint="https://trackapi.nutritionix.com/v2/natural/exercise"

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
response.raise_for_status()
result=response.json()
print(result)

exercise=result["exercises"][0]["name"]
duration=result["exercises"][0]["duration_min"]
calories=result["exercises"][0]["nf_calories"]

#in sheety, add in google sheet as project
sheety_url = "https://api.sheety.co/f6fd46d3dca29e9e937126f01649aac9/myWorkouts/workouts"
today = datetime.today().strftime("%d/%m/%Y")

headers={f"Authorization": "Bearer {BEARER_TOKEN}"}

#sheet name is workouts, so here, it is workout
data={
    "workout":{
        "date": today,
        "exercise": exercise,
        "duration": duration,
        "calories": calories,
    }
}

response = requests.post(url=sheety_url, json=data, headers=headers)
print(response.status_code)
print(response.text)