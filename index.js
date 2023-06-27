import mongoose from "mongoose";
import express from "express";
import dotenv from "dotenv";

dotenv.config();

const servidor = express();
servidor.use(express.json());

const animalSchema = new mongoose.Schema({
  nombre: {
    type: mongoose.Schema.Types.String,
    required: true,
  },
  fechaNacimiento: {
    type: mongoose.Schema.Types.Date,
    alias: "fecha_nacimiento",
  },
  sexo: {
    type: mongoose.Schema.Types.String,
    enum: ["MACHO", "HEMBRA"],
  },
});

const AnimalModel = mongoose.model("animales", animalSchema);

servidor
  .route("/animales")
  .post(async (req, res) => {
    const data = req.body;
    try {
      const nuevoAnimal = await AnimalModel.create(data);

      return res.status(201).json({
        message: "Animal creado exitosamente",
        content: nuevoAnimal.toJSON(),
      });
    } catch (error) {
      return res.status(400).json({
        message: "Error al crear el animal",
        content: error.message,
      });
    }
  })
  .get(async (req, res) => {
    const animales = await AnimalModel.find();

    return res.status(200).json({
      content: animales,
    });
  });

servidor
  .route("/animal/:id")
  .get(async (req, res) => {
    const { id } = req.params;
    try {
      const animal = await AnimalModel.findById(id);

      if (!animal) {
        return res.status(404).json({
          message: "Animal no existe",
        });
      }

      return res.status(200).json({
        content: animal.toJSON(),
      });
    } catch (error) {
      return res.status(400).json({
        message: "Error al buscar el animal",
        content: error.message,
      });
    }
  })
  .put(async (req, res) => {
    const { id } = req.params;
    const animal = await AnimalModel.findById(id);

    if (!animal) {
      return res.status(404).json({
        message: "Animal no existe",
      });
    }

    const animalActualizado = await AnimalModel.findByIdAndUpdate(
      id,
      req.body,
      { new: true }
    );

    return res.json({
      content: animalActualizado,
    });
  })
  .delete(async (req, res) => {
    const { id } = req.params;
    const animal = await AnimalModel.findById(id);

    if (!animal) {
      return res.status(404).json({
        message: "Animal no existe",
      });
    }

    await AnimalModel.deleteOne({ _id: id });

    return res.status(204).send();
  });

servidor.listen(3000, async () => {
  console.log("Servidor corriendo exitosamente");
  await mongoose.connect(process.env.MONGODB_URL);
  console.log("Base de datos conectada exitosamente");
});
