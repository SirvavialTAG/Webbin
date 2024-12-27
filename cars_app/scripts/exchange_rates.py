import requests
from datetime import datetime
from cars_app.models import ExchangeRate

def fetch_exchange_rates():
    url = "https://bbr.ru/graphql/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
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
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        rates = data["data"]["rates"]["elements"]
        for rate in rates:
            ExchangeRate.objects.update_or_create(
                from_currency=rate['fromCurrency']['code'],
                to_currency=rate['toCurrency']['code'],
                defaults={
                    "buy_rate": rate['buyRate'],
                    "sell_rate": rate['sellRate'],
                    "actual_at": datetime.now()
                }
            )
        print("Курсы валют обновлены.")
    else:
        print("Ошибка запроса:", response.status_code, response.text)
