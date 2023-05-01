from abc import ABC

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from school.models import Lesson, Course, Subscription
from school.validators import PermittedContentValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'name',
            'course',
            'preview',
            'description',
            'content'
        )
        validators = [PermittedContentValidator(field='content')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_num = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, required=False)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'name',
            'preview',
            'description',
            'lesson_num',
            'lessons',
            'subscription'
        )

    def create(self, validated_data):
        lessons_data = None
        if 'lesson_set' in validated_data:
            lessons_data = validated_data.pop('lessons')
        course = Course.objects.create(**validated_data)
        if lessons_data:
            for lesson_data in lessons_data:
                Lesson.objects.create(course=course, **lesson_data)
        return course

    def get_lesson_num(self, instance):
        lessons = Lesson.objects.filter(course=instance).all().count()
        if lessons:
            return lessons
        return 0

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    def get_subscription(self, instance):
        current_user = self._user(instance)
        subscriptions = Subscription.objects.filter(course=instance, user=current_user).first()
        if subscriptions:
            return 'subscribed'
        return 'not subscribed'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'user',
            'course'
        )


# class PaymentSerializer(serializers.Serializer, ABC):
#     terminal_key = serializers.CharField(max_length=20, default='1677659270153DEMO')
#     amount = serializers.IntegerField()
#     order_id = serializers.IntegerField()
