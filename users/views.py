from rest_framework import generics
from .serializers import UserCreateSerializer, UserSerializer
from rest_framework import generics, filters, viewsets, permissions
from .models import Payment, User
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

# class UserCreateView(generics.CreateAPIView):
#     serializer_class = UserCreateSerializer
#
# class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

class RegisterView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes_by_action = {
        'create': [permissions.AllowAny],
        'list': [permissions.AllowAny],
        'retrieve': [permissions.IsAuthenticated, IsOwnerOrAdmin],
        'update': [permissions.IsAuthenticated, IsOwnerOrAdmin],
        'partial_update': [permissions.IsAuthenticated, IsOwnerOrAdmin],
        'destroy': [permissions.IsAdminUser],
    }

    def get_permissions(self):
        try:
            permissions_classes = self.permission_classes_by_action[self.action]
        except KeyError:
            permissions_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permissions_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return UserProfileSerializer
        return UserSerializer

