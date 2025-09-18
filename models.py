from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
class customer(models.Model):
    cname=models.CharField(max_length=20,default="abc")
    lname=models.CharField(max_length=30)

    def __str__(self):
        return self.cname

class products(models.Model):
    product_id=models.IntegerField()
    name=models.CharField(max_length=20) 
    img =models.ImageField(null=True)
    desc = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    category =models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product_detail(models.Model):
    prod_id=models.IntegerField()
    prod_name=models.CharField(max_length=30) 
    prod_img =models.ImageField(null=True)
    prod_desc = models.TextField()
    prod_price = models.FloatField()
    prod_category =models.CharField(max_length=20)

    def __str__(self):
        return self.prod_name

class product_cart(models.Model):
    prod_id = models.ForeignKey(Product_detail, on_delete=models.CASCADE, default="")
    Product_name = models.CharField(max_length=300)
    Date_time = models.DateTimeField(auto_now=True, editable=False)
    Price = models.IntegerField(default=100)
    Quantity = models.IntegerField(default=1)  # ✅ Added for quantity
    cart_img = models.ImageField(null=True)
    Final_price = models.IntegerField()
    Order_id = models.IntegerField(default=0)
    Order_status = models.IntegerField(default=0)

class Register_table(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    password=models.CharField(max_length=40)
    cpassword=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.BigIntegerField()

class Checkout(models.Model):
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=10)  # Allows strings like '0987654321'
    address1 = models.TextField(blank=True)
    address2 = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=6, blank=True)  # Allows leading 0s
    ordernote = models.TextField(blank=True)

    def __str__(self):
        return f"{self.f_name} {self.l_name} - {self.email}"