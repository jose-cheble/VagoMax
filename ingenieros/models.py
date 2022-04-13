from platform import mac_ver
from pyexpat import model
from turtle import colormode
from urllib import request
from django.db import models
from django.utils.text import slugify
from datetime import datetime
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from os import getenv


# Create your models here.

class EngineerModel(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=40, null=True)
    email = models.EmailField()
    validated_user = models.BooleanField(null=False, default=False)

    def __str__(self) -> str:
        return f"{self.user_name} - {self.email}"


class AdministracionModel(models.Model):
    nombre_adm = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=100)
    direccion = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.nombre_adm} - {self.direccion}"

class EquiposModel(models.Model):
    nombre_edif = models.CharField(max_length=50)
    calle = models.CharField(max_length=50)
    equipo_numero = models.IntegerField()
    slug = models.SlugField(unique=True)
    ingeniero = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    administracion = models.ManyToManyField(AdministracionModel)
    pagina_numero = models.IntegerField()
    qr = models.ImageField(upload_to="qrcodes",blank=True)

    def save(self, *args, **kwargs):
        # To autopopulate the slug field
        self.slug = slugify(self.calle + " E" + str(self.equipo_numero))
        # To create the QR code automatically
        qrcode_image = qrcode.make( "http://127.0.0.1:8000/ingenieros/mis-equipos/"+str(self.slug))
        canvas = Image.new("RGB", (qrcode_image.pixel_size, qrcode_image.pixel_size))
        canvas.paste(qrcode_image)
        fname = f"{self.slug}-qr"+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr.save(fname, File(buffer), save=False)
        canvas.close
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.nombre_edif} - {self.calle} - {self.equipo_numero}"


class InspeccionesModel(models.Model):
    fecha = models.DateTimeField(default=datetime.now)
    observacion = models.TextField()
    equipo = models.ForeignKey(EquiposModel, on_delete=models.CASCADE, related_name="inspections")


# class PruebasDeSeguridadModel(models.Model):
#     fecha = models.DateTimeField(default=datetime.now)
#     observacion = models.TextField()
#     equipo = models.ForeignKey(EquiposModel, on_delete=models.CASCADE, related_name="inspections")


    



    
