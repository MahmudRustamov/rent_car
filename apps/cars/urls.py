from django.urls import path
from apps.cars.views import CarListAPIView, CarRentCreateAPIView

app_name = 'cars'

urlpatterns = [
    path('', CarListAPIView.as_view(), name='list'),
    path('<int:car_id>/rent/', CarRentCreateAPIView.as_view(), name='rent'),
]