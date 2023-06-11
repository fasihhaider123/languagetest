from django import forms
from .models import *
class UserRegisteration(forms.ModelForm):
    
    class Meta:
        model = AppUser
        fields  = '__all__'
     
        

class AudioForm(forms.ModelForm):
    
    class Meta:
        model = AudioData
        fields  = '__all__'
     