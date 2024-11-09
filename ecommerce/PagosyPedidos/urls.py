from django.urls import path

from . import views



urlpatterns = [
                path('',views.guardar_pedido,name="pedido_exitoso"),
                ]