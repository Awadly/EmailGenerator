from linkedin_scraper import actions
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def extract_name(driver):
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge')
        return name_element.text.strip()
    except Exception as e:
        print(f"Name element not found. Error: {e}")
        return None
def extract_bio(driver):
    try:
        bio_element = driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium')
        return bio_element.text.strip()
    except Exception as e:
        print(f"Bio element not found. Error: {e}")
        return None

def extract_about(driver):
    try:
        # Locate the about element
        about_element = driver.find_element(By.CSS_SELECTOR, 'div.inline-show-more-text--is-collapsed.inline-show-more-text--is-collapsed-with-line-clamp.full-width')
        
        if about_element:
            # Find the nested span element
            about_text_element = about_element.find_element(By.CSS_SELECTOR, 'span[aria-hidden="true"]')
            if about_text_element:
                return about_text_element.text.strip()
            else:
                print("About text not found.")
                return None
        else:
            print("About element not found.")
            return None
    except Exception as e:
        print(f"Error occurred while extracting About element. Error: {e}")
        return None

def scrape_linkedin_profile(profile_url, email, password):
    driver = webdriver.Chrome()

    # Log into LinkedIn
    actions.login(driver, email, password, timeout=30)
    print("Logged in successfully")

    # Navigate to the LinkedIn profile URL
    driver.get(profile_url)
    time.sleep(2)

    # Extract details
    name = extract_name(driver)
    bio = extract_bio(driver)
    about = extract_about(driver)

    # Close the driver
    driver.quit()

    return name, bio, about