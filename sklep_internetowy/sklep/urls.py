from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Widoki HTML (Strona sklepu)
    path('', views.coffee_shop_view, name='sklep-home'), # strona glowna sklepu
    path('kawy/<int:id>/', views.coffee_detail_html, name='coffee-detail-html'), # szczegóły konkretnej kawy po ID
    path("klienci/", views.customer_list_html, name="customer-list-html"), # lista klientow
    path("klienci/<int:id>/", views.customer_detail_html, name="customer-detail-html"), # szczegoly klienta
    path("klienci/dodaj/", views.customer_create_html, name="customer-create-html"), # strona do dodawania klientow przez html
    path("welcome/", views.welcome_view),
    # Widoki API 
    path('api/customers/', views.CustomerList.as_view(), name='customer-list'), # endpoint do pobierania listy i tworzenia klientów (POST/GET)
    path('api/customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'), # endpoint do operacji na konkretnym kliencie (GET/PUT/DELETE)
    path('api/producenci/', views.producent_list, name='producent-list'), # lista producentów w API
    path('api/producenci/<int:pk>/', views.producent_detail, name='producent-detail'), # endpoint do operacji na konkretnym producencie
    path('api/register/', views.register_user, name='api-register'), # endpoint rejestracji nowego konta użytkownika
    path('api/token/', obtain_auth_token, name='api-token'), # endpoint do logowania – zwraca token po podaniu loginu i hasła
    path('api/kawy/mocne/', views.strong_coffee_list, name='kawy-mocne'), # filtr: tylko bardzo mocne kawy
]
