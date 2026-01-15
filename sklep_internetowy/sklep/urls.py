from django.urls import path
from . import views

urlpatterns = [
    # Endpointy dla Klientów (Klasy)
    path('customers/', views.CustomerList.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'),
    
    # Endpointy dla Producentów (Funkcje)
    path('producenci/', views.producent_list, name='producent-list'),
    path('producenci/<int:pk>/', views.producent_detail, name='producent-detail'),
]