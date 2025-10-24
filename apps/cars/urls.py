from django.urls import path
from apps.cars.views import CarListAPIView, CarRentCreateAPIView, CarRetrieveAPIView, RentalListAPIView, RentalCancelAPIView

app_name = 'cars'

urlpatterns = [
    path('', CarListAPIView.as_view(), name='list'),
    path('<int:car_id>/', CarRetrieveAPIView.as_view(), name='detail'),
    path('<int:car_id>/rent/', CarRentCreateAPIView.as_view(), name='rent'),
    path('rentals/',RentalListAPIView.as_view(), name='rents'),
    path('rentals/<int:rental_id>/cancel/',RentalCancelAPIView.as_view(), name='return-car'),
]