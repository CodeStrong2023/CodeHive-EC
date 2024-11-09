from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.shortcuts import redirect

#Integracion carrito
import mercadopago
from django.conf import settings
from django.shortcuts import render




def metodo_pago_1(request):
    return render(request,"pagos/metodoPago1.html")

def metodo_pago_2(request):
    return render(request,"pagos/metodoPago2.html")



def metodo_pago_mercadopago(request):
    # Inicializar el SDK de MercadoPago con el access_token
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    # Calcular el total de la compra sumando los productos en el carrito
    total_carrito = 0
    if 'carro' in request.session:
        for item in request.session['carro'].values():
            total_carrito += float(item['precio']) * int(item.get('cantidad', 1))

    # Crear la preferencia de pago con el total calculado
    preference_data = {
        "items": [
            {
                "title": "Total del carrito",
                "quantity": 1,
                "unit_price": total_carrito,
                "currency_id": "ARS"  # Usa la moneda que estés usando
            }
        ],
        "back_urls": {
            "success": "http://tu-dominio.com/success",
            "failure": "http://tu-dominio.com/failure",
            "pending": "http://tu-dominio.com/pending"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)  # Creación de la preferencia
    preference = preference_response["response"]

    # Pasar la public_key y preference_id al template
    context = {
        "preference_id": preference['id'],
        "public_key": settings.MERCADO_PAGO_PUBLIC_KEY
    }

    return render(request, 'pagos/checkout.html', context)