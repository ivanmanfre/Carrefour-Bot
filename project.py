from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Specify the path to ChromeDriver
service = Service('/Users/ivanmanfredi/Downloads/chromedriver-mac-arm64/chromedriver')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service)

# Now you can use the driver to open pages, interact with web elements, etc.
driver.get('https://www.carrefour.com.ar/')


# Wait for the page to load
time.sleep(5)  # Adjust the sleep time based on your internet speed and page load time

# Now, find the elements containing the products' data
# Replace 'product-class', 'product-name', and 'product-price' with the correct selectors
products = driver.find_elements(By.CLASS_NAME, 'product-class')

for product in products:
    # Extract and print product details
    name = product.find_element(By.CLASS_NAME, 'product-name').text
    price = product.find_element(By.CLASS_NAME, 'product-price').text
    print(f'Name: {name}, Price: {price}')

