
from django.urls import path
from . import views

urlpatterns = [
    #admin
    path("apanel/kawy/dodaj/", views.coffee_create_admin, name="admin-coffee-create"), # dodawanie kawy przez admina
    path("apanel/zamowienia/", views.admin_orders_overview, name="admin-orders-view"), # przegląd zamówień przez admina
    path("apanel/producenci/dodaj/", views.producent_create_admin, name="admin-producents-create"), # dodawanie producenta przez admina
path("apanel/smaki/dodaj/", views.taste_create_admin, name="admin-tastes-create"), # dodawanie smaku przez admina
    #API endpoints
    path("api/register/", views.register_user, name="api-register"),
    path("api/token/login/", views.api_token_login, name="api-token-login"),
    path("api/smaki/", views.taste_list, name="taste-list"),
    path("api/smaki/create/", views.taste_create, name="taste-create"),
    path("api/smaki/update_delete/<int:pk>/", views.taste_update_delete, name="taste-update-delete"),
    path("api/producenci/", views.producent_list, name="producent-list"),
    path("api/producenci/create/", views.producent_create, name="producent-create"),
    path("api/producenci/<int:pk>/", views.producent_detail, name="producent-detail"),
    path("api/producenci/update_delete/<int:pk>/", views.producent_update_delete, name="producent-update-delete"),
    path("api/kawy/", views.coffee_list, name="coffee-list"),
    path("api/kawy/create/", views.coffee_create, name="coffee-create"),
    path("api/kawy/<int:pk>/", views.coffee_detail, name="coffee-detail"),
    path("api/kawy/update_delete/<int:pk>/", views.coffee_update_delete, name="coffee-update-delete"),
    path("api/kawy/mocne/", views.strong_coffee_list, name="coffee-strong"),
    path("api/kawy/startswith/<str:prefix>/", views.coffee_starts_with, name="coffee-startswith"),
    path("api/me/", views.my_customer_profile, name="my-customer-profile"),
    path("api/orders/", views.order_list_create, name="order-list-create"),
    path("api/orders/<int:pk>/", views.order_detail_delete, name="order-detail-delete"),
    path("api/order-items/add/", views.order_item_add, name="order-item-add"),

    # HTML
    path("", views.coffee_shop_view, name="sklep-home"), # strona główna sklepu z listą kaw
    path("kawy/<int:id>/", views.coffee_detail_html, name="coffee-detail-html"), # szczegóły kawy
    path("cart/", views.cart_detail_html, name="cart-detail"), # widok koszyka
    path("cart/add/<int:coffee_id>/", views.cart_add_html, name="cart-add"), # dodawanie kawy do koszyka
    path("cart/remove/<int:coffee_id>/", views.cart_remove_html, name="cart-remove"), # usuwanie kawy z koszyka
    path("cart/clear/", views.cart_clear_html, name="cart-clear"), # czyszczenie koszyka
    path("register/", views.register_html, name="register-html"), # rejestracja użytkownika
    path("login/", views.login_html, name="login-html"), # logowanie użytkownika
    path("logout/", views.logout_html, name="logout-html"), # wylogowanie użytkownika
    path("order/create/", views.order_create_html, name="order-create"), # tworzenie zamówienia z koszyka
    path("moje-zamowienia/", views.my_orders_html, name="my-orders"), # przeglądanie własnych zamówień
    path("konto/", views.my_profile_html, name="my-profile"), # przeglądanie i edycja profilu klienta
    path("kawy/mocne/", views.strong_coffee_html, name="coffee-strong-html"), # widok mocnych kaw
    path("kawy/szukaj/", views.coffee_starts_with_html, name="coffee-search-html"), # wyszukiwanie kaw po nazwie
]
