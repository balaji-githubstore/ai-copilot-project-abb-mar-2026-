from google import genai

def get_healed_locator(old_locator,html):
    client = genai.Client(api_key='')

    system_prompt="""
        you are a qa automation expert. 

        Rules: 
        - always return valid json
        - do not include extra text or demiliters 
        - output must strictly follow this format: 
            {"new_locator":"<xpath>"}
        - xpath must be unique
    """

    user_prompt=f"""
        A selenium test failed 
        Old xpath: {old_locator}

        html: {html}

        suggest better xpath
    """

    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        {
            "role": "system",
            "parts": [{"text": system_prompt}]
        },
        {
            "role": "user",
            "parts": [{"text": user_prompt}]
        }
    ],
    config={'temperature':0.2}
    )

    # verify output must be json
    import json
    response=json.loads(response.text)
    return response["new_locator"]
