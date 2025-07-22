from machine import Pin, I2C, Timer
import ssd1306
import time
import network
import gc
import urequests
import ujson

# ================= CONFIGURACIÓN =================
OLED_SCL = 12
OLED_SDA = 14
RELE_PIN = 2
FLUJO_PIN = 13

LINEA_SUPERIOR = 8
LINEA_FLUJO = 25
LINEA_BOMBA = 45
TEXTO_FIJO = " L/min"

WIFI_SSID = "FTT"
WIFI_PASS = "20252025"

# URL del puente en Vercel (reemplazar con tu URL)
VERCEL_BRIDGE_URL = "http://your-vercel-app-name.vercel.app/api/mensaje"

# ================= INICIALIZACIÓN OLED =================
def init_oled():
    try:
        i2c = I2C(scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=100000)
        oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        oled.text("Sistema Iniciado", 0, LINEA_SUPERIOR)
        oled.show()
        return oled
    except Exception as e:
        print(f"Error OLED: {e}")
        return None

oled = init_oled()

# ================= HARDWARE =================
rele = Pin(RELE_PIN, Pin.OUT, value=1)
flujo_pin = Pin(FLUJO_PIN, Pin.IN, Pin.PULL_UP)
pulsos = 0
PULSOS_POR_LITRO = 450

# ================= INTERRUPCIÓN FLUJO =================
def contar_pulsos(pin):
    global pulsos
    pulsos += 1
flujo_pin.irq(trigger=Pin.IRQ_FALLING, handler=contar_pulsos)

# ================= WIFI =================
def conectar_wifi():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        print("Conectando WiFi...")
        if oled:
            oled.fill(0)
            oled.text("Conectando WiFi...", 0, LINEA_SUPERIOR)
            oled.show()
        sta.connect(WIFI_SSID, WIFI_PASS)
        for _ in range(20):
            if sta.isconnected():
                break
            time.sleep(0.5)
    if sta.isconnected():
        ip = sta.ifconfig()[0]
        print(f"WiFi OK: {ip}")
        if oled:
            oled.fill(0)
            oled.text("IP:", 0, LINEA_SUPERIOR)
            oled.text(ip, 0, LINEA_SUPERIOR + 10)
            oled.show()
        return True
    else:
        print("Error WiFi")
        if oled:
            oled.fill(0)
            oled.text("Error WiFi", 0, LINEA_SUPERIOR)
            oled.show()
        return False

# ================= COMUNICACIÓN TELEGRAM =================
def enviar_a_telegram(mensaje):
    try:
        headers = {'Content-Type': 'application/json'}
        data = ujson.dumps({"mensaje": mensaje})
        response = urequests.post(VERCEL_BRIDGE_URL, data=data, headers=headers)
        response.close()
        print(f"Mensaje enviado a Telegram: {mensaje}")
        return True
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")
        return False

# ================= SISTEMA PRINCIPAL =================
ultima_alerta_telegram = 0

def actualizar_sistema(timer):
    global pulsos, ultima_alerta_telegram
    try:
        gc.collect()
        flujo = min(999.99, round((pulsos / PULSOS_POR_LITRO) * 60, 2))
        pulsos = 0

        if oled:
            oled.fill(0)
            oled.text("Flujo:", 0, LINEA_FLUJO)
            flujo_texto = f"{flujo:6.2f}"
            oled.text(flujo_texto, 48, LINEA_FLUJO)
            oled.text(TEXTO_FIJO, 90, LINEA_FLUJO)
            oled.text(f"Bomba: {'ON' if rele.value()==0 else 'OFF'}", 0, LINEA_BOMBA)
            oled.show()

        # Alerta por flujo bajo a Telegram (cada 5 minutos)
        if 0 < flujo < 1.0 and time.ticks_diff(time.ticks_ms(), ultima_alerta_telegram) > 300000:
            mensaje_alerta = f"ALERTA: Flujo bajo detectado: {flujo} L/min"
            if enviar_a_telegram(mensaje_alerta):
                ultima_alerta_telegram = time.ticks_ms()

    except Exception as e:
        print(f"Error en actualización: {e}")

# ================= INICIO =================
if conectar_wifi():
    print("Iniciando sistema principal...")
    timer = Timer(-1)
    timer.init(period=1000, mode=Timer.PERIODIC, callback=actualizar_sistema)
    try:
        while True:
            time.sleep(1) # Ahorro de energía
    except KeyboardInterrupt:
        timer.deinit()
        rele.value(1)
        print("Sistema detenido")
