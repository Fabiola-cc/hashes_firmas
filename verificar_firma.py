"""
Problema 5 – Verificación de firma digital (lado hospital).
  • Lee medisoft_pub.pem, SHA256SUMS.txt y SHA256SUMS.sig
  • Valida que el manifiesto fue firmado por MediSoft

Dependencia: pip install pycryptodome

Uso:
    python verificar_firma.py
    python verificar_firma.py --manifest SHA256SUMS.txt --sig SHA256SUMS.sig --pub medisoft_pub.pem
"""
import argparse
import os
import sys

from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256

def verify(manifest_path: str, sig_path: str, pub_path: str) -> bool:
    """Retorna True si la firma es válida, False en caso contrario."""
    for p in (manifest_path, sig_path, pub_path):
        if not os.path.isfile(p):
            print(f"[ERROR] Archivo no encontrado: {p}")
            sys.exit(1)

    with open(pub_path, "rb") as f:
        pub_key = RSA.import_key(f.read())

    with open(manifest_path, "rb") as f:
        content = f.read()

    with open(sig_path, "rb") as f:
        signature = f.read()

    digest   = SHA256.new(content)
    verifier = pss.new(pub_key)

    try:
        verifier.verify(digest, signature)
        return True
    except (ValueError, TypeError):
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="SHA256SUMS.txt")
    parser.add_argument("--sig",      default="SHA256SUMS.sig")
    parser.add_argument("--pub",      default="medisoft_pub.pem")
    args = parser.parse_args()

    sep = "=" * 60
    print(f"\n{sep}")
    print("  VERIFICACIÓN DE FIRMA DIGITAL — MediSoft")
    print(sep)
    print(f"  Manifiesto : {args.manifest}")
    print(f"  Firma      : {args.sig}")
    print(f"  Clave pub  : {args.pub}")
    print(sep)

    valid = verify(args.manifest, args.sig, args.pub)

    if valid:
        print("\n  ✓ FIRMA VÁLIDA")
        print("  El manifiesto fue creado por el titular de la clave privada.")
        print("  Los hashes en SHA256SUMS.txt no han sido alterados.")
    else:
        print("\n  ✗ FIRMA INVÁLIDA")
        print("  ADVERTENCIA: el manifiesto fue modificado o la firma es incorrecta.")
        print("  No confíes en los archivos de este paquete.")

    print(f"\n{sep}\n")
    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
