from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..utils import get_response  # Importamos la función de respuesta desde utils.py
from django.shortcuts import render
import json


class ChatbotView(View):


    def post(self, request, *args, **kwargs):
        try:
            # Parsear el cuerpo de la solicitud
            body = json.loads(request.body)
            user_message = body.get('message', '')

            if not user_message:
                return JsonResponse({'error': 'No se proporcionó ningún mensaje.'}, status=400)

            # Llamar a la función en utils.py para obtener la respuesta
            bot_response = get_response(user_message)
            print(f"Contenido de request.body: {request.body}")

            # Devolver la respuesta en formato JSON
            return JsonResponse({'response': bot_response}, status=200)
        except Exception as e:
            # Manejo de errores
            return JsonResponse({'error': f'Ocurrió  error: {str(e)}'}, status=500)

    def get(self, request, *args, **kwargs):
        # Opcionalmente puedes manejar GET si es necesario
        return JsonResponse({'error': 'Método GET no permitido.'}, status=405)