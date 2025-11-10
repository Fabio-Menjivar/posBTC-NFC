import requests
import json

# URL base de la API (ajusta según sea necesario)
BASE_URL = "http://127.0.0.1:8000"

def test_conversion(amount):
    """
    Prueba el endpoint de conversión con la cantidad especificada.
    """
    url = f"{BASE_URL}/convertir/"
    headers = {"Content-Type": "application/json"}
    data = {"amount": amount}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Lanza un error para códigos de estado 4XX/5XX
        
        result = response.json()
        print(f"✅ Prueba exitosa para ${amount:.2f} USD")
        print(f"   Resultado: {result['value']:.8f} BTC")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al realizar la petición para ${amount:.2f} USD:")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Código de estado: {e.response.status_code}")
            print(f"   Respuesta: {e.response.text}")
        else:
            print(f"   Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de la API de conversión USD a BTC\n")
    
    # Casos de prueba
    test_cases = [
        1.0,      # Caso básico
        100.0,    # Cantidad mayor
        0.01,     # Cantidad pequeña
        9999.99,  # Cantidad grande
    ]
    
    # Ejecutar pruebas
    for amount in test_cases:
        test_conversion(amount)
        print()  # Espacio entre pruebas
    
    print("✅ Pruebas completadas")
