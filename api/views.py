from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from base.models import News
from .serializers import NewsSerializer
from rest_framework.response import Response

# Create your views here.
class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer