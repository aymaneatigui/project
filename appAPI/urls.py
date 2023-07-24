from django.urls import path
from appAPI.views import UsersList, UserRUD


urlpatterns =[
    path('users/', UsersList.as_view(), name='users'),
    path("user/<int:pk>/", UserRUD.as_view(), name='user'),
]
