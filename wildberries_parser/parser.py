from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki")
    time.sleep(5)  # Ждем загрузки
    
    products = driver.find_elements(By.CSS_SELECTOR, "article.product-card__wrapper")
    print(f"Найдено товаров: {len(products)}")
    
    for product in products[:3]:  # Первые 3 товара
        name = product.find_element(By.CSS_SELECTOR, "a.product-card__link").get_attribute("aria-label")
        price = product.find_element(By.CSS_SELECTOR, "span.price__lower-price").text
        print(f"{name[:50]}... | Цена: {price}")
        
finally:
    driver.quit()