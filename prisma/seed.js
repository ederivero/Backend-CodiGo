import prisma from "@prisma/client";

const conexion = new prisma.PrismaClient();

async function poblar() {
  const usuarios = [
    {
      correo: "ederiveroman@gmail.com",
      password: "123123123",
      nombre: "Roberto",
      apellido: "de Rivero",
    },
    {
      correo: "juanperez@gmail.com",
      password: "123123123",
      nombre: "Juan",
      apellido: "Perez",
    },
  ];

  await Promise.all(
    usuarios.map(
      async (usuario) =>
        await conexion.usuario.upsert({
          create: usuario,
          update: usuario,
          where: { correo: usuario.correo },
        })
    )
  );
}

poblar();
