import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/scrape")
def scrape():
    email = "bostrommalin474@gmail.com"
    password = "Bajsbajs123"

    # Initialize the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the login page
        driver.get("https://www.merinfo.se/user/login")

        # Accept Cookies (if there's a cookie banner)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "qc-cmp2-consent-info"))
            )

            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-47sehv')]//span[text()='GODKÄNN']"))
            )

            consent_button.click()
            time.sleep(2)
            driver.refresh()
        except Exception as e:
            print("Error accepting cookies or no cookie banner found:", e)
        
        # Wait for the login page elements
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @inputmode='email']"))
        )

        # Find the email and password fields and log in
        email_input = driver.find_element(By.XPATH, "//input[@type='text' and @inputmode='email']")
        password_input = driver.find_element(By.XPATH, "//input[@id='current-password']")
        email_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        # Wait for login to complete
        WebDriverWait(driver, 20).until(
            EC.url_changes("https://www.merinfo.se/user/login")
        )

        # Navigate to the desired URL after login
        driver.get("https://www.merinfo.se/search?q=19861228-0050")

        # Wait for the link containing the name to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://www.merinfo.se/person')]"))
        )

        # Find the anchor tag and extract the name
        name_element = driver.find_element(By.XPATH, "//a[contains(@href, 'https://www.merinfo.se/person/Vendels%C3%B6/Richard-Mikael-Haglind-1986/btp0s-40k2y')]")
        name_text = name_element.text

        return jsonify({"name": name_text})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

