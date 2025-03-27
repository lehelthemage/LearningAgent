from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import logging

logger = logging.getLogger(__name__)

class WebAutomation:
    def __init__(self):
        self.driver = uc.Chrome()

    def load_page(self, url):
        self.driver.get(url)
        print(f"🌍 Loaded page: {url}")

    def input_text(self, selector, value):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.send_keys(value)
        print(f"⌨️ Input text '{value}' into {selector}")

    def click(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.click()
        print(f"🖱️ Clicked {selector}")

    def submit_form(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.submit()
        print(f"📨 Submitted form {selector}")

    def read_elements(self, selector):
        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        texts = [el.text for el in elements]
        print(f"📖 Read elements: {texts}")
        return texts

def execute_task(task):
    """Executes a given task."""
    logger.info(f"Executing task: {task['description']}")
    for step in task["steps"]:
        action = step["action"]
        parameters = step["parameters"]
        logger.debug(f"Performing action: {action} with parameters: {parameters}")
        # Add logic to call primitive web I/O functions here
    logger.info(f"Task execution completed: {task['description']}")
