from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user


urlpatterns = [
    path("signup/", sign_up, name="sign_up"),
    path("signin/", sign_in, name="sign_in"),
    path("activate/<str:uidb64>/<str:token>/", activate_user, name="activate_user"),
    path("signout/", sign_out, name="sign_out"),
]
