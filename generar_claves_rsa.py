"""
Problema 4 – Generación de claves RSA y firma digital.
  • Genera par RSA-2048 → medisoft_priv.pem / medisoft_pub.pem
  • Firma SHA256SUMS.txt con RSA-PSS → SHA256SUMS.sig

Dependencia: pip install pycryptodome
"""
import hashlib
import os
import sys

from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256

PRIV_KEY  = "medisoft_priv.pem"
PUB_KEY   = "medisoft_pub.pem"
MANIFEST  = "SHA256SUMS.txt"
SIG_FILE  = "SHA256SUMS.sig"

#  1. Generar par de claves RSA-2048 
print("\n[1/3] Generando par de claves RSA-2048 ...")
key = RSA.generate(2048)

with open(PRIV_KEY, "wb") as f:
    f.write(key.export_key("PEM"))
print(f"  Clave privada  → {PRIV_KEY}  (NO COMPARTIR)")

with open(PUB_KEY, "wb") as f:
    f.write(key.publickey().export_key("PEM"))
print(f"  Clave pública  → {PUB_KEY}   (se puede distribuir)")

#  2. Leer manifiesto 
if not os.path.isfile(MANIFEST):
    print(f"\n[ERROR] {MANIFEST} no encontrado. Ejecuta primero generar_manifiesto.py")
    sys.exit(1)

print(f"\n[2/3] Leyendo {MANIFEST} y calculando SHA-256 del contenido ...")
with open(MANIFEST, "rb") as f:
    content = f.read()

digest = SHA256.new(content)
print(f"  SHA-256 del manifiesto: {digest.hexdigest()}")

#  3. Firmar con RSA-PSS 
print(f"\n[3/3] Firmando con clave privada (RSA-PSS) → {SIG_FILE} ...")
signer    = pss.new(key)
signature = signer.sign(digest)

with open(SIG_FILE, "wb") as f:
    f.write(signature)

print(f"  Tamaño de firma : {len(signature)} bytes")
print(f"  Firma guardada  → {SIG_FILE}")
print("\n  Proceso completado. Distribuye junto al paquete:")
print(f"    • {MANIFEST}  (manifiesto de hashes)")
print(f"    • {SIG_FILE}        (firma digital)")
print(f"    • {PUB_KEY}  (clave pública para verificación)\n")
