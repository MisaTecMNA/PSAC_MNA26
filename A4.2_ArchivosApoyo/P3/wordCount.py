"""
Programa: wordCount.py
Descripción: Cuenta frecuencias de palabras y genera archivos de resultados individuales.
Salida: Archivos [Nombre].Results.txt con formato tabular según lo especificado en las instrucciones
"""
import sys
import time
import os


def get_words(filename):
    """
    Lee el archivo y retorna una lista de palabras.
    """
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                if not clean_line:
                    continue
                # Separar por espacios
                line_words = clean_line.split()
                if not line_words:
                    continue
                words.extend(line_words)
    except FileNotFoundError:
        sys.stderr.write(f"Error: El archivo '{filename}' no existe.\n")
        return None
    except UnicodeDecodeError:
        sys.stderr.write(f"Error: El archivo '{filename}' no es texto válido.\n")
        return None
    except OSError as error:
        sys.stderr.write(f"Error leyendo '{filename}': {error}\n")
        return None
    return words


def count_frequencies(words):
    """
    Cuenta la frecuencia de cada palabra.
    Retorna un diccionario {palabra: frecuencia}.
    """
    if not words:
        return {}

    freq_dict = {}
    for word in words:
        # Se cuenta la palabra tal cual aparece
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict


def write_results_file(filename, frequencies, elapsed_time):
    """
    Escribe el archivo de resultados específico para el archivo de entrada.
    Formato: Row Labels [tab] Count of [Nombre]
    Orden: Frecuencia Descendente.
    """
    # 1. Definir nombre de salida: TC1.txt -> TC1.Results.txt
    base_name = os.path.basename(filename)
    name_no_ext = os.path.splitext(base_name)[0]
    output_filename = f"{name_no_ext}.Results.txt"

    # 2. Ordenar datos: Frecuencia Descendente, luego Alfabético
    sorted_items = sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))

    lines = []
    # Encabezado estilo tabla dinámica
    lines.append(f"Row Labels\tCount of {name_no_ext}")

    for word, count in sorted_items:
        lines.append(f"{word}\t{count}")

    # Pie de página con tiempo
    footer_info = f"\n\nExecution time: {elapsed_time:.4f} seconds"

    full_content = "\n".join(lines) + footer_info

    # 3. Escribir archivo
    try:
        with open(output_filename, "w", encoding='utf-8') as f:
            f.write(full_content)
        print(f"Generado: {output_filename} ({len(sorted_items)} palabras únicas)")

    except OSError as error:
        sys.stderr.write(f"Error escribiendo '{output_filename}': {error}\n")


def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print("Uso: python wordCount.py TC1.txt TC2.txt ...")
        sys.exit(1)

    input_files = sys.argv[1:]

    # Procesamos cada archivo de forma independiente
    for filename in input_files:
        start_time = time.time()

        words = get_words(filename)

        if words is not None:
            frequencies = count_frequencies(words)

            end_time = time.time()
            elapsed = end_time - start_time

            write_results_file(filename, frequencies, elapsed)
        else:
            print(f"Saltando '{filename}' por errores de lectura.")


if __name__ == "__main__":
    main()
