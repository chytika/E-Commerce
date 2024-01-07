from django.shortcuts import render, HttpResponse
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Address, Wishlist


# Create your views here.
def index(request):
    products = Product.objects.all().order_by("Category_id")
    #  To filter with product status
    # products = Product.objects.filter(product_status ="In_review", featured="True")


    context = {
        "products":products
    }
    return render(request, 'core/index.html', context)




def product_list_view(request):
    products = Product.objects.all()
    #  To filter with product status
     #products = Product.objects.filter(product_status ="In_review", featured="True")


    context = {
        "products":products
    }
    return render(request, 'core/product_list.html', context)



def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories":categories
    }
    return render(request, 'core/category_list.html', context)