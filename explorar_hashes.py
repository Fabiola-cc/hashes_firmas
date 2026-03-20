import hashlib

strings = ["MediSoft-v2.1.0", "medisoft-v2.1.0"]

algorithms = [
    ("MD5",      hashlib.md5),
    ("SHA-1",    hashlib.sha1),
    ("SHA-256",  hashlib.sha256),
    ("SHA3-256", hashlib.sha3_256),
]

# Compute all hashes
results = []
for s in strings:
    for algo_name, algo_fn in algorithms:
        digest = algo_fn(s.encode()).hexdigest()
        bits = len(digest) * 4
        hex_len = len(digest)
        results.append((s, algo_name, bits, hex_len, digest))

# Print table
col_widths = {
    "input":   17,
    "algo":    8,
    "bits":    10,
    "hexlen":  10,
    "hash":    64,
}

header = (
    f"{'Input':<{col_widths['input']}} "
    f"{'Algoritmo':<{col_widths['algo']}} "
    f"{'Bits':>{col_widths['bits']}} "
    f"{'Hex len':>{col_widths['hexlen']}} "
    f"{'Hash':<{col_widths['hash']}}"
)

separator = "-" * len(header)

print("\n" + separator)
print(header)
print(separator)

prev_input = None
for (inp, algo, bits, hexlen, digest) in results:
    if prev_input and prev_input != inp:
        print(separator)          # blank row between the two strings
    display_input = inp if inp != prev_input else ""
    print(
        f"{display_input:<{col_widths['input']}} "
        f"{algo:<{col_widths['algo']}} "
        f"{bits:>{col_widths['bits']}} "
        f"{hexlen:>{col_widths['hexlen']}} "
        f"{digest:<{col_widths['hash']}}"
    )
    prev_input = inp

print(separator)
print()