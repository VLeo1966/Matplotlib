from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Импортируем модуль CSV
import csv

# Если используем Google Chrome, то пишем driver = webdriver.Chrome()
driver = webdriver.Firefox()

# URL страницы
url = 'https://www.divan.ru/category/divany-i-kresla'

# Открытие страницы
driver.get(url)

# Использование WebDriverWait для ожидания появления элемента на странице
wait = WebDriverWait(driver, 10)
prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='ui-LD-ZU KIkOH' and @data-testid='price']")))

# Открытие CSV файла для записи
with open('prices.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])  # Записываем заголовок столбца

    # Записываем цены в CSV файл
    for price in prices:
        writer.writerow([price.text])

# Закрытие драйвера
driver.quit()
