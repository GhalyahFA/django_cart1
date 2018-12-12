from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import datetime
from cart.extras import generate_order_id
from art.models import Product, Profile
from cart.models import OrderItem, Order


def get_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order= Order.objects.filter(owner=user_profile, is_ordered=False)
    if order:
        return order[0]
    else:
        messages.info(request, "Your cart is empty!")

@login_required
def add_to_cart(request, **kwargs):
    user_profile= get_object_or_404(Profile, user=request.user)
    product= Product.objects.filter(id=kwargs.get('item_id', "")).first()
    if product in request.user.profile.merchandise.all():
        messages.info(request, 'You already own this product')
    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user_profile,is_ordered=False)
    user_order.items.add(order_item)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
        messages.info(request, 'item added to cart')
    return redirect (reverse('cart:order_summary'))

@login_required
def delete_from_cart(request, item_id):
    item_to_delete= OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, 'Item has been deleted successfully')
    return redirect(reverse('cart:order_summary'))

@login_required
def order_details(request, **kwargs):
    existing_order = get_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'order_summary.html', context)

@login_required
def checkout(request, **kwargs):

    order_to_purchase = get_pending_order(request)
    order_to_purchase.is_ordered= True
    order_to_purchase.save()
    order_to_purchase.date_ordered=datetime.datetime.now()

    order_items= order_to_purchase.items.all()
    order_items.update(is_ordered= True, date_ordered= datetime.datetime.now())

    user_profile= get_object_or_404(Profile, user=request.user)
    order_products = [item.product for item in order_items]
    user_profile.merchandise.add(*order_products)
    user_profile.save()
    messages.info(request, "Thank you for your purhcase!")
    # order_to_purchase.exclude(?????)
    return redirect(reverse('profile'))

    context = {
        'order': order_to_purchase,
        'order_items': order_items,
        'user_profile': user_profile,
    }

    return render(request, 'checkout.html', context)
