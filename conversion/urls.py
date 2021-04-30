from django.urls import path
from conversion import views

urlpatterns = [
    path('convert/latest/', views.Convert.as_view())
]