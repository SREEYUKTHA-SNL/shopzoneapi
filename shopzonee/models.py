from django.db import models

# Create your models here.
class Login(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=20)
    role=models.CharField(max_length=10)
class Registration(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    
    number=models.CharField(max_length=50,default="number")
    login_id=models.OneToOneField(Login,on_delete=models.CASCADE)
    role=models.CharField(max_length=50)

class Category(models.Model):
    categoryname = models.CharField(max_length=20)
 

    def __str__(self):
        return self.categoryname

class Subcategory(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategoryname = models.CharField(max_length=20)
    subcategory_image = models.URLField(max_length=200)

    def __str__(self):
        return self.subcategoryname

class Product(models.Model):
    productname = models.CharField(max_length=20, default="name")
    price = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    size = models.CharField(max_length=10, default="size")
    color = models.CharField(max_length=10, default="color")
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.productname
class Review(models.Model):
    productname = models.CharField(max_length=20, default="name")
    productid = models.CharField(max_length=20, default="id")
    username = models.CharField(max_length=20, default="username")
    userid = models.CharField(max_length=20, default="userid")
    reviewdescription=models.CharField(max_length=50)
class Cart(models.Model):
    productid = models.CharField(max_length=20, default="id")
    productname = models.CharField(max_length=20, default="productname")
    userid = models.CharField(max_length=20, default="userid")
    quantity=models.CharField(max_length=50)
    cart_status=models.IntegerField(default=1)
    description=models.CharField(max_length=100,null=True)

    price=models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
    
class Wishlist(models.Model):
    productid = models.CharField(max_length=20, default="id")
    productname = models.CharField(max_length=20, default="productname")
    userid = models.CharField(max_length=20, default="userid")
    wishlist_status=models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
class Order(models.Model):
    productid = models.CharField(max_length=20, default="id")
    productname = models.CharField(max_length=20, default="productname")
    userid = models.CharField(max_length=20, default="userid")
    quantity = models.CharField(max_length=50)
    order_status = models.CharField(max_length=50, default="Pending")
    date = models.DateField(auto_now_add=True)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
class Address(models.Model):
    userid = models.OneToOneField(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    house_no = models.IntegerField()
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
