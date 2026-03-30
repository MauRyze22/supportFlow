from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class UserCustomForm(UserCreationForm):
    email = forms.EmailField(required=True)
    numero = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit = False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ['usuario']
        widgets = {
            'foto': forms.FileInput(),
            'biografia': forms.Textarea(attrs={'rows':4})    
        }
    
    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.usuario.email = self.cleaned_data['email']
        if commit:
            perfil.save()
            perfil.usuario.save()
        return perfil