from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.Home, name='home'),
    path('news/<slug:slug>/', views.NewsDetail, name='news-detail'), 
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('add-comment/<int:id>/', views.AddComment, name='add_comment'),
    path('bookmark/<int:id>/', views.BookmarkNews, name='bookmark_news'),
    path ('profile/<slug:username>/', views.ProfileView, name='profile_view'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)