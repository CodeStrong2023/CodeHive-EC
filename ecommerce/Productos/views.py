from django.shortcuts import render
from Carrito.carrito import Carro
from GestionUsuarios.models import Producto, Categoria, Juego, Detalles
from django.db.models import Q
from django.http import JsonResponse

def api_mostrar_catalogo(request):
    categorias_seleccionadas = request.GET.getlist('categoria')  # Obtiene las categorías seleccionadas
    productos = filtrar_productos(categorias=categorias_seleccionadas)  # Filtra según categorías

    return render(request, 'Productos/catalogo.html', {
        'productos': productos,
        'categorias_seleccionadas': categorias_seleccionadas
    })



#def api_detalle_producto(request, producto_id):
  #  producto = Producto.objects.filter(id=producto_id).values(
    #    'id', 'nombre', 'descripcion', 'stock', 'categoria__tipo', 'juego__nombre'
   # ).first()

    #if producto:
    #    return JsonResponse(producto, safe=False)
  #  else:
    #    return JsonResponse({'error': 'Producto no encontrado'}, status=404)


def api_detalle_producto(request, producto_id):
    # Obtén el objeto Producto completo, no solo un diccionario
    producto = Producto.objects.select_related('categoria', 'juego').filter(id=producto_id).first()

    # Verifica si el producto existe
    if not producto:
        return render(request, 'Productos/producto_no_encontrado.html')

    # Verifica si el producto ya está en el carrito
    carro = Carro(request)
    producto_en_carro = str(producto.id) in carro.carro  # Cambiado de producto['id'] a producto.id

    return render(request, 'Productos/ver_producto.html', {'producto': producto, 'producto_en_carro': producto_en_carro})
    



def api_ver_juegos(request):
    juegos = Juego.objects.all()

    juegos_list = []
    for juego in juegos:
        juegos_list.append({
            'id': juego.id,
            'logo': juego.logo if juego.logo else None,  
            'plataforma': juego.plataforma,
            'nombre': juego.nombre,
            'url_pagina': juego.url_pagina,
        })

    return JsonResponse({'juegos': juegos_list})


def api_buscar_productos(request):
    query = request.GET.get('q', '')
    categoria = request.GET.get('categoria_id', '') 
    juego = request.GET.get('juego_id', '')  
    precio_min = request.GET.get('precio_min', 0)  
    precio_max = request.GET.get('precio_max', 100000)  

    productos = Producto.objects.all().values('id', 'nombre', 'descripcion', 'categoria__arma', 'categoria__armadura', 'juego__nombre', 'precio')

    if query:
        productos = productos.filter(nombre__icontains=query)

    if categoria:
        productos = productos.filter(categoria_id=categoria)

    if juego:
        productos = productos.filter(juego_id=juego)

    productos = productos.filter(precio__gte=precio_min, precio__lte=precio_max)

    return JsonResponse(list(productos), safe=False)


def filtrar_productos(categorias):
    # Obtener todos los productos
    productos = Producto.objects.all().select_related('categoria')
    
    # Aplicar el filtro solo si hay categorías especificadas
    if categorias:
        query = Q()
        for categoria in categorias:
            query |= Q(categoria__tipo=categoria)  # Crear una condición OR para cada categoría
        productos = productos.filter(query)  # Aplicar el filtro de categoría
    
    return productos



def filtrar_por_precio(request):
    # Obtener los valores de precio_min y precio_max del GET
    precio_min = int(request.GET.get('precio_min', 500))  # Valor mínimo por defecto: 500
    precio_max = int(request.GET.get('precio_max', 100000))  # Valor máximo por defecto: 100000

    # Filtrar productos según el rango de precios
    productos = Producto.objects.filter(precio__gte=precio_min, precio__lte=precio_max)
    
    # Pasar los productos filtrados y los valores de precio al contexto
    return render(request, 'Productos/catalogo.html', {
        'productos': productos,
        'precio_min': precio_min,
        'precio_max': precio_max,
    })
