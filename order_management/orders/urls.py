from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("create/", views.create_order, name="create-order"),
    path("list/", views.list_orders, name="order-list"),
    path("update/<int:order_id>", views.update_order, name="update-order"),
    path("remove/<int:order_id>", views.remove_order, name="remove-order"),
]
