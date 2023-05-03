import { items } from "../data.js";

export function crearItem(req, res) {
  console.log(req.body);
  const data = req.body;
  items.push(data);
  res.json({
    message: "Item agregado exitosamente",
    content: data,
  });
}

export const listarItems = (req, res) => {
  res.json({
    content: items,
  });
};

export const devolverUnItem = (req, res) => {
  console.log(req.params);
  const { id } = req.params;
  const item = items[id];

  res.json({
    content: item ?? null,
  });
};

export function eliminarItem(req, res) {
  const { id } = req.params;
  delete items[id];

  res.json({
    message: "Item eliminado exitosamente",
  });
}
