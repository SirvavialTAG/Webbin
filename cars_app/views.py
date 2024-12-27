import os
from django.http import JsonResponse
from .scripts.exchange_rates import fetch_exchange_rates
from core.models import Cars
from django.shortcuts import render
from datetime import datetime
from .utils import (
    get_exchange_rate,
    calculate_customs_clearance,
    calculate_unified_rate_rub,
    calculate_duty_for_old_car,
    calculate_utilization_fee
)



def update_exchange_rates(request):
    fetch_exchange_rates()
    return JsonResponse({"status": "Курсы валют обновлены."}) # При переходе /cars/exchange_rates/ - обновляет курсы валют





def calculate_duty(request):
    cars = Cars.objects.all()  # Получаем данные из таблицы Cars
    exchange_rate = get_exchange_rate("EUR", "RUB")  # Получаем актуальный курс евро к рублю
    current_year = datetime.now().year  # Получаем текущий год
    results = []

    for car in cars:
        try:
            # Расчёт возраста автомобиля
            age = current_year - car.year

            # Расчёт таможенного оформления
            customs_clearance = calculate_customs_clearance(car.price)

            # Расчёт единой ставки
            if age < 3:
                unified_rate = calculate_unified_rate_rub(car.price, car.engine_volume, exchange_rate)
            else:
                unified_rate = calculate_duty_for_old_car(car.engine_volume, age, exchange_rate)

            # Расчёт утилизационного сбора
            utilization_fee = calculate_utilization_fee(age)

            # Общая пошлина
            total_duty = customs_clearance + unified_rate + utilization_fee

            results.append({
                'model': car.model,
                'price': car.price,
                'engine_volume': car.engine_volume,
                'age': age,
                'customs_clearance': customs_clearance,
                'unified_rate': unified_rate,
                'utilization_fee': utilization_fee,
                'total_duty': total_duty,
            })
        except ValueError as e:
            # Если курс не найден или возраст некорректен, добавляем ошибку
            results.append({
                'model': car.model,
                'error': str(e)
            })

    return render(request, 'customs_duties.html', {'results': results})
