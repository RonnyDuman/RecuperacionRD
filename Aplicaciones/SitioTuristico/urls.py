from django.urls import path
from . import views


urlpatterns = [
    path('', views.listaSitios, name='inicio'),
    path('lista/', views.listaSitiosT, name='lista'),                     
    path('nuevo/', views.mostrarSitio, name='mostrarCrear'),  
    path('nuevoST/', views.procesarCreacionSitio, name='ejecutarCrear'),                 
    path('editar/<int:pk>', views.editarSitio, name='mostrarEditar'),
    path('editarST/<int:pk>', views.procesarEdicionSitio, name='ejecutarEditar'),     
    path('eliminar/<int:pk>', views.eliminarSitio, name='eliminar'),

    #rutas para el inicio de sesion
    path('Iniciarlogin/', views.preserntarLogin, name='preserntarLogin'),
    path('login/', views.IniciarSesion, name='login'),

    path('pasarela/', views.sesionInicada, name='loginIn'),


    path('registro/', views.registro, name='registro'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('cerrar_sesion/', views.cerrar_sesion, name='logout'),

    #rutas para ver los dashboars

    path('dashboard/', views.dashboard, name='dashboard'),

    #ruta para enviar a telegram la notificaion
    path('dashboard/enviarImagenTelegram/', views.enviar_imagen_telegram),



]