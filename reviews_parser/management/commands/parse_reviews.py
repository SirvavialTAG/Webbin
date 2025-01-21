from django.core.management.base import BaseCommand
from playwright.sync_api import sync_playwright
from asgiref.sync import sync_to_async
from reviews_parser.models import Review, CompanyRating

class Command(BaseCommand):
    help = 'Парсит отзывы и сохраняет их в базе данных'

    @sync_to_async
    def save_company_rating(self, rating_value):
        """ Сохраняем рейтинг компании в базе данных """
        company_name = 'Tomiko Trade'
        CompanyRating.objects.update_or_create(
            company_name=company_name,
            defaults={'rating': rating_value}
        )

    @sync_to_async
    def save_review(self, user_name, stars_count, review_date):
        """ Сохраняем отзыв в базе данных """
        Review.objects.update_or_create(
            user_name=user_name,
            rating=stars_count,
            review_date=review_date
        )

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

            # Сохраняем рейтинг компании в БД
            self.save_company_rating(rating_value)

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

                # Сохраняем отзыв в базе данных
                self.save_review(user_name, stars_count, review_date)

                self.stdout.write(f"Имя пользователя: {user_name}")
                self.stdout.write(f"Дата отзыва: {review_date}")
                self.stdout.write(f"Оценка: {stars_count} звезд")

            # Закрытие браузера
            context.close()

            browser.close()
