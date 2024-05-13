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
        
@app.get("/productos/{producto_id}")
async def obtener_producto_id(producto_id: int):
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        response = await client.get(f"{SUPABASE_URL}PRODUCTO?id_producto=eq.{producto_id}", headers=headers)

        if response.status_code == 200:
            producto = response.json()
            return producto
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener producto")

@app.post("/producto")
async def crear_producto(nombre: str, descripcion: str, codigo_producto: str, id_marca: int, id_categoria: int, stock: str, imagen: str, precio: str):
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "codigo_producto": codigo_producto,
            "id_marca": id_marca,
            "id_categoria": id_categoria,
            "stock": stock,
            "imagen": imagen,
            "precio": precio
        }
        response = await client.post(SUPABASE_URL + "PRODUCTO", headers=headers, json=data)

        if response.status_code == 201:
            nuevo_producto = response.json()
            return nuevo_producto
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al crear producto")

@app.put("/productos/{producto_id}")
async def actualizar_producto(producto_id: int, nombre: str, descripcion: str, codigo_producto: str, id_marca: int, id_categoria: int, stock: str, imagen: str, precio: str):
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "codigo_producto": codigo_producto,
            "id_marca": id_marca,
            "id_categoria": id_categoria,
            "stock": stock,
            "imagen": imagen,
            "precio": precio
        }
        response = await client.get(SUPABASE_URL + "PRODUCTO?id_producto=eq." + producto_id, headers=headers , json=data)
        if response.status_code == 200:
            producto_actualizado = response.json()
            return producto_actualizado
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al actualizar producto")

@app.delete("/productos/{producto_id}")
async def eliminar_producto(producto_id: int):
    async with httpx.AsyncClient() as client:
        headers = {"apikey": SUPABASE_API_KEY}
        response = await client.delete(f"{SUPABASE_URL}PRODUCTO?id_producto=eq.{producto_id}", headers=headers)

        if response.status_code == 204:  # 204 significa "No Content" (éxito en la eliminación)
            return {"message": "Producto eliminado correctamente"}
        elif response.status_code == 404:  # 404 significa "Not Found" (producto no encontrado)
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al eliminar producto")
        

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

@app.get("/dolar")
async def get_daily_dollar():
    api_key = '8db42ec4dc88e3fac4f33afaff52008f8daede54'
    url_base = 'https://api.cmfchile.cl/api-sbifv3/recursos_api/dolar'
    headers = {"apikey": api_key}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url_base, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail="Error al obtener información del dólar")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error HTTP: {str(e)}")
    

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)