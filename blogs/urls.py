from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from blogs import views

router = DefaultRouter()
router.register(r'blogs', views.BlogsView, basename='blogs')
router.register(r'tags', views.TagsView, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('sample/', views.UserView.as_view()),
    # path('leaderboard/', views.LeaderBoardView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
