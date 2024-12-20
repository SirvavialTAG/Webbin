import sqlite3
from datetime import datetime


current_year = datetime.now().year


def get_car_data():
    # Подключение к базе данных
    conn = sqlite3.connect("cars.sqlite3")  # Открытие соединения с базой данных SQLite
    cursor = conn.cursor()

    # Получение данных об автомобилях из таблицы
    cursor.execute("SELECT id, model, year, price, engine_volume FROM cars")
    car_data = cursor.fetchall()  # Извлечение всех строк результата запроса

    conn.close()  # Закрытие соединения с базой данных
    return car_data  # Возврат списка данных об автомобилях

# Функция загрузки курсов валют
def load_exchange_rates(file_path):
    """
    Загружает курсы валют из текстового файла и возвращает словарь.
    """
    exchange_rates = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        currency = None
        for line in lines:
            line = line.strip()
            if line.startswith("Из "):  # Определение валюты
                parts = line.split()
                currency = parts[1]  # Например, USD, EUR
            elif line.startswith("Курс покупки:"):
                buy_rate = float(line.split(":")[1].strip())
            elif line.startswith("Курс продажи:"):
                sell_rate = float(line.split(":")[1].strip())
                # После определения курса продажи добавляем данные
                if currency:
                    exchange_rates[currency] = {'buy': buy_rate, 'sell': sell_rate}
    return exchange_rates

# Таблицы расчёта таможенных сборов

def get_customs_duty_rub(price):
    """
    Расчет таможенной пошлины в рублях по таблице 1
    """
    if price <= 200000:
        return 775  # Пошлина для автомобилей до 200,000 руб.
    elif price <= 450000:
        return 1550
    elif price <= 1200000:
        return 3100
    elif price <= 2700000:
        return 8530
    elif price <= 4200000:
        return 12000
    elif price <= 5500000:
        return 15500
    elif price <= 7000000:
        return 20000
    elif price <= 8000000:
        return 23000
    elif price <= 9000000:
        return 25000
    elif price <= 10000000:
        return 27000
    else:
        return 30000  # Пошлина для автомобилей дороже 10,000,000 руб.

# Для автомобилей моложе 3-х лет
def get_customs_duty_euro(price_euro):
    """
    Расчет таможенной пошлины в евро по таблице 2
    """
    if price_euro <= 8500:
        return max(0.54 * price_euro, 2.5 * 1)  # Минимум между % от цены и фиксированной ставкой
    elif price_euro <= 16700:
        return max(0.48 * price_euro, 3.5 * 1)
    elif price_euro <= 42300:
        return max(0.48 * price_euro, 5.5 * 1)
    elif price_euro <= 84500:
        return max(0.48 * price_euro, 7.5 * 1)
    elif price_euro <= 169000:
        return max(0.48 * price_euro, 15 * 1)
    else:
        return max(0.48 * price_euro, 20 * 1)  # Для автомобилей дороже 169,000 евро

# Утилизационный сбор
def calculate_utilization_fee(age):
    """
    Расчет утилизационного сбора
    """
    multiplier = 0.17 if age <= 3 else 0.26  # Коэффициент зависит от возраста автомобиля
    return multiplier * 20000  # Утилизационный сбор рассчитывается как произведение коэффициента на базовую ставку


# Загружаем курсы валют
exchange_rates = load_exchange_rates('exchange_rates.txt')

# Основной расчет
car_data = get_car_data()  # Получаем данные об автомобилях

for car in car_data:
    car_id, model, year, price, engine_volume = car  # Распаковка данных об автомобиле

    # Вычисляем возраст автомобиля
    age = current_year - year  # Текущий год минус год выпуска автомобиля

    # Таможенные сборы в рублях
    customs_rub = get_customs_duty_rub(price)  # Расчет таможенной пошлины в рублях

    # Перевод цены в евро и расчет для автомобилей младше 3-х лет
    price_euro = price / exchange_rates['EUR']['sell']  # Конвертация цены из рублей в евро
    customs_euro = get_customs_duty_euro(price_euro) if age <= 3 else 0  # Пошлина в евро только для молодых автомобилей

    # Утилизационный сбор
    utilization_fee = calculate_utilization_fee(age)  # Расчет утилизационного сбора

    # Вывод данных по текущему автомобилю
    print(f"Авто {model}, Год выпуска: {year}, Цена: {price} руб., Объем двигателя: {engine_volume} куб.см")
    print(f"Таможенная пошлина (рубли): {customs_rub}")
    if age <= 3:
        print(f"Таможенная пошлина (евро): {customs_euro:.2f}")
    print(f"Утилизационный сбор: {utilization_fee:.2f} руб.")
    print("-")  # Разделитель для вывода
