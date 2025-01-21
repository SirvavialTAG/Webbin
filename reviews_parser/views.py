from django.shortcuts import render
from .models import Review, CompanyRating

def review_slider(request):
    company_rating = CompanyRating.objects.first()  # Получаем текущий рейтинг компании
    reviews = Review.objects.all()  # Получаем все отзывы
    return render(request, 'parsers/review_slider.html', {'reviews': reviews, 'company_rating': company_rating})
