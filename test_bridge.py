import urequests
import time

def test_bridge():
    url = "http://puente-esp8266-telegram.vercel.app/api/mensaje"
    
    # Mensaje simple
    response = urequests.post(url, json={"mensaje": "Prueba desde Python"})
    print(f"Status: {response.status_code}, Respuesta: {response.text}")
    
    # Simular flujo de datos
    for i in range(1, 6):
        mensaje = f"Lectura {i}: {i*0.5} L/min"
        response = urequests.post(url, json={"mensaje": mensaje})
        print(f"Enviado: {mensaje} - Status: {response.status_code}")
        time.sleep(2)

if __name__ == "__main__":
    test_bridge()