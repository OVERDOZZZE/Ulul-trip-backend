from django.contrib.auth import password_validation
from rest_framework import serializers, exceptions
from src.users.models import User
from src.users.registration_validators import validate_number


class ProfileEditSerializer(serializers.ModelSerializer):
    user_slug = serializers.HiddenField(default='')
    name = serializers.CharField(max_length=100, min_length=2,
                                 help_text='Name should contain only alphabetical characters')
    number = serializers.CharField(max_length=9,
                                   help_text=['Numbers length is should be 9', 'Number should contain only digits'])
    username = serializers.CharField(max_length=30, min_length=2,
                                     help_text='Username should contain only alphanumeric characters')
    image = serializers.ImageField(allow_null=True,
                                   default='static/media/user_images/default_image/default_user_image.jpeg')

    class Meta:
        model = User
        fields = ['id', 'user_slug', 'name', 'username', 'number', 'image']

    def validate(self, attrs):
        name = attrs.get('name', '')
        username = attrs.get('username', '')
        if not name.isalpha() and name.count(' ') > 1:
            raise serializers.ValidationError(
                f'The users name is not valid, make sure that it contains only alphabetical characters')
        if not username.isalnum():
            raise serializers.ValidationError(
                f'The users username: {username} should only contain alphanumeric characters', 400)
        username1 = User.objects.filter(username=username).exists()
        if username1:
            raise serializers.ValidationError(f'This username: {username} is not available, please write new one', 400)
        return super().validate(attrs)

    def validate_number(self, number):
        try:
            validate_number(number)
        except exceptions.ValidationError as error:
            raise serializers.ValidationError(f'error: {error.get_codes()}')
        return number


class ChangePasswordSerializer(serializers.ModelSerializer):
    password_old = serializers.CharField(
        max_length=30,
        min_length=6,
        help_text=password_validation.password_validators_help_texts(),
        write_only=True,
        style={'input_type': 'password'}
    )
    password_new_again = serializers.CharField(
        max_length=30,
        min_length=6,
        write_only=True,
        help_text=password_validation.password_validators_help_texts(),
        style={'input_type': 'password'}
    )
    password_new = serializers.CharField(
        max_length=30,
        min_length=6,
        write_only=True,
        help_text=password_validation.password_validators_help_texts(),
        style={'input_type': 'password'},
    )
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email', 'password_old', 'password_new', 'password_new_again')

    def validate_password_new(self, password_new):
        errors = {}
        try:
            password_validation.validate_password(password=password_new)
        except exceptions.ValidationError as exc:
            errors['password_new'] = list(exc.get_codes())
        if errors:
            raise serializers.ValidationError(str(errors))

        return password_new


