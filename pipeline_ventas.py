import glob
import os
import sqlite3
import pandas as pd

def ejecutar_pipeline():
    print("🚀 Iniciando pipeline de procesamiento de ventas...")

    # 1. EXTRACCIÓN: Leer todos los CSV de la carpeta data_cruda
    archivos = glob.glob("data_cruda/*.csv")
    if not archivos:
        print("⚠️ No se encontraron archivos CSV en 'data_cruda/'.")
        return

    lista_df = []
    for archivo in archivos:
        df_temp = pd.read_csv(archivo)
        df_temp["Sucursal"] = os.path.basename(archivo).replace("ventas_", "").replace(".csv", "").capitalize()
        lista_df.append(df_temp)

    df = pd.concat(lista_df, ignore_index=True)

    # 2. TRANSFORMACIÓN Y LIMPIEZA
    df["Producto"] = df["Producto"].astype(str).str.strip().str.title()
    df["Vendedor"] = df["Vendedor"].astype(str).str.strip().str.title()

    df["Precio_Unitario"] = (
        df["Precio_Unitario"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.strip()
        .astype(float)
    )

    df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce").fillna(0).astype(int)
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="mixed", dayfirst=True).dt.strftime("%Y-%m-%d")

    df = df.drop_duplicates()
    df = df[df["Cantidad"] > 0]
    df["Total_Venta"] = df["Cantidad"] * df["Precio_Unitario"]

    # 3. CARGA EN BASE DE DATOS SQL (SQLite)
    conexion = sqlite3.connect("ventas_consolidadas.db")
    df.to_sql("ventas", conexion, if_exists="replace", index=False)

    # 4. CONSULTAS SQL PARA REPORTE EJECUTIVO
    query_por_producto = """
        SELECT 
            Producto,
            SUM(Cantidad) AS Unidades_Vendidas,
            ROUND(SUM(Total_Venta), 2) AS Ingresos_Totales
        FROM ventas
        GROUP BY Producto
        ORDER BY Ingresos_Totales DESC;
    """

    query_por_sucursal = """
        SELECT 
            Sucursal,
            COUNT(*) AS Operaciones,
            ROUND(SUM(Total_Venta), 2) AS Facturacion_Total
        FROM ventas
        GROUP BY Sucursal
        ORDER BY Facturacion_Total DESC;
    """

    df_resumen_producto = pd.read_sql_query(query_por_producto, conexion)
    df_resumen_sucursal = pd.read_sql_query(query_por_sucursal, conexion)
    conexion.close()

    # 5. EXPORTAR REPORTE FINAL EN EXCEL MULTI-HOJA
    nombre_reporte = "Reporte_Ejecutivo_Ventas.xlsx"
    with pd.ExcelWriter(nombre_reporte, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Base_Limpia", index=False)
        df_resumen_producto.to_excel(writer, sheet_name="Resumen_Productos", index=False)
        df_resumen_sucursal.to_excel(writer, sheet_name="Resumen_Sucursales", index=False)

    print("✅ Proceso completado con éxito.")
    print("📊 Base de datos actualizada: 'ventas_consolidadas.db'")
    print(f"📑 Reporte generado: '{nombre_reporte}'")

if __name__ == "__main__":
    ejecutar_pipeline()
