import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


NAUKRI_USERNAME = os.getenv("NAUKRI_USERNAME")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")


def main():
    if not NAUKRI_USERNAME or not NAUKRI_PASSWORD:
        print("NAUKRI_USERNAME and NAUKRI_PASSWORD must be set")
        return

    print(f"Logging in to Naukri with username: {NAUKRI_USERNAME}")
    print(f"Logging in to Naukri with password: {NAUKRI_PASSWORD}")

    # Login to Naukri
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-gpu-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    print("Opening Naukri login page")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Navigating to Naukri login page")
        driver.get("https://www.naukri.com/nlogin/login")

        wait = WebDriverWait(driver, 20)

        print("Entering username")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        username_field.send_keys(NAUKRI_USERNAME)
        
        print("Entering password")
        password_field = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
        password_field.send_keys(NAUKRI_PASSWORD)


        print("Clicking login button")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        print("Waiting for login to complete...")
        time.sleep(10)

        print("Navigating to profile summary page...")
        driver.get("https://www.naukri.com/mnjuser/profile")

        time.sleep(10)

        print("Locating the resume upload input...")
        resume_upload_input = wait.until(EC.presence_of_element_located((By.ID, "attachCV")))

        resume_path = os.path.abspath("resume.pdf")
        if not os.path.exists(resume_path):
            print(f"Error: Resume file not found at {resume_path}")
            return
            
        print(f"Uploading resume from {resume_path}...")

        resume_upload_input.send_keys(resume_path)

        print("Waiting for upload confirmation...")
        time.sleep(10)

        print("Profile updated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error.png")

    finally:
        print("Closing browser")
        driver.quit()


if __name__ == "__main__":
    main()
