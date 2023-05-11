import mongoose from "mongoose";
import express from "express";

const conectarMongo = async () => {
  await mongoose.connect("mongodb://127.0.0.1:27017/almacen");
  console.log("Base de datos conectada exitosamente");
};

conectarMongo();
