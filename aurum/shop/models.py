import uuid
from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PilImage

class Company(models.Model):
    email     = models.CharField(max_length=100 , blank=True, null=True, help_text="Enter Email for Contact us")
    phone     = models.CharField(max_length=100 , blank=True, null=True, help_text="Enter phone for Contact us")
    address   = models.CharField(max_length=100 , blank=True, null=True, help_text="Enter address for Contact us")
    instagram = models.CharField(max_length=100 ,default="#" , blank=True, null=True, help_text="Enter instagram link for Contact us")
    facebook  = models.CharField(max_length=100 ,default="#" , blank=True, null=True, help_text="Enter facebook link for Contact us")
    telegram  = models.CharField(max_length=100 ,default="#" , blank=True, null=True, help_text="Enter telegram link for Contact us")
    twitter   = models.CharField(max_length=100 ,default="#" , blank=True, null=True, help_text="Enter twitter for Contact us")
    images = models.ManyToManyField('Image')
    
    def __str__(self):
        return "Arum site EMAIL is {}".format(self.email)


class Category(models.Model):
    name = models.CharField(max_length=100 , help_text="Enter a Product Category...")

    def __str__(self):
        return "Category : {}".format(self.name)

class Image(models.Model):
    image = models.ImageField(default='default.jpg',upload_to='product_images')

    def save(self, *args, **kwargs):
        super().save(*args , **kwargs)

        img = PilImage.open(self.image.path)
        
        if img.height > 300 or img.width > 300 :
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Product(models.Model):
    
    STATUS_CHOICES = (
        ('available' , 'Available'),
        ('not_available' , 'Not Available')
    )
    SEX_CHOICES = (
        ('men' , "Men`s"),
        ('women' , "Women`s"),
        ('boy' , "Boy`s"),
        ('girl' , "Girl`s")
    )

    name = models.CharField(max_length=100 , help_text="Enter Product Name...")
    description = models.TextField(max_length=1000 , help_text="Enter a description for this product")
    price = models.CharField(max_length=100 ,help_text="Enter a PRICE for this product")
    brand = models.CharField(max_length=100 ,help_text="Enter a BRAND for this product")
    sold_nums = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add = True)
    status  = models.CharField(max_length = 60 , choices = STATUS_CHOICES , default = 'available')
    sex  = models.CharField(max_length = 60 , choices = SEX_CHOICES , default = 'men')
    category = models.ForeignKey('Category',on_delete=models.SET_NULL , null = True)
    images = models.ManyToManyField('Image')

    def __str__(self):
        return "Product name is {}".format( self.name )

    class Meta:
        ordering = ('-created',)


class ProductInstance(models.Model):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4,
                            editable= False , help_text = "Unique ID for particular Product in whole Shop")
    product = models.ForeignKey('Product',on_delete=models.SET_NULL,null = True)
    size = models.CharField(max_length=50 ,help_text="Enter Size for this product")
    color = models.CharField(max_length=50 ,help_text="Enter Color for this product")
    num = models.IntegerField(help_text="Enter Avalible Number for this product")
    
    def __str__ (self) :
        return "{0} , ({1})".format(self.id , self.product.name)

class CartItem(models.Model):
    item = models.ForeignKey('ProductInstance',on_delete=models.SET_NULL,null = True)
    order_num = models.IntegerField(default=1)

    @property
    def item_total(self):
        return self.order_num * int(self.item.product.price)

    class Meta :
        ordering = ['item']

    def __str__ (self) :
        return "Name : {0} , Size : {1} , Color : {2} , Order Num : {3}".format(self.item.product.name , self.item.size , self.item.color , self.order_num)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL , null = True)
    item_list = models.ManyToManyField(CartItem)
    updated = models.DateTimeField(auto_now = True)
    is_paid = models.BooleanField(default=False)
    total = models.IntegerField(default=0)

    @property
    def cart_total(self):
        sum = 0
        for c in self.item_list.all() :
            sum += c.item_total
        return sum

    def __str__ (self) :
        return "Cart for:{0}".format(self.user)
    
class Comment(models.Model):
    STATUS_CHOICES = (
        ('published' , 'Published '),
        ('waiting' , 'Waiting')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    status  = models.CharField(max_length = 60 , choices = STATUS_CHOICES , default = 'published')
    created = models.DateTimeField(auto_now_add = True)
    user_like=models.ManyToManyField(User,related_name="likes",blank=True)
    user_dislike=models.ManyToManyField(User,related_name="dislikes",blank=True)