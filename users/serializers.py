from rest_framework import serializers
from .models import User, Payment
from courses.serializers import CourseSerializer, LessonSerializer

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'avatar')

class PaymentSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(read_only=True)
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'payment_date',
            'paid_course',
            'paid_lesson',
            'amount',
            'payment_method',
        ]