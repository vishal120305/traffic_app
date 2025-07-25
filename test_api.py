import requests

sample_input = [
    1,     # Peak type
    120, 80,     # 2-w V, 2-w S
    10, 5,       # Vikram V, Vikram S
    200, 150,    # Car V, Car S
    50, 40,      # Auto V, Auto S
    30, 20,      # LCV V, LCV S
    5, 2,        # Tractor V, Tractor S
    10, 8,       # Bus V, Bus S
    40, 30,      # Truck V, Truck S
    4, 3,        # Rickshaw V, Rickshaw S
    6, 5,        # e-Rickshaw V, e-Rickshaw S
    10, 8,       # Cycle V, Cycle S
    1, 1,        # Horse D V, Horse D S
    800,         # Total V
    3.5,         # Lane Width
    1.2,         # IDSS
    1.0,         # IDOS
    0.8,         # Median
    72,          # Leq
    2,           # Landuse
    2.5,         # Wind Speed
    65.0,        # Relative Humidity
    1010,        # Atm Pressure
    32.0 ,123 ,32,12,3   # Temperature
]

response = requests.post("http://127.0.0.1:5000/predict", json={"features": sample_input})

if response.ok:
    print("✅ Prediction:", response.json())
else:
    print("❌ Error:", response.text)
