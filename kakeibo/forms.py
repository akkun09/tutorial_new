from django import forms	
from .models import Kakeibo,Category
from django.contrib.auth.forms import AuthenticationForm

	
class KakeiboForm(forms.ModelForm):	
   class Meta:	
       model = Kakeibo	
       fields =['date', 'category', 'money', 'memo']  	

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['category_name']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label