Description of table columns

Product_Name: H1 of Product

Price: List price (no discounts). This column is just referencial and has no influence whatsoever in calculations.

Price_Per_KG: Column used for calculations and it is sensitive to discounts and promotions EXCEPTION WITH 3X2

Product_Category : Type of Product
Scrape_date
Inflation_rate: Price variation in price_per_kg between present and previous Scrape_Date
Category_Inflation_Rate: Average between scrape_date inflation_rate for each category
Monthly_Inflation_Rate: Sum of every day Category_Inflation_Day

