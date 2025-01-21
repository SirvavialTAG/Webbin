from django.core.management.base import BaseCommand
from playwright.sync_api import sync_playwright

class Command(BaseCommand):
    help = 'Парсит отзывы'

    def handle(self, *args, **kwargs):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Переход на страницу
            page.goto("https://2gis.ru/vladivostok/firm/70000001067259118/tab/reviews?m=131.843447%2C43.293872%2F12.57")

            # Извлекаем заголовок "Отзывы"
            reviews_header = page.locator("h1").text_content()
            self.stdout.write(f"Заголовок: {reviews_header}")

            # Извлекаем рейтинг компании
            rating_value = page.locator("div._13nm4f0").text_content()
            self.stdout.write(f"Рейтинг компании: {rating_value}")

            # Извлекаем отзывы
            reviews = page.locator("div._1k5soqfl")
            review_count = reviews.count()
            self.stdout.write(f"Найдено {review_count} отзывов")

            for i in range(review_count):
                # Извлекаем имя пользователя
                user_name = reviews.nth(i).locator("span._16s5yj36").get_attribute("title")

                # Извлекаем дату отзыва
                review_date = reviews.nth(i).locator("div._139ll30").text_content()

                # Извлекаем звездную оценку (количество звезд)
                stars_count = len(reviews.nth(i).locator("svg[fill='#ffb81c']").all())

                self.stdout.write(f"Имя пользователя: {user_name}")
                self.stdout.write(f"Дата отзыва: {review_date}")
                self.stdout.write(f"Оценка: {stars_count} звезд")

            # Закрытие браузера
            context.close()
            browser.close()
