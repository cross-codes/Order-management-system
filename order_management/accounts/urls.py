from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("userupdate/<int:user_id>", views.update_profile, name="update_profile"),
    path("removeuser/<int:user_id>", views.remove_user, name="remove_user"),
]
