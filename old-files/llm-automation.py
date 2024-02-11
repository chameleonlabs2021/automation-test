from selenium import webdriver
from selenium.webdriver.common.by import By
import openai

def get_css_selector(description):
    # Use OpenAI's API to interpret the description and generate a CSS selector
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",  # Replace with the latest available model
        prompt=f"Translate this description into a CSS selector: '{description}'",
        max_tokens=60
    )
    return response.choices[0].text.strip()

def main():
    # Your OpenAI API key
    openai.api_key = "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"

    # URL to visit
    url = 'https://www.facebook.com/'

    # Description of the element to interact with
    description = "the first blue button on the page"

    # Initialize the browser
    driver = webdriver.Chrome()  # Ensure you have chromedriver installed
    driver.get(url)

    try:
        # Get CSS selector from the LLM
        css_selector = get_css_selector(description)

        # Find the element and interact with it
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        element.click()
        print(f"Clicked on element with CSS selector: {css_selector}")


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up
        driver.quit()

if __name__ == "__main__":
    main()
