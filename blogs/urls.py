from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blogs import views

router = DefaultRouter()
router.register(r'blogs', views.BlogsView, basename='blogs')
router.register(r'tags', views.TagsView, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
