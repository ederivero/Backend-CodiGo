import express from "express";
import cors from "cors";
import morgan from "morgan";
import { itemRouter } from "./routes/items.routes.js";

const servidor = express();
servidor.use(
  cors({
    origin: ["http://127.0.0.1:5500"],
    methods: "GET, DELETE, POST",
    allowedHeaders: ["Authorization", "Content-Type"],
  })
);
servidor.use(morgan("combined"));
// middleware
// antes de ir al controlador final pasara por aca
servidor.use(express.json());
servidor.use(itemRouter);

const PORT = 3000;

servidor.get("/inicio", (req, res) => {
  res.json({
    message: "Bienvenido a mi API con cambios",
  });
});

servidor.listen(PORT, () => {
  console.log("Servidor corriendo exitosamente");
});
