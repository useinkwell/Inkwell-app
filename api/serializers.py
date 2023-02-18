from rest_framework import serializers

from user.models import User, Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    # by default, the serializer.save() saves a user instance with the password
    # in raw text. So we use a custom serializer save() method to ensure that
    # the password for the user instance is saved correctly and encrypted.
    def save(self, **kwargs):
        
        email = self.validated_data.get('email')
        user_name = self.validated_data.get('user_name')
        first_name = self.validated_data.get('first_name')
        last_name = self.validated_data.get('last_name')
        password = self.validated_data.get('password') # raw text password
        user = User(
            email=email,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name
        )
        
        if password:
            user.set_password(password) # encrypts the raw password
            user.save()
        return user
        