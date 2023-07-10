FROM node:19.9.0

WORKDIR /app

# Copio mis archivos al directorio de trabajo
COPY package.json ./
COPY package-lock.json ./

RUN npm install

# Copiar todo lo demas del codigo
COPY . .

EXPOSE 5000

CMD [ "npm", "start"]