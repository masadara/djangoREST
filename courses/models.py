from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='course_previews/', verbose_name='Превью', null=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='Превью', null=True)
    video_url = models.URLField(verbose_name='Ссылка на видео', null=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"