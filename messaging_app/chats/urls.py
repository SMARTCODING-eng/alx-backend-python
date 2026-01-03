#!/usr/bin/env python3
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

NestedDefaultRouter = routers.DefaultRouter()
NestedDefaultRouter.register(r'messages', MessageViewSet, basename='Conversation-messages')


urlpatterns = [

    path('', include(router.urls)),
    path('', include(NestedDefaultRouter.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
