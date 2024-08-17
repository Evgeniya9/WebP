import requests
from bs4 import BeautifulSoup
import json

# URL страницы с вакансиями
url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

# Ключевые слова для поиска
keywords = ["Django", "Flask"]

# Список для хранения информации о вакансиях
vacancies = []

# Запрос на страницу
response = requests.get(url)
response.raise_for_status()

# Парсинг HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Поиск блоков вакансий
vacancy_blocks = soup.find_all('div', class_='vacancy-serp-item')

for block in vacancy_blocks:
    # Получение ссылки на вакансию
    link = block.find('a', class_='serp-item__title')['href']

    # Получение вилки зп
    salary_block = block.find('span', class_='vacancy-serp-item__compensation')
    if salary_block:
        salary = salary_block.text.strip()
        if 'USD' in salary:  # Проверка на наличие валюты USD
            # Обработка вилки зп (может быть нужно добавить логику для обработки различных форматов)
            # Например: "от 100 000 до 200 000 USD"
            # salary = salary.replace('USD', '').replace(' ', '')
            # salary = salary.split('до')
            # salary = [int(s.replace(',', '')) for s in salary]
            pass
        else:
            continue  # Переход к следующей вакансии, если валюта не USD
    else:
        salary = None

    # Получение названия компании
    company = block.find('a', class_='serp-item__company').text.strip()

    # Получение города
    city = block.find('span', class_='serp-item__location').text.strip()

    # Получение описания вакансии
    description = block.find('div', class_='g-user-content').text.strip()

    # Проверка на наличие ключевых слов
    found_keywords = False
    for keyword in keywords:
        if keyword in description:
            found_keywords = True
            break

    # Добавление вакансии в список, если найдены ключевые слова
    if found_keywords:
        vacancies.append({
            'link': link,
            'salary': salary,
            'company': company,
            'city': city
        })

# Сохранение информации в JSON файл
with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, indent=4, ensure_ascii=False)
