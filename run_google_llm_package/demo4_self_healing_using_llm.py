from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from google import genai


URL = "https://opensource-demo.orangehrmlive.com/"
LOGIN_BUTTON_XPATH = "//button[normalize-space()='Submit']"


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




driver = webdriver.Chrome()
driver.maximize_window()
driver.get(URL)

try:
    login_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))
    )
except:
    LOGIN_BUTTON_XPATH= get_healed_locator(LOGIN_BUTTON_XPATH,driver.page_source)

    login_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))
    )
    
login_button.click()
