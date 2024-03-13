from rest_framework.serializers import ModelSerializer

from main import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        

class UserRealtionSerializer(ModelSerializer):
    class Meta:
        model = models.UserReletion
        fields = '__all__'
        
        
class ChatSerializer(ModelSerializer):
    class Meta:
        model = models.Chat
        fields ='__all__'
        
        
class MassageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'