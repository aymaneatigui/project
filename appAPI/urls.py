from django.urls import path
from appAPI.views import UsersList, UserRUD, message, SignUpView, LoginView

# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns =[
    path('users/', UsersList.as_view(), name='users'),
    path("user/<int:pk>/", UserRUD.as_view(), name='user'),
    path("secret/", message.as_view()),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    # path("api-token-auth/", obtain_auth_token)
]
