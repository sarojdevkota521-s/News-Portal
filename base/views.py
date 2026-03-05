import string

from django.shortcuts import render, redirect
from django.http import HttpResponse

from accounts import views
from .models import Tag, News, Comment, NewsView

from accounts.views import jwt_login_required  
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
import nepali_datetime
from datetime import datetime
import requests

# Create your views here.

def get_nepali_date():
    now = datetime.now()
    nepali_date = nepali_datetime.date.from_datetime_date(now.date())
    return nepali_date.strftime("%K %m %d ")


def get_weather():
    api_key = "fe3980b3c291792dd093206612ef816f"

    url = f"https://api.openweathermap.org/data/2.5/weather?q=Kathmandu,np&units=metric&appid={api_key}"

    response = requests.get(url).json()

    if "main" in response:
        temperature = response['main']['temp']
        description = response['weather'][0]['description']
    else:
        temperature = "N/A"
        description = "Weather unavailable"

    return temperature, description

@jwt_login_required
def Home(request):
    temperature, description = get_weather()
    nepali_date = get_nepali_date()

    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    news = News.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)| Q(tags__name__icontains=q)).order_by('-published_at').distinct()
    context={
        "jwt_user": request.jwt_user,
        "news": news,
        "temperature": temperature,
        "description": description,
        "nepali_date": nepali_date,
    }
    
    return render(request, "home.html", context)

@jwt_login_required
def NewsDetail(request, slug):
    news = get_object_or_404(News, slug=slug)
    try:
        NewsView.objects.create(news=news,user=request.jwt_user) 
        News.objects.filter(id=news.id).update(view=F('view') + 1)
    except IntegrityError:
        pass
    news.arefresh_from_db()
    return render(request, "news_detail.html", {"jwt_user": request.jwt_user, "news": news})
        

@jwt_login_required
def AddComment(request, id):
    if request.method == 'POST':
        news = News.objects.get(id=id)
        content = request.POST.get('content')
        Comment.objects.create(news=news, user=request.jwt_user, content=content)
    return redirect('news-detail', slug=id)