from django.urls import path
from . import views
from .middlewares.auth import auth_middleware
from .views import Cart
from .views import CheckOut

urlpatterns = [
    path('', views.homePage, name="home"),
    path('login/', views.login, name="login"),
    path('cart/login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('cart/', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders/', views.orders, name="orders"),
    path('payment/', views.payment, name="payment"),
    path('<uuid:order_id>', views.orderview, name="orderview"),

]
