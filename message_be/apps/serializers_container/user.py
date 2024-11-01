from message_be.apps.serializers_container import serializers, User, RefreshToken, AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'image']

def validated_user_data(email, username):
    if not username.isalnum():
        raise serializers.ValidationError('The username should only contain alphanumeric characters')
    if User.objects.filter(email = email).exists():
        raise serializers.ValidationError('This email is already in use.')
    if User.objects.filter(username = username).exists():
        raise serializers.ValidationError('This username is already in use.')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=80, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        validated_user_data(attrs.get('email', ''), attrs.get('username', ''))
        return attrs

    def create(self, validated_data):
        validated_data['is_active'] = True
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        token = RefreshToken.for_user(user)
        return {
            'user': {
                'email': user.email,
                'username': user.username,
            },
            'access_token': str(token.access_token),
        }

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        refresh = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'username': user.username,
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }