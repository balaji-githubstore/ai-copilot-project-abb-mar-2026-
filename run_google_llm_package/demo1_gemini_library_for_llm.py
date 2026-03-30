"""
pip install google-genai

"""
from google import genai

client = genai.Client(api_key='')

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="""
what is the captial of france""",
    config={'temperature':0}
)

print(response.text)


