from django import forms
from .models import Customer, Mover, Order, Photo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'location', 'phone']  
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['origin', 'origin_location', 'destination', 'destination_location', 'need_pro_mover', 'need_box_packer', 'move_date']

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class MoverForm(forms.ModelForm):
    class Meta:
        model = Mover
        fields = ['name', 'location', 'phone', 'vehicle_type', 'mover_type']  # حذف فیلد last_name
