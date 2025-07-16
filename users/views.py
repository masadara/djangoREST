from rest_framework import generics
from .serializers import UserCreateSerializer
from rest_framework import generics, filters, viewsets
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']