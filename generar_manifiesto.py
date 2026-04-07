"""
Problema 3 – Lado MediSoft: generar_manifiesto.py
Recibe rutas de archivos como argumentos (mínimo 5),
calcula SHA-256 de cada uno y agrega líneas a SHA256SUMS.txt.

Uso:
    python generar_manifiesto.py archivo1 archivo2 ... archivoN
"""
import hashlib
import sys
import os

MANIFEST = "SHA256SUMS.txt"

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    paths = sys.argv[1:]

    if len(paths) < 5:
        print(f"[ERROR] Se requieren al menos 5 archivos. Se recibieron {len(paths)}.")
        sys.exit(1)

    new_entries = []
    errors = []

    for path in paths:
        if not os.path.isfile(path):
            errors.append(f"  ✗ No encontrado: {path}")
            continue
        digest = sha256_file(path)
        name   = os.path.basename(path)
        new_entries.append((digest, name, path))

    if errors:
        print("\n[ADVERTENCIA] Archivos no procesados:")
        for e in errors:
            print(e)

    if not new_entries:
        print("[ERROR] Ningún archivo válido para procesar.")
        sys.exit(1)

    # Append to manifest (creates file if absent)
    with open(MANIFEST, "a") as f:
        for digest, name, _ in new_entries:
            f.write(f"{digest}  {name}\n")

    # Print summary
    col_hash = 64
    col_name = max(len(n) for _, n, _ in new_entries) + 2
    sep = "-" * (col_hash + col_name + 5)

    print(f"\n=== Manifiesto actualizado: {MANIFEST} ===\n")
    print(f"{'SHA-256':<{col_hash}}  {'Archivo'}")
    print(sep)
    for digest, name, _ in new_entries:
        print(f"{digest}  {name}")
    print(sep)
    print(f"\n{len(new_entries)} entrada(s) agregadas a {MANIFEST}.\n")

if __name__ == "__main__":
    main()
