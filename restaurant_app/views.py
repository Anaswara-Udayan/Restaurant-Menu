from django.shortcuts import render,redirect
from django.urls import reverse
from . models import MenuItem,OrderItem
from . forms import OrderForm
from django.utils.crypto import get_random_string


# Create your views here.

def index(request):
    return render(request,'index.html')


def menu_view(request):
    print(request,'menu')
    menu_items = MenuItem.objects.all()
    # Handle form submission
    if request.method == 'POST':
        order_items = []
        # Iterate through form data to extract items
        for key, value in request.POST.items():
            if key.startswith('form-') and '-name' in key:
                index = key.split('-')[1]
                name = value
                quantity_key = f'form-{index}-quantity'
                quantity = request.POST.get(quantity_key, '0')
                price_key = f'form-{index}-price'
                price = request.POST.get(price_key, '0')

                order_item = {
                    'name': name,
                    'quantity': quantity,
                    'price': float(price)*float(quantity)
                }
                if int(quantity) > 0:
                    order_items.append(order_item)
        request.session['order_items'] = order_items
        return redirect(reverse('order'))

    # Render menu template with menu items
    return render(request, 'menu.html', {'menu_items': menu_items})


def order_view(request):
    # Read-only data from session
    order_items = request.session.get('order_items', [])
    subtotal = 0
    for item in order_items:
        subtotal+=float(item['price'])

    # Input data
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Generate unique order number
            order_no = get_random_string(length=10)
            
            # Save order and order items to database
            order = form.save(commit=False)
            order.order_no = order_no
            order.subtotal = subtotal
            order.save()

            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item_name=item['name'],
                    menu_item_quantity=item['quantity'],
                    item_amount=item['price'],
                )

            # Clear session data after saving to database
            request.session['order_items'] = []

            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'order.html', {'order_items': order_items, 'form': form,'subtotal':subtotal})

def order_success_view(request):
    return render(request, 'order_success.html')