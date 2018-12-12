from django.urls import path
from cart import views

app_name= 'cart'

urlpatterns=[
path('add-to-cart/<item_id>', views.add_to_cart, name="add_to_cart"),
path('item/delete/<item_id>', views. delete_from_cart, name='delete_item'),
# path('success/', views.success, name='purchase_success'),
path('order_summary/', views.order_details, name='order_summary'),
path('checkout/', views.checkout, name='checkout'),
]
