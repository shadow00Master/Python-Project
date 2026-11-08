from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import Product_Form
from .models import Product

@login_required
def all_Product(request):
    products = Product.objects.filter(user=request.user)
    inventory = products.order_by('category')
    return render(request, 'Inventory/all_Product.html', {
        'inventory': inventory,
    })

@login_required
def add_Product(request):
    if request.method == 'POST':
        form = Product_Form(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('Inventory:all_Product')
    else:
        form = Product_Form()

    return render(request, 'Inventory/add_Product.html', {'form': form})


@login_required
def update_Product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        form = Product_Form(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('Inventory:all_Product')
    else:   
        form = Product_Form(instance=product)
    return render(request, 'Inventory/update_Product.html', {'form': form})


@login_required
def delete_Product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == "POST":
        # form = Product_Form(request.POST)
        # if form.is_valid():
        product.delete()
        return redirect('Inventory:all_Product')
    return redirect('Inventory:all_Product')