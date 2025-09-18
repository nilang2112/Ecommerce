from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('base', views.base, name="base"),
    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login"),
    path('ad_login', views.ad_login, name="ad_login"),
    path('about', views.about, name="about"),
    path('registration_details', views.registration_details, name="registration_Details"),
    path('fetchloginpage', views.fetchloginpage, name="fetchloginpage"),
    path("addtocart", views.addtocart, name="addtocart"),
    path('cart/', views.view_cart, name='cart'),
    path('removeitem/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('payment-success', views.payment_success, name='payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/fetchcheckoutdata/', views.fetchcheckoutdata, name='fetchcheckoutdata'),
    # path('checkout_det/', views.checkout_det, name='checkout_det')
    path('processpayment/', views.processpayment, name='processpayment'),
    path('payment_handler/', views.payment_handler, name='payment_handler'),
    path('success_payment/', views.success_payment, name="success_payment"),
    path('book/', views.booking_view, name='booking_view'),
    path('bill/',views.bill,name='bill'),
    path('logout/', views.logout, name='logout'),
    
]
