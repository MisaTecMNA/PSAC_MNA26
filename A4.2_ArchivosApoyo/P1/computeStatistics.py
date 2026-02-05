# pylint: disable=invalid-name
"""
Programa: computeStatistics.py
Descripción: Calcula estadísticas descriptivas de múltiples archivos de texto.
Salida: Archivo .txt con formato tabular.
"""
import sys
import time


def read_file(filename):
    """
    Lee un archivo y retorna una lista de números.
    Maneja datos inválidos e imprime errores en consola de error (stderr).
    """
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    number = float(clean_line)
                    data.append(number)
                except ValueError:
                    # Reportar error sin detener ejecución
                    sys.stderr.write(f"Error en {filename}, línea {line_num}: "
                                     f"'{clean_line}' no es numérico.\n")
    except FileNotFoundError:
        sys.stderr.write(f"Error: El archivo '{filename}' no fue encontrado.\n")
        return None
    return data


def calculate_stats(data):
    """Calcula métricas: Count, Mean, Median, Mode, SD, Variance."""
    if not data:
        return None

    count = len(data)
    mean = sum(data) / count

    # Mediana
    sorted_data = sorted(data)
    mid = count // 2
    if count % 2 == 1:
        median = sorted_data[mid]
    else:
        median = (sorted_data[mid - 1] + sorted_data[mid]) / 2.0

    # Moda
    frequency = {}
    for item in data:
        frequency[item] = frequency.get(item, 0) + 1

    max_freq = max(frequency.values())
    # Si todos los números aparecen 1 sola vez, no hay moda útil (ej. floats)
    if max_freq == 1:
        mode = "#N/A"
    else:
        modes = [k for k, v in frequency.items() if v == max_freq]
        mode = modes[0]  # Tomamos el primero si hay múltiples

    # Varianza y Desviación Estándar
    if count < 2:
        variance = 0.0
    else:
        variance = sum((x - mean) ** 2 for x in data) / (count - 1)

    std_dev = variance ** 0.5

    return {
        "COUNT": count, "MEAN": mean, "MEDIAN": median,
        "MODE": mode, "SD": std_dev, "VARIANCE": variance
    }


def print_results(results, filenames, elapsed_time):
    """
    Imprime los resultados en formato tabular (matriz transpuesta)
    y los guarda en StatisticsResults.txt.
    """
    metrics = ["COUNT", "MEAN", "MEDIAN", "MODE", "SD", "VARIANCE"]

    # Construcción de encabezados
    # Usamos tabuladores \t para alinear columnas
    header = "TC\t" + "\t".join([name.replace(".txt", "") for name in filenames])

    rows = [header]

    for metric in metrics:
        row_parts = [metric]
        for name in filenames:
            val = results[name][metric]

            # Formateo de salida similar al ejemplo
            if val == "#N/A":
                row_parts.append(val)
            elif metric == "COUNT":
                row_parts.append(f"{int(val)}")
            elif metric == "MODE":
                row_parts.append(f"{val}")
            else:
                # Flotantes con 2 decimales o formato general si es muy grande
                row_parts.append(f"{val:.2f}")

        rows.append("\t".join(row_parts))

    final_output = "\n".join(rows)

    # 1. Imprimir en pantalla
    print(final_output)
    print(f"\nTiempo de ejecución: {elapsed_time:.6f} s")

    # 2. Guardar en archivo .txt
    output_filename = "StatisticsResults.txt"
    with open(output_filename, "w", encoding='utf-8') as f:
        f.write(final_output)
        f.write(f"\n\nTiempo de ejecución: {elapsed_time:.6f} s")

    print(f"\nArchivo generado exitosamente: {output_filename}")


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print("Uso: python computeStatistics.py TC1.txt TC2.txt ...")
        sys.exit(1)

    filenames = sys.argv[1:]
    start_time = time.time()

    all_results = {}

    # Procesar cada archivo
    for filename in filenames:
        data = read_file(filename)
        if data is None:
            # Si no se lee, llenamos con ceros para mantener la tabla
            all_results[filename] = {k: 0 for k in ["COUNT", "MEAN", "MEDIAN",
                                                    "MODE", "SD", "VARIANCE"]}
            continue

        stats = calculate_stats(data)
        all_results[filename] = stats

    end_time = time.time()
    elapsed = end_time - start_time

    print_results(all_results, filenames, elapsed)


if __name__ == "__main__":
    main()
