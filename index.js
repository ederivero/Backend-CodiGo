import express from "express";

const PORT = 5000;
const app = express();

app.get("/", (req, res) => {
  res.json({
    message: "Hola desde docker",
  });
});

app.listen(PORT, () => {
  console.log(`Servidor corriendo exitosamente en el puerto ${PORT}`);
});
