from django.urls import path
from appAPI.views import UsersList
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('users', UsersList, basename='users')

urlpatterns = router.urls
