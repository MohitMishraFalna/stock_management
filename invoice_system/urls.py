from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="InvoiceSystem"),
    path('checking/', views.checking, name="InvoiceSystem"),
    path('addnewcustomer/', views.addNewCustomer, name="addnewcustomer"),
    path('addnewproduct/', views.addnewproduct, name="addnewproduct"),
    path('ganrateaddress/', views.ganrateaddress, name="ganrateaddress"),
    path('productsearch/', views.productsearch, name="productsearch"),
    path('addtocart/', views.addtocart, name="addtocart"),
    path('productupdate/', views.productupdate, name="productupdate"),
    path('palceOrder/', views.palceOrder, name="palceOrder"),
    path('invoiceprint/', views.invoiceprint, name="invoiceprint"),
    path('ordercancel/', views.ordercancel, name="ordercancel"),
    # path('sentinvoicebymail/', views.sentinvoicebymail, name="sentinvoicebymail"),
    path('ordercancelupdate/', views.ordercancelupdate, name="ordercancelupdate"),
    path('productcancelupdate/', views.productcancelupdate, name="productcancelupdate"),
    path('updateproduct/', views.updateproduct, name="updateproduct"),
    path('newproductinoldid/', views.newproductinoldid, name="newproductinoldid"),
    path('searchcustomerdetails/', views.searchcustomerdetails, name="searchcustomerdetails"),
    path('dueclear/', views.dueclear, name="dueclear"),
    path('updatedue/', views.updatedue, name="updatedue"),
    path('demo/', views.demo, name="demo"),
]