from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from base.models import News
from .serializers import NewsSerializer
from rest_framework.response import Response

# Create your views here.
class NewsViewSet(viewsets.ViewSet):
    def list(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many= True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        id=pk
        pass
        # news= News.objects.get()
