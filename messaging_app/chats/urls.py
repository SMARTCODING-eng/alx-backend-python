#!/usr/bin/env python3
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include

routers = DefaultRouter()
routers.register(r'conversations', ConversationViewSet, basename='conversation')
routers.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(routers.urls)),
    
]
