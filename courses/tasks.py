from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import User
from courses.models import Subscription, Course

@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)
    recipient_list = list(subscriptions.values_list('user__email', flat=True))  # Явно приведём к списку

    subject = f'Обновления курса "{course.title}"'
    message = f'В курсе "{course.title}" появились новые материалы. Заходите посмотреть обновления!'

    # Выводим информацию перед отправкой
    print(f"Отправляем письмо с '{settings.DEFAULT_FROM_EMAIL}' на следующие адреса:")
    for email in recipient_list:
        print(f" - {email}")

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
