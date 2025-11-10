from fastapi import FastAPI
from pydantic import BaseModel, Field

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

# IMPORTANTE: Esta es una tasa de conversión FIJA solo para el ejemplo.
# En una aplicación real, deberías obtener esta tasa de una API externa.
TASA_USD_A_BTC = 0.000029  # Ejemplo: 1 USD = 0.000029 BTC

# --- Endpoint de la API ---

@app.post("/convertir/", response_model=BTCResponse)
async def convertir_usd_a_btc(request: AmountRequest):
    """
    Recibe un monto en USD y lo convierte a BTC.

    - **amount**: La cantidad en dólares (USD).
    - **Respuesta**: El valor equivalente en Bitcoin (BTC).
    """
    
    # Realiza el cálculo de conversión
    btc_value = request.amount * TASA_USD_A_BTC
    
    # Devuelve el resultado usando el modelo de respuesta Pydantic
    # FastAPI se encargará de validarlo (en este caso, que sea > 0)
    # y serializarlo a JSON.
    return BTCResponse(value=btc_value)