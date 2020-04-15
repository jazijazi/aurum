from .models import Company , Product , Cart
from django.db.models import Q

def aboutus(request):   #dont forget add this to settings
    aboutus_G = Company.objects.all().last()

    return {
        'aboutus_G': aboutus_G,  # Add 'aboutus_G' to the all templates
    }

def shop(request): #dont forget add this to settings
    men   = Product.objects.filter( Q(sex = 'men'),Q(status = 'available') )[:5]
    women = Product.objects.filter( Q(sex = 'women'),Q(status = 'available') )[:5]
    girls = Product.objects.filter( Q(sex = 'girl'),Q(status = 'available') )[:5]
    boys  = Product.objects.filter( Q(sex = 'boy'),Q(status = 'available') )[:5]
    featured_product = Product.objects.filter(Q(status = 'available'))[:2]

    return {
        'men':men , 'women':women , 'girls':girls , 'boys':boys , 'featured_product':featured_product,
    }


def cart(request):
    if request.user.is_authenticated:
        try: #for check Cart exist or not
            headercart = Cart.objects.get(user=request.user , is_paid=False)
        except Cart.DoesNotExist:
            headercart = None
    else :
        headercart = None
    return{'headercart':headercart}