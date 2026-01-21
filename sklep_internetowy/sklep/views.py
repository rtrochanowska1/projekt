from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from .models import Customer, Producent, Coffee
from .serializers import CustomerSerializer, ProducentSerializer, UserSerializer, CoffeeSerializer


# Widoki API

@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) # każdy może się zarejestrować
def register_user(request): # rejestracja nowego użytkownika przez api
    if request.method == 'GET':
        return Response({"message": "Prześlij dane metodą POST (username, password, email), aby się zarejestrować."})
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Zarejestrowano pomyślnie"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def strong_coffee_list(request):
    """Filtrowanie kaw o mocy >= 4"""
    kawy = Coffee.objects.filter(taste__coffee_strength__gte=4)
    serializer = CoffeeSerializer(kawy, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def producent_list(request):
    """Zarządzanie listą producentów."""
    if request.method == 'GET':
        producenci = Producent.objects.all()
        serializer = ProducentSerializer(producenci, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"detail": "Musisz być zalogowany."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ProducentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) # wymagany token dla wszystkich akcji
def producent_detail(request, pk):
    """Szczegóły, edycja i usuwanie producenta"""
    try:
        producent = Producent.objects.get(pk=pk)
    except Producent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProducentSerializer(producent)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProducentSerializer(producent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_staff: # tylko admin
            return Response({"detail": "Tylko admin może usuwać producentów."}, status=status.HTTP_403_FORBIDDEN)
        producent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # admin widzi wszystkich, user tylko swoich
        customers = Customer.objects.all() if request.user.is_staff else Customer.objects.filter(wlasciciel=request.user)
        surname_query = request.query_params.get('surname', None)
        if surname_query:
            customers = customers.filter(surname__icontains=surname_query)    
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Dodawanie nowego klienta i przypisywanie go do zalogowanego użytkownika."""
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciciel=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetail(APIView):
    """Obsługa konkretnego klienta."""
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            if user.is_staff:
                return Customer.objects.get(pk=pk)
            return Customer.objects.get(pk=pk, wlasciciel=user)
        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self.get_object(pk, request.user)
        if not customer: return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = self.get_object(pk, request.user)
        if not customer: return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk, request.user)
        if not customer: return Response(status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Widoki dla HTML

def welcome_view(request):
    now = datetime.datetime.now()
    return HttpResponse(f"<html><body>Witaj w naszym sklepie! Czas: {now}</body></html>")

def coffee_shop_view(request):
    """Widok główny sklepu"""
    coffees = Coffee.objects.all()
    return render(request, "sklep/coffee/shop.html", {'coffees': coffees}) # wyswietla kawy

def coffee_detail_html(request, id):
    try:
        coffee = Coffee.objects.get(id=id)
    except Coffee.DoesNotExist:
        raise Http404("Kawa nie istnieje")
    return render(request, "sklep/coffee/detail.html", {'coffee': coffee})

def customer_list_html(request):
    """Lista klientów"""
    customers = Customer.objects.all()
    return render(request, "sklep/customer/list.html", {'customers': customers})

def customer_detail_html(request, id):
    """Informacje i usuwanie klienta"""
    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        raise Http404("Klient nie istnieje")
    if request.method == "POST": 
        customer.delete()
        return redirect('customer-list-html')
    return render(request, "sklep/customer/detail.html", {'customer': customer})

def customer_create_html(request):
    """Dodawanie klienta."""
    if request.method == "POST":
        name = request.POST.get('imie')
        surname = request.POST.get('nazwisko')
        email = request.POST.get('email')
        if name and surname:
            Customer.objects.create(name=name, surname=surname, email=email)
            return redirect('customer-list-html')
    return render(request, "sklep/customer/create.html")
