from django.db import models

class ExchangeRate(models.Model):
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=4)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=4)
    actual_at = models.DateTimeField()

    def __str__(self):
        return f"{self.from_currency}/{self.to_currency} - {self.buy_rate}"

