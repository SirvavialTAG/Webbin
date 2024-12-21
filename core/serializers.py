from rest_framework import serializers
from .models import Cars, Brands

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Cars
        fields = "__all__"