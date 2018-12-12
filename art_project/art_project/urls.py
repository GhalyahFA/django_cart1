from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from art import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.user_profile, name= 'profile'),
    path('', views.home, name= 'home'),
    path('category/<slug:slug>/', views.product_category, name='category'),
    path('', include('cart.urls', namespace='cart')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
