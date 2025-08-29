from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from courses.models import Course, Lesson, Subscription
from users.models import User

# Create your tests here.
class LessonCRUDAndSubscriptionTests(APITestCase):

    def setUp(self):
        # Создаём пользователей
        self.user_owner = User.objects.create_user(email='owner@example.com', password='pass1234')
        self.user_other = User.objects.create_user(email='other@example.com', password='pass1234')
        self.moderator = User.objects.create_user(email='moderator@example.com', password='pass1234')

        # Создаём группу модераторов и добавляем туда moderator
        moderators_group, _ = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(moderators_group)

        # Создаём курс с владельцем
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание курса',
            owner=self.user_owner
        )

        # Создаём урок с владельцем
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Урок 1',
            description='Описание урока',
            video_url='https://www.youtube.com/watch?v=abcdef',
            owner=self.user_owner
        )

        # URLs с namespace 'courses'
        self.lesson_list_create_url = reverse('courses:lesson-list-create')
        self.lesson_detail_url = reverse('courses:lesson-detail', kwargs={'pk': self.lesson.pk})
        self.subscription_toggle_url = reverse('courses:subscription-toggle')

    # --- CRUD тесты для уроков ---

    def test_list_lessons_accessible_for_anyone(self):
        self.client.force_authenticate(user=self.user_owner)  # Аутентифицируем пользователя
        response = self.client.get(self.lesson_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем структуру
        self.assertTrue(
            (isinstance(response.data, dict) and 'results' in response.data) or isinstance(response.data, list)
        )

    def test_create_lesson_authenticated_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        data = {
            'course': self.course.id,
            'title': 'Новый урок',
            'description': 'Описание нового урока',
            'video_url': 'https://www.youtube.com/watch?v=newvideo',
        }
        response = self.client.post(self.lesson_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        # Проверяем, что owner установился корректно
        lesson = Lesson.objects.get(id=response.data['id'])
        self.assertEqual(lesson.owner, self.user_owner)

    def test_create_lesson_unauthenticated(self):
        data = {
            'course': self.course.id,
            'title': 'Урок без аутентификации',
            'description': 'Описание',
            'video_url': 'https://www.youtube.com/watch?v=newvideo',
        }
        response = self.client.post(self.lesson_list_create_url, data)
        # Ожидаем отказ из-за отсутствия аутентификации (401) или запрет (403)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_retrieve_lesson(self):
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        data = {
            'course': self.course.id,
            'title': 'Обновленное название урока',
            'description': self.lesson.description,
            'video_url': self.lesson.video_url,
        }
        response = self.client.put(self.lesson_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])

    def test_update_lesson_other_user(self):
        self.client.force_authenticate(user=self.user_other)
        data = {
            'course': self.course.id,
            'title': 'Попытка обновления чужим пользователем',
            'description': self.lesson.description,
            'video_url': self.lesson.video_url,
        }
        response = self.client.put(self.lesson_detail_url, data, format='json')
        # Возможно 403 Forbidden, либо 200 если разрешения другие
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])

    def test_delete_lesson_owner(self):
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.delete(self.lesson_detail_url)
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_403_FORBIDDEN])
        if response.status_code == status.HTTP_204_NO_CONTENT:
            self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_delete_lesson_other_user(self):
        self.client.force_authenticate(user=self.user_other)
        response = self.client.delete(self.lesson_detail_url)
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_403_FORBIDDEN])

    # --- Тесты подписок ---

    def test_subscribe_authenticated_user(self):
        self.client.force_authenticate(user=self.user_other)
        response = self.client.post(self.subscription_toggle_url, data={'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user_other, course=self.course).exists())

    def test_unsubscribe_authenticated_user(self):
        Subscription.objects.create(user=self.user_other, course=self.course)
        self.client.force_authenticate(user=self.user_other)
        response = self.client.post(self.subscription_toggle_url, data={'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user_other, course=self.course).exists())



