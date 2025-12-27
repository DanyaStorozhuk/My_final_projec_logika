from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from .models import Comments, Restaurant, CustomUser, Order, Workers, Menu, Special
from main.forms import CustomUserForm, CommentsForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from main import urls
from django.templatetags.static import static
from .forms import OrderForm, WorkersForm, CommentsForm, MenuForm, MenuOrder, OrderFormMenu, OrderFood
from main.mixings import UserAdminMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
##################################################################################

def not_login_user(request):
    if not request.user.is_authenticated:
        return render(request, "not_login_user.html")


def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:home-page')

    else:
        form = CustomUserForm()

    return render(request, 'register.html', {'form': form})



def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main:start_page')
    else:
        form = AuthenticationForm() 

    return render(request, 'registration/login.html', {'form': form})

################################################################################

class CustomUserCreateView(CreateView):
    model = CustomUser
    context_object_name = 'customuser'
    template_name = 'register.html'


class RestaurantView(TemplateView):
    model = Restaurant
    context_object_name = 'restaurant'
    template_name = 'home.html'

#----------------------------------------------------
class OrderList(ListView):
    model = Order
    context_object_name = 'order'
    template_name = 'order_users.html'

    def get_queryset(self):
        return Order.objects.exclude(status='cancelled')
    

class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    context_object_name = "context_order"
    template_name = 'order.html'
    success_url = reverse_lazy('main:order')


class OrderUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['status']
    success_url = reverse_lazy('main:order')

    def test_func(self):
        return self.request.user.role == 'admin'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("У вас немає прав на зміну статусу!")
    
    
#----------------------------------------------------

class ReviewsListView(ListView):
    model = Comments
    context_object_name = 'comments'
    template_name = 'comments_list.html'


class ReviewsCreateView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentsForm
    template_name = 'comments.html'
    success_url = reverse_lazy('main:comments-create')

#---------------------------------------------------
class WorkersListView(ListView):
    model = Workers
    context_object_name = 'workers'
    template_name = 'workers_list.html'


class WorkersCreateView(UserAdminMixin, CreateView):
    model = Workers
    form_class = WorkersForm
    context_object_name = 'workers'
    template_name = 'workers.html'
    success_url = reverse_lazy('main:workers-create')


#----------------------------------------------------



class MenuListView(ListView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu_list.html'




class MenuCreateView(UserAdminMixin, CreateView):
    model = Menu
    form_class = MenuForm
    template_name = 'menu.html'
    success_url = reverse_lazy('main:menu-create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.all()
        return context

#----------------------------------------------------



class MenuOrderView(LoginRequiredMixin, CreateView):
    model = MenuOrder
    form_class = OrderFormMenu
    context_object_name = 'order-menu'
    template_name = 'order_menu.html'
    success_url = reverse_lazy('main:order_menu')



class HomeView(TemplateView):
    template_name = 'home.html'

#---------------------------------------------------------

class SpecialList(LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = 'special'
    template_name = 'special.html'
    
    def get_queryset(self):
        return self.request.user.favorite.all()


class AddSpecial(LoginRequiredMixin, View):
    def get(self, request, pk):
        i = get_object_or_404(Menu, pk=pk)
        request.user.favorite.add(i)
        return redirect("main:special")
    
#-----------------------------------------------------------

class StartView(TemplateView):
    template_name = 'start_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aurum_logo_url'] = static('img/aurun.img.png')
        context["menu"] = Menu.objects.all()
        return context
    
#------------------------------------------------------------

class MoreInformation(TemplateView):
    template_name = 'more_information.html'

#-------------------------------------------------------------
class OrderUpdateFood(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MenuOrder
    fields = ['status']
    success_url = reverse_lazy('main:start_page')

    def test_func(self):
        return self.request.user.role == 'admin'
    
    def handle_no_permission(self):
        return HttpResponseForbidden("У вас немає прав на зміну статусу!")
    
    
    
    
class OrderFoodList(LoginRequiredMixin, ListView):
    model = MenuOrder
    form_class = OrderFood
    context_object_name = "orderfood"
    template_name = 'order_food.html'
    success_url = reverse_lazy('main:order')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(status="cancelled")
        return queryset