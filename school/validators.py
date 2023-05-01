from rest_framework import serializers


class PermittedContentValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        content = value.get('content')
        if content:
            if 'https://www.youtube.com' not in content:
                raise serializers.ValidationError('Запрещенный ресурс')
