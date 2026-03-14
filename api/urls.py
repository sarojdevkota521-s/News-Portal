from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('newsapi', views.NewsViewSet, basename='news-api')

urlpatterns = router.urls