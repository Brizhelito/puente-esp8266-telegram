require("dotenv").config();
const express = require("express");
const axios = require("axios");

const app = express();
// Middleware para parsear JSON
app.use(express.json());

// Ruta para recibir mensajes del ESP8266
// Vercel redirigirá las solicitudes de /api/mensaje aquí
app.post("/api/mensaje", async (req, res) => {
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
      text: `📡 Mensaje del ESP8266:\n\n${mensaje}`,
    });

    res.status(200).json({ status: "Mensaje enviado a Telegram" });
  } catch (error) {
    console.error("Error al enviar a Telegram:", error.message);
    res.status(500).json({
      error: "Error al enviar el mensaje",
      details: error.message,
    });
  }
});

// Endpoint GET para enviar mensajes usando query params
app.get("/api/mensaje", async (req, res) => {
  const { mensaje } = req.query;

  if (!mensaje) {
    return res.status(400).json({ error: "Falta el parámetro mensaje en la query" });
  }

  try {
    console.log("Mensaje recibido por GET:", mensaje);

    // Enviar mensaje a Telegram
    const telegramUrl = `https://api.telegram.org/bot${process.env.TELEGRAM_TOKEN}/sendMessage`;
    await axios.post(telegramUrl, {
      chat_id: process.env.CHAT_ID,
      text: `📡 Mensaje del ESP8266 (GET):\n\n${mensaje}`,
    });

    res.status(200).json({ status: "Mensaje enviado a Telegram" });
  } catch (error) {
    console.error("Error al enviar a Telegram:", error.message);
    res.status(500).json({
      error: "Error al enviar el mensaje",
      details: error.message,
    });
  }
});

// Exportar la app para Vercel
module.exports = app;
