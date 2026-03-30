"""
pip install google-genai

"""
from google import genai

client = genai.Client(api_key='')

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        {
            "role": "system",
            "parts": [{"text": "You are json generator. Give only json output "}]
        },
        {
            "role": "user",
            "parts": [{"text": "Generate json data for 5 people with different names, ages, and cities."}]
        }
    ],
    config={'temperature':0}
)
print(response.text)

import json

result=json.loads(response.text)
print(result)
print(result[0]['name'])




