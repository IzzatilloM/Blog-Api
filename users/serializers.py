from rest_framework import serializers
from django.contrib.auth.models  import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','email','first_name','last_name','date_joined')
        required_fields = ['first_name',]
        extra_kwargs = {
            'password':{
                'write_only':True,
            }
        }
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=3, max_length=32)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        return attrs
