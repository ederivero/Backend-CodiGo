const socket = io("http://127.0.0.1:3000");
const mensaje = document.getElementById("mensaje");
const mensajes = document.getElementById("mensajes");

mensajes.scrollIntoView(false);
let id;
socket.on("connect", () => {
  id = socket.id;
  console.log(socket.id);
});

mensaje.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    socket.emit("message", { usuario: id, mensaje: mensaje.value });
    mensaje.value = "";
  }
});

socket.on("historial", (data) => {
  mensajes.innerHTML = "";
  data.forEach((element) => {
    const div = document.createElement("div");
    const paragraph = document.createElement("p");

    paragraph.innerText = `${element.usuario} dice (${element.hora}): ${element.mensaje}`;
    div.appendChild(paragraph);
    mensajes.appendChild(div);
  });
});

socket.on("saludo", (argumentos) => {
  console.log(argumentos);
});
