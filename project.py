from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
from datetime import datetime, timedelta
import os
import psycopg2
import re

# Database connection parameters
dbname = 'portfolio'
user = 'postgres'
password = 'mamama00'
host = 'localhost'
port= '5433'
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
    elif 'te-en-saquitos' in url:
        return "Te en Saquitos"
    elif 'cacao-en-polvo' in url:
        return "Cacao en Polvo"
    elif 'yerba' in url:
        return "Yerba Mate"
    elif 'vino-tinto' in url:
        return "Vino Tinto"
    elif 'cerveza' in url:
        return "Cerveza"
    elif '-con-gas-' in url or 'soda' in url:
        return "Agua con Gas"
    elif 'jugo-' in url:
        return "Jugo Concentrado"
    elif '-cola-' in url:
        return "Gaseosa"
    elif 'caldo-' in url:
        return "Caldo Concentrado"
    elif 'vinagre-' in url:
        return "Vinagre"
    elif 'mayonesa-' in url:
        return "Mayonesa"
    elif 'sal-fina' in url:
        return "Sal Fina"
    elif 'mermelada' in url:
        return "Mermelada"
    elif 'dulce-de-batata' in url:
        return "Dulce de Batata"
    elif 'azucar-' in url:
        return "Azucar"
    elif 'lentejas-' in url:
        return "Lentejas"
    elif 'arvejas-' in url:
        return "Arvejas"
    elif '/tomate-perita-' in url:
        return "Tomate Enlatado"
    elif '/pan-' in url:
        return "Pan Lactal"
    elif 'galletitas-chocolinas' in url or 'galletitas-dulces' in url or 'galletitas-toddy' in url or 'galletitas-chocolate' in url:
        return "Galletita Dulces"
    elif '/galletitas-cerealitas' in url or '/galletitas-crackers-la-providencia' in url or 'galletitas-crackers-traviata'in url:
        return "Galletita de Agua"
    elif 'harina-de-trigo' in url:
        return "Harina de Trigo"
    elif 'arroz-' in url:
        return "Arroz"
    elif '/fideos-' in url:
        return "Pastas"
    elif '/asado-' in url:
        return "Asado"
    elif '/carnaza-' in url:
        return "Carnaza"
    elif '/carre-' in url:
        return "Carre de Cerdo"
    elif '/paleta-el' in url:
        return "Paleta Vaca"
    elif '/carne-picada-' in url:
        return "Carne Picada"
    elif '/milanesa-de-nalga-' in url:
        return "Nalga"
    ##Falta Higado
    elif '/pechito-de-cerdo-' in url:
        return "Pechito de Cerdo"
    elif '/pollo-entero-congelado-' in url:
        return "Pollo"
    elif '/filet-de-merluza-' in url:
        return "Filet de Merluza"
    elif '/mortadela-' in url:
        return "Mortadela"
    elif '/paleta-cocida' in url:
        return "Paleta Cocida"
    elif '/salchichon-' in url:
        return "Salchichon"
    elif '/salame-' in url:
        return "Salame"
    elif '/aceite-de-girasol-' in url:
        return "Aceite de Girasol"
    elif '/margarina-en-pan-' in url:
        return "Margarina"
    elif '/leche-ultra-entera-' in url or '/leche-multivitaminas-' in url:
        return "Leche Entera"
    elif '/leche-en-polvo-' in url:
        return "Leche en Polvo"
    elif '/queso-crema-' in url or '/queso-fundido-' in url:
        return "Queso untable"
    elif '/queso-cuartirolo-' in url:
        return "Queso Cuartirolo"
    elif '/queso-en-hebras-' in url or '/queso-rallado-' in url:
        return "Queso Rallado"
    elif '/manteca-' in url:
        return "Manteca"
    elif '/yogur-bebible-' in url:
        return "Yogur Bebible"
    elif '/dulce-de-leche-' in url:
        return "Dulce de Leche"
    elif '/huevo-' in url or '/huevos-blancos-' in url:
        return "Huevo"
    elif '/manzana-red-' in url:
        return "Manzana Roja"
    elif '/pera-' in url:
        return "Pera"
    elif '/batata-x-kg' in url:
        return "Batata"
    elif '/acelga-' in url:
        return "Acelga"
    elif '/cebolla-x-kg' in url:
        return "Cebolla"
    elif '/choclo-en-granos' in url:
        return "Choclo en Granos"
    elif '/lechuga-' in url:
        return "Lechuga"
    elif '/tomate-x-kg' in url:
        return "Tomate"
    elif '/zapallo-' in url:
        return "Zapallo"
    
    

    else:
        return "Unknown Product Type"
# Price format conversion function
def convert_price_format(price_str):
    # Remove the currency symbol and any spaces
    price_str = price_str.replace("$", "").strip()
    
    # Remove thousand separators (dots) and replace decimal comma with a dot
    price_str = price_str.replace(".", "").replace(",", ".")
    
    # Convert to float
    return float(price_str)
def update_category_inflation_rate(conn, scrape_date):
    cur = conn.cursor()
    
    # Calculate the daily category inflation rate
    calculate_inflation_query = """
    WITH daily_inflation AS (
        SELECT
            product_category,
            AVG(inflation_rate) AS avg_inflation_rate
        FROM
            product_prices
        WHERE
            scrape_date = %s AND inflation_rate IS NOT NULL
        GROUP BY
            product_category
    )
    UPDATE product_prices p
    SET category_inflation_rate = d.avg_inflation_rate
    FROM daily_inflation d
    WHERE p.product_category = d.product_category AND p.scrape_date = %s;
    """
    
    cur.execute(calculate_inflation_query, (scrape_date, scrape_date))
    conn.commit()

def update_partial_monthly_category_inflation_rate(conn, year, month):
    cur = conn.cursor()
    
    # Adjusted query to calculate the partial monthly category inflation rate
    calculate_partial_monthly_inflation_query = """
    WITH daily_category_rates AS (
        SELECT
            product_category,
            scrape_date,
            AVG(category_inflation_rate) AS daily_avg_inflation_rate
        FROM
            product_prices
        WHERE
            EXTRACT(YEAR FROM scrape_date) = %s AND
            EXTRACT(MONTH FROM scrape_date) = %s
        GROUP BY
            product_category, scrape_date
    ),
    monthly_inflation AS (
        SELECT
            product_category,
            SUM(daily_avg_inflation_rate) AS sum_monthly_inflation_rate
        FROM
            daily_category_rates
        GROUP BY
            product_category
    )
    UPDATE product_prices p
    SET monthly_category_inflation_rate = m.sum_monthly_inflation_rate
    FROM monthly_inflation m
    WHERE p.product_category = m.product_category AND
          EXTRACT(YEAR FROM p.scrape_date) = %s AND
          EXTRACT(MONTH FROM p.scrape_date) = %s;
    """
    
    cur.execute(calculate_partial_monthly_inflation_query, (year, month, year, month))
    conn.commit()


def insert_into_db(product_data):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    
    # SQL query to find the previous price_per_kg
    prev_price_query = """
    SELECT price_per_kg FROM product_prices
    WHERE product_name = %s AND scrape_date < %s
    ORDER BY scrape_date DESC
    LIMIT 1;
    """
    
    # Updated insert query to include the inflation rate
    insert_query = """
    INSERT INTO product_prices (product_name, price, price_per_kg, product_category, scrape_date, inflation_rate)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (product_name, scrape_date) DO NOTHING;
    """
    
    for data in product_data:
        product_name, product_price, product_price_per_kg, product_cat, scrape_date = data
        
        # Convert price and price_per_kg to float
        product_price = convert_price_format(product_price)
        product_price_per_kg = convert_price_format(product_price_per_kg)
        
        # Retrieve the previous day's price_per_kg for the product
        cur.execute(prev_price_query, (product_name, scrape_date))
        result = cur.fetchone()
        prev_price_per_kg = result[0] if result else None
        
        # Calculate the inflation rate if the previous price is available
        inflation_rate = None
        if prev_price_per_kg is not None:
            inflation_rate = ((product_price_per_kg - prev_price_per_kg) / prev_price_per_kg) * 100
        
        # Insert the data along with the calculated inflation rate
        cur.execute(insert_query, (product_name, product_price, product_price_per_kg, product_cat, scrape_date, inflation_rate))
    
    conn.commit()

    # After inserting, calculate and update the category inflation rates
    update_category_inflation_rate(conn, scrape_date)
    # Also, update the partial monthly category inflation rate
    current_year = datetime.now().year
    current_month = datetime.now().month
    update_partial_monthly_category_inflation_rate(conn, current_year, current_month)

    cur.close()
    conn.close()

# Adjust this path to where you save your file
product_urls_file = 'product_urls.txt'
product_urls = read_product_urls(product_urls_file)

# Current date 
scrape_date = datetime.now().strftime('%Y-%m-%d')

# Prepare a list to hold product data
products_data = []

for url in product_urls:
  try:
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
    elif "%" in price_element.text:
        product_price_element = driver.find_element(By.XPATH, '//*[@class="valtech-carrefourar-product-price-0-x-listPrice"]') 
        product_price = product_price_element.text
    else:
        product_price = price_element.text
    
    # Assuming price per kg is always desired and correctly located
    product_price_per_kg = driver.find_element(By.XPATH, '//*[contains(@class, "dynamic-weight-price-0-x-currencyContainer")]').text
    
    products_data.append([product_name, product_price, product_price_per_kg, product_cat, scrape_date])
  except (NoSuchElementException, TimeoutException) as e:
        print(f"Error processing URL {url}: {e}")
        continue  # Skip this URL and move to the next one
    

# Insert data into the database
insert_into_db(products_data)

# Clean up by closing the driver after all operations
driver.quit()
