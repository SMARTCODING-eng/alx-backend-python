#!/usr/bin/env python3
from rest_framework import routers
# from rest_framework.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

NestedDefaultRouter = routers.DefaultRouter()
NestedDefaultRouter.register(r'messages', MessageViewSet, basename='Conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(NestedDefaultRouter.urls)),

]
