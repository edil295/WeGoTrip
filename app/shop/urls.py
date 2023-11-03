from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='list_products'),
    path('order/', views.OrderCreateView.as_view(), name='add_order'),
    path('payment/', views.PaymentCreateView.as_view(), name='add_payment'),
    path('confirm_order/<int:pk>/', views.ConfirmOrderView.as_view(), name='confirm_order'),
]
