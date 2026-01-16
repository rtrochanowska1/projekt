from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.CustomerList.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'),
    path('producenci/', views.producent_list, name='producent-list'),
    path('producenci/<int:pk>/', views.producent_detail, name='producent-detail'),
    path('', views.coffee_shop_view, name='sklep-home'), 
    path("welcome/", views.welcome_view),
    path("klienci/", views.customer_list_html, name="customer-list-html"),
    path("klienci/<int:id>/", views.customer_detail_html, name="customer-detail-html"),
    path("klienci/dodaj/", views.customer_create_html, name="customer-create-html"),
]