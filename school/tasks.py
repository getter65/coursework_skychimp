import datetime
import hashlib

import requests
from celery import shared_task
from celery.contrib import rdb
from django.conf import settings
from django.core.mail import send_mail

from school.models import Course, Lesson, CourseUpdateLog, LessonUpdateLog, PaymentLog, Payment
from users.models import User


@shared_task
def update_course_check(course_pk):
    start_sending = True
    print(f'task for {course_pk}')
    course_item = Course.objects.filter(pk=course_pk).first()
    if not course_item:
        start_sending = False
    else:
        last_course_update = CourseUpdateLog.objects.filter(course=course_item).last()
        last_pk = last_course_update.pk
        previous_update = CourseUpdateLog.objects.filter(course=course_item, pk__lt=last_pk).order_by('pk').last()

        print(f'обновление в {previous_update.change}')
        if datetime.datetime.now().astimezone() - previous_update.change < datetime.timedelta(hours=4):
            start_sending = False
        else:
            lessons_from_course = Lesson.objects.filter(course=course_item).all()
            if lessons_from_course:
                for lesson in lessons_from_course:
                    last_lesson_update = LessonUpdateLog.objects.filter(lesson=lesson).last()
                    if last_lesson_update:
                        print(f'обновление в {last_lesson_update.change}')
                        if datetime.datetime.now().astimezone() - previous_update.change < datetime.timedelta(hours=4):
                            start_sending = False
                            break

                        start_sending = True

    if start_sending:
        recipients = [user.email for user in User.objects.filter(subscription__course=course_item).all()]
        send_mail(
            subject='Обновления в курсе',
            message=f'Курс {course_item.name}, на который вы подписаны, был обновлен.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipients
        )


@shared_task()
def check_status():
    payment_logs = PaymentLog.objects.filter(is_checked=False).all()
    print(payment_logs)
    if payment_logs:
        for payment_log in payment_logs:
            payment = Payment.objects.filter(paymentlog=payment_log).first()
            print(payment)
            payment_bank_id = payment_log.bank_payment_id
            print(payment_bank_id)
            token_str = str(settings.TERMINAL_PASSWORD) + str(payment_bank_id) + str(settings.TERMINAL_KEY)
            token_sha = hashlib.sha256(token_str.encode())
            token = token_sha.hexdigest()
            print(token)

            data_for_request = {
                "TerminalKey": settings.TERMINAL_KEY,
                "PaymentId": payment_bank_id,
                "Token": token
            }

            response = requests.post('https://securepay.tinkoff.ru/v2/GetState', json=data_for_request)

            response_dict = response.json()
            print(response_dict)

            payment_log.is_checked = True
            payment_log.save()

            payment.status_check = response_dict['Status']
            payment.save()


