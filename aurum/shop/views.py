from django.shortcuts import render , redirect
from django.views import generic
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse , JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.views.decorators.csrf import csrf_protect
from .models import Company , Category , Product , ProductInstance  , Cart , CartItem , Comment

from functools import reduce
import operator

def index(request):
    featured_products = Product.objects.all().order_by('-sold_nums')[:4]
    
    context = {'featured_products' : featured_products}
    return render (request , 'shop/home.html' , context)

def about(request):
    context = {}
    return render (request , 'shop/about.html' , context)

class ProductDetailView(FormMixin , generic.DetailView):
    model = Product
    template_name = 'shop/item.html'
    form_class = CommentForm
    loadcomment = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related'] = Product.objects.filter( Q(sex__iexact = self.object.sex) , ~Q(id__exact = self.object.id) ,
                Q(name__icontains=self.object.name) | Q(brand__icontains = self.object.brand) | Q(category_id__exact = self.object.category_id) ).order_by('-created')[:4]
        context['comments'] = Comment.objects.filter( Q(product_id__exact = self.kwargs.get('pk')) , Q(status__exact = 'published') ).order_by('-created')[:self.loadcomment]
        context['form'] = CommentForm()
        return context

    def get_success_url(self):
        messages.success(self.request , f'Your Comment Submited')
        return reverse('shop:ProductDetail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid()  :
            return self.form_valid(form)
        #else:
        #    return self.form_invalid(form)
        if self.request.POST.get('loadmorecomment') and self.request.is_ajax(): #load more comment
            mt = int (self.request.POST.get('loadmorecomment'))
            self.loadcomment = self.loadcomment + (mt * 5)
        if self.request.POST.get('deletecomment') and self.request.is_ajax(): #delete comment
            pk = self.request.POST.get('pk')
            Comment.objects.filter(id=pk , user=request.user).delete()
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user ##!!!!!
        form.instance.product = self.object    ##!!!!!
        form.save()
        return super(ProductDetailView, self).form_valid(form)

#for like or dislike a commnet
def like_dislike(request): 
    user = request.user
    if request.method=='POST' and request.is_ajax() :
        comment = Comment.objects.get(id = request.POST.get('pk'))
        if request.POST.get('like'): #delete from dislike and add to likes
            if comment.user_dislike.filter(id=user.id).exists():
                comment.user_dislike.remove(user)
            if not comment.user_like.filter(id=user.id):
                comment.user_like.add(user)

        elif request.POST.get('dislike'): #delete from like and add to dislikes
            if comment.user_like.filter(id=user.id).exists():
                comment.user_like.remove(user)
            if not comment.user_dislike.filter(id=user.id):
                comment.user_dislike.add(user)
            
        #return like number and dislike number with JSON    
        return JsonResponse({'liked':comment.user_like.count() , 'disliked':comment.user_dislike.count()})

class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'Products'
    template_name = 'shop/catalog.html'
    #queryset = Book.objects.filter(title__icontains = 'hitler')[:5]

    #ordering = ['-created']

    ''' def get(self, request, *args, **kwargs):
        if (self.request.GET.get('pgnum')):
            self.paginate_by = self.request.GET.get('pgnum')
        return super(ProductListView, self).get(request, *args, **kwargs) '''

    def get(self, request, *args, **kwargs): 
        ######################################## FOR FILTER ###########################################
        if (self.request.GET.get('size')) or (self.request.GET.get('gender')) or (self.request.GET.get('category')):
            #All is str
            gender = self.request.GET.get('gender')
            size = self.request.GET.get('size')
            category = self.request.GET.get('category')
            
            category_args = []
            size_args = []

            if(gender  == ""):
                a = Q()
            else :
                a = Q(sex__iexact = gender)      
            
            if (category != ""):
                sp = [x.strip() for x in category.split(',')]
                for cat in sp :
                    category_args.append(Q(category__id = cat))

            if (size != ""):
                zp = [x.strip() for x in size.split(',')]
                for size_item in zp :
                    size_args.append(Q(productinstance__size = size_item))

            self.queryset = Product.objects.filter(a , reduce(operator.or_, category_args ,Q()) ,
                                                        reduce(operator.or_, size_args ,Q()) ).distinct() #Q() for initial !
            
            self.paginate_by = 3

        ######################################## FOR Sorting ###########################################
        if (self.request.GET.get('sortby')):
            self.ordering = [self.request.GET.get('sortby')]
        ############################### FOR Nums Product in one Page ##################################
        if (self.request.GET.get('pgnum')):
            self.paginate_by = self.request.GET.get('pgnum')



        return super(ProductListView, self).get(request, *args, **kwargs)


    paginate_by = 3

    #def get_queryset(self):
        #return Book.objects.filter(title__icontains='hitler')[:5]

    def get_context_data(self , **kwargs):
        context = super(ProductListView , self).get_context_data(**kwargs)
        context['categorys'] = Category.objects.all()
        context['sizes'] = ProductInstance.objects.order_by('size').values('size').distinct()
        context['sexs'] = Product.objects.order_by('sex').distinct('sex')
        context['max_price_product'] = Product.objects.order_by('price').first()
        return context

@login_required
def cart(request):
    #add to cart
    if request.method == "POST" and request.POST.get('formchoice') == 'formchoice' : # and re..
        if request.user.is_authenticated :
            # 1.select productinstance and add to CartItem
            choice = request.POST.get('choice')
            slt = choice.split("#") 

            pro = ProductInstance.objects.get(product_id = request.POST.get('product') , size__iexact = slt[0] , color__iexact = slt[1])
            cartitem = CartItem.objects.create(item = pro , order_num=1)
            # 2.Create or select Cart For currentuser
            cart, created = Cart.objects.get_or_create(user=request.user , is_paid=False)
            # 3.Add cartitem to cart
            cart.item_list.add(cartitem)
        else :
            messages.success(request , f'You Are Not Login !')
            return redirect('shop:catalog')  #go here      
    else :
        try :
            cart = Cart.objects.get(user=request.user , is_paid=False)
        except Cart.DoesNotExist :
            cart = None

    context = {'cart':cart}
    return render (request , 'shop/cart.html' , context)

@login_required
def del_cart_item(request):
    if request.method=="POST" and request.is_ajax():
        id = request.POST.get("cartitemid")
        try :
            cart = Cart.objects.get(user=request.user , is_paid=False)
        except Cart.DoesNotExist:                                                                                                       
            messages.error(request, f'No Cart For Delete')                                                                                                       
            return redirect('shop:index')
                    
        cart.item_list.filter(id=id).delete()
        #return HttpResponse("Item deleted !")
        return redirect('shop:cart')
@login_required
def calcu_cart_item(request):
    if request.method=="POST" and request.is_ajax():
        id = request.POST.get("cartitemid")
        new_order_num = int(request.POST.get("new_order_num"))
        try :
            cart = Cart.objects.get(user=request.user , is_paid=False)
        except Cart.DoesNotExist:                                                                                                       
            messages.error(request, f'No Cart For Edit')                                                                                                       
            return redirect('shop:index')
                    
        cart.item_list.filter(id=id).update(order_num = new_order_num)
        #return HttpResponse("Item deleted !")
        return redirect('shop:cart')

@login_required
def payment(request):
    context = {}
    return render (request , 'shop/payment.html' , context)

@login_required
def factor(request):
    try :
        cart = Cart.objects.get(user=request.user , is_paid=False)
    except Cart.DoesNotExist:
        messages.error(request, f'No Cart For Buy')                                                                                                       
        return redirect('shop:index')
    
    for c in cart.item_list.all():
        c.item.num = c.item.num - c.order_num #az mojodi kam kon
        c.item.save()
        c.item.product.sold_nums += c.order_num #be tedad foroukhteh shodeha azafe kon
        c.item.product.save()

    #cart.update(is_paid = True) #update just work on qs like .filter .get
    cart.is_paid = True 
    cart.save()

    context = {'cart':cart}
    return render (request , 'shop/factor.html' , context)