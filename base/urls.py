from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.Home, name='home'),
    path('news/<slug:slug>/', views.NewsDetail, name='news-detail'), 
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('add-comment/<int:id>/', views.AddComment, name='add_comment'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)