import random
import string
from django.shortcuts import render, redirect
from django.urls import reverse

from myproject import settings
from .models import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from django.shortcuts import render
from .models import products

def base(request):
    products_list = Product_detail.objects.all()
    return render(request, "base.html", {"pro_lis": products_list})

def index(request):
    return render(request,"index.html")
def logout(request):
    # Clear specific session variables
    request.session.pop('logid', None)  # Remove 'logid' if it exists
    request.session.pop('logname', None)  # Remove 'logname' if it exists

    return redirect("index")  # Redirect to the index page

def home(request):
    return render(request,"home.html")

def registration(request):
     return render(request,"registration.html")

def login(request):
    return render(request,"login.html")

def ad_login(request):
    return render(request,"ad_login.html")

def about(request):
    return render(request,"about.html")

def cart(request):
    return render(request,"cart.html")

def checkout(request):
    return render(request,"checkout.html")

def fetchloginpage(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            checkuser=Register_table.objects.get(email=email,password=password)
            request.session["logid"]=checkuser.id
            request.session['logname']=checkuser.first_name
        except: checkuser=None
        if checkuser is not None:
            return redirect("base")
        else:
            messages.warning(request,"email or password is not match please try again........")
            return render(request,"login.html")

    return redirect("/")

def registration_details(request):
    first_name=request.POST.get('fname')
    last_name=request.POST.get('lname')
    password=request.POST.get('password')
    cpassword=request.POST.get('cpassword')
    email=request.POST.get('email')
    phone=request.POST.get('phone')
    if Register_table.objects.filter(email=email).exists():
        messages.error(request,"user is already taken")
        return render(request,"registration.html")
    if password != cpassword:
        messages.error(request,"Password is not match...")
        return render(request,"registration.html")
    if phone:
        if int(len(phone))!=10:
            messages.error(request, "Enter Valid 10-digit Mobile Number...")
            return render(request, "registration.html")
    storedata=Register_table(first_name=first_name,last_name=last_name,password=password,cpassword=cpassword,email=email,phone=phone)
    storedata.save()
    return redirect("login")

from django.shortcuts import redirect
from django.contrib import messages
from .models import product_cart, Product_detail

# ✅ UPDATED addtocart view with quantity logic
def addtocart(request):
    if request.method == 'POST':
        #if request.session.is_empty():
         #   messages.error(request, "Please login")
          #  return redirect("index.html")
        if 'logid' not in request.session:
            messages.error(request, "Please login to add products to your cart.")
            return redirect("login")  # Redirect to the login page
        
        cartname = request.POST.get("proname")
        cartprice = request.POST.get("proprice")
        proid = request.POST.get("prod_id")
        proimg1 = request.POST.get("proimg")
        quantity = int(request.POST.get("quantity", 1))  # Get quantity from form, default 1
        
        try:
            product = Product_detail.objects.get(id=proid)
            price = int(float(cartprice))

            # Check if product already in cart
            existing = product_cart.objects.filter(prod_id=product).first()
            if existing:
                existing.Quantity += quantity
                existing.Final_price = existing.Quantity * existing.Price
                existing.save()
            else:
                cartdata = product_cart(
                    prod_id=product,
                    Product_name=cartname,
                    Price=price,
                    Quantity=quantity,
                    Final_price=price * quantity,
                    cart_img=product.prod_img 
                )
                cartdata.save()
            messages.success(request, 'Product is added to Cart.')
        except Exception as e:
            messages.error(request, "Error adding product to cart: " + str(e))
        
        return redirect(request.META.get('HTTP_REFERER'))
    
    messages.error(request, "Invalid request method.")
    return redirect("index.html")

def view_cart(request):
    #if 'logid' not in request.session:
     #       messages.error(request, "Please login to View to your cart.")
      #      return redirect("login")
    if request.session.is_empty():
        messages.error(request, "Please login")
        return redirect("login.html")
    
    cartitems = product_cart.objects.all()  # You may want to filter by user
    total_amount = sum(item.Final_price for item in cartitems)

    return render(request, 'cart.html', {'cartitems': cartitems , 'total_amount': total_amount})

from django.shortcuts import redirect, get_object_or_404

def remove_from_cart(request, product_id):
    if request.session.is_empty():
        messages.error(request, "Please login to remove items from your cart.")
        return redirect("login.html")
    cart_item = get_object_or_404(product_cart, id=product_id)

    cart_item.delete()
    messages.success(request, "Product removed from cart successfully.")

    return redirect('cart')

from django.shortcuts import render

def cart_view(request):
    
    cartitems = request.session.get('cart', [])
    total_amount = sum(item['Final_price'] for item in cartitems)  # Calculate total price

    return render(request, 'cart.html', {
        'cartitems': cartitems,
        'total_amount': total_amount,
    })
        

def update_quantity(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        action = request.POST.get('action')  # 'increase' or 'decrease'

        cart_item = get_object_or_404(product_cart, id=cart_id)

        if action == 'increase':
            cart_item.Quantity += 1
        elif action == 'decrease' and cart_item.Quantity > 1:
            cart_item.Quantity -= 1

        cart_item.Final_price = cart_item.Quantity * cart_item.Price
        cart_item.save()

    return redirect('cart')
#def checkout(request):
 #   if request.method == 'POST':
        # You can implement actual order saving or payment logic here
   #     messages.success(request, "Checkout completed successfully! (Simulated)")
        # Clear the cart after checkout
        #product_cart.objects.all().delete()  # or filter by user if applicable
  #  return redirect('cart')
def payment_success(request):
    payment_id = request.GET.get('payment_id')
    amount=request.GET.get('amount')
    # Handle post-payment logic here (e.g., update order status, send confirmation email)
    return render(request, 'payment_success.html', {'payment_id': payment_id},{'amount': amount})

    #return redirect('booking_view') chang


def checkout(request):
    if request.session.is_empty():
        messages.error(request, "Please login")
        return redirect("login.html")
    
    cartitems = product_cart.objects.all()  # Optionally filter by user/session
    total_amount = float (sum(item.Final_price for item in cartitems))
    with_ship_amt =total_amount + 100
    request.session['amount'] = with_ship_amt
    return render(request, 'checkout.html', {
        'cartitems': cartitems,
        'total_amount': total_amount,
    })

def fetchcheckoutdata(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        city = request.POST.get('city')
        district = request.POST.get('district')
        zipcode = request.POST.get('zipcode')
        message = request.POST.get('message')

        # Create checkout entry (NO user field here)
        checkout = Checkout.objects.create(
            f_name=fname,
            l_name=lname,
            email=email,
            phone=phone,
            address1=add1,
            address2=add2,
            city=city,
            district=district,
            zipcode=zipcode,
            ordernote=message,
        )
        checkout.save()
       
        return redirect('booking_view')  # or redirect to a thank you page
    

    return redirect(checkout)
def process_payment(request):
    return render(request,"process_payment.html")

print("RAZORPAY_KEY:", settings.RAZORPAY_KEY)
print("RAZORPAY_SECRET:", settings.RAZORPAY_SECRET_KEY)
payment_amount=0

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET_KEY))
print(razorpay_client)

def processpayment(request):
    
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET_KEY))
    print(razorpay_client)

    if request.method == 'POST':
        amount = request.session.get('amount')
        
        currency = "INR"
        print(amount)
        payment_capture = 1  # Auto capture
        print("amount",amount)
        order_data = {
            "amount": amount*100,
            "currency": currency,
            "payment_capture": payment_capture
        }
        print(order_data)

        order = razorpay_client.order.create(order_data)
        print(order)
        
        razorpay_order_id = order['id']
        print(razorpay_order_id)
        callback_url = request.build_absolute_uri(reverse('payment_handler'))

        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZORPAY_KEY,
            'razorpay_amount': amount,
            'currency': currency,
            'callback_url': callback_url
        }

        return render(request, 'process_payment.html', context=context)
        # return HttpResponse("Payment processed.")
        
    else:
        return HttpResponseNotAllowed(['POST'])


def success_payment(request):
    return render(request,"payment_success.html")

@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        print("it works")
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            print(payment_id)
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            amount = request.session.get('amount')
          
            signature = request.POST.get('razorpay_signature', '')
            print(payment_id)
            print(razorpay_order_id)
            print(signature)
            print(amount)
            if not payment_id or not razorpay_order_id or not signature:
                print("One or more required parameters are missing.")
                return HttpResponseBadRequest("Missing parameters.")

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            
            print(f"Verification result: {result}")
            
            if result:
                 return render(request, 'payment_success.html',{'order_id':razorpay_order_id,'amount_paid': amount })
            else:
                return HttpResponse("Failed to capture payment.")
        except Exception as e:
            print(f"Error processing payment: {e}")
            return HttpResponseBadRequest("Invalid payment data.")
    else:
        return HttpResponseBadRequest("Invalid request method.")
def booking_view(request):
    return render(request, 'post_redirect.html', {
        'process_payment_url': reverse('processpayment'),})

def bill(request):
    if not request.session.get("logid"):
        messages.error(request, "Please login to view your bill.")
        return redirect("login")

    # Get cart items
    first_name = request.session.get("logname")
    cartitems = product_cart.objects.all()  # Filter by user/session if needed
    total_amount = sum(item.Final_price for item in cartitems)
    with_ship_amt = total_amount + 100
    random_invoice = ''.join(random.choices(string.digits, k=8))

    # Optionally store again in session (useful if user lands here directly)
    request.session['amount'] = with_ship_amt
    request.session['logname']=first_name
    context = {
        'cartitems': cartitems,
        'total_amount': total_amount,
        'with_ship_amt': with_ship_amt,
        'invoice_no': random_invoice,
        'first_name': first_name,
         # type: ignore
    }
    product_cart.objects.all().delete() 

    return render(request, 'bill.html', context)

