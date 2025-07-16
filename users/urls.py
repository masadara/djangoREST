from django.urls import path
from .views import UserCreateView, PaymentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('user/', UserCreateView.as_view(), name='user-create'),
] + router.urls