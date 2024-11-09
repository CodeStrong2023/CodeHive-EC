from django.db import models





class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_id = models.IntegerField()
    usuario_nombre = models.CharField(max_length=255)
    total = models.FloatField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - Usuario {self.usuario_nombre}"

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto_nombre = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    subtotal = models.FloatField()
    imagen = models.URLField()  # Almacena la URL de la imagen del producto

    def __str__(self):
        return f"{self.producto_nombre} - Pedido {self.pedido.id}"
