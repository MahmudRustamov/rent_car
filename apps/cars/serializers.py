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

class CarRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        exclude = ['created_at']



class RentalListSerializer(serializers.ModelSerializer):
    cars = CarSerializer(read_only=True)

    class Meta:
        model = Rental
        fields = ['id', 'cars', 'start_date', 'end_date', 'total_price', 'is_returned', 'created_at']


class ReturnCarSerializer(serializers.ModelSerializer):
    cars = CarSerializer(read_only=True)

    class Meta:
        model = Rental
        fields = ['id', 'cars', 'start_date', 'end_date', 'total_price', 'status', 'is_returned']
        read_only_fields = ['id', 'cars', 'start_date', 'end_date', 'total_price', 'is_returned']


