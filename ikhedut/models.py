from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=60)
    mobile=models.CharField(max_length=60)
    message=models.TextField()
 
    def __str__(self):
        return self.name    
    
class Signup(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=60)
    image = models.ImageField(upload_to="userimages/",default="media/userimages/default.png")
    
    def __str__(self):
        return self.user.username

class CropSale(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE ,null=True,blank=True)
    crop = models.CharField(max_length=50,db_index=True)
    quantity = models.IntegerField()
    price = models.IntegerField()   
    image = models.ImageField(upload_to="crop_img/",null=True, blank=True)
    is_approved = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.crop

class Ad(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="ads",null=True,blank=True)
    fullname = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    state=models.CharField(max_length=50,default="Gujarat")
    city = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="ad_img/", null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"{self.productname} ({self.user.username})"
        return self.productname

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=30)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(CropSale, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.added_at + timedelta(minutes=30)

    @property
    def subtotal(self):
        if not self.product:
            return 0
        return round((self.product.price / 20) * self.quantity, 2)

class Order(models.Model):
    STATUS_CHOICES = (
        ("placed", "Placed"),   
        ("cancel_requested", "Cancel Requested"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),)

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders",null=True,blank=True)

    fullname = models.CharField(max_length=150)
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    address = models.TextField()

    payment_method = models.CharField(max_length=20)

    cardholdername=models.CharField(max_length=50, blank=True, null=True)
    card_number = models.CharField(max_length=25, blank=True, null=True)
    card_expiry = models.CharField(max_length=10, blank=True, null=True)
    card_cvv = models.CharField(max_length=10, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="placed")

    cancel_requested_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def can_cancel(self):
        return self.status == "placed" and \
               timezone.now() <= self.created_at + timedelta(hours=24)

    def __str__(self):
        return f"Order #{self.fullname}"

    def should_be_completed(self):
        return (
            self.status == "placed"
            and timezone.now() >= self.created_at + timedelta(days=10)
        )

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(CropSale,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} Item"
    
