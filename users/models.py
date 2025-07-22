from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from courses.models import Course, Lesson
from django.conf import settings

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser должен иметь is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватарка')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный курс'
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный урок'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, verbose_name='Способ оплаты'
    )

    def __str__(self):
        target = self.paid_course or self.paid_lesson
        return f"Оплата {target} пользователем {self.user} ({self.amount} руб.)"