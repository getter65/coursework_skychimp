import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from school.models import Course, Lesson, Subscription, Payment, PaymentLog, CourseUpdateLog, LessonUpdateLog
from school.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from school.permissions import UserChangeLessonPermissionManager, UserChangeCoursePermissionManager, \
    UserRetrieveCoursePermissionManager, UserRetrieveLessonPermissionManager

from school.tasks import update_course_check, check_status


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'update': [UserChangeCoursePermissionManager],
        'partial_update': [UserChangeCoursePermissionManager],
        'list': [IsAdminUser],
        'retrieve': [UserRetrieveCoursePermissionManager],
        'destroy': [IsAdminUser]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):
        self.object = serializer.save()
        new_log = CourseUpdateLog.objects.create(course=self.object)
        update_course_check.delay(self.object.pk)


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [UserRetrieveLessonPermissionManager]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    lookup_field = 'slug'


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [UserChangeLessonPermissionManager]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    lookup_field = 'slug'

    def perform_update(self, serializer):
        self.object = serializer.save()
        new_log = LessonUpdateLog.objects.create(course=self.object)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class PaymentView(APIView):

    def get(self, *args, **kwargs):
        payment = None
        price = 0
        user = self.request.user

        lesson_slug = self.kwargs.get('slug')

        if lesson_slug:
            lesson = get_object_or_404(Lesson, slug=lesson_slug)
            price = lesson.price

            payment = Payment.objects.create(
                lesson=lesson,
                user=user,
                amount=price
            )
        else:
            course_pk = self.kwargs.get('pk')
            if course_pk:
                course = get_object_or_404(Course, pk=course_pk)
                price = course.price
                payment = Payment.objects.create(
                    course=course,
                    user=user,
                    amount=price
                )

        data_for_request = {
            "TerminalKey": settings.TERMINAL_KEY,
            "Amount": price,
            "OrderId": payment.pk
        }
        response = requests.post('https://securepay.tinkoff.ru/v2/Init', json=data_for_request)

        response_dict = response.json()
        print(response_dict)

        if response_dict.get('Success'):
            payment_pk = response_dict.get('OrderId')
            PaymentLog.objects.create(
                payment=Payment.objects.get(pk=payment_pk),
                success=response_dict.get('Success'),
                error_code=response_dict.get('ErrorCode'),
                terminal_key=response_dict.get('TerminalKey'),
                status=response_dict.get('Status'),
                bank_payment_id=response_dict.get('PaymentId'),
                amount=response_dict.get('Amount'),
                payment_url=response_dict.get('PaymentURL'),
            )

        return Response({
            'url': response_dict['PaymentURL']
        })
