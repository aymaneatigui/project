from rest_framework import serializers
from appAPI.models import MyUser

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(label='Username')
    email = serializers.CharField(label='Email')
    first_name = serializers.CharField(label='First Name', source='fname')
    last_name = serializers.CharField(label='Last Name', source='lname')

    class Meta:
        model = MyUser
        fields = ['id','email','password','username','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}

