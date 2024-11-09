from django.shortcuts import redirect,render
from PagosyPedidos.models import Pedido, PedidoDetalle
from datetime import datetime
import mercadopago
from django.conf import settings

def metodo_pago_mercadopago(request):
    # Guardar el pedido en la base de datos
    if 'carro' in request.session:
        carro = request.session['carro']
        usuario_id = request.session.get('user_id')
        usuario_nombre = request.session.get('username')

        # Calcular el total del pedido
        total = sum(float(item['precio']) * int(item['cantidad']) for item in carro.values())

        # Crear el pedido
        pedido = Pedido.objects.create(
            usuario_id=usuario_id,
            usuario_nombre=usuario_nombre,
            total=total,
            fecha_pedido=datetime.now()
        )

        # Crear detalles del pedido
        for item in carro.values():
            PedidoDetalle.objects.create(
                pedido=pedido,
                producto_nombre=item['nombre'],
                cantidad=item['cantidad'],
                precio_unitario=float(item['precio']),
                subtotal=float(item['precio']) * int(item['cantidad']),
                imagen=item['imagen']
            )

    # Inicializar el SDK de MercadoPago
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    # Crear la preferencia de pago con el total calculado
    preference_data = {
        "items": [
            {
                "title": "Compra Total",
                "quantity": 1,
                "unit_price": total,
                "currency_id": "ARS",
            }
        ],
        "back_urls": {
            "success": "http://tu-dominio.com/success",
            "failure": "http://tu-dominio.com/failure",
            "pending": "http://tu-dominio.com/pending"
        },
        "auto_return": "approved",
    }

    # Crear la preferencia
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    # Pasar la public_key y preference_id al template
    context = {
        "preference_id": preference['id'],
        "public_key": settings.MERCADO_PAGO_PUBLIC_KEY
    }

    return render(request, 'pagos/checkout.html', context)
