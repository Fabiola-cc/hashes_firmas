"""
Problema 2: Generación de Claves / Verificación HIBP
Calcula SHA-1 de contraseñas comunes y consulta Have I Been Pwned
usando k-Anonymity (solo se envían los primeros 5 chars del hash SHA-1).
"""
import hashlib
import urllib.request

PASSWORDS = ["admin", "123456", "hospital", "medisoft2024"]

def sha1_hex(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest().upper()

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def query_hibp(sha1_hash: str) -> int:
    """Retorna el número de veces que el hash aparece en filtraciones.
    Usa k-Anonymity: solo envía los primeros 5 caracteres."""
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    req = urllib.request.Request(url, headers={"User-Agent": "MediSoft-Lab"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode()

    for line in body.splitlines():
        h, count = line.split(":")
        if h.upper() == suffix.upper():
            return int(count)
    return 0

#  Header 
w = {"pw": 16, "sha256": 64, "sha1": 40, "count": 12}
sep = "-" * (w["pw"] + w["sha256"] + w["sha1"] + w["count"] + 9)

print("\n" + sep)
print(
    f"{'Contraseña':<{w['pw']}} "
    f"{'SHA-256':<{w['sha256']}} "
    f"{'SHA-1':<{w['sha1']}} "
    f"{'Filtraciones':>{w['count']}}"
)
print(sep)

for pw in PASSWORDS:
    h256 = sha256_hex(pw)
    h1   = sha1_hex(pw)
    try:
        count = query_hibp(h1)
    except Exception as e:
        count_str = f"Error: {e}"
        print(f"{pw:<{w['pw']}} {h256:<{w['sha256']}} {h1:<{w['sha1']}} {count_str}")
        continue

    flag = " ⚠ COMPROMETIDA" if count > 0 else " ✓ No encontrada"
    print(
        f"{pw:<{w['pw']}} {h256:<{w['sha256']}} {h1:<{w['sha1']}} "
        f"{count:>{w['count']},}{flag}"
    )
