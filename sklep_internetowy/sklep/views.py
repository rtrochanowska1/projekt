import datetime
from functools import wraps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import CoffeeTaste, Producent, Coffee, Customer, Order, OrderItem
from .serializers import (
    RegisterSerializer,
    CoffeeTasteSerializer,
    ProducentSerializer,
    CoffeeSerializer,
    CustomerSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from .forms import CoffeeForm, ProducentForm, CoffeeTasteForm, UserProfileForm, CustomerProfileForm
# Widoki API
# Rejestracja użytkownika
@api_view(["POST"])
@permission_classes([AllowAny])
def api_token_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"detail": "Wymagane: username i password."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "Nieprawidłowe dane logowania."}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == "GET":
        return Response({"message": "Wyślij POST: username, password, email, first_name, last_name (opcjonalnie)."})
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        Customer.objects.get_or_create(user=user)
        return Response({"message": "Zarejestrowano pomyślnie"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Widoki dla CoffeeTaste
@api_view(["GET"])
@permission_classes([AllowAny])
def taste_list(request):
    tastes = CoffeeTaste.objects.all()
    return Response(CoffeeTasteSerializer(tastes, many=True).data)

# Tworzenie nowego smaku kawy (tylko admin)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def taste_create(request):
    serializer = CoffeeTasteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Szczegóły smaku kawy
@api_view(["PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def taste_update_delete(request, pk):
    taste = get_object_or_404(CoffeeTaste, pk=pk)

    if request.method == "PUT":
        serializer = CoffeeTasteSerializer(taste, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    taste.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Lista wszystkich producentów
@api_view(["GET"]) 
@permission_classes([AllowAny])
def producent_list(request):
    producenci = Producent.objects.all()
    return Response(ProducentSerializer(producenci, many=True).data)

# Tworzenie nowego producenta (tylko admin)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def producent_create(request):
    serializer = ProducentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Szczegóły producenta
@api_view(["GET"])
@permission_classes([AllowAny])
def producent_detail(request, pk):
    producent = get_object_or_404(Producent, pk=pk)
    return Response(ProducentSerializer(producent).data)

# Aktualizacja i usuwanie producenta (tylko admin)
@api_view(["PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def producent_update_delete(request, pk):
    producent = get_object_or_404(Producent, pk=pk)

    if request.method == "PUT":
        serializer = ProducentSerializer(producent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    producent.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Widoki dla Coffee
# Lista wszystkich kaw
@api_view(["GET"])
@permission_classes([AllowAny])
def coffee_list(request):
    coffees = Coffee.objects.select_related("taste", "producent").all()
    return Response(CoffeeSerializer(coffees, many=True).data)

# Szczegóły kawy
@api_view(["GET"])
@permission_classes([AllowAny])
def coffee_detail(request, pk):
    coffee = get_object_or_404(Coffee.objects.select_related("taste", "producent"), pk=pk)
    return Response(CoffeeSerializer(coffee).data)

# Tworzenie nowej kawy (tylko admin)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def coffee_create(request):
    serializer = CoffeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Szczegóły, aktualizacja i usuwanie kawy
@api_view(["PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def coffee_update_delete(request, pk):
    coffee = get_object_or_404(Coffee, pk=pk)

    if request.method == "PUT":
        serializer = CoffeeSerializer(coffee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    coffee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#mocne kawy
@api_view(["GET"])
@permission_classes([AllowAny])
def strong_coffee_list(request):
    coffees = Coffee.objects.select_related("taste", "producent").filter(taste__coffee_strength__gte=4)
    return Response(CoffeeSerializer(coffees, many=True).data)


#kawy, których nazwa zaczyna się od danego początku
@api_view(["GET"])
@permission_classes([AllowAny])
def coffee_starts_with(request, prefix):
    prefix = (prefix or "").strip()
    if not prefix:
        return Response({"detail": "Przedrostek nie może być pusty."}, status=status.HTTP_400_BAD_REQUEST)

    coffees = Coffee.objects.select_related("taste", "producent").filter(name__istartswith=prefix)
    return Response(CoffeeSerializer(coffees, many=True).data)


# Widoki dla Order i OrderItem
# Lista i tworzenie zamówień
@api_view(["GET", "PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_customer_profile(request):
    customer, _ = Customer.objects.get_or_create(user=request.user)

    if request.method == "GET":
        return Response(CustomerSerializer(customer).data)

    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lista i tworzenie zamówień
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    customer, _ = Customer.objects.get_or_create(user=request.user)

    if request.method == "GET":
        orders = Order.objects.filter(customer=customer).prefetch_related("items")
        return Response(OrderSerializer(orders, many=True).data)

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Szczegóły i usuwanie zamówienia
@api_view(["GET", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_detail_delete(request, pk):
    customer, _ = Customer.objects.get_or_create(user=request.user)
    order = get_object_or_404(Order, pk=pk, customer=customer)

    if request.method == "GET":
        return Response(OrderSerializer(order).data)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Dodawanie pozycji do zamówienia
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_item_add(request):
    customer, _ = Customer.objects.get_or_create(user=request.user)

    serializer = OrderItemSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    order = serializer.validated_data["order"]
    if order.customer_id != customer.id:
        return Response({"detail": "Nie możesz dodawać pozycji do cudzego zamówienia."},
                        status=status.HTTP_403_FORBIDDEN)

    coffee = serializer.validated_data["coffee"]
    serializer.save(price_at_order=coffee.price)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# Widoki dla HTML

# mocne kawy
def strong_coffee_html(request):
    coffees = (
        Coffee.objects
        .select_related("taste", "producent")
        .filter(taste__coffee_strength__gte=4)
    )
    return render(
        request,
        "sklep/coffee/strong.html",
        {"coffees": coffees},
    )

# kawy z nazwą zaczynającą się od podanego ciągu
def coffee_starts_with_html(request):
    prefix = request.GET.get("q", "").strip()
    coffees = []

    if prefix:
        coffees = (
            Coffee.objects
            .select_related("taste", "producent")
            .filter(name__istartswith=prefix)
        )

    return render(
        request,
        "sklep/coffee/search.html",
        {"coffees": coffees, "prefix": prefix},
    )

# Strona główna sklepu z listą kaw
def coffee_shop_view(request):
    coffees = Coffee.objects.select_related("taste", "producent").all()
    return render(request, "sklep/coffee/shop.html", {"coffees": coffees})

# Szczegóły kawy
def coffee_detail_html(request, id):
    coffee = get_object_or_404(Coffee.objects.select_related("taste", "producent"), id=id)
    return render(request, "sklep/coffee/detail.html", {"coffee": coffee})

# Obsługa koszyka zakupów w sesji
def _get_cart(session):
    cart = session.get("cart")
    if cart is None:
        cart = {}
        session["cart"] = cart
    return cart

# Wyświetlanie zawartości koszyka
def cart_detail_html(request):
    cart = _get_cart(request.session)

    ids = [int(k) for k in cart.keys()]
    coffees = Coffee.objects.filter(id__in=ids)
    coffee_map = {c.id: c for c in coffees}

    items = []
    total = 0
    for coffee_id_str, qty in cart.items():
        coffee_id = int(coffee_id_str)
        coffee = coffee_map.get(coffee_id)
        if not coffee:
            continue
        line_total = coffee.price * qty
        total += line_total
        items.append({"coffee": coffee, "qty": qty, "line_total": line_total})

    return render(request, "sklep/cart/detail.html", {"items": items, "total": total})

# Dodawanie kawy do koszyka
def cart_add_html(request, coffee_id):
    if request.method != "POST":
        raise Http404()

    coffee = get_object_or_404(Coffee, id=coffee_id)
    cart = _get_cart(request.session)

    key = str(coffee.id)
    cart[key] = cart.get(key, 0) + 1
    request.session.modified = True

    return redirect("cart-detail")

# Usuwanie kawy z koszyka
def cart_remove_html(request, coffee_id):
    if request.method != "POST":
        raise Http404()

    cart = _get_cart(request.session)
    key = str(coffee_id)

    if key in cart:
        del cart[key]
        request.session.modified = True

    return redirect("cart-detail")

# Czyszczenie koszyka
def cart_clear_html(request):
    if request.method != "POST":
        raise Http404()

    request.session["cart"] = {}
    request.session.modified = True
    return redirect("cart-detail")

# Rejestracja użytkownika
def register_html(request):
    if request.method == "GET":
        return render(request, "sklep/auth/register.html")

    data = {
        "username": request.POST.get("username"),
        "password": request.POST.get("password"),
        "email": request.POST.get("email"),
        "first_name": request.POST.get("first_name"),
        "last_name": request.POST.get("last_name"),
    }
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        Customer.objects.get_or_create(user=user)
        return redirect("login-html")

    return render(request, "sklep/auth/register.html", {"errors": serializer.errors})

# Logowanie użytkownika
def login_html(request):
    if request.method == "GET":
        return render(request, "sklep/auth/login.html")

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, "sklep/auth/login.html", {"error": "Nieprawidłowe dane logowania."})

    login(request, user)
    Customer.objects.get_or_create(user=user)
    return redirect("sklep-home")

# Wylo#gowanie użytkownika
def logout_html(request):
    logout(request)
    return redirect("sklep-home")

# Tworzenie zamówienia z zawartości koszyka
@login_required
def order_create_html(request):
    if request.method != "POST":
        raise Http404()

    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Koszyk jest pusty.")
        return redirect("cart-detail")

    customer, _ = Customer.objects.get_or_create(user=request.user)
    order = Order.objects.create(customer=customer)

    coffee_ids = [int(k) for k in cart.keys()]
    coffees = Coffee.objects.filter(id__in=coffee_ids)
    coffee_map = {c.id: c for c in coffees}

    for coffee_id_str, qty in cart.items():
        coffee = coffee_map.get(int(coffee_id_str))
        if not coffee:
            continue

        OrderItem.objects.create(
            order=order,
            coffee=coffee,
            quantity=qty,
            price_at_order=coffee.price,
        )

    request.session["cart"] = {}
    request.session.modified = True

    messages.success(request, f"Zamówienie nr {order.id} zostało złożone.")
    return redirect("sklep-home")


#widoki tylko dla zalogowanych uzytkownikow- admin ich nie widzi
# Przeglądanie własnych zamówień (tylko zalogowani)
@login_required
def my_orders_html(request):
    if request.user.is_staff:
        raise PermissionDenied()
    customer, _ = Customer.objects.get_or_create(user=request.user)

    orders = (
        Order.objects
        .filter(customer=customer)
        .prefetch_related("items__coffee")
        .order_by("-date_ordered")
    )

    return render(request, "sklep/order/my_orders.html", {"orders": orders})

# Przeglądanie i edycja profilu klienta (tylko zalogowani)
@login_required
def my_profile_html(request):
    if request.user.is_staff:
        raise PermissionDenied()
    customer, _ = Customer.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        customer_form = CustomerProfileForm(request.POST, instance=customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, "Profil został zaktualizowany.")
            return redirect("my-profile")
    else:
        user_form = UserProfileForm(instance=request.user)
        customer_form = CustomerProfileForm(instance=customer)
    return render(request, "sklep/customer/my_profile.html", {
        "user_form": user_form,
        "customer_form": customer_form,
    })


#tylko dla admina, uztkownik nie ma do tego dostepu
#dodawanie kawy przez admina (HTML)
@staff_member_required
def coffee_create_admin(request):

    if request.method == "POST":
        form = CoffeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sklep-home")
    else:
        form = CoffeeForm()

    return render(request, "sklep/admin/coffee_create.html", {"form": form})


#przegląd zamówień przez admina
@staff_member_required
def admin_orders_overview(request):
    # zamówienia z klientem i userem + pozycje i kawy w pozycjach
    orders = (
        Order.objects
        .select_related("customer__user")
        .prefetch_related("items__coffee")
        .order_by("-date_ordered")
    )

    # Grupowanie: customer_id -> lista zamówień
    grouped = {}
    for o in orders:
        grouped.setdefault(o.customer_id, []).append(o)

    customers = (
        Customer.objects
        .select_related("user")
        .filter(id__in=grouped.keys())
        .order_by("user__username")
    )

    # lista struktur gotowych do template
    data = []
    for c in customers:
        data.append({
            "customer": c,
            "orders": grouped.get(c.id, []),
        })

    return render(request, "sklep/admin/orders_view.html", {"data": data})

@staff_member_required
def producent_create_admin(request):
    if request.method == "POST":
        form = ProducentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sklep-home")
    else:
        form = ProducentForm()
    return render(request, "sklep/admin/producent_create.html", {"form": form})

@staff_member_required
def taste_create_admin(request):
    if request.method == "POST":
        form = CoffeeTasteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sklep-home")
    else:
        form = CoffeeTasteForm()
    return render(request, "sklep/admin/taste_create.html", {"form": form})