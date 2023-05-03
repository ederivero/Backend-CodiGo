import { Router } from "express";
import * as controller from "../controllers/items.controllers.js";
export const itemRouter = Router();

itemRouter
  .route("/items")
  .get(controller.listarItems)
  .post(controller.crearItem);

itemRouter
  .route("/item/:id")
  .get(controller.devolverUnItem)
  .delete(controller.eliminarItem);
