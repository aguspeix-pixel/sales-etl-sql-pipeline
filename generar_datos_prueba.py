import os
import pandas as pd

os.makedirs("data_cruda", exist_ok=True)

# Datos sucios Sucursal Norte
datos_norte = {
    "Fecha": ["2026-11-01", "02/11/2026", "2026-11-02", "2026-11-03", "2026-11-03"],
    "Producto": ["  teclado mecanico ", "Mouse Gamer", "TECLADO MECANICO", "Monitor 24", "Monitor 24"],
    "Cantidad": [2, 5, 1, None, 1],
    "Precio_Unitario": ["$45.00", "25.50", "$45.00", "$180.00", "$180.00"],
    "Vendedor": ["Juan", "ana", "Juan", "Ana", "Ana"]
}

# Datos sucios Sucursal Sur
datos_sur = {
    "Fecha": ["2026-11-01", "2026-11-04", "05/11/2026"],
    "Producto": ["mouse gamer", "Auriculares USB", "teclado mecanico"],
    "Cantidad": [3, 4, 2],
    "Precio_Unitario": ["25.50", "$60.00", "45.00"],
    "Vendedor": ["CARLOS", "carlos", "Laura"]
}

pd.DataFrame(datos_norte).to_csv("data_cruda/ventas_norte.csv", index=False)
pd.DataFrame(datos_sur).to_csv("data_cruda/ventas_sur.csv", index=False)

print("✅ Archivos CSV de prueba generados en 'data_cruda/'")