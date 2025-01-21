from django.db import models

class Review(models.Model):
    user_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    review_date = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user_name} - {self.rating} stars on {self.review_date}"

class CompanyRating(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.company_name} - Rating: {self.rating}"
