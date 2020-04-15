from django.contrib import admin
from .models import Company , Category , Product , ProductInstance , Cart , CartItem , Image , Comment
# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone' , 'address')
    fieldsets = (
        (None , {
            'fields':('email','phone','address')
        }),
        ('Links',{
            'fields':('instagram','facebook','telegram','twitter')
        }),
        ('Carousel Images',{
            'fields':('images',)
        })
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price' , 'brand', 'sex' , 'category' , 'sold_nums' , 'status' , 'display_size' , 'display_color' , 'created')
    list_filter = ('status' , 'created')
    inlines = [ProductInstanceInline]

    def display_size(self , obj):
        return " , ".join([pro.size for pro in ProductInstance.objects.filter(product = obj)])
    display_size.short_description = 'Size' 
    
    def display_color(self , obj):
        return " , ".join([pro.color for pro in ProductInstance.objects.filter(product = obj)])
    display_size.short_description = 'Color' 

@admin.register(ProductInstance)
class InstanceAdmin(admin.ModelAdmin):    
    list_display = ('product', 'size' , 'color' , 'num')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user','is_paid','cart_total',)
    list_filter = ('is_paid','updated')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('item',)

def delete_with_file(modeladmin , request , queryset):
    queryset.delete()

delete_with_file.short_description = 'Delete With File'
@admin.register(Image)
class Image(admin.ModelAdmin):
    list_display = ('image',)
    actions = [delete_with_file,]

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('user','subject' , 'product' ,'like_number','dislike_number', 'status' , 'created')
    list_filter = ('status','created')
    def like_number(self , obj):
        return obj.user_like.count()
    like_number.short_description = 'like number' 
    def dislike_number(self , obj):
        return obj.user_dislike.count()
    dislike_number.short_description = 'dislike number' 

