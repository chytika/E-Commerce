from django.shortcuts import render, HttpResponse
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Address, Wishlist


# Create your views here.
def index(request):
    products = Product.objects.all()

    context = {
        "products":products
    }
    return render(request, 'core/index.html', context)