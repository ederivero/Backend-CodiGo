import prisma from "@prisma/client";
import express from "express";

const conexion = new prisma.PrismaClient({ log: ["info"] });
const servidor = express();
const PORT = process.env.PORT ?? 3000;

servidor
  .route("/tareas")
  .post(async (req, res) => {
    const resultado = await conexion.tarea.create({
      data: {
        fechaVencimiento: new Date("2023-05-15"),
        nombre: "Ir a la piscina",
        descripcion: "Ir a nadar estilo libre",
        estado: prisma.EstadoTarea.PENDIENTE,
        usuarioId: 1,
      },
    });

    return res.json({
      message: "Tarea creada exitosamente",
      content: resultado,
    });
  })
  .get(async (req, res) => {
    const resultado = await conexion.tarea.findMany();

    return res.json({
      content: resultado,
    });
  })
  .put(async (req, res) => {
    const nuevaData = {
      nombre: "Ir a la biblioteca",
      descripcion: "Ir a la biblioteca con los lentes de lectura",
      estado: prisma.EstadoTarea.CANCELADO,
    };

    const tareaActualizada = await conexion.tarea.update({
      data: nuevaData,
      where: { id: 1 },
    });

    return res.json({
      data: tareaActualizada,
      message: "Tarea actualizada exitosamente",
    });
  })
  .delete(async (req, res) => {
    await conexion.tarea.delete({ where: { id: 1 } });

    return res.status(204).send();
  });

servidor.listen(PORT, () => {
  console.log("Servidor corriendo exitosamente");
});
