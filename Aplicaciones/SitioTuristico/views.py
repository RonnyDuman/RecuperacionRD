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
    sitio.save()
    messages.success(request, '¡El sitio turístico se agregó correctamente!')

    return redirect('lista')

#Definimos la funcion editarSitio
def editarSitio(request, pk):
    sitio = get_object_or_404(SitioTuristico, pk=pk)
    return render(request, 'editar.html', {'sitio': sitio})

#Definimos la funcion procesarEdicionSitio
def procesarEdicionSitio(request, pk):
    sitio = get_object_or_404(SitioTuristico, pk=pk)

    # Asignar los nuevos valores de los campos básicos del formulario al objeto sitio
    sitio.pais = request.POST.get('pais')
    sitio.nombre = request.POST.get('nombre')
    sitio.descripcion = request.POST.get('descripcion')
    sitio.requiere_visa = request.POST.get('requiere_visa') == 'True'
    sitio.fecha_fundacion = request.POST.get('fecha_fundacion')
    sitio.email_contacto = request.POST.get('email_contacto')
    sitio.telefono_contacto = request.POST.get('telefono_contacto')

    # Procesar actualización de la foto principal si se ha enviado una nueva
    nueva_foto_principal = request.FILES.get('foto_principal')
    if nueva_foto_principal:

        # Eliminar el archivo anterior si existe físicamente en el sistema
        if sitio.foto_principal and os.path.isfile(sitio.foto_principal.path):
            os.remove(sitio.foto_principal.path)

        # Asignar la nueva imagen
        sitio.foto_principal = nueva_foto_principal

        # Procesar actualización de la foto secundaria si se ha enviado una nueva
    nueva_foto_secundaria = request.FILES.get('foto_secundaria')
    if nueva_foto_secundaria:
        if sitio.foto_secundaria and os.path.isfile(sitio.foto_secundaria.path):
            os.remove(sitio.foto_secundaria.path)
        sitio.foto_secundaria = nueva_foto_secundaria

        # Procesar actualización del archivo PDF si se ha enviado uno nuevo
    nuevo_pdf = request.FILES.get('historia_pdf')
    if nuevo_pdf:
        if sitio.historia_pdf and os.path.isfile(sitio.historia_pdf.path):
            os.remove(sitio.historia_pdf.path)
        sitio.historia_pdf = nuevo_pdf

        # Guardar los cambios realizados al objeto sitio en la base de datos
    sitio.save()

        # Mostrar un mensaje de éxito al usuario
    messages.success(request, '¡El sitio turístico se actualizó correctamente!')

    # Redireccionar a la vista que lista los sitios turísticos
    return redirect('lista')

#Definimos la funcion eliminarSitio
def eliminarSitio(request, pk):
    sitio = get_object_or_404(SitioTuristico, pk=pk)

# Verifica si existe una foto principal asociada y la elimina del sistema de archivos
    if sitio.foto_principal and os.path.isfile(sitio.foto_principal.path):
     os.remove(sitio.foto_principal.path)

     # Verifica si existe una foto secundaria asociada y la elimina del sistema de archivos
    if sitio.foto_secundaria and os.path.isfile(sitio.foto_secundaria.path):
     os.remove(sitio.foto_secundaria.path)
     # Verifica si existe un archivo PDF asociado y lo elimina del sistema de archivos
    if sitio.historia_pdf and os.path.isfile(sitio.historia_pdf.path):
     os.remove(sitio.historia_pdf.path)