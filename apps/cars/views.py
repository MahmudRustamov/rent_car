from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.cars.models import Car, Rental
from apps.cars.pagination import CustomPageNumberPagination
from apps.cars.serializers import CarSerializer, CarRentCreateSerializer, RentalSerializer


class CarListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CarSerializer
    pagination_class = CustomPageNumberPagination
    queryset = Car.objects.all()

    def get_queryset(self):
        cars = Car.objects.all()
        brand = self.request.query_params.get('brand')
        ordering = self.request.query_params.get('ordering')
        is_available = self.request.query_params.get('is_available')

        if brand:
            cars = cars.filter(brand__icontains=brand)
        if ordering and ordering in ['price_per_day', '-price_per_day' ]:
            cars = cars.order_by(ordering)
        if is_available and ordering in ['price_per_day', '-price_per_day' ]:
            cars = cars.filter(is_available=bool(is_available))

        return cars


class CarRentCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarRentCreateSerializer
    queryset = Rental.objects.all()


    def post(self, request, *args, **kwargs):
        car_id = self.kwargs.get('car_id')
        user = self.request.user

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
             return Response(data={'message': 'Car not found'}, status=404)

        if not car.is_available:
            return Response(data={'message': 'Car is not available'}, status=400)

        if user.rentals.filter(is_returned=False):
            return Response(data={'message': 'You have already rented a car'}, status=400)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        total_price = serializer.validated_data['days'] * car.price_per_day
        print(serializer.validated_data)
        rental = Rental.objects.create(
            user = user,
            car = car,
            total_price = total_price,
            **serializer.validated_data
        )

        response_serializer = RentalSerializer(rental)
        return Response(data=response_serializer.data, status=201)





