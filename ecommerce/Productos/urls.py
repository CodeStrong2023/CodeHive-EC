from django.urls import path
from . import views


app_name = 'producto' #Se crea namespace para poder acceder a estas URLs desde templates que no le pertenecen a la app

urlpatterns = [
    path('api/catalogo/', views.api_mostrar_catalogo, name='api_mostrar_catalogo'),
    path('api/producto/<int:producto_id>/', views.api_detalle_producto, name='api_detalle_producto'),
    path('api/buscar/', views.api_buscar_productos, name='api_buscar_productos'),
    path('api/categorias/', views.filtrar_productos, name='api_obtener_categorias'),
    path('api/juegos/', views.api_ver_juegos, name='api_ver_juegos'),
    path('api/filtrar-precio/', views.filtrar_por_precio, name='filtrar_por_precio'),
    
]
 #comentario