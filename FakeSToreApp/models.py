from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField()
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField()
    image = models.URLField()
    rate = models.FloatField()
    count = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    
class User(models.Model):
    username=models.CharField()
    email=models.EmailField()
    password=models.CharField()
    
    def __str__(self):
        return self.username
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
     
    
    
    
