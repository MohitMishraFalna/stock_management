from django.forms import EmailInput
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.template.loader import render_to_string, get_template
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.template import Context
from django.shortcuts import render
from django.db.models import Q  
from xhtml2pdf import pisa 
from .models import *
import requests 
import json 
import os

# Create your views here.
def index(request):
    return render(request, 'invoice_system/home.html')

def checking(request):
    if request.method=="GET":
        # get the value from jquery ajax.
        cn = request.GET.get('cust_name')
    try:
        # if the variable is not empty then retrieve the data from database table
        if cn != '':
            # retrieve data from database table
            # exist = Customer.objects.filter(Q(customer_name__iexact=cn) & Q(customer_contact__iexact=cc) | Q(customer_email__iexact=cc))
            exist = Customer.objects.filter(Q(customer_name__istartswith=cn))
            # create a empty list and append letter
            customer_details = []
            # run the loop and retrieve the item one by one.
            for item in exist:
                # retrive the item and append in customer_details = [] list.
                customer_details.append({'customer_name':item.customer_name, 'customer_contact':item.customer_contact, 'customer_email':item.customer_email, 'customer_due':item.due_amt})
                # the value convert in json and append in response variable.
                response = json.dumps(customer_details, default=str)
                # send the responst in jquery ajax.
            return HttpResponse(response)
    except Exception as e:
            return HttpResponse('{e}')
    return render(request, 'invoice_system/home.html')    

def addNewCustomer(request):
    #if method is get then condition is true and controller check the further line
    if request.method == "GET":
        #this line catch the json from the javascript ajax.
        cust_info = request.GET.get("customerinfo")
        #fill the value in variable which is coming from ajax.
        #it is a json so first we will get the value from using json.loads method.
        #cust_name is a key which is pass by javascript json. 
        #as we know json is a key value pair. the cust_name is a key which pass by javascript json
        cust_name = json.loads(cust_info)['cust_name'].title()
        cust_cont = json.loads(cust_info)['cust_cont']
        cust_email = json.loads(cust_info)['cust_email']
        cust_gender = json.loads(cust_info)['cust_gender'].title()
        cust_cityname = json.loads(cust_info)['cust_cityname']
        cust_dis = json.loads(cust_info)['cust_distrcit']
        cust_pincode = json.loads(cust_info)['cust_pincode']
        cust_state = json.loads(cust_info)['cust_state']
        cust_contry = json.loads(cust_info)['cust_contry']
        cust_due = 0
        try:
            if cust_name != '' and cust_cont != '' and cust_email != '' and cust_gender != '' and cust_cityname != '' and cust_dis != '' and cust_pincode != '' and cust_state != '' and cust_contry != '' and cust_due != '':
                new_customer = Customer(customer_name=cust_name, customer_contact=cust_cont, customer_email=cust_email, gender=cust_gender, city_name=cust_cityname, pincode=cust_pincode, district=cust_dis, state_name=cust_state, contry_name=cust_contry, due_amt=cust_due)
                new_customer.save()
                return HttpResponse("New Customer is Created.")
        except Exception as e:
            return HttpResponse(f"exception is {e}")
        return render(request, 'invoice_system/home.html')

def addnewproduct(request):
    if request.method=="GET":
        #this line catch the json from the javascript ajax.
        product_info = request.GET.get('productinfo')
        #fill the value in variable which is coming from ajax.
        #it is a json so first we will get the value from using json.loads method.
        #cust_name is a key which is pass by javascript json. 
        #as we know json is a key value pair. the cust_name is a key which pass by javascript json.
        prod_name = json.loads(product_info)['prod_name'].title()
        prod_qty1 = json.loads(product_info)['prod_qty1']
        prod_price = json.loads(product_info)['prod_price']
        prod_discount = json.loads(product_info)['prod_dis'].title()
        try:
            if prod_name != '' and prod_qty1 != '' and prod_price != '' and prod_discount != '':
                addnewproduct_save = Products(product_name=prod_name, product_qty=prod_qty1, product_price=prod_price, product_discount=prod_discount)
                addnewproduct_save.save()
                return HttpResponse("Your Stock Room is Add one Product.")
        except Exception as e:
            return HttpResponse(f"exception is {e}")
    return render(request, 'invoice_system/home.html')

def ganrateaddress(request):
    if request.method == "GET":
        pincode = request.GET.get("addressinfo")
        try:
            # addres ="http://postalpincode.in/api/postoffice/"+pincode
            addres = "http://postalpincode.in/api/pincode/"+pincode
            addr = requests.get(addres)
            return HttpResponse(addr)
        except Exception as e:
            print(e)
            return HttpResponse(f"exception is {e}")
    return render(request, 'invoice_system/home.html')

def productsearch(request):
    if request.method=="GET":
        # get the value from jquery ajax.
        search_prod = request.GET.get("mysearchitem")
        dynamic_search_prod = request.GET.get("searchProductName")
        # if the variable is not empty then retrieve the data from database table
        try:                
            if search_prod != '' or dynamic_search_prod != '':
                # create a empty list and append letter
                search_item = []
                # retrieve data from database table
                match = Products.objects.filter(Q(product_name__icontains=search_prod) or Q(product_name__icontains=dynamic_search_prod))
                print(match)
                if match:
                    # run the loop and retrieve the item one by one.
                    for ma in match:
                        # retrive the item and append in search_item = [] list.
                        search_item.append({'product_name':ma.product_name, 'product_qty':ma.product_qty,'product_price':ma.product_price})
                        # the value convert in json and append in response variable.
                        response = json.dumps(search_item, default=str)
                        # send the responst in jquery ajax.
                    print(response)
                    return HttpResponse(response)
                else:
                    return HttpResponse('')
        except Exception as e:
            pass
    return render(request, 'invoice_system/home.html')

# This method using get query and send the data in clint side. this process retrieve the single record.
def addtocart(request):
    if request.method == "GET":
        add_item = request.GET.get('pr_name')
        dynamic_add_item = request.GET.get('dynamic_addproduct_name')
        print(dynamic_add_item)
        try:
            if add_item != '':
                result = Products.objects.get(product_name=add_item)
                response_dict = {'product_name':result.product_name, 'product_qty':result.product_qty, 'product_price':result.product_price, 'product_discount':result.product_discount}
                response = json.dumps(response_dict, default=str)
                return HttpResponse(response)
            else:
                result = Products.objects.get(product_name=dynamic_add_item)
                response_dict = {'product_name':result.product_name, 'product_qty':result.product_qty, 'product_price':result.product_price, 'product_discount':result.product_discount}
                response = json.dumps(response_dict, default=str)
                return HttpResponse(response)
        except Exception as e:
            print(f'{e}')
    return render(request, 'invoice_system/home.html')

def productupdate(request):
    if request.method=='GET':
        prod_name = request.GET.get('prod_name')
        prod_qty = request.GET.get('prod_qty')
        try:
            result0 = Products.objects.get(product_name=prod_name)
            db_prod_qty = {'db_prod_qty':result0.product_qty}
            take_prod_qty = db_prod_qty['db_prod_qty']
            add_prod_qty = take_prod_qty + int(prod_qty)
            result = Products.objects.filter(product_name=prod_name).update(product_qty=add_prod_qty)
        except Exception as e:
            return HttpResponse("{}")
        return HttpResponse("Your Stock Inventory Updated from "+prod_qty)

def palceOrder(request):
    if request.method == 'GET':
        # get id from Customer table.
        customer_email = request.GET.get('customer_email')
        # insert the record in orders table.
        total_amt = request.GET.get('total_amt')
        paid_amt = request.GET.get('paid_amt')
        due_amt = request.GET.get('due_amt')
        cash_discount = request.GET.get('cash_discount')
        order_status = request.GET.get('order_status').title()
        # insert the record in ProductOrder table.
        prod_name = request.GET.getlist('prod_name[]')
        prod_qty = request.GET.getlist('prod_qty[]')
        paidableamt = request.GET.getlist('paidableamt[]')

        try:
            result = Customer.objects.get(customer_email=customer_email)
            get_id = {"customer_id":result.customer_id}
            get_due = {"cust_due":result.due_amt}
            cust_id = get_id['customer_id']
            cust_due = get_due['cust_due']
            if paid_amt != '' and total_amt != '' and cash_discount != '' and due_amt != '' and cust_id != '' and order_status != '':
                place_order = Orders(paid_amt=paid_amt, total_amt=total_amt, cash_discount=cash_discount, due_amt=due_amt, customer_id=cust_id, order_status=order_status)
                place_order.save()
            
            result1 = Orders.objects.latest('order_no')
            get_orderNo = {"orderno":result1.order_no}
            get_orderDue = {"order_due":result1.due_amt}
            orderNo = get_orderNo['orderno']
            order_due = get_orderDue['order_due']

            for i in range(0, len(prod_name)):
                prodname_res = Products.objects.get(product_name=prod_name[i])
                get_prod_id = {'product_id':prodname_res.product_id}
                get_prod_name = {'product_name':prodname_res.product_name}
                get_prod_qty = {'product_qty':prodname_res.product_qty}
                prod_id = get_prod_id['product_id']
                db_prod_name = get_prod_name['product_name']
                db_prod_qty = get_prod_qty['product_qty']
                if orderNo != '' and paidableamt != '' and prod_id != '' and prod_qty != '' and db_prod_qty != '':
                    recordinsertmiddletable = ProductOrder(order_qty=prod_qty[i], paidable_amount=paidableamt[i], order_id=orderNo, product_id=prod_id, product_status='Completed')
                    recordinsertmiddletable.save()
                    sub_prod_qty = db_prod_qty - int(prod_qty[i])
                    change_db = Products.objects.filter(product_name=db_prod_name).update(product_qty=sub_prod_qty)
                # if i == len(prod_name):
                    update_custDue = cust_due + order_due
                    updateCustomerDue = Customer.objects.filter(customer_email=customer_email).update(due_amt=update_custDue)
            return HttpResponse()
        except Exception as e:
            print(e)
            return HttpResponse("{e}")
    # return HttpResponse("This is Place Order Page.")
    return render(request, 'invoice_system/invoiceprint.html')

def invoiceprint(request):
    # if request.method == 'GET':
    cancelorderno = request.GET.get('orderNo')
    print(f'invoiceprint {cancelorderno}')
    if cancelorderno:
        # get_orderNo = {"orderno":result1.order_no}
        # orderNo = get_orderNo['orderno']
        printeditem = []
        printeditemsecond = []
        if cancelorderno != '':
            try:
                outputprint = ProductOrder.objects.select_related('order').filter(order_id=cancelorderno)       
                for output in outputprint:
                    printeditem.append({'customertable_customer_name':output.order.customer.customer_name, 'customertable_customer_contact':output.order.customer.customer_contact,
                        'customertable_customer_email':output.order.customer.customer_email, 'customertable_gender':output.order.customer.gender,
                        'customertable_city_name':output.order.customer.city_name, 'customertable_pincode':output.order.customer.pincode,
                        'customertable_district':output.order.customer.district, 'customertable_state_name':output.order.customer.state_name,
                        'customertable_contry_name':output.order.customer.contry_name, 'customertable_due_amt':output.order.customer.due_amt,
                
                        'ordertable_orderNo':output.order.order_no, 'ordertable_order_date':output.order.order_date, 
                        'ordertable_paid_amt':output.order.paid_amt, 'ordertable_cash_discount':output.order.cash_discount,
                        'ordertable_due_amt':output.order.due_amt, 'ordertable_total_amt':output.order.total_amt,
                        'ordertable_order_status':output.order.order_status,
                    })
                    break
                for outputsecond in outputprint:
                    printeditemsecond.append({'producttable_product_name':outputsecond.product.product_name, 'producttable_product_price':outputsecond.product.product_price,
                        'producttable_product_discount':outputsecond.product.product_discount,

                        'prodordertable_qty':outputsecond.order_qty, 'prodordertable_paidable':outputsecond.paidable_amount 
                    })
                context = {'print':printeditem, 'printsecond':printeditemsecond}
                # sentinvoicebymail(context) 
                print(context)
            except Exception as e:
                return HttpResponse(f'{e}')
    
    else:
        result1 = Orders.objects.latest('order_no')
        get_orderNo = {"orderno":result1.order_no}
        orderNo = get_orderNo['orderno']
        # print(orderNo)
        printeditem = []
        printeditemsecond = []
        if orderNo != '':
            try:
                outputprint = ProductOrder.objects.select_related('order').filter(order_id=orderNo)       
                for output in outputprint:
                    printeditem.append({'customertable_customer_name':output.order.customer.customer_name, 'customertable_customer_contact':output.order.customer.customer_contact,
                        'customertable_customer_email':output.order.customer.customer_email, 'customertable_gender':output.order.customer.gender,
                        'customertable_city_name':output.order.customer.city_name, 'customertable_pincode':output.order.customer.pincode,
                        'customertable_district':output.order.customer.district, 'customertable_state_name':output.order.customer.state_name,
                        'customertable_contry_name':output.order.customer.contry_name, 'customertable_due_amt':output.order.customer.due_amt,
                
                        'ordertable_orderNo':output.order.order_no, 'ordertable_order_date':output.order.order_date, 
                        'ordertable_paid_amt':output.order.paid_amt, 'ordertable_cash_discount':output.order.cash_discount,
                        'ordertable_due_amt':output.order.due_amt, 'ordertable_total_amt':output.order.total_amt,
                        'ordertable_order_status':output.order.order_status,
                    })
                    break
                # print(printeditem)
                for outputsecond in outputprint:
                    printeditemsecond.append({'producttable_product_name':outputsecond.product.product_name, 'producttable_product_price':outputsecond.product.product_price,
                        'producttable_product_discount':outputsecond.product.product_discount,

                        'prodordertable_qty':outputsecond.order_qty, 'prodordertable_paidable':outputsecond.paidable_amount 
                    })
                context = {'print':printeditem, 'printsecond':printeditemsecond}
                # sentinvoicebymail(context) 
            except Exception as e:
                return HttpResponse(f'{e}')
    return render(request, 'invoice_system/invoiceprint.html', context)
    
def ordercancel(request):
    if request.method=='GET':
        order_cancel=request.GET.get('ordercancel')
        email_cancel=request.GET.get('emailcancel')
        try:
            product_name_update=request.GET.getlist('prdnameemail[]')
            if order_cancel != '':
                outputprint = ProductOrder.objects.select_related('order').filter(order_id=order_cancel)       
                for output in outputprint:
                    cstm_due = output.order.customer.due_amt
                    ord_order_no = output.order.order_no
                    ord_due = output.order.due_amt
                    ord_status = output.order.order_status
                    if ord_status != 'Cancel':
                        update_custDue = cstm_due - ord_due
                        updateCustomerDue = Customer.objects.filter(customer_email=email_cancel).update(due_amt=update_custDue)
                    break
                i = 0
                for outputsecond in outputprint:
                    prdt_name = outputsecond.product.product_name
                    prdt_qty = outputsecond.product.product_qty
                    prdt_price = outputsecond.product.product_price
                    prdt_disc = outputsecond.product.product_discount
                    prdord_qty = outputsecond.order_qty 
                    if ord_status != 'Cancel':
                        add_prod_qty = prdt_qty + prdord_qty
                        updateproductqty = Products.objects.filter(product_name=product_name_update[i]).update(product_qty=add_prod_qty)
                        deleteProductOrdercancelrecord=ProductOrder.objects.filter(order_id=order_cancel).update(product_status='Cancel')
                    i = i+1

                updateorderstatus = Orders.objects.filter(order_no=order_cancel).update(order_status='Cancel')
                return HttpResponse('this is work')
        except Exception as e:
            return HttpResponse(f'{e}')
    return render(request, 'invoice_system/home.html')
# context is a argument and This argument sent by invoiceprint function
# def sentinvoicebymail(context):
#     d = dict(context)
#     customer_email = d['print'][0]['customertable_customer_email']
#     print(customer_email)
#     try:
#         template = get_template('invoice_system/sentinvoicebymail.html')
#         html  = template.render(d)
#         file = open('invoice.pdf', "w+b")
#         pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
#                 encoding='utf-8')

#         subject = 'Ordered Invoice'
#         message = 'This Mail Recieved by Mohit Mishra & Company Private Limited'
#         sender_email = 'mohitmishra.falna850@gmail.com'
#         reciever_email = customer_email

#         file.seek(0)
#         pdf = file.read()
#         file.close()     
#         email = EmailMessage(subject, message, sender_email, [reciever_email])
#         email.attach_file('invoice.pdf')
#         email.send()
#         # return HttpResponse(pdf, 'application/pdf')   
#     except Exception as e:
#         return HttpResponse('{e}')
#     return HttpResponse()   

def ordercancelupdate(request):
    if request.method == "GET":
        orderNo = request.GET.get('orderNo')
        orderandcustomerdetails = []
        productorderandproductdetails = []
        try:
            ordernumberdetails = ProductOrder.objects.select_related('order').filter(order_id=orderNo)
            for ordnumdet in ordernumberdetails:
                orderandcustomerdetails.append({'customer_name':ordnumdet.order.customer.customer_name, 'customer_email':ordnumdet.order.customer.customer_email, 'customer_contact':ordnumdet.order.customer.customer_contact,'customer_due':ordnumdet.order.customer.due_amt,

                'order_date':ordnumdet.order.order_date,'paid_amt':ordnumdet.order.paid_amt,
                'total_amt':ordnumdet.order.total_amt,'cash_discount':ordnumdet.order.cash_discount,
                'order_due':ordnumdet.order.due_amt,'orderNo':ordnumdet.order.order_no, 'order_status':ordnumdet.order.order_status,
                })
                break
            for ordnumdetsecond in ordernumberdetails:
                productorderandproductdetails.append({'product_id':ordnumdetsecond.product.product_id, 'product_name':ordnumdetsecond.product.product_name,'product_price':ordnumdetsecond.product.product_price
                ,'product_discount':ordnumdetsecond.product.product_discount,

                'order_qty':ordnumdetsecond.order_qty,'paidable_amount':ordnumdetsecond.paidable_amount,
                })            
            # context = {'ordandcustdetails':orderandcustomerdetails,'prodandproddetails':productorderandproductdetails}
            response = json.dumps({'ordandcustdetails':orderandcustomerdetails,'prodandproddetails':productorderandproductdetails}, default=str)
            return HttpResponse(response)
        except Exception as e:
            print(e)
            return HttpResponse(f'{e}')
    return render(request, 'invoice_system/home.html')

def productcancelupdate(request):
    if request.method == 'GET':
        order_no = request.GET.get('orderNo')
        email = request.GET.get('customer_email')
        product_name = request.GET.get('prod_name')
        try:
            if order_no != '':
                prt_prodid = Products.objects.get(product_name=product_name)
                db_prod_id = {'prt_prod_id':prt_prodid.product_id}
                prt_prod_id = db_prod_id['prt_prod_id']

                db_prod_qty = {'prt_prod_qty':prt_prodid.product_qty}
                prt_prod_qty = db_prod_qty['prt_prod_qty']  

                prdord_price = ProductOrder.objects.get(product_id=prt_prod_id, order_id=order_no)
                product_price = {'prod_id':prdord_price.paidable_amount}
                payble_amt = product_price['prod_id']

                product_qty = {'prod_qty':prdord_price.order_qty}
                prd_qty = product_qty['prod_qty']             

                result = ProductOrder.objects.select_related('order').filter(order_id=order_no)  
                print(result)
                for output in result:
                    cstm_due = output.order.customer.due_amt
                    ord_due = output.order.due_amt
                    ord_status = output.order.order_status
                    order_total = output.order.total_amt
                    
                if ord_status != 'Cancel':
                    update_total = order_total - payble_amt
                    update_orddue = ord_due - payble_amt
                    update_custDue = cstm_due - payble_amt
                    updateorderstatus = Orders.objects.filter(order_no=order_no).update(due_amt=update_orddue, total_amt=update_total)
                    updateCustomerDue = Customer.objects.filter(customer_email=email).update(due_amt=update_custDue)
                    add_prod_qty = prt_prod_qty + prd_qty
                    print(add_prod_qty)
                    updateproductqty = Products.objects.filter(product_id=prt_prod_id).update(product_qty=add_prod_qty)
                    deleteProductOrdercancelrecord=ProductOrder.objects.filter(product_id=prt_prod_id).update(product_status='Cancel')
                else:
                    return HttpResponse('Your Order has been Canceled.')

            return HttpResponse('this is work')
        except Exception as e:
            return HttpResponse(f'{e}')            
    return render(request, 'productcancelupdate/home.html')
    # return HttpResponse('this is one.')

def updateproduct(request):
    if request.method == 'GET':
        order_no = request.GET.get('orderNo')
        prod_name = request.GET.get('prod_name')
        prod_qty_str = request.GET.get('prod_qty')
        prod_payable_str = request.GET.get('prod_payable')
        prod_total_str = request.GET.get('prod_total')

        prt_prodid = Products.objects.get(product_name=prod_name)
        db_prod_id = {'prt_prod_id':prt_prodid.product_id}
        prt_prod_id = db_prod_id['prt_prod_id']  

        db_prod_qty = {'prt_prod_qty':prt_prodid.product_qty}
        prt_prod_qty = db_prod_qty['prt_prod_qty'] 

        prdord_price = ProductOrder.objects.get(product_id=prt_prod_id, order_id=order_no)
        product_qty = {'prod_qty':prdord_price.order_qty}
        db_prd_qty = product_qty['prod_qty']  

        prod_qty = int(prod_qty_str)
        prod_payable = float(prod_payable_str)
        prod_total = float(prod_total_str)

        calculated_qty = db_prd_qty - prod_qty

        if db_prd_qty > prod_qty:
            updateproducts = prt_prod_qty + calculated_qty
            updateprodorderqtytotal = ProductOrder.objects.filter(product_id=prt_prod_id, order_id=order_no).update(order_qty=prod_qty, paidable_amount=prod_payable)
            updateordertotal = Orders.objects.filter(order_no=order_no).update(total_amt=prod_total)
            updateproductqty = Products.objects.filter(product_id=prt_prod_id).update(product_qty=updateproducts)
        if db_prd_qty < prod_qty:
            updateproducts = prt_prod_qty + calculated_qty
            updateprodorderqtytotal = ProductOrder.objects.filter(product_id=prt_prod_id, order_id=order_no).update(order_qty=prod_qty, paidable_amount=prod_total)
            updateordertotal = Orders.objects.filter(order_no=order_no).update(total_amt=prod_total)
            updateproductqty = Products.objects.filter(product_id=prt_prod_id).update(product_qty=updateproducts)

    return render(request, 'invoice_system/home.html')

def newproductinoldid(request):
    if request.method == 'GET':
        # get id from Customer table.
        customer_email = request.GET.get('customer_email')
        order_no_one = request.GET.get('order_no')
        # insert the record in orders table.
        total_amt = request.GET.get('total_amt')
        paid_amt = request.GET.get('paid_amt')
        due_amt = request.GET.get('due_amt')
        cash_discount = request.GET.get('cash_dis')
        customer_due = request.GET.get('customer_due')
        # insert the record in ProductOrder table.
        prod_name = request.GET.getlist('prod_name[]')
        prod_qty = request.GET.getlist('prod_qty[]')
        paidableamt = request.GET.getlist('paidableamt[]')
        print(prod_name)
        printeditemsecond = []
        try:
            outputprint = ProductOrder.objects.select_related('order').filter(order_id=order_no_one) 
            
            for outputsecond in outputprint:
                printeditemsecond.append({'producttable_product_name':outputsecond.product.product_name,
                'prodordertable_qty':outputsecond.order_qty, 'prodordertable_paidable':outputsecond.paidable_amount 
            })
            result = Customer.objects.get(customer_email=customer_email)
            get_id = {"customer_id":result.customer_id}
            cust_id = get_id['customer_id']

            result1 = Orders.objects.get(order_no=order_no_one)
            get_orderstatus = {"order_status":result1.order_status}
            order_status = get_orderstatus['order_status']

            newinOLDID = Orders(order_no=order_no_one, paid_amt=paid_amt, total_amt=total_amt, cash_discount=cash_discount, due_amt=due_amt, customer_id=cust_id, order_status=order_status)
            newinOLDID.save()  

            db_len = len(printeditemsecond)
            for i in range(db_len, len(prod_name)):
                prodname_res = Products.objects.get(product_name=prod_name[i])
                get_prod_id = {'product_id':prodname_res.product_id}
                get_prod_name = {'product_name':prodname_res.product_name}
                get_prod_qty = {'product_qty':prodname_res.product_qty}
                prod_id = get_prod_id['product_id']
                db_prod_name = get_prod_name['product_name']
                db_prod_qty = get_prod_qty['product_qty']
                if order_no_one != '' and paidableamt != '' and prod_id != '' and prod_qty != '' and db_prod_qty != '':
                    recordinsertmiddletable = ProductOrder(order_qty=prod_qty[i], paidable_amount=paidableamt[i], order_id=order_no_one, product_id=prod_id, product_status='Completed')
                    recordinsertmiddletable.save()
                    sub_prod_qty = db_prod_qty - int(prod_qty[i])
                    change_db = Products.objects.filter(product_name=db_prod_name).update(product_qty=sub_prod_qty)
                    
                    updateCustomerDue = Customer.objects.filter(customer_email=customer_email).update(due_amt=customer_due)
            return HttpResponse('Your Data is saved Successfully')                          
        except Exception as e:
            return HttpResponse(f'{e}')        
    return render(request, 'invoice_system/home.html')

def searchcustomerdetails(request):
    if request.method=="GET":
        # get the value from jquery ajax.
        search_customer_details = request.GET.get("customer_name")
        # if the variable is not empty then retrieve the data from database table
        try:                
            if search_customer_details != '':
                # create a empty list and append letter
                search_item = []
                # retrieve data from database table
                match = Customer.objects.filter(Q(customer_name__icontains=search_customer_details))
                print(match)
                if match:
                    # run the loop and retrieve the item one by one.
                    for ma in match:
                        # retrive the item and append in search_item = [] list.
                        search_item.append({'customer_id':ma.customer_id, 'customer_name':ma.customer_name, 'customer_email':ma.customer_email, 'customer_contact':ma.customer_contact})
                        # the value convert in json and append in response variable.
                        response = json.dumps(search_item, default=str)
                        # send the responst in jquery ajax.
                    return HttpResponse(response)
                else:
                    return HttpResponse('')
        except Exception as e:
            return HttpResponse(f'{e}')
    return render(request, 'invoice_system/duerecoverandbillprint.html')

def dueclear(request):
    if request.method == 'GET':
        customer_email = request.GET.get('cust_email')
        print(customer_email)
        try:
            if customer_email != None:
                result = Customer.objects.get(customer_email=customer_email)
                get_id = {"customer_id":result.customer_id}
                get_due = {"customer_id":result.due_amt}
                cust_id = get_id['customer_id']
                cust_due = get_due['customer_id']
                result1 = Orders.objects.filter(customer_id=cust_id, order_status='Pending')
                record = []
                printeditemsecond = []
                for res in result1:
                    record.append({'order_no':res.order_no,'total_amt':res.total_amt, 'paid_amt':res.paid_amt, 'cash_discount':res.cash_discount, 'due_amt':res.due_amt, 'order_status':res.order_status})                   
                for i in range(0, len(record)):
                    ord_id = record[i]['order_no']
                    prod_name = ProductOrder.objects.select_related('order').filter(order_id=ord_id)
                    for outputsecond in prod_name:
                        printeditemsecond.append({'producttable_product_name':outputsecond.product.product_name})
                # send two object in one http response.
                print(printeditemsecond)
                response = json.dumps({'record':record, 'printeditemsecond':printeditemsecond},default=str)
                return HttpResponse(response)
        except Exception as e:
            return HttpResponse(f'{e}')
    return render(request, 'invoice_system/duerecoverandbillprint.html')

def updatedue(request):
    if request.method == 'GET':
        ord_no = request.GET.get('order_no')
        try:
            if ord_no != '':
                cust_due = ProductOrder.objects.select_related('order').filter(order_id=ord_no)      
                for output in cust_due:
                    cstm_id = output.order.customer.customer_id
                    cstm_due = output.order.customer.due_amt
                    ord_due = output.order.due_amt
                duecompleted = Orders.objects.filter(order_no=ord_no).update(due_amt=ord_due, order_status='Completed')
                custduecalculate = cstm_due - ord_due
                custduecomplete = Customer.objects.filter(customer_id=cstm_id).update(due_amt=custduecalculate)
                return HttpResponse('Your Due Completed Successfully')
        except Exception as e:
            return HttpResponse(f'{e}')
    return render(request, 'invoice_system/home.html')

def demo(request):
    return render(request, 'invoice_system/home.html')
