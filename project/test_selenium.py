import unittest
<<<<<<< HEAD
import time
=======
>>>>>>> main
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
<<<<<<< HEAD
from selenium.common.exceptions import TimeoutException
=======
>>>>>>> main
from webdriver_manager.chrome import ChromeDriverManager

class QuizFlowTest(unittest.TestCase):
    def setUp(self):
<<<<<<< HEAD
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:5000"
        self.wait = WebDriverWait(self.driver, 10)

        self.test_username = f"user{int(time.time())}"
        self.test_password = "password123"
        self.test_email = f"{self.test_username}@example.com"

    def test_signup_login_quiz_flow(self):
        driver = self.driver
        wait = self.wait

        # === SIGNUP ===
        driver.get(f"{self.base_url}/signup")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.test_username)
        driver.find_element(By.ID, "email").send_keys(self.test_email)
        driver.find_element(By.ID, "password").send_keys(self.test_password)
        driver.find_element(By.ID, "confirm_password").send_keys(self.test_password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait.until(EC.url_contains("/login"))

        # === LOGIN ===
        driver.get(f"{self.base_url}/login")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.test_username)
        driver.find_element(By.ID, "password").send_keys(self.test_password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # === QUIZ START ===
        driver.get(f"{self.base_url}/quiz")
        heading = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".quiz-heading")))
        self.assertIn("CareerCompass", heading.text)

        # === SECTION 1: SELECT CLUSTERS ===
        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quiz-card")))
        for card in cards[:3]:
            card.click()
        driver.find_element(By.CSS_SELECTOR, "button.button[type='submit']").click()

        # === SECTION 2: SLIDERS (quiz2) ===
        sliders = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='range']")))
        for slider in sliders:
            slider.send_keys(Keys.ARROW_RIGHT * 5)
        driver.find_element(By.CSS_SELECTOR, "button.button[type='submit']").click()

        # === SECTION 3: SLIDERS (quiz3) ===
        sliders = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='range']")))
        for slider in sliders:
            slider.send_keys(Keys.ARROW_RIGHT * 5)
        driver.find_element(By.CSS_SELECTOR, "button.button[type='submit']").click()

        # === SECTION 4: SLIDERS (quiz4) ===
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='range']")))
            
            slider_count = len(driver.find_elements(By.CSS_SELECTOR, "input[type='range']"))
            
            for i in range(slider_count):
                slider = driver.find_elements(By.CSS_SELECTOR, "input[type='range']")[i]
                driver.execute_script("arguments[0].scrollIntoView(true);", slider)
                time.sleep(0.2)  
                slider.send_keys(Keys.ARROW_RIGHT * 5)

            submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            submit_btn.click()

            wait.until(EC.url_contains("/results"))
            result_header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            self.assertIn("Your Top 5 Career Matches", result_header.text)
        except TimeoutException:
            self.fail("Failed to reach /results from quiz4.")

=======
        # installs/chromedriver automatically for you
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        # point this at wherever your Flask app is running
        self.base_url = "http://127.0.0.1:5000"

    def test_complete_quiz_flow(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # 1) LOGIN
        driver.get(f"{self.base_url}/login")
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("your_username")
        driver.find_element(By.NAME, "password").send_keys("your_password")
        driver.find_element(By.XPATH, "//button[.='Login']").click()

        # 2) NAVIGATE TO QUIZ
        driver.get(f"{self.base_url}/quiz")
        # verify we landed on the quiz page
        heading = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".quiz-heading")))
        self.assertIn("CareerCompass", heading.text)

        # 3) SECTION 2: Select exactly 3 statements
        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quiz-card")))
        # click the first three
        for card in cards[:3]:
            card.click()

        # click Next
        driver.find_element(By.CSS_SELECTOR, "button.button[type='submit']").click()

        # 4) SECTION 3 & 4: sliders (if you have 2 sliders)
        sliders = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='range']")))
        for slider in sliders:
            # move each slider a bit to the right
            slider.send_keys(Keys.ARROW_RIGHT * 5)

        # click Next
        driver.find_element(By.CSS_SELECTOR, "button.button[type='submit']").click()

        # 5) FINAL ASSERT: ensure we see results page
        # e.g. check URL or a results header
        self.assertTrue(driver.current_url.endswith("/results"))
        result_header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.assertIn("Your Results", result_header.text or "Results")
>>>>>>> main

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
