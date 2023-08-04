from rest_framework import serializers
from appAPI.models import MyUser

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(label='Username')
    email = serializers.CharField(label='Email')
    first_name = serializers.CharField(label='First Name')
    last_name = serializers.CharField(label='Last Name')

    class Meta:
        model = MyUser
        fields = ['id','email','password','username','first_name','last_name']
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving the user
        password = validated_data.pop('password')
        user = MyUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user