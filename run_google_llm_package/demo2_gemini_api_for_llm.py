import requests

# https://ai.google.dev/api/all-methods

API_KEY=''
MODEL_NAME = 'gemini-3-flash-preview'

payload={
"contents":[
    {
        "parts":[{"text":"The capital of France is"}]
    }
],
"generationConfig":{
    "temperature":0.7
}
}

response=requests.post(
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}",
    headers={"Content-Type": "application/json"},
    json=payload
    )

response.raise_for_status()

response_json = response.json()
# generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
# print(generated_text)

print(response_json)