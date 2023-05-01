from django.conf import settings
from django.db import models
from django.utils.text import slugify

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', **NULLABLE, verbose_name='превью')
    description = models.CharField(max_length=500, verbose_name='описание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, **NULLABLE, on_delete=models.CASCADE, verbose_name='автор')
    price = models.PositiveIntegerField(verbose_name='цена курса', default=500000)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class CourseUpdateLog(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    change = models.DateTimeField(auto_now=True, verbose_name='последнее изменение')


class Lesson(models.Model):
    name = models.CharField(max_length=250, verbose_name='название', unique=True)
    preview = models.ImageField(upload_to='lessons/', **NULLABLE, verbose_name='превью')
    description = models.CharField(max_length=500, verbose_name='описание')
    slug = models.SlugField(max_length=50, unique=True, **NULLABLE, verbose_name='ссылка на урок')
    content = models.CharField(max_length=350, **NULLABLE, verbose_name='ссылка на материалы')
    course = models.ForeignKey(Course, **NULLABLE, on_delete=models.CASCADE, verbose_name='курс')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, **NULLABLE, on_delete=models.CASCADE, verbose_name='автор')
    price = models.PositiveIntegerField(verbose_name='цена урока', default=100000)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='последнее изменение')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class LessonUpdateLog(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    change = models.DateTimeField(auto_now=True, verbose_name='последнее изменение')


class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'trans'

    PAYMENT_CHOICES = [
        (CASH, 'наличные'),
        (TRANSFER, 'перевод')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, **NULLABLE, on_delete=models.CASCADE, verbose_name='пользователь')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты', **NULLABLE)
    course = models.ForeignKey(Course, **NULLABLE, on_delete=models.CASCADE, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, **NULLABLE, to_field="slug", on_delete=models.CASCADE, verbose_name='оплаченный урок')
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method_of_payment = models.CharField(max_length=5, choices=PAYMENT_CHOICES, default=TRANSFER, verbose_name='способ оплаты')
    status_check = models.CharField(max_length=50, **NULLABLE, verbose_name='статус платежа')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        if self.course:
            return f'{self.user} - {self.datetime} - {self.course}'
        return f'{self.user} - {self.datetime} - {self.lesson}'


class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name='платеж')
    success = models.BooleanField(verbose_name='успешность платежа')
    error_code = models.CharField(max_length=10, verbose_name='код ошибки')
    terminal_key = models.CharField(max_length=50, verbose_name='ключ терминала', **NULLABLE)
    status = models.CharField(max_length=50, verbose_name='статус', **NULLABLE)
    bank_payment_id = models.CharField(max_length=50, **NULLABLE, verbose_name='идентификатор платежа в системе банка')
    amount = models.IntegerField(verbose_name='сумма', **NULLABLE)
    payment_url = models.CharField(max_length=50, **NULLABLE, verbose_name='url для оплаты')
    is_checked = models.BooleanField(verbose_name='платеж проверен', default=False)


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
