from django.shortcuts import redirect
from .models import Pedido, PedidoDetalle
from datetime import datetime

def guardar_pedido(request):
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

        # Redireccionar o realizar alguna acción
        return redirect('pedido_exitoso')
