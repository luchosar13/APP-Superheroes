from pymongo import MongoClient
import json
import os

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

try:
    print("Conectando a MongoDB...")
    client = MongoClient(mongo_uri)
    db = client["personajes"]
    coleccion = db["datos"]
except Exception as e:
    print(f"Error general: {e}")

if coleccion.count_documents({}) == 0:
    print("Colección vacía. Insertando datos desde data.json...")
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    result = coleccion.insert_many(data)
    print(f"Total documentos insertados: {len(result.inserted_ids)}")
else:
    print("La colección ya tiene datos. No se realiza inserción.")
