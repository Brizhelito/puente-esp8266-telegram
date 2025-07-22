require("dotenv").config();
const express = require("express");
const axios = require("axios");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para parsear JSON
app.use(express.json());

// Ruta para recibir mensajes del ESP8266
app.post("/mensaje", async (req, res) => {
  const { mensaje } = req.body;

  if (!mensaje) {
    return res.status(400).json({ error: "Falta el campo mensaje" });
  }

  try {
    console.log("Mensaje recibido:", mensaje);

    // Enviar mensaje a Telegram
    const telegramUrl = `https://api.telegram.org/bot${process.env.TELEGRAM_TOKEN}/sendMessage`;
    await axios.post(telegramUrl, {
      chat_id: process.env.CHAT_ID,
      text: `📡 Mensaje del ESP8266:\n${mensaje}`,
    });

    res.json({ status: "Mensaje enviado a Telegram" });
  } catch (error) {
    console.error("Error al enviar a Telegram:", error.message);
    res.status(500).json({
      error: "Error al enviar el mensaje",
      details: error.message,
    });
  }
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Puente Telegram escuchando en http://localhost:${PORT}`);
  console.log(
    `Ruta para enviar mensajes: POST http://localhost:${PORT}/mensaje`
  );
});
