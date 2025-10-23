from rest_framework import serializers
from apps.cars.models import Car, Rental


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'year', 'price_per_day']



class CarRentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ["start_date", "days", "payment_method"]

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'




