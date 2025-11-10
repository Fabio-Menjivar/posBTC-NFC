from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx
import asyncio

# --- Modelos de Pydantic ---

# Modelo para el cuerpo de la petición
# Se asegura de que 'amount' sea un float y mayor que 0.
class AmountRequest(BaseModel):
    amount: float = Field(
        gt=0,  # 'gt' significa 'greater than' (mayor que)
        description="La cantidad en USD a convertir, debe ser mayor que 0."
    )

# Modelo para el cuerpo de la respuesta
# Se asegura de que 'value' sea un float y mayor que 0.
# Aunque la lógica de conversión debería garantizar esto si la entrada es > 0,
# es buena práctica definirlo si es un requisito de la respuesta.
class BTCResponse(BaseModel):
    value: float = Field(
        gt=0,
        description="El valor equivalente en BTC, debe ser mayor que 0."
    )

# --- Inicialización de la App ---

app = FastAPI(
    title="API de Conversión USD a BTC",
    description="Una API simple para convertir un monto de USD a BTC."
)

# --- Lógica de Conversión ---

# URL de la API de CoinGecko para obtener el precio actual de BTC en USD
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

async def obtener_tasa_btc() -> float:
    """Obtiene la tasa actual de BTC a USD desde la API de CoinGecko"""
    try:
        async with httpx.AsyncClient() as client:
            params = {
                'ids': 'bitcoin',
                'vs_currencies': 'usd'
            }
            response = await client.get(COINGECKO_API_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return 1 / data['bitcoin']['usd']  # Convertimos a USD a BTC
    except (httpx.RequestError, httpx.HTTPStatusError, KeyError) as e:
        raise HTTPException(
            status_code=503,
            detail=f"No se pudo obtener la tasa actual de BTC: {str(e)}"
        )

# --- Endpoint de la API ---

@app.post("/convertir/", response_model=BTCResponse)
async def convertir_usd_a_btc(request: AmountRequest):
    """
    Recibe un monto en USD y lo convierte a BTC usando la tasa actual.

    - **amount**: La cantidad en dólares (USD).
    - **Respuesta**: El valor equivalente en Bitcoin (BTC).
    """
    try:
        # Obtenemos la tasa actual de BTC a USD
        tasa_btc = await obtener_tasa_btc()
        
        # Realizamos el cálculo de conversión
        btc_value = request.amount * tasa_btc
        
        # Devolvemos el resultado
        return BTCResponse(value=btc_value)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar la conversión: {str(e)}"
        )