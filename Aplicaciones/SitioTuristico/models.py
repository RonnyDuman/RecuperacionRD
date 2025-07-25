from django.db import models

# Create your models here.

# Creamos el modelo SitioTuristico
class SitioTuristico(models.Model):
    pais = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    requiere_visa = models.BooleanField(default=False)
    foto_principal = models.FileField(upload_to='sitios/fotos_principales/')
    foto_secundaria = models.FileField(upload_to='sitios/fotos_secundarias/')
    historia_pdf = models.FileField(upload_to='sitios/historias/')
    fecha_fundacion = models.DateField()
    email_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

#Creamos el modelo Usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)