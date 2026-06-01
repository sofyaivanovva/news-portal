from rest_framework import serializers
from django.contrib.auth.models import User
from .models import News


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    title = serializers.CharField(
        max_length=200,
        allow_blank=True,
        error_messages={'required': 'Это поле обязательно.'},
    )
    content = serializers.CharField(
        allow_blank=True,
        error_messages={'required': 'Это поле обязательно.'},
    )

    class Meta:
        model = News
        fields = ['id', 'title', 'summary', 'content', 'author', 'author_name', 'date_created']
        read_only_fields = ['author', 'date_created']

    def validate_title(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError('Это поле обязательно.')
        if len(value.strip()) < 5:
            raise serializers.ValidationError('Заголовок должен содержать минимум 5 символов.')
        return value

    def validate_summary(self, value):
        if value and len(value) < 10:
            raise serializers.ValidationError('Краткое описание должно содержать минимум 10 символов.')
        return value

    def validate_content(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError('Это поле обязательно.')
        if len(value) < 50:
            raise serializers.ValidationError('Минимум 50 символов.')
        return value
