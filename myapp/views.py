import csv
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SaleForm, PurchaseForm
from .models import SparePart
from django.shortcuts import render
from django.utils.dateparse import parse_date
from .models import Sale, Purchase
from myapp import models
from django.db.models import Sum

def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'index.html')


@login_required
def home(request):
    query = request.GET.get('q', '').strip()
    if query:
        spare_parts = SparePart.objects.filter(name__icontains=query) | SparePart.objects.filter(part_number__icontains=query)
    else:
        spare_parts = SparePart.objects.all()

    context = {
        'spare_parts': spare_parts,
        'query': query,
    }
    return render(request, 'home.html', context)




def sell_spare_part(request, spare_part_id):
    spare_part = SparePart.objects.get(pk=spare_part_id)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.spare_part = spare_part
            if spare_part.stock >= sale.quantity:
                sale.total_amount = (sale.quantity * sale.selling_price) + sale.tax
                sale.profit =  (sale.quantity * sale.selling_price) - (sale.quantity * spare_part.price) - sale.tax
                sale.save()
                # Update stock
                spare_part.stock -= sale.quantity
                spare_part.save()
                return redirect('home')
            else:
                form.add_error(None, 'Not enough stock available')
    else:
        form = SaleForm()
    return render(request, 'sell_spare_part.html', {'form': form, 'spare_part': spare_part})

def purchase_spare_part(request, spare_part_id):
    spare_part = get_object_or_404(SparePart, id=spare_part_id)
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.spare_part = spare_part
            purchase.total_amount = purchase.quantity * purchase.purchase_price + purchase.tax
            purchase.profit = (purchase.quantity * spare_part.price) - (purchase.quantity * purchase.purchase_price) - purchase.tax
            purchase.save()
            spare_part.stock += purchase.quantity
            spare_part.save()
            return redirect('home')
    else:
        form = PurchaseForm()
    return render(request, 'purchase_spare_part.html', {'form': form, 'spare_part': spare_part})

@login_required
def sales_records(request):
    # Get start and end dates from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Filter sales based on the provided date range
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        sales = Sale.objects.filter(date__range=[start_date, end_date])
    else:
        sales = Sale.objects.all()

    # Calculate the total profit for the filtered sales
    total_profit = sales.aggregate(total_profit=Sum('profit'))['total_profit'] or 0

    context = {
        'sales': sales,
        'total_profit': total_profit,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'sales_records.html', context)



@login_required
def purchases_records(request):
    # Get start and end dates from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Filter purchases based on the provided date range
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        purchases = Purchase.objects.filter(date__range=[start_date, end_date])
    else:
        purchases = Purchase.objects.all()

    # Calculate the total profit for the filtered purchases
    total_profit = purchases.aggregate(total_profit=Sum('profit'))['total_profit'] or 0

    context = {
        'purchases': purchases,
        'total_profit': total_profit,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'purchases_records.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the index page after logout
