"""
Problema 3 – Lado hospital: verificar_paquete.py
Lee SHA256SUMS.txt, recalcula el SHA-256 de cada archivo listado
y reporta cuáles pasaron y cuáles fallaron.

Uso:
    python verificar_paquete.py [--manifest SHA256SUMS.txt]
"""
import hashlib
import sys
import os
import argparse

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="SHA256SUMS.txt",
                        help="Ruta al archivo de manifiesto (default: SHA256SUMS.txt)")
    args = parser.parse_args()

    if not os.path.isfile(args.manifest):
        print(f"[ERROR] Manifiesto no encontrado: {args.manifest}")
        sys.exit(1)

    with open(args.manifest) as f:
        lines = [l.strip() for l in f if l.strip()]

    entries = []
    for line in lines:
        parts = line.split(None, 1)   # split on first whitespace
        if len(parts) != 2:
            continue
        expected_hash, filename = parts
        entries.append((expected_hash.lower(), filename))

    if not entries:
        print("[ERROR] El manifiesto está vacío o tiene formato inválido.")
        sys.exit(1)

    ok = []
    fail = []
    missing = []

    for expected, filename in entries:
        if not os.path.isfile(filename):
            missing.append(filename)
            continue
        actual = sha256_file(filename)
        if actual == expected:
            ok.append(filename)
        else:
            fail.append((filename, expected, actual))

    # ── Reporte ──────────────────────────────────────────────────────────────
    total = len(entries)
    sep   = "=" * 72
    print(f"\n{sep}")
    print(f"  REPORTE DE VERIFICACIÓN — {args.manifest}")
    print(sep)
    print(f"  Total de entradas : {total}")
    print(f"  ✓ Correctos        : {len(ok)}")
    print(f"  ✗ Fallidos         : {len(fail)}")
    print(f"  ? Ausentes         : {len(missing)}")
    print(sep)

    if ok:
        print("\n[✓] Archivos CORRECTOS:")
        for f in ok:
            print(f"    {f}")

    if missing:
        print("\n[?] Archivos NO ENCONTRADOS:")
        for f in missing:
            print(f"    {f}")

    if fail:
        print("\n[✗] Archivos COMPROMETIDOS o CORRUPTOS:")
        for filename, expected, actual in fail:
            print(f"\n  Archivo  : {filename}")
            print(f"  Esperado : {expected}")
            print(f"  Calculado: {actual}")
            # Show first differing nibble
            diff = [i for i, (a, b) in enumerate(zip(expected, actual)) if a != b]
            if diff:
                print(f"  Primer dígito hex diferente en posición: {diff[0]}")

    verdict = "✓ PAQUETE ÍNTEGRO" if not fail and not missing else "✗ PAQUETE COMPROMETIDO"
    print(f"\n  Veredicto final: {verdict}")
    print(sep + "\n")

    sys.exit(0 if not fail and not missing else 1)

if __name__ == "__main__":
    main()
