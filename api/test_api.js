const axios = require('axios');

const BASE_URL = 'http://localhost:3000/api/mensaje'; // Cambia el puerto si usas otro, o pon la URL de Vercel

async function testPostMensaje() {
  try {
    const res = await axios.post(BASE_URL, { mensaje: 'Mensaje de prueba POST' });
    console.log('POST:', res.data);
  } catch (err) {
    console.error('Error POST:', err.response ? err.response.data : err.message);
  }
}

async function testGetMensaje() {
  try {
    const res = await axios.get(BASE_URL + '?mensaje=Mensaje%20de%20prueba%20GET');
    console.log('GET:', res.data);
  } catch (err) {
    console.error('Error GET:', err.response ? err.response.data : err.message);
  }
}

async function main() {
  await testPostMensaje();
  await testGetMensaje();
}

main();
