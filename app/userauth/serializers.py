from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from core.models import CommunityMember, Community

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


class CommunityProfileSerializer(serializers.ModelSerializer):
    """ community profile serializer """

    class Meta:
        model = Community
        fields = ('id', 'name', 'image',)
        read_only_field = ('id', 'name', 'image',)


class CommunityMemberSerializer(serializers.ModelSerializer):
    """ community profile serializer """
    community = CommunityProfileSerializer(read_only=True)

    class Meta:
        model = CommunityMember
        fields = ('community',)
        read_only_field = ('community',)


class ProfileSerializer(serializers.ModelSerializer):
    """ User Profile Serializer """
    community = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'exp', 'about', 'age',
                  'password', 'image', 'community',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def get_community(self, profile):
        community_member = CommunityMember.objects.filter(user=profile)
        communities = Community.objects.filter(communitymember__in=community_member)
        serializer = CommunityProfileSerializer(instance=communities, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        """ update user """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
