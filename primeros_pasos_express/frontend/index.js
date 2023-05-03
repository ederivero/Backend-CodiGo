async function traerItems() {
  const response = await fetch("http://127.0.0.1:3000/items", {
    method: "GET",
  });

  const data = await response.json();

  console.log(data);
}

traerItems();
