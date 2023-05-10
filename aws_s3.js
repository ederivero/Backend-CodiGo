import s3 from "aws-sdk/clients/s3.js";
import fs from "fs";

async function subirArchivo() {
  const conector = new s3({
    region: "us-east-2",
    credentials: {
      accessKeyId: "xxxxxxx",
      secretAccessKey: "xxxxxxxxxxxxxxxxxx",
    },
  });

  const archivo = fs.createReadStream("portrait.jpg");

  const resultado = await conector
    .upload({
      Bucket: "xxxxx",
      Body: archivo,
      Key: "portrait.jpg",
    })
    .promise();

  console.log(resultado);
}

async function devolverUrl() {
  const conector = new s3({
    region: "us-east-2",
    credentials: {
      accessKeyId: "xxxxxxx",
      secretAccessKey: "xxxxxxxxxxxxxxxxx",
    },
  });

  const url = conector.getSignedUrl("getObject", {
    Bucket: "xxxxxxx",
    Key: "portrait.jpg",
    Expires: 60,
  });

  console.log(url);
}

// subirArchivo();
devolverUrl();
