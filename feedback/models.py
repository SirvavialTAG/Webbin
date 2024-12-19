from django.db import models



class Feedback(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя")
    phone_number = models.CharField(max_length=16, verbose_name="Телефон")
    content = models.TextField(max_length=200, verbose_name="Сообщение")
    privacy_policy_agreed = models.BooleanField(default=False, verbose_name="Согласие с политикой конфиденциальности")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"{self.name} ({self.phone_number})"
