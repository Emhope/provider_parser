# RPA Parser

Проект для автоматического парсинга тарифов с сайта `rialcom.ru` с использованием Selenium + Pandas.

## Требования

- python3.10
- драйвер Chrome, работающий с selenium

## Установка

### 1. Установите Poetry (если ещё не установлен)

```bash
pip install poetry
```

### 2. Клонируйте репозиторий и установите зависимости

```bash
git clone https://github.com/USERNAME/provider_parser.git
cd provider_parser
poetry install
```

## Настройка Selenium

Проект разработан для работы с  **Google Chrome** . Перед запуском убедитесь, что Selenium корректно взаимодействует с браузером и следующий код выполняется без ошибок:

```python
from selenium import webdriver
driver = webdriver.Chrome()
```

## Запуск парсера

```bash
poetry run python provider_parser/main.py
```

## Результаты

После проделанных команд к корне проекта появится файл 'data.xlsx' с извлеченной информацией из сайта
