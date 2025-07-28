from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from courses.models import Course, Lesson, Subscription
from .paginators import MyPagination, LessonPagination
from .serializers import CourseSerializer, LessonSerializer
from courses.permissions import IsModeratorOrOwner
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    # permission_classes = [IsAuthenticated, IsModeratorOrOwner]
    permission_classes = [AllowAny]
    pagination_class = MyPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    # permission_classes = [IsAuthenticated & IsModeratorOrOwner]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user or not self.request.user.is_authenticated:
            raise NotAuthenticated('Требуется аутентификация')
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated & IsModeratorOrOwner]
    permission_classes = [AllowAny]

class SubscriptionToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # request.user гарантированно аутентифицирован или 401
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'error': 'course_id не передан'}, status=400)
        course = get_object_or_404(Course, id=course_id)
        subscription_qs = Subscription.objects.filter(user=request.user, course=course)
        if subscription_qs.exists():
            subscription_qs.delete()
            message = 'подписка удалена'
            status_code = status.HTTP_200_OK
        else:
            Subscription.objects.create(user=request.user, course=course)
            message = 'подписка добавлена'
            status_code = status.HTTP_201_CREATED
        return Response({'message': message}, status=status_code)

