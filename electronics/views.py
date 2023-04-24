from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from electronics.forms import RegisterForm
from electronics.models import Category, Electronica, Order
from electronics.serializers import ElectronicaSerializer, UserSerializer
from electronics.utils import DataMixin


def pageNotFound(request, exeption):
    return HttpResponseNotFound('<h1>page not found</h1>')


class IndexView(DataMixin, TemplateView):
    template_name = "electronics/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="index")
        return dict(list(context.items()) + list(mixin.items()))


class AboutView(DataMixin, TemplateView):
    template_name = "electronics/about.html"

    def get_context_data(self, **kwargs):
        return self.get_user_context(title="about page")


class ContactView(DataMixin, TemplateView):
    template_name = "electronics/contacts.html"

    def get_context_data(self, **kwargs):
        return self.get_user_context(title="contacts")


class ElectronicaShowView(DataMixin, ListView):
    model = Electronica
    template_name = "electronics/all_cats.html"
    context_object_name = "electronics"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title='context.get("electronica").title')
        return dict(list(context.items()) + list(mixin.items()))


class CategoryView(DataMixin, DetailView):
    model = Category
    template_name = "electronics/detail_cat.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        activ = self.data()
        context['page_obj'] = activ
        mixin = self.get_user_context(title="category")
        return dict(list(context.items()) + list(mixin.items()))

    def data(self):
        queryset = self.object.electronica_set.all()
        paginator = Paginator(queryset, 3)
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


class SingleElectronicaView(DataMixin, DetailView):
    model = Electronica
    template_name = "electronics/single_electronmica.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title=context.get("product").name)
        return dict(list(context.items()) + list(mixin.items()))

    def post(self, request, **kwargs):
        my_data = request.POST
        user = request.user
        newCart = Order()
        newCart.costumer = user
        newCart.made_in = my_data.get("country", None)
        if my_data.get("country") == "S":
            newCart.made_in = "China"
        newCart.quantity = my_data.get("quantity", None)
        newCart.product = Electronica.objects.get(pk=my_data.get("product_id", None))
        newCart.save()
        return redirect('order')


class ProfileView(DataMixin, TemplateView):
    template_name = "electronics/profile.html"

    def post(self, request, **kwargs):
        my_bln = request.POST.get("balance")
        if my_bln:
            request.user.balance = my_bln
            request.user.save()
        return redirect('profile')


class Register(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = "electronics/register.html"
    success_url = reverse_lazy('costumerLogin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="registration")
        return dict(list(context.items()) + list(mixin.items()))


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'electronics/login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="login")
        return dict(list(context.items()) + list(mixin.items()))


class OrderPageView(DataMixin, ListView):
    template_name = "electronics/orders.html"
    model = Order

    def get_queryset(self):
        user = self.request.user
        cart = Order.objects.select_related("costumer").select_related("product").filter(costumer=user,
                                                                                         isSelling=False).all()
        return cart

    def get_context_data(self, **kwargs):
        totalSum = 0
        for i in self.object_list:
            totalSum += i.product.price * i.quantity
        context = super().get_context_data(**kwargs)
        context["total"] = totalSum
        mixin = self.get_user_context(title="order")
        return dict(list(context.items()) + list(mixin.items()))

    def post(self, request, **kwargs):
        cart = request.POST.get("cart_id", None)
        if cart:
            Order.objects.get(pk=cart).delete()
            messages.error(request, "product deleted")
        else:
            return HttpResponseNotFound

        return redirect('order')


@login_required
def costumerLogout(request):
    logout(request)
    messages.error(request, "success log out")
    return redirect("/")


#
#
def buyAll(request):
    if request.method == "POST":
        userItems = Order.objects.select_related("product").select_related("product__category").filter(
            costumer=request.user, isSelling=False).all()
        itemsMoney = 0
        for i in userItems:
            itemsMoney += i.product.price
        if request.user.balance > itemsMoney:
            Order.objects.filter(costumer=request.user, isSelling=False).all().order_by('product').update(
                isSelling=True)
            request.user.balance = request.user.balance - itemsMoney
            request.user.save()
        else:
            messages.error(request, "no maney")
            return redirect('order')
        messages.info(request, "success selling")
        return redirect('profile')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ElectronicaViewSet(viewsets.ModelViewSet):
    queryset = Electronica.objects.all()
    serializer_class = ElectronicaSerializer

    def get_permissions(self):
        if self.action == 'post' or self.action == 'put' or self.action == 'delete':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
