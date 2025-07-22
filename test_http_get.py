import urequests

# Cambia esta URL si tu endpoint es diferente
target_url = "http://puente-esp8266-telegram.vercel.app/api/mensaje"

# Mensaje de prueba
def test_mensaje_get():
    mensaje = "Mensaje de prueba desde test_http_get.py"
    url = f"{target_url}?mensaje={mensaje}"
    print(f"Enviando GET a: {url}")
    try:
        response = urequests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Respuesta: {response.text}")
        response.close()
    except Exception as e:
        print(f"Error al enviar GET: {e}")

if __name__ == "__main__":
    test_mensaje_get()
