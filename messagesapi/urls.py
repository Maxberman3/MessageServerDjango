from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from messagesapi import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('registration', views.UserController.as_view(), name='registration'),
    path('token', obtain_auth_token, name='token'),
    path('messages', views.MessageList.as_view(), name='messages'),
    path('messages/<int:pk>', views.MessageDetail.as_view(),
         name='specific_message'),
    path('users/<int:pk>/messages', views.UserMessages.as_view(),
         name='specific_users_messages')
]

urlpatterns = format_suffix_patterns(urlpatterns)
