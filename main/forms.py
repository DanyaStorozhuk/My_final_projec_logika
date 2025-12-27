from django import forms
from main.models import Comments, Order, Restaurant, Workers, Menu, CustomUser, MenuOrder, Special, MenuOrder
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["email", "role", "phone"]



class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name","address", "time_opening_restoran", "title", "contact_admin", "opening_time", "closing_time"]


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["author", "text", "rating"]
    
class WorkersForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = ["role", "name","photo", "rating"]

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "type1","type2", "title", "photo", "price"]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user","time", "phone", "guests_count"]
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class OrderFormMenu(forms.ModelForm):
    menu_items = forms.ModelChoiceField(
        queryset=Menu.objects.all(),
        label="Обрати страву",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = MenuOrder
        fields = ["menu_items", "customer", "phone", "street", "pay"]




class OrderFood(forms.ModelForm):
    class Meta:
        model = MenuOrder
        fields = ["name","type1","type2","customer", "phone", "street", "pay",]
   
