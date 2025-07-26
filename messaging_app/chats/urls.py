#!/usr/bin/env python3
from rest_framework import routers 
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

conversations_router = routers.DefaultRouter()
conversations_router.register(r'messages', MessageViewSet, basename='Conversation-messages')


urlpatterns = [
    path('', include(routers.urls)),
    path('', include(conversations_router.urls)),

]
