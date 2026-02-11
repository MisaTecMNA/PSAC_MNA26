"""
Este script calcula el costo total de las ventas basándose en un catálogo
de precios y un registro de ventas proporcionados en formato JSON.
"""
import json
import sys
import time


def load_json(filename):
    """Carga un archivo JSON y devuelve los datos."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Archivo '{filename}' JSON no valido.")
        return None


def create_price_map(catalogue):
    """Convierte la lista del catálogo en un diccionario."""
    price_map = {}
    for item in catalogue:
        title = item.get('title')
        price = item.get('price')
        if title and price is not None:
            price_map[title] = price
    return price_map


def compute_total_cost(price_map, sales_record):
    """Calcula el costo total de las ventas."""
    total_cost = 0.0
    for sale in sales_record:
        product = sale.get('Product')
        quantity = sale.get('Quantity')

        if product is None or quantity is None:
            continue

        if product in price_map:
            try:
                total_cost += price_map[product] * quantity
            except (TypeError, ValueError):
                print(f"Error encontrado para {product}")
        else:
            print(f"'{product}' no encontrado, omitido.")

    return total_cost


def main():
    """Función principal para ejecutar el cálculo de ventas."""
    if len(sys.argv) != 3:
        print("Uso: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)

    start_time = time.time()

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    catalogue_data = load_json(catalogue_file)
    sales_data = load_json(sales_file)

    if catalogue_data and sales_data:
        price_map = create_price_map(catalogue_data)
        total_cost = compute_total_cost(price_map, sales_data)

        end_time = time.time()
        elapsed_time = end_time - start_time

        output_lines = [
            "Costo Total de Ventas",
            f"Costo Total: ${total_cost:,.2f}",
            f"Tiempo Transcurrido: {elapsed_time:.4f} segundos"
        ]

        for line in output_lines:
            print(line)

        with open("SalesResults.txt", "a", encoding='utf-8') as result_file:
            result_file.write(f"\n--- Resultados para {sales_file} ---\n")
            result_file.write("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    main()
