from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from .models import Customer, Producent, COUNTRY, Coffee, CoffeeTaste
from .serializers import CustomerSerializer, ProducentSerializer

class CustomerList(APIView):
    def get(self, request):
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


def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użytkowniku! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)


def customer_list_html(request):
    surname_query = request.GET.get('nazwisko') 
    if surname_query:
        customers = Customer.objects.filter(surname__icontains=surname_query)
    else:
        customers = Customer.objects.all()
    return render(request, "sklep/customer/list.html", {'customers': customers})

def customer_detail_html(request, id):
    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        raise Http404("Klient nie istnieje")
    
    if request.method == "POST": 
        customer.delete()
        return redirect('customer-list-html')
        
    return render(request, "sklep/customer/detail.html", {'customer': customer})

def customer_create_html(request):
    if request.method == "POST":
        name = request.POST.get('imie')
        surname = request.POST.get('nazwisko')
        email = request.POST.get('email')
        if name and surname:
            Customer.objects.create(name=name, surname=surname, email=email)
            return redirect('customer-list-html')
    return render(request, "sklep/customer/create.html")

def customer_update_html(request, id):
    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        raise Http404("Klient nie istnieje")

    if request.method == "POST":
        customer.name = request.POST.get('imie')
        customer.surname = request.POST.get('nazwisko')
        customer.email = request.POST.get('email')
        customer.save()
        return redirect('customer-detail-html', id=customer.id)

    return render(request, "sklep/customer/update.html", {'customer': customer})


def producent_list_html(request):
    producenci = Producent.objects.all()
    return render(request, "sklep/producent/list.html", {'producenci': producenci})

def producent_detail_html(request, id):
    try:
        producent = Producent.objects.get(id=id)
    except Producent.DoesNotExist:
        raise Http404("Producent nie istnieje")
    
    if request.method == "POST":
        producent.delete()
        return redirect('producent-list-html')

    return render(request, "sklep/producent/detail.html", {'producent': producent})

from .models import Producent, COUNTRY

def producent_create_html(request):
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        country_from_form = request.POST.get('country')
        
        if name_from_form and country_from_form:
            Producent.objects.create(
                name=name_from_form, 
                country=country_from_form
            )
            return redirect('coffee-list-html')
            
    return render(request, "sklep/coffee/create.html", {'countries': COUNTRY})


def coffee_list_html(request):
    coffees = Coffee.objects.all()
    return render(request, "sklep/coffee/list.html", {'coffees': coffees})

def coffee_detail_html(request, id):
    try:
        coffee = Coffee.objects.get(id=id)
    except Coffee.DoesNotExist:
        raise Http404("Kawa nie istnieje")
    
    if request.method == "POST":
        coffee.delete()
        return redirect('coffee-list-html')
        
    return render(request, "sklep/coffee/detail.html", {'coffee': coffee})

def coffee_create_html(request):
    tastes = CoffeeTaste.objects.all()
    producenci = Producent.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        c_type = request.POST.get('type')
        price = request.POST.get('price')
        taste_id = request.POST.get('taste')
        producent_id = request.POST.get('producent')

        if name and price:
            new_coffee = Coffee(
                name=name,
                type=c_type,
                price=price
            )
            if taste_id:
                new_coffee.taste = CoffeeTaste.objects.get(id=taste_id)
            if producent_id:
                new_coffee.producent = Producent.objects.get(id=producent_id)
            
            new_coffee.save()
            return redirect('coffee-list-html')

    return render(request, "sklep/coffee/create.html", {
        'tastes': tastes,
        'producenci': producenci,
        'types': Coffee.COFFEE_TYPES 
    })

def coffee_shop_view(request):
    """Widok dla klientów - tylko przeglądanie i koszyk"""
    coffees = Coffee.objects.all()
    return render(request, "sklep/coffee/shop.html", {'coffees': coffees})

def sklep_home(request):
    kawy = Coffee.objects.all()
    return render(request, "sklep/coffee/shop.html", {'coffees': kawy})
