from rest_framework import serializers
from base.models import News,Comment,NewsView,Bookmark,Tag
from accounts.models import User

class RagisterSerializer(serializers.Serializer):
    class Meta:
        model= User
        fields = [ '__all__' ]

class NewsSerializer(serializers.Serializer):
    class Meta:
        model = News
        fields = '__all__'
    

