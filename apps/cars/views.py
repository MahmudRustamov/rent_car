from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.cars.models import Car, Rental
from apps.cars.pagination import CustomPageNumberPagination
from apps.cars.serializers import CarSerializer, CarRentCreateSerializer, RentalSerializer, CarRetrieveSerializer, \
    RentalListSerializer, ReturnCarSerializer


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


class CarRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CarRetrieveSerializer
    queryset = Car.objects.all()

    def get(self, *args, **kwargs):
        car_id = self.kwargs.get('car_id')
        try:
            car = Car.objects.get(pk=car_id)
        except Car.DoesNotExist:
            return Response(data={'message': 'Car is not available'}, status=400)

        if not car.is_available:
            return Response({"message": "This car is not available"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RentalListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    serializer_class = RentalListSerializer
    queryset = Rental.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = user.rentals.all().order_by('-created_at')
        status_param = self.request.query_params.get('status')
        ordering = self.request.query_params.get('ordering')

        if status_param:
            if status_param.lower() == 'active':
                queryset = queryset.filter(is_returned=False)
            elif status_param.lower() == 'completed':
                queryset = queryset.filter(is_returned=True)

        if ordering in ['start_date', '-start_date']:
            queryset = queryset.order_by(ordering)

        return queryset


class RentalCancelAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReturnCarSerializer

    def post(self, request, rental_id):
        try:
            rental = request.user.rentals.get(pk=rental_id)
        except Rental.DoesNotExist:
            return Response(data={'errors': 'Rental not found'}, status=400)

        if rental.status in ['completed', 'cancelled']:
            return Response(data={'errors': 'You can not cancel this rental because it is already cancelled or completed'}, status=status.HTTP_400_BAD_REQUEST)

        rental.status = 'cancelled'
        rental.save()

        rental.car.is_available = True
        rental.save()
        serializer = self.get_serializer(rental)

        return Response(data={"message": "Rental cancelled","rental": serializer.data},status=status.HTTP_200_OK)
