from django.contrib import admin
from .models import*
# Register your models here.

class show_customer(admin.ModelAdmin):
    list_display = ['cname','lname']
admin.site.register(customer,show_customer)

class show_product(admin.ModelAdmin):
    product_display=['product_id','name','img','desc','price','category']
admin.site.register(products,show_product)

class show_productdetails(admin.ModelAdmin):
    list_display=['prod_id','prod_name','prod_img','prod_desc','prod_price','prod_category']
admin.site.register(Product_detail,show_productdetails)

class show_cart(admin.ModelAdmin):
    list_display=['prod_id','Product_name','Date_time','Price','cart_img','Final_price','Order_id','Order_status']
admin.site.register(product_cart,show_cart)

class show_register(admin.ModelAdmin):
    list_display=['first_name','last_name','password','cpassword','email','phone']
admin.site.register(Register_table,show_register)


admin.site.register(Checkout)
