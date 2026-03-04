from django.shortcuts import render, redirect
from .models import Tag, News, Comment

from accounts.views import jwt_login_required  
# Create your views here.

@jwt_login_required
def Home(request):
    news=News.objects.all()
    return render(request, "home.html", {"jwt_user": request.jwt_user, "news": news})

@jwt_login_required
def NewsDetail(request, slug):
    news = News.objects.get(id=slug)
    comment = news.comments.all()
    return render(request, "news_detail.html", {"jwt_user": request.jwt_user, "news": news, "comment": comment})

@jwt_login_required
def AddComment(request, id):
    if request.method == 'POST':
        news = News.objects.get(id=id)
        content = request.POST.get('content')
        Comment.objects.create(news=news, user=request.jwt_user, content=content)
    return redirect('news-detail', slug=id)