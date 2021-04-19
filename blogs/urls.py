from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from blogs import views

router = DefaultRouter()
router.register(r'blogs', views.BlogsView, basename='blogs')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)









# urlpatterns = [
#     path('blogs/', BlogsView.as_view(), name = 'blogs'),
#     path('comments/<str:pk>', CommentsView.as_view(), name = 'comments'),
#     path('likes/<str:pk>', LikesView.as_view(), name = 'likes'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)