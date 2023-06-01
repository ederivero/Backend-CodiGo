import mongoose from "mongoose";
import express from "express";

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

const conectarMongo = async () => {
  await mongoose.connect("mongodb://127.0.0.1:27017/almacen");
  console.log("Base de datos conectada exitosamente");
};

conectarMongo();
