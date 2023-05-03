import express from "express";

const servidor = express();

servidor.listen(8000, () => {
  console.log("Servidor levantado en el puerto 8000");
});
