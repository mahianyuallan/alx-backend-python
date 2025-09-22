"""
URL configuration for messaging_app project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from chats import views as chat_views  # make sure chats/views.py has your viewsets

# Register DRF viewsets
router = routers.DefaultRouter()
router.register(r"conversations", chat_views.ConversationViewSet, basename="conversation")
router.register(r"messages", chat_views.MessageViewSet, basename="message")

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT auth endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Your API
    path("api/", include(router.urls)),
]
