from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

User = settings.AUTH_USER_MODEL


@shared_task
def deactivate_inactive_users():
    from django.contrib.auth import get_user_model
    User = get_user_model()

    threshold_date = timezone.now() - timedelta(seconds=5)
    inactive_users = User.objects.filter(last_login__lt=threshold_date, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"{count} пользователей заблокировано."