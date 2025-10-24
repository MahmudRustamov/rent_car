from django.urls import path
from apps.accounts.views import RegisterView, LoginView, LogoutAPIView, ProfileRetrieveAPIView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', ProfileRetrieveAPIView.as_view(), name='profile'),

]