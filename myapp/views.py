from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SaleForm, PurchaseForm
from .models import SparePart

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
    query = request.GET.get('q')
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
def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the index page after logout
