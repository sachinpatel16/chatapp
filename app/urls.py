from django.contrib import admin
from django.urls import path, include

from app import views
urlpatterns = [
    path("", views.home, name="home"),
    path("create-group/", views.create_group, name="create_group"),
    path("assign-user/<int:room_id>/", views.assign_user_to_group, name="assign_user"),
    path('chat/<str:room_name>/', views.chat, name='chat'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    # path('chat/', views.chat, name='default-chat'),
    path("singup/", views.singup, name="reg"),
    path("singin/", views.singin, name="login"),
    path('logout/', views.logout_view, name='logout'),
]
