from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

# Specify the path to ChromeDriver
service = Service('/Users/ivanmanfredi/Downloads/chromedriver-mac-arm64/chromedriver')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service)

# Function to read URLs from a file
def read_product_urls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]
def determine_product_cat(url):
    # Simplified logic for determining product type based on URL
    if 'arlistan' in url or 'cafe-instantaneo' in url:
        return "Café Instantáneo"
    elif 'te' in url:
        return "Te en Saquitos"
    elif 'cacao-en-polvo' in url:
        return "Cacao en Polvo"
    elif 'yerba' in url:
        return "Yerba Mate"
    else:
        return "Unknown Product Type"
# Adjust this path to where you save your file
product_urls_file = 'product_urls.txt'
product_urls = read_product_urls(product_urls_file)


# Prepare a list to hold product data
products_data = []

for url in product_urls:
    product_cat = determine_product_cat(url)
    driver.get(url)
    time.sleep(5)  # Adjust sleep time based on page load times
    
    product_name = driver.find_element(By.XPATH, '//h1[contains(@class, "productNameContainer")]').text
    # Check for "c/u" in the price text to decide which XPath to use
    price_element = driver.find_element(By.XPATH, '//*[contains(@class, "product-price-0-x-sellingPriceValue")]')
    if "c/u" in price_element.text:
        # If "c/u" is present, use an alternate XPath for the regular price
        product_price_element = driver.find_element(By.XPATH, '//*[@class="valtech-carrefourar-product-price-0-x-listPrice"]') 
        product_price = product_price_element.text
    else:
        product_price = price_element.text
    
    # Assuming price per kg is always desired and correctly located
    product_price_per_kg = driver.find_element(By.XPATH, '//*[contains(@class, "dynamic-weight-price-0-x-currencyContainer")]').text
    
    products_data.append([product_name, product_price, product_price_per_kg, product_cat])

# Write to CSV outside the loop
csv_file = 'products_prices.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'Price per KG', 'Product Category'])  # Write header
    writer.writerows(products_data)

print(f'Data saved to {csv_file}')

# Clean up by closing the driver after all operations
driver.quit()
