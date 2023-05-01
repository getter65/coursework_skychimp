from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from school.models import Payment
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'user',
            'datetime',
            'course',
            'lesson',
            'amount',
            'method_of_payment'
        )


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True)

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        payment_data = validated_data.pop('payment_set')
        user = User.objects.create(**validated_data)

        for payment in payment_data:
            Payment.objects.create(user=user, **payment)

        return validated_data

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'avatar',
            'phone',
            'city',
            'payments'
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'email',
            'avatar',
            'phone',
            'city',
        )
