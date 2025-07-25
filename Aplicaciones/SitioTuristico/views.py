from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import SitioTuristico
import os
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.hashers import make_password, check_password
import random
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
import base64
from io import BytesIO
from PIL import Image
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.

#Definimos la funcion listaSitios
def listaSitios(request):
    return render(request, 'index.html')

#Definimos la funcion listaSitiosT
def listaSitiosT(request):
    sitios = SitioTuristico.objects.all()
    return render(request, 'principal.html', {'sitios': sitios})

#Definimos la funcion MostrarSitios
def mostrarSitio(request):
    return render(request, 'crear.html')

#Definimos la funcion procesarCreacionSitio
def procesarCreacionSitio(request):
     # Obtener los datos enviados desde el formulario mediante POST
    pais = request.POST.get('pais')
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')

    # Convertir el valor recibido de requiere_visa a booleano
    requiere_visa = request.POST.get('requiere_visa') == 'True'

    # Obtener archivos subidos por el usuario desde el formulario (imágenes y PDF)
    foto_principal = request.FILES.get('foto_principal')
    foto_secundaria = request.FILES.get('foto_secundaria')
    historia_pdf = request.FILES.get('historia_pdf')

    # Otros campos del formulario
    fecha_fundacion = request.POST.get('fecha_fundacion')
    email_contacto = request.POST.get('email_contacto')
    telefono_contacto = request.POST.get('telefono_contacto')

    # Crear una instancia del modelo SitioTuristico con los datos obtenidos
    sitio = SitioTuristico(
        pais=pais,
        nombre=nombre,
        descripcion=descripcion,
        requiere_visa=requiere_visa,
        foto_principal=foto_principal,
        foto_secundaria=foto_secundaria,
        historia_pdf=historia_pdf,
        fecha_fundacion=fecha_fundacion,
        email_contacto=email_contacto,
        telefono_contacto=telefono_contacto
    )