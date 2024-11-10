"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include #necesario para traer las url de las apps
from django.http import HttpResponse #importo el httresponse, para agregar una funcion y crear una url momentanea
"""def home(request):
    return HttpResponse("Bienvenido a la página principal")"""

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('GestionUsuarios.urls')),#url de la aplicacion gestion usuarios
    path('', include('InterfazGeneral.urls')), #url interfaz
    path('carrito/', include('Carrito.urls')),  # Incluir las URLs del carrito
    path('pagos-y-pedidos/', include('PagosyPedidos.urls')),# Incluir las URLs de los pedidos 
    path('producto/', include('producto.urls')),  # URL para la aplicación Productos
    path('pagos/', include(('pagos.urls', 'pagos'), namespace='pagos')),  # URL para la aplicación Productos

   

]

