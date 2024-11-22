from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home_Path'),
    path('room/<str:pk>', views.room, name='Room_Path'),

    path('create-room', views.createRoom, name='Create_Room_Path'),
    path('update-room/<str:pk>', views.updateRoom, name='Update_Room_Path'),
    path('delete-room/<str:pk>', views.deleteRoom, name='Delete_Room_Path'),

    path('signIn', views.signIn, name='signIn_Path'),
    path('signOut', views.signOut, name='signOut_Path'),
    path('signUp', views.signUp, name='signUp_Path'),
    
    path('delete-message/<str:pk>', views.deleteMessage, name='Delete_Message_Path'),

    path('user-profile/<str:pk>', views.userProfile, name='User_Profile_Path'),

    path('update-user', views.updateUser, name='Update_User_Path'),

    path('topics', views.topics, name='Topics_Path'),
    path('activities', views.activities, name='Activities_Path'),
]