from typing import Union

from fastapi import FastAPI,HTTPException

import httpx

app = FastAPI()



SUPABASE_URL = "https://dfrsqtseebonqtptjjck.supabase.co/rest/v1/"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRmcnNxdHNlZWJvbnF0cHRqamNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU0MDkyMDIsImV4cCI6MjAzMDk4NTIwMn0.A-bL8uaHjYsLNGw448ffmIC0KV4CmHS2yERlwCI-rao"

@app.get("/productos")
async def obtener_productos():
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        response = await client.get(SUPABASE_URL + "PRODUCTO", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener productos")

@app.get("/marca")
async def obtener_marcas():
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        response = await client.get(SUPABASE_URL + "MARCA", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener marcas")

@app.get("/categoria")
async def obtener_categorias():
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        response = await client.get(SUPABASE_URL + "CATEGORIA", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener categoria")



@app.get("/precio")
async def obtener_precio():
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        response = await client.get(SUPABASE_URL + "PRECIO", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener precios")



@app.get("/detalleProducto")
async def obtener_detalleProducto():
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        response = await client.get(SUPABASE_URL + "PRODUCTO", headers=headers)

        if response.status_code == 200:
            productos = response.json()
            # Recuperar datos de marcas y categorías
            marcas = await obtener_marcas()
            categorias = await obtener_categorias()

            # Unir datos de marcas y categorías a los productos
            for producto in productos:
                id_marca = producto.get("id_marca")
                id_categoria = producto.get("id_categoria")
                producto["marca"] = next((marca for marca in marcas if marca["id_marca"] == id_marca), None)
                producto["categoria"] = next((categoria for categoria in categorias if categoria["id_categoria"] == id_categoria), None)
            
            return productos
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener productos")



@app.get("/detallePrecio")
async def obtener_detalle_precios():
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        response = await client.get(SUPABASE_URL + "PRECIO", headers=headers)

        if response.status_code == 200:
            precios = response.json()
            productos = await obtener_productos()

            # Unir datos de productos a los detalles de precio
            for precio in precios:
                id_producto = precio.get("id_producto")
                precio["producto"] = next((producto for producto in productos if producto["id_producto"] == id_producto), None)
                
            return precios
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener detalle de precios")

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)