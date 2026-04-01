from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def type_slowly(element, text, delay=0.15):
    for character in text:
        element.send_keys(character)
        time.sleep(delay)

print("Starting the Google Search & Login Automation...")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    # --- STEP 1: GO TO GOOGLE ---
    driver.get("https://www.google.com")
    print("Opened Google.")
    
    # Find the search box (Google's search box usually has name='q')
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    
    print("Searching for the organization portal...")
    type_slowly(search_box, "Secure Organization Login local")
    search_box.send_keys(Keys.ENTER)
    
    # --- STEP 2: NAVIGATE TO YOUR ACTUAL LOCAL APP ---
    # In a real scenario, you'd click a link. 
    # Since localhost isn't on Google, we simulate the 'Click' by navigating to our URL.
    print("Simulating clicking the search result...")
    time.sleep(2) 
    driver.get("http://localhost:5000")
    
    # --- STEP 3: LOGIN PROCESS (Your existing code) ---
    print("Navigated to the login page.")
    
    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    type_slowly(username_input, "admin@example.com")
    
    password_input = driver.find_element(By.ID, "password")
    type_slowly(password_input, "SecurePass123")
    
    # Solve CAPTCHA
    captcha_text = driver.find_element(By.ID, "captcha-display").text
    print(f"Bot read CAPTCHA: {captcha_text}")
    type_slowly(driver.find_element(By.ID, "captcha_input"), captcha_text)
    
    driver.find_element(By.ID, "login-btn").click()
    
    # --- STEP 4: OTP VERIFICATION ---
    otp_input = wait.until(EC.presence_of_element_located((By.ID, "otp")))
    
    with open("otp_inbox.txt", "r") as file:
        retrieved_otp = file.read().strip()
    
    print(f"Retrieved OTP: {retrieved_otp}")
    type_slowly(otp_input, retrieved_otp)
    
    driver.find_element(By.ID, "login-btn").click()
    print("Login Successful!")
    time.sleep(5)

finally:
    driver.quit()
