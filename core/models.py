from django.db import models

class Brands(models.Model):
    country = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'brands'


class Cars(models.Model):
    model = models.CharField(max_length=250)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.IntegerField()
    transmission = models.CharField(max_length=20)
    engine_volume = models.CharField(max_length=250)
    drive = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    power_volume = models.CharField(max_length=250)
    brand_country = models.ForeignKey(Brands, models.DO_NOTHING, blank=True, null=True)
    exchange_rate = models.ForeignKey(ExchangeRates, models.DO_NOTHING, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'cars'



