from django.urls import path

from .views import buy_item, create_order, show_item

urlpatterns = [
    path('buy/<int:pk>/', buy_item),
    path('item/<int:pk>/', show_item),
    path('new_order/', create_order),
]
