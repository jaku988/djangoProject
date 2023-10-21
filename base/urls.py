from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('login/', views.login_page, name="login_page"),
    path('logout/', views.logout_user, name="logout_user"),
    path('register/', views.register_user, name="register_user"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>', views.user_profile, name="user_profile"),
    path('create-room/', views.create_room, name="create_room"),
    path('update-room/<str:pk>/', views.update_room, name="update_room"),
    path('delete-room/<str:pk>/', views.delete_room, name="delete_room"),
    path('topic-list/', views.topic_list, name="topic_list"),
    path('topic-list/create-topic', views.create_topic, name="create_topic"),
    path('delete-message/<str:pk>/', views.delete_message, name="delete_message"),
]
