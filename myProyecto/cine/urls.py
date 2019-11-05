#tendra todas las url del sitio web
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name='HOME'),
    path('galeria/',galeria,name='GALE'),
    path('formulario/',formulario2,name='FORMU'),
    path('quienes_somos/',quienes_somos,name='QUIEN'),  
    path('eliminar_pelicula/<id>/',eliminar_pelicula,name='ELIMINAR'),
    path('login/',login,name='LOGIN'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRAR_SESION'),
    path('login_iniciar/',login_iniciar,name='LOGIN_INICIAR'),
    path('agregar_carro/<id>/',agregar_carro,name='AGREGAR_CARRO'),
    path('carrito/',carrito,name='CARRITO'),
    path('vaciar_carrito/',vacio_carrito,name='VACIARCARRITO'),
]