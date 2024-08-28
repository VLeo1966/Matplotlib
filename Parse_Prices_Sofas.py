from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Инициализация веб-драйвера (замените путь на путь к вашему драйверу)
driver = webdriver.Firefox()

# URL страницы с диванами
url = 'https://www.divan.ru/category/divany-i-kresla'
# Открытие страницы
driver.get(url)
# Ждем некоторое время, чтобы страница полностью загрузилась
wait = WebDriverWait(driver, 3)

# Открытие CSV файла для записи
with open('divan_prices.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])  # Записываем заголовок столбца

    # Парсинг данных с двух страниц
    for _ in range(2):
        # Прокручиваем страницу вниз до конца
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Использование WebDriverWait для ожидания появления цен на странице
        wait = WebDriverWait(driver, 3)
        prices = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//span[@class='ui-LD-ZU KIkOH' and @data-testid='price']")
        ))

        # Записываем цены в CSV файл
        for price in prices:
            writer.writerow([price.text])

# Закрытие драйвера
driver.quit()

print("Цены успешно сохранены в файл 'divan_prices.csv'")

# Шаг 2: Очистка данных и преобразование цен в числовой формат

def clean_price(price):
    # Удаляем "руб." и пробелы, преобразуем в число
    return int(price.replace('руб.', '').replace(' ', ''))

# Чтение данных из исходного CSV файла и их обработка
input_file = 'divan_prices.csv'
output_file = 'cleaned_divan_prices.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Читаем заголовок и записываем его в новый файл
    header = next(reader)
    writer.writerow(header)

    # Обрабатываем и записываем данные строк
    for row in reader:
        clean_row = [clean_price(row[0])]
        writer.writerow(clean_row)

print(f"Обработанные данные сохранены в файл {output_file}")

# Шаг 3: Построение гистограммы на основе очищенных данных

# Загрузка данных из CSV-файла
data = pd.read_csv(output_file)

# Получаем столбец с ценами
prices = data['Price']

# Построение гистограммы
plt.hist(prices, bins=10, edgecolor='black')

# Добавление заголовка и меток осей
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (₽)')
plt.ylabel('Частота')

# Показ гистограммы
plt.show()