from django.urls import path
from . import views


app_name="pagos"

urlpatterns = [
    path('metodo1/', views.metodo_pago_1, name='metodo_pago_1'),#Metodos de pago. 
    path('metodo2/', views.metodo_pago_2, name='metodo_pago_2'),
    path('metodo_pago/', views.metodo_pago_mercadopago, name='metodo_pago'),

]
