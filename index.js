import express from "express";
import { Server } from "socket.io";
import { createServer } from "http";

const servidor = express();
const httpServidor = createServer(servidor);
const io = new Server(httpServidor, { cors: { origin: "*" } });
const historial = [];

io.on("connection", (cliente) => {
  console.log(cliente.id);
  cliente.emit("historial", historial);

  cliente.on("message", (argumentos) => {
    console.log(argumentos);
    historial.push({ ...argumentos, hora: new Date() });
    io.emit("historial", historial);
  });

  cliente.emit("saludo", { message: "Buenas!!!" });
  //   io.emit("saludo", { message: "Buenas!!!" });
});

httpServidor.listen(3000, () => {
  console.log("Servidor corriendo exitosamente");
});
