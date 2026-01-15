from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer, Producent
from .serializers import CustomerSerializer, ProducentSerializer

# --- CUSTOMER (Osoba) - Klasy APIView (Zadanie 5) ---

class CustomerList(APIView):
    """Lista wszystkich klientów lub dodanie nowego."""
    def get(self, request):
        # Zadanie 3 pkt 3: Filtrowanie po fragmencie nazwiska
        surname_query = request.query_params.get('surname', None)
        if surname_query:
            customers = Customer.objects.filter(surname__icontains=surname_query)
        else:
            customers = Customer.objects.all()
        
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetail(APIView):
    """Pobranie, modyfikacja lub usunięcie pojedynczego klienta."""
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self.get_object(pk)
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = self.get_object(pk)
        if not customer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        if customer:
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


# --- PRODUCENT (Stanowisko) - Widoki funkcyjne (Zadanie 3) ---

@api_view(['GET', 'POST'])
def producent_list(request):
    if request.method == 'GET':
        producenci = Producent.objects.all()
        serializer = ProducentSerializer(producenci, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProducentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def producent_detail(request, pk):
    try:
        producent = Producent.objects.get(pk=pk)
    except Producent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProducentSerializer(producent)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        producent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# --- DODATKOWE IMPORTY DLA LAB 8 ---
from django.shortcuts import render, redirect  # Potrzebne do renderowania szablonów i przekierowań
from django.http import HttpResponse, Http404  # Potrzebne do podstawowych odpowiedzi i błędów
import datetime # Do widoku welcome_view

# 1. Prosty widok powitalny (Listing 1)
def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj w sklepie z kawą! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)

# 2. Widok listy klientów (odpowiednik Osoba) zwracający HTML (Listing 10)
def customer_list_html(request):
    # Pobieramy wszystkie obiekty Customer z bazy poprzez QuerySet
    customers = Customer.objects.all()

    return render(request,
                  "sklep/customer/list.html", # Ścieżka do Twojego szablonu
                  {'customers': customers}) # Przekazanie danych do szablonu

# 3. Widok szczegółów klienta z obsługą błędu 404 i usuwania (Listing 16, 20)
def customer_detail_html(request, id):
    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        raise Http404("Klient o podanym id nie istnieje")

    # Obsługa usuwania metodą POST (Listing 20)
    if request.method == "POST":
        customer.delete()
        return redirect('customer-list-html')

    return render(request,
                  "sklep/customer/detail.html",
                  {'customer': customer})

# 4. Widok dodawania klienta przez formularz HTML (Listing 17)
def customer_create_html(request):
    if request.method == "GET":
        return render(request, "sklep/customer/create.html")
    
    elif request.method == "POST":
        # Pobieranie danych z formularza
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')

        if name and surname and email:
            # Tworzenie nowego obiektu w bazie
            Customer.objects.create(
                name=name,
                surname=surname,
                email=email
            )
            return redirect('customer-list-html')
        else:
            error = "Wszystkie pola są wymagane."
            return render(request, "sklep/customer/create.html", {'error': error})