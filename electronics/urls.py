from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('all/electronics', ElectronicaShowView.as_view(), name='electronics'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('orders/', OrderPageView.as_view(), name="order"),
    path('buy/all/product/', buyAll, name="buy_all"),
    path('electronics/<slug:slug>/', CategoryView.as_view(), name="category"),
    path('electronics/<slug:cat_slug>/<slug:slug>', SingleElectronicaView.as_view(), name='single_electronica'),
    path('register/', Register.as_view(), name="costumerRegister"),
    path('login/', cache_page(60)(LoginUser.as_view()), name="costumerLogin"),
    path('auth/logout/', costumerLogout, name="costumerLogout"),
]
