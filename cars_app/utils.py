from cars_app.models import ExchangeRate


def get_exchange_rate(from_currency, to_currency):
    """
    Получает текущий курс валюты из таблицы ExchangeRate.

    :param from_currency: Исходная валюта (например, EUR)
    :param to_currency: Целевая валюта (например, RUB)
    :return: Текущий курс валюты (buy_rate)
    """
    # Находим актуальный курс
    exchange_rate = ExchangeRate.objects.filter(
        from_currency=from_currency,
        to_currency=to_currency
    ).order_by('-actual_at').first()

    if not exchange_rate:
            raise ValueError(f"Курс обмена для {from_currency} -> {to_currency} не найден!")

    return exchange_rate.buy_rate


def calculate_customs_clearance(price_in_rub):
    """
    Рассчитывает таможенное оформление на основе стоимости автомобиля.

    :param price_in_rub: Стоимость автомобиля в рублях
    :return: Таможенное оформление в рублях
    """
    customs_table = [
        (200000, 775),
        (450000, 1550),
        (1200000, 3100),
        (2700000, 8530),
        (4200000, 12500),
        (5500000, 15500),
        (7000000, 23000),
        (8000000, 25000),
        (10000000, 27000),
        (float('inf'), 30000),
    ]
    for limit, fee in customs_table:
        if price_in_rub <= limit:
            return fee


from decimal import Decimal

def calculate_unified_rate_rub(price_in_rub, engine_volume, exchange_rate):
    """
    Рассчитывает единую ставку для автомобилей младше 3 лет.

    :param price_in_rub: Стоимость автомобиля в рублях (Decimal или float)
    :param engine_volume: Объём двигателя в куб. см (int или float)
    :param exchange_rate: Курс евро к рублю (Decimal или float)
    :return: Единая ставка в рублях (float)
    """
    # Убедимся, что все значения приведены к Decimal для точных расчетов
    price_in_rub = Decimal(price_in_rub)
    engine_volume = Decimal(engine_volume)
    exchange_rate = Decimal(exchange_rate)

    # Перевод стоимости в евро
    price_in_euro = price_in_rub / exchange_rate

    # Таблица категорий: (лимит стоимости в евро, процент, ставка за 1 куб. см в евро)
    unified_rate_table = [
        (8500, 54, 2.5),
        (16700, 48, 3.5),
        (42300, 48, 5.5),
        (84500, 48, 7.5),
        (169000, 48, 15),
        (float('inf'), 48, 20),
    ]

    # Перебираем таблицу ставок
    for limit, percent, rate_per_cc in unified_rate_table:
        if price_in_euro <= limit:
            # Считаем пошлину
            duty_by_percent = price_in_euro * (Decimal(percent) / 100)  # Пошлина по проценту (в евро)
            duty_by_volume = engine_volume * Decimal(rate_per_cc)      # Пошлина по объёму двигателя (в евро)
            duty_in_euro = max(duty_by_percent, duty_by_volume)        # Выбираем максимальную пошлину
            # Переводим пошлину обратно в рубли и округляем до двух знаков
            return float(round(duty_in_euro * exchange_rate, 2))

    # Если ничего не найдено (что маловероятно)
    raise ValueError("Не удалось вычислить пошлину для заданных параметров.")

def calculate_duty_for_old_car(engine_volume, age, euro_to_rub_rate):
    global duty_in_euro
    try:
        # Преобразование engine_volume в число
        engine_volume = int(engine_volume)  # Используйте float(), если объем может быть дробным
    except ValueError:
        raise ValueError("Объем двигателя должен быть числом.")
    """
    Рассчитывает единую ставку для автомобилей старше 3 лет.

    :param engine_volume: Рабочий объём двигателя в куб. см.
    :param age: Возраст автомобиля в годах.
    :param euro_to_rub_rate: Курс евро к рублю (из ExchangeRate).
    :return: Пошлина в рублях.
    """
    # Таблицы ставок для разных возрастных категорий
    duty_table_3_5_years = [
        (1000, 1.5),
        (1500, 1.7),
        (1800, 2.5),
        (2300, 2.7),
        (3000, 3.0),
        (float('inf'), 3.6),
    ]

    duty_table_older_5_years = [
        (1000, 3.0),
        (1500, 3.2),
        (1800, 3.5),
        (2300, 4.8),
        (3000, 5.0),
        (float('inf'), 5.7),
    ]

    # Выбор таблицы ставок в зависимости от возраста
    if 3 <= age <= 5:
        duty_table = duty_table_3_5_years
    elif age > 5:
        duty_table = duty_table_older_5_years
    else:
        raise ValueError("Возраст автомобиля должен быть больше 3 лет для этой функции.")

    # Нахождение соответствующей ставки
    for limit, rate in duty_table:
        if engine_volume <= limit:
            duty_in_euro = engine_volume * rate
            break

    # Перевод пошлины из евро в рубли
    duty_in_rub = float(duty_in_euro) * float(euro_to_rub_rate)
    return round(duty_in_rub, 2)


def calculate_utilization_fee(age):
    """
    Рассчитывает утилизационный сбор на основе возраста автомобиля.

    :param age: Возраст автомобиля в годах
    :return: Утилизационный сбор в рублях
    """
    base_fee = 20000  # Базовый сбор в рублях
    if age < 3:
        multiplier = 0.17
    else:
        multiplier = 0.26
    return round(multiplier * base_fee, 2)
