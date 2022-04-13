from cProfile import label
from email.policy import default
from tkinter import Label
from xml.dom.minidom import AttributeList
from django import forms
from .models import EquiposModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class NuevoEquipoForm(forms.ModelForm):
    pagina_numero = forms.IntegerField(
        max_value=46,
        min_value=11,
    )

    equipo_numero = forms.IntegerField(
        min_value=1
    )

    slug = forms.SlugField(label="slug-label", required=False, widget=forms.TextInput(attrs={'type':'hidden'}))
    

    class Meta:
        model = EquiposModel
        exclude = ['qr', 'ingeniero']
        labels = {
            "nombre_edif": "Nombre del Edificio",
            "calle": "Calle N°",
            "equipo_numero": "Equipo N°",
            "ingeniero": "Ingeniero",
            "administracion": "Administracion",
            "pagina_numero": "Pagina N°",
        }



        error_messages = {
            "pagina_numero": {
                'min_value': ("La pagina no puede ser menor a 11"),
                'max_value': ("La pagina no puede ser mayor a 46"),
            },
            "equipo_numero": {
                'min_value': ("El N° de equipo no puede ser menor a E01")
            }
        }

        

class NuevaInspeccionForm(forms.Form):
    observacion = forms.CharField(label="Observaciones", widget=forms.Textarea)
    pagina = forms.IntegerField(label="Página N°", max_value=46, min_value=11)


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=50)
    last_name = forms.CharField(label="Apellido", max_length=100)
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirma contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

        error_messages = {
            "username": {
                'unique': ("El nombre de usuario ya exist")}}