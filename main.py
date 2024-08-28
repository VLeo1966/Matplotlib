from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Шаг 1: Парсинг цен с сайта

# Инициализация веб-драйвера
driver = webdriver.Firefox()

# URL страницы с объявлениями
url = 'https://www.cian.ru/snyat-kvartiru-1-komn-ili-2-komn/'

# Открытие страницы
driver.get(url)

# Ждем некоторое время, чтобы страница полностью загрузилась
time.sleep(5)

# Парсинг цен
prices = driver.find_elements(By.XPATH, "//span[@data-mark='MainPrice']/span")

# Открытие CSV файла для записи цен
with open('prices.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Price'])  # Записываем заголовок столбца

    # Записываем цены в CSV файл
    for price in prices:
        writer.writerow([price.text])

# Закрытие драйвера
driver.quit()

# Шаг 2: Очистка данных и преобразование цен в числовой формат

def clean_price(price):
    # Удаляем "₽/мес." и пробелы, преобразуем в число
    return int(price.replace(' ₽/мес.', '').replace(' ', ''))

# Чтение данных из исходного CSV файла и их обработка
input_file = 'prices.csv'
output_file = 'cleaned_prices.csv'

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
plt.title('Гистограмма цен на квартиры')
plt.xlabel('Цена (₽)')
plt.ylabel('Частота')

# Показ гистограммы
plt.show()

