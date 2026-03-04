from django.shortcuts import render, redirect

from accounts import views
from .models import Tag, News, Comment, NewsView

from accounts.views import jwt_login_required  
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

# Create your views here.

@jwt_login_required
def Home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    news = News.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)| Q(tags__name__icontains=q)).order_by('-published_at').distinct()
    
    
    return render(request, "home.html", {"jwt_user": request.jwt_user, "news": news})

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