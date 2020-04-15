from django.urls import path , re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'
urlpatterns = [
    path('' , views.index , name="index"),
    path('about/' , views.about , name="about"),
    path('cart/' , views.cart , name="cart"),
    path('del_cart_item/' , views.del_cart_item , name="delcartitem"),
    path('calcu_cart_item/' , views.calcu_cart_item , name="calcucartitem"),
    path('catalog/' , views.ProductListView.as_view(), name="catalog"),
    path('payment/' , views.payment, name="payment"),
    path('factor/' , views.factor, name="factor"),
    path('like_dislike/' , views.like_dislike, name="like_dislike"),
    re_path(r'^detail/(?P<pk>\d+)/$',views.ProductDetailView.as_view(), name='ProductDetail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
