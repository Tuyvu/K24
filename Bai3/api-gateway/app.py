from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Định tuyến yêu cầu đến User Service
@app.get("/users")
async def get_user():
    response = requests.get(f"http://user-service:8001/")
    return response.json()

# Định tuyến yêu cầu đến Product Service
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    response = requests.get(f"http://product-service:8002/products/{product_id}")
    return response.json()