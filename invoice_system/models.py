from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=50)
    customer_contact = models.CharField(max_length=12)
    customer_email = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10)
    city_name = models.CharField(max_length=30)
    pincode = models.CharField(max_length=8)
    district = models.CharField(max_length=30, default='')
    state_name = models.CharField(max_length=30)
    contry_name = models.CharField(max_length=30)
    due_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "customers"
    
    def __str__(self):
        return self.customer_name

class Orders(models.Model):
    order_no = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)
    paid_amt = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt = models.DecimalField(max_digits=10, decimal_places=2)
    cash_discount = models.DecimalField(max_digits=10, decimal_places=2, default='')
    due_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order_status = models.CharField(max_length=15, default='')
    class Meta:
        db_table = "orders" 

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50, unique=True)
    product_qty = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_discount = models.IntegerField()
    def __str__(self):
        return self.product_name

    class Meta:
            db_table = "products"

class ProductOrder(models.Model):
    productorder_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    order_qty = models.IntegerField()
    paidable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    product_status = models.CharField(max_length=15, default='')
    class Meta:
        db_table = "productorder"

