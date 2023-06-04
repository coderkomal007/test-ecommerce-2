# mainapp/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def _str_(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def _str_(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

# mainapp/views.py
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    # Logic to add product to the cart
    return redirect('cart')

def cart(request):
    # Logic to display the cart with added products
    return render(request, 'cart.html')

# urls.py
from django.urls import path
from mainapp import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
]

# templates/product_list.html
{% for product in products %}
    <h2>{{ product.name }}</h2>
    <p>{{ product.price }}</p>
    <a href="{% url 'product_detail' product.id %}">View Details</a>
    <a href="{% url 'add_to_cart' product.id %}">Add to Cart</a>
{% endfor %}

# templates/product_detail.html
<h2>{{ product.name }}</h2>
<p>{{ product.description }}</p>
<p>{{ product.price }}</p>
<a href="{% url 'add_to_cart' product.id %}">Add to Cart</a>

# templates/cart.html
{% for item in cart_items %}
    <h2>{{ item.product.name }}</h2>
    <p>Quantity: {{ item.quantity }}</p>
    <p>Price: {{ item.product.price }}</p>
{% endfor %}
<p>Total Price: {{ total_price }}</p>

