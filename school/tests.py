from rest_framework.test import APITestCase
from rest_framework import status

from school.models import Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        test_email = 'test@te.ru'
        test_password = 'abc123'

        self.user = User(
            email=test_email,
            first_name='First',
            last_name='Last',
            phone='999',
            city='Nowhere',
            is_superuser=True,
            is_staff=True
        )
        self.user.set_password(test_password)
        self.user.save()

        response = self.client.post(
            '/api/token/',
            {
                'email': test_email,
                'password': test_password
            }
        )
        self.access_token = response.json().get('access')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(name='test course', description='test description')

    def test_lesson_create(self):
        self.test_model_lesson_name = 'test lesson'
        self.test_model_lesson_slug = self.test_model_lesson_name.replace(' ', '-')
        self.test_model_lesson_description = 'test test'
        self.test_model_lesson_content = 'https://www.youtube.com'

        response = self.client.post(
            '/lessons/create/',
            {
                'name': self.test_model_lesson_name,
                'description': self.test_model_lesson_description,
                'course': self.course.pk,
                "content": self.test_model_lesson_content
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_retrieve(self):
        self.test_lesson_create()
        response = self.client.get(
            f'/lessons/{self.test_model_lesson_slug}/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                'name': self.test_model_lesson_name,
                'course': self.course.pk,
                'preview': None,
                'description': self.test_model_lesson_description,
                'content': self.test_model_lesson_content
            }
        )

    def test_lesson_list(self):
        self.test_lesson_create()
        response = self.client.get(
            '/lessons/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            [{
                'name': self.test_model_lesson_name,
                'course': self.course.pk,
                'preview': None,
                'description': self.test_model_lesson_description,
                'content': self.test_model_lesson_content
            }]
        )

    def test_lesson_update(self):
        self.test_lesson_create()
        self.test_model_lesson_updated_name = 'updated ' + self.test_model_lesson_name
        response = self.client.patch(
            f'/lessons/update/{self.test_model_lesson_slug}/',
            {
                'name': self.test_model_lesson_updated_name
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                'name': self.test_model_lesson_updated_name,
                'course': self.course.pk,
                'preview': None,
                'description': self.test_model_lesson_description,
                'content': self.test_model_lesson_content
            }
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        test_email = 'test@te.ru'
        test_password = 'abc123'

        self.user = User(
            email=test_email,
            first_name='First',
            last_name='Last',
            phone='999',
            city='Nowhere',
            is_superuser=True,
            is_staff=True
        )
        self.user.set_password(test_password)
        self.user.save()

        response = self.client.post(
            '/api/token/',
            {
                'email': test_email,
                'password': test_password
            }
        )
        self.access_token = response.json().get('access')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(name='test course', description='test description')

    def test_subscription_create(self):

        response = self.client.post(
            '/subscriptions/create/',
            {
                'course': self.course.pk,
                'user': self.user.pk
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_destroy(self):
        self.test_subscription_create()
        response = self.client.delete(
            '/subscriptions/destroy/1/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
