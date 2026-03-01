from django.shortcuts import render, redirect
from .models import Tag, News

from accounts.views import jwt_login_required  
# Create your views here.

@jwt_login_required
def Home(request):
    news=News.objects.all()
    return render(request, "home.html", {"jwt_user": request.jwt_user, "news": news})

@jwt_login_required
def NewsDetail(request, slug):
    news = News.objects.get(id=slug)
    return render(request, "news_detail.html", {"jwt_user": request.jwt_user, "news": news})

