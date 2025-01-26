import requests

# URL del servidor de Ollama
url = "http://localhost:11434/api/generate"

# Prompt inicial que define el rol del asistente
prompt_init = """Eres un asistente virtual especializado en ayudar a los usuarios con los servicios web de SportZone. 
Tu tarea es responder preguntas de manera amigable y profesional, proporcionar información sobre los servicios 
disponibles y guiar a los usuarios en el uso de la plataforma.

Instrucciones específicas:
1. Responde siempre en español.
2. La empresa se llama SportZone.
3. Si el usuario hace una pregunta que no está relacionada con SportZone o sus servicios web, responde de manera educada y redirige la conversación hacia temas relacionados con la aplicación web. Por ejemplo:
   - "Lo siento, solo puedo ayudarte con temas relacionados con SportZone y nuestra aplicación web. ¿En qué más puedo ayudarte respecto a nuestros servicios?"
4. Sé claro, conciso y amigable en tus respuestas.
"""
model = "deepseek-r1:7b"
# Enviar el prompt inicial solo una vez
initial_payload = {
    "model": model,
    "prompt": prompt_init,
    "stream": False
}
response = requests.post(url, json=initial_payload)

if response.status_code != 200:
    print("Error al inicializar el asistente:", response.text)
    exit()
try:
    # Bucle interactivo
    while True:
        # Solicitar la entrada del usuario
        user_input = input("\nTú: ")
        
        # Salir del bucle si el usuario escribe "salir"
        if user_input.lower() == "salir":
            print("¡Hasta luego!")
            break

        # Crear el payload con solo la pregunta actual
        payload = {
            "model": model,
            "prompt": user_input,  # Solo envía la pregunta actual
            "stream": False
        }

        # Enviar la solicitud POST al servidor de Ollama
        response = requests.post(url, json=payload)

        # Obtener la respuesta del modelo
        if response.status_code == 200:
            response_data = response.json()
            print("\nAsistente:", response_data["response"])
        else:
            print("Error:", response.status_code, response.text)

finally:
    # Detener el modelo cuando el script termine
    
    stop_url = "http://localhost:11434/api/stop"
    stop_payload = {"model": model}
    stop_response = requests.post(stop_url, json=stop_payload)
    
    if stop_response.status_code == 200:
        print("Modelo detenido correctamente.")
    else:
        print("Error al detener el modelo:", stop_response.text)
