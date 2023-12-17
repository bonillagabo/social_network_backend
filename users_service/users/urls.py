from django.urls import path
from . import views

urlpatterns = [
    path("create", views.createUser), 
    path("<str:username>", views.getUser)
]
