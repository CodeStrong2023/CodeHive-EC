import json  # Importamos el módulo json para trabajar con datos en formato JSON
from django.http import JsonResponse  # Importamos JsonResponse para enviar respuestas JSON
from django.shortcuts import render
from .models import Validacion  # Importamos el modelo Validacion
from django.contrib.auth.hashers import make_password  # Importamos para hash de contraseñas
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def registerUser(request):
   
    if request.method == 'POST':  # Verificamos que el método de la solicitud sea POST
        print(request.body.decode('utf-8')) #sin la aclaracion em mostraria solo bits
        #try:
            #data = json.loads(request.body)
        #print(data)  # Cargamos los datos del cuerpo de la solicitud en formato JSON
        #except json.JSONDecodeError:
            #return JsonResponse({'success': False, 'message': 'Datos JSON inválidos.'}, status=400)
        
        mail =  request.POST.get('register_email')   # obtenemso el crudo del html xD
        contraseña = request.POST.get('register_password') 
        confirmarContraseña=request.POST.get('confirm_password')

        if contraseña != confirmarContraseña:
            #return JsonResponse({'success': False, 'message': 'Contraseña incorrecta.'}, status=409)
          return render(request, 'GestionUsuarios/registro.html', {
                'error': 'Las contraseñas no coinciden.Vuelva a intentarlo',
                'register_password': contraseña  # Volver a rellenar el campo de correo
            })

        if Validacion.objects.filter(correo=mail).exists():  # Comprobamos si el correo ya existe en la base de datos
            return JsonResponse({'success': False, 'message': 'El correo ya está registrado.'}, status=409)

        # Creamos un objeto de tipo Validacion con los datos obtenidos
        nuevoUsuario = Validacion(correo=mail, contraseña=make_password(contraseña))  # Guardamos la contraseña de manera segura
        nuevoUsuario.save()  # Guardamos el nuevo usuario en la base de datos

        # Enviamos la respuesta de éxito al front con el código 201
        return JsonResponse({'success': True, 'message': 'Usuario registrado correctamente'}, status=201)

    # Si no es un método POST, devolvemos un error 405 (Method Not Allowed)
   
    return render(request,'GestionUsuarios/registro.html')




        

