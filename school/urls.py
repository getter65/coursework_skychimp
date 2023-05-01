from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path
from school.apps import SchoolConfig
from school.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView, PaymentView

app_name = SchoolConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/<str:slug>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lessons/update/<str:slug>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscriptions/destroy/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_destroy'),
    path('payment/<int:pk>/', PaymentView.as_view(), name='payment_course'),
    path('payment/<str:slug>/', PaymentView.as_view(), name='payment_lesson'),
    ]

urlpatterns += router.urls
