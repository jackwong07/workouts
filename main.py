
import requests
from datetime import datetime
import os
#updates this google sheet: https://docs.google.com/spreadsheets/d/1N6tz8NlNDcBLYncJVP6o2qa1qNvrbRlcw4eyC-j7-R8/edit#gid=0
#uses Sheety API to update google sheet, Bearer Auth in Sheety settings: https://sheety.co/docs/authentication.html
#

# #set as environment variables
# APP_ID = os.environ["APP_ID"]
# API_KEY = os.environ["API_KEY"]
# BEARER_TOKEN=os.environ["BEARER"]



#----------Exercise input
exercise_input=input("What exercise did you do today?")

exercise_headers={
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_parameters={
    "query":exercise_input,
    "weight_kg": 58,
    "height_cm": 170.18,
    "age": 32,
}

exercise_endpoint="https://trackapi.nutritionix.com/v2/natural/exercise"

try:
    response = requests.post(url=exercise_endpoint, json=exercise_parameters, headers=exercise_headers)
    response.raise_for_status()
    result=response.json()
    print(result)
    exercise=result["exercises"][0]["name"]
    duration=result["exercises"][0]["duration_min"]
    calories_burned=result["exercises"][0]["nf_calories"]
except IndexError:
    exercise=""
    duration=""
    calories_burned=""




#-------------Nutrition input
nutrition_input = input("What did you eat today?")
#servings_input = input("How many servings?")
nutrition_parameters={
    "query":nutrition_input,
    #"num_servings": servings_input,
    "line_delimited":False,
}

nutrition_endpoint="https://trackapi.nutritionix.com/v2/natural/nutrients"

nut_response = requests.post(url=nutrition_endpoint, json=nutrition_parameters, headers=exercise_headers)
nut_response.raise_for_status()
nut_result=nut_response.json()


nut_name=nut_result["foods"][0]["food_name"]
nut_calories=nut_result["foods"][0]["nf_calories"]
nut_total_fat=nut_result["foods"][0]["nf_total_fat"]
nut_protein=nut_result["foods"][0]["nf_protein"]


#-----------------Update Sheety/Google Sheet
#in sheety, add in google sheet as project
sheety_url = "https://api.sheety.co/f6fd46d3dca29e9e937126f01649aac9/myWorkouts/workouts"
today = datetime.today().strftime("%d/%m/%Y")

sheety_headers={f"Authorization": "Bearer {BEARER_TOKEN}"}

#sheet name is workouts, so here, it is workout
data={
    "workout":{
        "date": today,
        "exercise": exercise,
        "duration": duration,
        "caloriesBurned": calories_burned,
        "foodName": nut_name,
        "caloriesEaten": nut_calories,
        "totalFatGrams": nut_total_fat,
        "proteinGrams": nut_protein,
    }
}

response = requests.post(url=sheety_url, json=data, headers=sheety_headers)
print(response.status_code)
print(response.text)
