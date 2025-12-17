from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
  cid=models.AutoField(primary_key=True)
  cname=models.CharField(max_length=50)

  def __str__(self):
    return self.cname

class Product(models.Model):
  pid=models.AutoField(primary_key=True)
  pname=models.CharField(max_length=50)
  pdis=models.TextField()
  pprice=models.FloatField()
  pimage=models.ImageField(upload_to='product')
  cat=models.ForeignKey(Category,on_delete=models.CASCADE)
  
  def __str__(self):
    return self.pname
  
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.pprice

    def __str__(self):
        return f"{self.user.username} - {self.product.pname}"
      
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    notes = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.pname} ({self.quantity})"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

