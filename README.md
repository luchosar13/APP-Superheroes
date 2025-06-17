# 🦸‍♂️ Superhéroes & Villanos App

Aplicación web para gestionar un catálogo de superhéroes y villanos. Permite visualizar, agregar, modificar y eliminar personajes, filtrarlos por editorial, y ver imágenes asociadas.

## 📝 Descripción

Esta aplicación tiene como objetivo administrar información detallada de superhéroes y villanos, incluyendo:

- Nombre del personaje
- Nombre real
- Año de aparición
- Casa editorial
- Biografía
- Equipamiento
- Imagen

Los datos se almacenan en una base de datos MongoDB, y la interfaz web fue desarrollada con Flask.

## ⚙️ Tecnologías utilizadas

- **Backend:** Python, Flask
- **Base de datos:** MongoDB
- **Contenedores:** Docker, Docker Compose
- **Frontend:** HTML, CSS, Bootstrap
- **Dependencias:** pymongo, Flask

## 🚀 Funcionalidades

- 🔎 **Listado general de personajes** en formato de cards.
- 🖼️ **Vista detalle** de cada personaje con galería de imágenes.
- ➕ **Agregar personajes** con formulario.
- 🖊️ **Editar personajes** existentes.
- ❌ **Eliminar personajes**.
- 🗂️ **Filtrar por casa editorial**.
- 🔍 **Búsqueda por nombre**.
- 📁 **Gestión de imágenes** en carpeta estática.
- 🍃 **API conectada a MongoDB** para persistencia.

## 🧪 Requisitos para correr el proyecto

### Arquitectura

El único requisito para este proyecto es tener Docker Engine y Docker Compose en tu máquina local.

### Código

- Para levantar el proyecto:
  
  `sudo docker compose up --build`

### Visualización

- `localhost:5000/`
   
   En esta ubicación vas a encontrar la página inicial en donde vas a poder navegar por las diferentes funcionalidades.
