from django.urls import path
from appAPI.views import UsersList
from rest_framework.routers import DefaultRouter

router = DefaultRouter
router.register(r'users', UsersList)