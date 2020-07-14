from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    """ serializer for register class """

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """ serializer for user login """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ validate and authenticate the user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = 'User not Found, Please Try Different User'
            raise serializers.ValidationError(
                {'message': msg},
                code='authentication'
            )
        attrs['user'] = user
        return attrs
