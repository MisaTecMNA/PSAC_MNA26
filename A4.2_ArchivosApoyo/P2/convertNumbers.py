"""
Programa: convertNumbers.py
Descripción: Convierte números de archivos a binario y hexadecimal.
Salida: Archivo ConvertionResults.txt con formato tabular.
"""
import sys
import time


def to_binary(number):
    """
    Convierte entero a binario usando algoritmo de división sucesiva.
    Maneja negativos con signo simple.
    """
    if number == 0:
        return "0"

    is_negative = number < 0
    num = abs(number)
    binary = ""

    while num > 0:
        remainder = num % 2
        binary = str(remainder) + binary
        num = num // 2

    if is_negative:
        return "-" + binary
    return binary


def to_hexadecimal(number):
    """
    Convierte entero a hexadecimal usando algoritmo de residuos.
    """
    if number == 0:
        return "0"

    hex_map = "0123456789ABCDEF"
    is_negative = number < 0
    num = abs(number)
    hex_str = ""

    while num > 0:
        remainder = num % 16
        hex_str = hex_map[remainder] + hex_str
        num = num // 16

    if is_negative:
        return "-" + hex_str
    return hex_str


def process_file(filename):
    """
    Lee un archivo y retorna una lista de tuplas (item, numero, bin, hex).
    """
    results = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                text = line.strip()
                if not text:
                    continue
                try:
                    num = int(text)
                    bin_val = to_binary(num)
                    hex_val = to_hexadecimal(num)
                    results.append((i, num, bin_val, hex_val))
                except ValueError:
                    sys.stderr.write(f"Error {filename} linea {i}: "
                                     f"'{text}' invalido.\n")
                    results.append((i, text, "#N/A", "#N/A"))
    except FileNotFoundError:
        sys.stderr.write(f"Error: Archivo '{filename}' no encontrado.\n")
        return None
    return results


def print_results(all_results, elapsed_time):
    """
    Imprime resultados concatenados y guarda en archivo.
    """
    lines = []

    for filename, data in all_results.items():
        if data is None:
            continue

        # Nombre de columna dinámico basado en el archivo (TC1, TC2...)
        col_name = filename.replace(".txt", "")

        # Encabezado para este archivo
        header = f"ITEM\t{col_name}\tBIN\tHEX"
        lines.append(header)

        for item, num, bin_v, hex_v in data:
            # Formato de fila
            row = f"{item}\t{num}\t{bin_v}\t{hex_v}"
            lines.append(row)

        # Espacio entre archivos
        lines.append("")

    final_output = "\n".join(lines).strip()

    # Pie de página con tiempo
    time_info = f"\n\nTiempo de ejecución: {elapsed_time:.6f} s"

    # 1. Imprimir en pantalla
    print(final_output)
    print(time_info)

    # 2. Guardar en archivo
    with open("ConvertionResults.txt", "w", encoding='utf-8') as f:
        f.write(final_output)
        f.write(time_info)

    print("\nArchivo 'ConvertionResults.txt' generado exitosamente.")


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print("Uso: python convertNumbers.py TC1.txt TC2.txt ...")
        sys.exit(1)

    start_time = time.time()
    filenames = sys.argv[1:]
    all_data = {}

    for fname in filenames:
        all_data[fname] = process_file(fname)

    end_time = time.time()
    elapsed = end_time - start_time

    print_results(all_data, elapsed)


if __name__ == "__main__":
    main()
