from django.urls import path
from . import views


app_name="pagos"

urlpatterns = [
    
    path('metodo_pago/', views.metodo_pago_mercadopago, name='metodo_pago'),

]
