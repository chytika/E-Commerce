from django.db import models
# from enum import unique
# from sys import prefix
# from pyexpat import model
# from pyparsing import alphas
# from email.policy import default
# from unicodedata import decimal
from shortuuid.django_fields import ShortUUIDField 
from django.utils.html import mark_safe
from userauths.models import User


# Create your models here.

STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipping"),
    ("delivered", "Delivered"),
)


STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("reject", "Reject"), 
    ("In_review", "In Review"),
     ("published", "Published"),

)

RATING = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"), 
    (4, "⭐⭐⭐⭐ "),
    (5, "⭐⭐⭐⭐⭐"),

)




def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length= 10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')

    class Meta:
        verbose_name_plural = "Catergories"

    def category_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length= 10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user_directory_path')
    description = models.TextField(null=True, blank=True)

    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    chat_resp_time = models.CharField(max_length=100, default=100)
    shipping_on_time = models.CharField(max_length=100, default=100)
    authentic_rating = models.CharField(max_length=100, default=100)
    days_return = models.CharField(max_length=100, default=100)
    warranty_time = models.CharField(max_length=100, default=100)
    

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
       verbose_name_plural = "Vendors"

    def Vendor_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.image.url))
    
    def __str__(self):
        return self.title
    


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length= 10, max_length=30, prefix="cat", alphabet="abcdefgh12345")

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')
    description = models.TextField(null=True, blank=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=9999999999999, decimal_places=2)
    old_price = models.DecimalField(max_digits=9999999999999, decimal_places=2)


    specifications = models.TextField(null=True, blank=True)
    # tags = models.ForeignKey(User, on_delete=models.CASCADE)
   
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="In_review")


    status = models.BooleanField(default=True)
    In_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length= 10, max_length=30, prefix="sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Products"

    def producct_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def _get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"



################################ Cart, Order, OrderItems and Address ##########################
################################ Cart, Order, OrderItems and Address ##########################
################################ Cart, Order, OrderItems and Address ##########################

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999999, decimal_places=2)
    paid_track = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="Processing")

    class Meta:
        verbose_name_plural = "Cart Orders"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=100)
    product = models.CharField(max_length=200)
    items = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.CharField(max_length=200, default=0)
    price = models.DecimalField(max_digits=9999999999999, decimal_places=2)
    total = models.DecimalField(max_digits=9999999999999, decimal_places=2)


    class Meta:
        verbose_name_plural = "Cart Order Items"


    def order_image(self):
        return mark_safe("<img src='/media/%s' width='50' height='50'/>" % (self.image))
    


################################ product review, wishlists,  and Address ##########################
################################ product review, wishlists,  and Address ##########################
################################ product review, wishlists,  and Address ##########################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"


    # def order_image(self):
    #      return mark_safe("<img src='/media/%s' width='50' height='50'/>" % (self.image))
        
    def __str__(self):
        return self.product.title
    
    def _get_rating(self):
        return self.rating



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlists"

    def __str__(self):
        return self.product.title
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "address"