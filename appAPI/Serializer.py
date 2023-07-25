from rest_framework import serializers
from appAPI.models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','email','password','username','first_name','last_name']
