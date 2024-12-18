from venv import create

import requests
import json
import time
from datetime import datetime


# Функция для получения данных с API
def fetch_exchange_rates():
    # URL GraphQL-эндпоинта
    url = "https://bbr.ru/graphql/"

    # Заголовки (скопированы из браузера)
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    # Тело запроса (Variables и Query)
    payload = {
        "query": """
        query RatesList($rateType: RateTypeEnum, $citySlug: String, $range: InputRateRange, $officeId: Int) {
          rates(
            noPagination: true
            rateType: $rateType
            citySlug: $citySlug
            officeId: $officeId
            range: $range
          ) {
            actualAt
            elements {
              id
              rateType
              fromCurrency {
                code
              }
              toCurrency {
                code
              }
              buyRate
              sellRate
            }
          }
        }
        """,
        "variables": {
            "rateType": "CASH_EXCHANGE",
            "citySlug": "vladivostok",
            "officeId": 7,
            "range": {"start": 0, "end": 10000}
        }
    }

    # Отправка запроса
    response = requests.post(url, json=payload, headers=headers)

    # Проверка результата
    if response.status_code == 200:
        data = response.json()
        return data["data"]["rates"]["elements"]
    else:
        print("Ошибка запроса:", response.status_code, response.text)
        return []


# Функция для записи данных в файл
def save_rates_to_file(rates):
    with open("../exchange_rates.txt", "w", encoding="utf-8") as file:
        file.write(f"Курсы валют на {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for rate in rates:
            file.write(f"Из {rate['fromCurrency']['code']} в {rate['toCurrency']['code']}:\n")
            file.write(f"  Курс покупки: {rate['buyRate']}\n")
            file.write(f"  Курс продажи: {rate['sellRate']}\n\n")


# Основная функция
def main():
    while True:
        # Получаем курсы валют
        rates = fetch_exchange_rates()

        if rates:
            # Записываем курсы в файл
            save_rates_to_file(rates)
            print("Курсы обновлены и сохранены в файл.")
        else:
            print("Не удалось получить курсы.")
        return

if __name__ == "__main__":
    main()
