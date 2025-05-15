import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

class QuizFlowTest(unittest.TestCase):
    def setUp(self):
        # Start browser and test setup
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:5000"
        self.wait = WebDriverWait(self.driver, 10)

        # Generate unique test user
        timestamp = int(time.time())
        self.test_username = f"user{timestamp}"
        self.test_email = f"{self.test_username}@example.com"
        self.test_password = "password123"

    def test_complete_quiz_flow(self):
        driver = self.driver
        wait = self.wait

        # === SIGNUP ===
        driver.get(f"{self.base_url}/signup")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.test_username)
        driver.find_element(By.ID, "email").send_keys(self.test_email)
        driver.find_element(By.ID, "password").send_keys(self.test_password)
        driver.find_element(By.ID, "confirm_password").send_keys(self.test_password)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()


        # Wait until redirected to login
        wait.until(EC.url_contains("/login"))

        # === LOGIN ===
        driver.get(f"{self.base_url}/login")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.test_username)
        driver.find_element(By.ID, "password").send_keys(self.test_password)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # === QUIZ SECTION 1: Choose 3 clusters ===
        driver.get(f"{self.base_url}/quiz")

        heading = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".quiz-heading")))
        self.assertIn("CareerCompass", heading.text)

        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quiz-card")))
        for card in cards[:3]:
            driver.execute_script("arguments[0].click();", card)
            time.sleep(0.2)

        selected = driver.find_elements(By.CSS_SELECTOR, ".quiz-card.selected")
        assert len(selected) == 3, f"Expected 3 cards selected, got {len(selected)}"

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(0.5)
        next_button.click()

        # === QUIZ SECTION 2: Interest sliders ===
        sliders = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='range']")))
        for slider in sliders:
            driver.execute_script("arguments[0].scrollIntoView(true);", slider)
            time.sleep(0.2)
            slider.send_keys(Keys.ARROW_RIGHT * 5)

        btn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Continue to Stage 3']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", btn2)
        time.sleep(0.5)
        btn2.click()

        # === QUIZ SECTION 3: Enjoyment sliders ===
        sliders = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='range']")))
        for slider in sliders:
            driver.execute_script("arguments[0].scrollIntoView(true);", slider)
            time.sleep(0.2)
            slider.send_keys(Keys.ARROW_RIGHT * 5)

        btn3 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Continue to Stage 4']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", btn3)
        time.sleep(0.5)
        btn3.click()

        # === QUIZ SECTION 4: Demographic sliders ===
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='range']")))
        slider_count = len(driver.find_elements(By.CSS_SELECTOR, "input[type='range']"))

        for i in range(slider_count):
            sliders = driver.find_elements(By.CSS_SELECTOR, "input[type='range']")
            slider = sliders[i]
            driver.execute_script("arguments[0].scrollIntoView(true);", slider)
            time.sleep(0.2)
            slider.send_keys(Keys.ARROW_RIGHT * 5)

        btn4 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='See My Top Careers']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", btn4)
        time.sleep(0.5)
        btn4.click()

        # === RESULTS ===
        try:
            wait.until(EC.url_contains("/results"))
            result_header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            self.assertIn("Your Top 5 Career Matches", result_header.text)
        except TimeoutException:
            self.fail("Did not reach /results page after completing quiz.")


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
