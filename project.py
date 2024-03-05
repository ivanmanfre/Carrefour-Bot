from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

# Specify the path to ChromeDriver
service = Service('/Users/ivanmanfredi/Downloads/chromedriver-mac-arm64/chromedriver')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service)

def determine_product_cat(url):
    # Example logic to determine product type based on URL
    if 'arlistan' in url:
        return "Cafe Instantaneo"
    elif 'cafe-instantaneo' in url:
        return "Cafe Instantaneo"
    else:
        return "Unknown Product Type"
# List of product URLs
product_urls = [
    'https://www.carrefour.com.ar/infusion-a-base-de-cafe-arlistan-en-frasco-100-g-727996/p',
    'https://www.carrefour.com.ar/cafe-instantaneo-dolca-suave-origenes-en-frasco-100-g-729425/p',
    'https://www.carrefour.com.ar/cafe-instantaneo-la-virginia-especial-clasico-170-g/p'
]

# Prepare a list to hold product data
products_data = []

for url in product_urls:
    # Determine the product type based on the URL
    product_cat = determine_product_cat(url)

    # Navigate to the product page
    driver.get(url)
    time.sleep(5)
    
    # Extract the product name and price

    product_name = driver.find_element(By.XPATH, '//h1[@class="vtex-store-components-3-x-productNameContainer vtex-store-components-3-x-productNameContainer--quickview mv0 t-heading-4"]').text
    product_price = driver.find_element(By.XPATH, '//*[@class="valtech-carrefourar-product-price-0-x-sellingPriceValue"]').text
    
    print(f'Product: {product_name}, Price: {product_price}, Category:{product_cat} ')

    # Append product data to the list
    products_data.append([product_name, product_price, product_cat])


    # Specify the CSV file name
    csv_file = 'products_prices.csv'

    # Write product data to a CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Price', 'Product Cat'])  # Writing header
        writer.writerows(products_data)

    print(f'Data saved to {csv_file}')
