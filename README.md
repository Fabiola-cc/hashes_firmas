# Lab — Hashes y Firmas Digitales · MediSoft S.A.

## Descripción del proyecto

MediSoft S.A. distribuye software de diagnóstico a hospitales en Guatemala, Honduras y El Salvador. El software controla equipos de laboratorio críticos y debe cumplir regulaciones de integridad de dispositivos médicos.

Un incidente reciente expuso la vulnerabilidad del proceso de distribución: un atacante comprometió un mirror no oficial e inyectó código malicioso en un paquete de actualización. Los hospitales lo descargaron sin poder detectar la manipulación.

Este laboratorio implementa **dos capas de protección** para evitar que ese ataque se repita:

1. **Integridad de distribución** — cada archivo del paquete se acompaña de su hash SHA-256. El hospital recalcula los hashes al recibirlos y los compara contra un manifiesto publicado por MediSoft. Cualquier modificación, por mínima que sea, produce un hash completamente diferente y es detectada de inmediato.

2. **Autenticación de origen** — el manifiesto de hashes es firmado digitalmente por MediSoft con una clave privada RSA-2048. El hospital verifica la firma con la clave pública correspondiente, garantizando que el manifiesto no fue reemplazado por el atacante (incluso si comprometió el servidor).

Adicionalmente se exploran las propiedades fundamentales de las funciones hash (efecto avalancha, resistencia a colisiones) y la inseguridad de usar SHA-256 directo para almacenamiento de contraseñas, verificando hashes contra la base de datos pública Have I Been Pwned.

---

## Instalación

```bash
pip install pycryptodome
```

Librería estándar de Python (`hashlib`, `urllib`) cubre el resto.

---

## Estructura del repositorio

```
explorar_hashes.py       # Problema 1 — comparación de algoritmos hash
generacion_claves.py     # Problema 2 — verificación HIBP
generar_manifiesto.py    # Problema 3a — rol MediSoft: genera SHA256SUMS.txt
verificar_paquete.py     # Problema 3b — rol hospital: verifica integridad
generar_claves_rsa.py    # Problema 4  — genera RSA-2048 y firma el manifiesto
verificar_firma.py       # Problema 5  — valida la firma digital
```

---

## Uso

### Problema 1 — Comparación de algoritmos

```bash
python explorar_hashes.py
```

### Problema 2 — Verificación HIBP

```bash
python generacion_claves.py
```

### Problema 3 — Verificación de integridad

```bash
# MediSoft publica el release
python generar_manifiesto.py archivo1 archivo2 archivo3 archivo4 archivo5

# Hospital verifica el paquete recibido
python verificar_paquete.py
```

### Problemas 4 y 5 — Firma y verificación digital

```bash
python generar_claves_rsa.py   # genera claves y firma SHA256SUMS.txt
python verificar_firma.py      # valida la firma con la clave pública
```

---

## Ejemplos de ejecución

### Problema 1

```
------------------------------------------------------------------------------------------------------------------
Input             Algoritmo       Bits    Hex len Hash
------------------------------------------------------------------------------------------------------------------
MediSoft-v2.1.0   MD5              128         32 cac2fe40370e3a68f0a4927c20c75c89
                  SHA-1            160         40 3ab92abc44e23465b154e887f90c3a5e0d642c65
                  SHA-256          256         64 64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996
                  SHA3-256         256         64 3b0af4c0a9078e2ddc1606313db9206dcb3a4dbf423d78c0cf16929d303e30d2
------------------------------------------------------------------------------------------------------------------
medisoft-v2.1.0   MD5              128         32 fa386a0d796e388b24cb3302c185a445
                  SHA-1            160         40 4fe9fa8c97db362ecce61ee6302a92f0505217cd
                  SHA-256          256         64 ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e
                  SHA3-256         256         64 569daf2d0645c0ab6c0a7960cb552f28ac1a222284fa5605ab11cfe0a2dce82c
------------------------------------------------------------------------------------------------------------------
```

### Problema 2 — Verificación HIBP

```
---------------------------------------------------------------------------------------------------------------------------------------------
Contraseña       SHA-256                                                          SHA-1                                    Filtraciones
---------------------------------------------------------------------------------------------------------------------------------------------
admin            8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 D033E22AE348AEB5660FC2140AEC35850C4DA997   42,085,691 ⚠ COMPROMETIDA
123456           8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92 7C4A8D09CA3762AF61E59520943DC26494F8941B  209,972,844 ⚠ COMPROMETIDA
hospital         8afe3c83decffdf6dc48597a3f1a52be7c6e2b97b4bdf3b15e20a87a1f657f01 2B2D005E88CE14A4112785BB266B2C0C16BE7EB4      118,791 ⚠ COMPROMETIDA
medisoft2024     78c12e8e24dfd7836c748c33dff2e9150c028d69488f203485e13f4a6daa777c F80CF41ABF90CAA2EC08527F641C40B4ABFE4DB9            0 ✓ No encontrada
---------------------------------------------------------------------------------------------------------------------------------------------
```

> Nota: Aunque se calcula SHA-256 para cada contraseña, la consulta a Have I Been Pwned se realiza con SHA-1, ya que su API funciona con el modelo de k-Anonymity (solo se envían los primeros 5 caracteres del hash). Esto demuestra que, aunque se use hashing, contraseñas débiles siguen siendo inseguras porque ya existen en bases de datos públicas.

### Problema 3 
- **Generación de manifiesto**
```
=== Manifiesto actualizado: SHA256SUMS.txt ===

SHA-256                                                           Archivo
-----------------------------------------------------------------------------
a744466056eb0c632d4813558b2d5b84869a77ed712bc42727b6c647df7b7e48  f1.txt
756f58192f52ea3af4068ffbce461a010766ed6e77227fe2484d428b6d58b379  f2.txt
2677068ac10d6a8ba1daafd9daa74b68cf8c592f3ffc405600055ddcf50b7346  f3.txt
6edc4310f852408c232715c53c787042eb38320419a0a58d4adb382aba265489  f4.txt
dc50f034defe6be6a471d733b579c561eac42ea8b0bcc368bb370685717205b8  f5.txt
-----------------------------------------------------------------------------

5 entrada(s) agregadas a SHA256SUMS.txt.
```
- **Paquete íntegro vs. comprometido**
```
# Verificación limpia
========================================================================
  REPORTE DE VERIFICACIÓN — SHA256SUMS.txt
========================================================================
  Total de entradas : 5
  ✓ Correctos        : 5
  ✗ Fallidos         : 0
  ? Ausentes         : 0
========================================================================

[✓] Archivos CORRECTOS:
    f1.txt
    f2.txt
    f3.txt
    f4.txt
    f5.txt

  Veredicto final: ✓ PAQUETE ÍNTEGRO
========================================================================

# Tras mutar un byte en config.json
========================================================================
  REPORTE DE VERIFICACIÓN — SHA256SUMS.txt
========================================================================
  Total de entradas : 5
  ✓ Correctos        : 4
  ✗ Fallidos         : 1
  ? Ausentes         : 0
========================================================================

[✓] Archivos CORRECTOS:
    f1.txt
    f2.txt
    f4.txt
    f5.txt

[✗] Archivos COMPROMETIDOS o CORRUPTOS:

  Archivo  : f3.txt
  Esperado : 2677068ac10d6a8ba1daafd9daa74b68cf8c592f3ffc405600055ddcf50b7346
  Calculado: 6edc4310f852408c232715c53c787042eb38320419a0a58d4adb382aba265489
  Primer dígito hex diferente en posición: 0

  Veredicto final: ✗ PAQUETE COMPROMETIDO
========================================================================
```

### Problemas 4 y 5 — Firma digital

```
# Firma generada con éxito
[1/3] Generando par de claves RSA-2048 ...
  Clave privada  → medisoft_priv.pem  (NO COMPARTIR)
  Clave pública  → medisoft_pub.pem   (se puede distribuir)

[2/3] Leyendo SHA256SUMS.txt y calculando SHA-256 del contenido ...
  SHA-256 del manifiesto: 00c43b2b1bbfc05a71942e6b6a8a09d7623283b55f5ec9da354b9ffb5b0f1256

[3/3] Firmando con clave privada (RSA-PSS) → SHA256SUMS.sig ...
  Tamaño de firma : 256 bytes
  Firma guardada  → SHA256SUMS.sig

  Proceso completado. Distribuye junto al paquete:
    • SHA256SUMS.txt  (manifiesto de hashes)
    • SHA256SUMS.sig        (firma digital)
    • medisoft_pub.pem  (clave pública para verificación)

# Verificación con manifiesto original
  ✓ FIRMA VÁLIDA
  El manifiesto fue creado por el titular de la clave privada.
  Los hashes en SHA256SUMS.txt no han sido alterados

# Tras cambiar un carácter en SHA256SUMS.txt
  ✗ FIRMA INVÁLIDA
  ADVERTENCIA: el manifiesto fue modificado o la firma es incorrecta.
  No confíes en los archivos de este paquete
```

---

## Preguntas de análisis

### Problema 1

**¿Cuántos bits cambiaron entre los dos hashes SHA-256? ¿Qué propiedad demuestra?**

```
SHA-256("MediSoft-v2.1.0") = 64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996
SHA-256("medisoft-v2.1.0") = ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e

XOR → 120 de 256 bits cambiaron (46.9 %)
```

Cambiar únicamente la capitalización de la primera letra (`M` → `m`) alteró casi la mitad de todos los bits del hash. Esto demuestra el **efecto avalancha**: una función hash criptográfica está diseñada para que cualquier modificación mínima en el input —incluso un solo bit— produzca un output que difiere en aproximadamente el 50 % de sus bits. Esta propiedad es fundamental para detectar manipulaciones: no existe correlación observable entre inputs similares y sus hashes.

---

**¿Por qué MD5 es considerado inseguro para integridad de archivos?**

MD5 produce un digest de solo **128 bits** (32 caracteres hexadecimales). Esto lo hace vulnerable por dos razones concretas:

1. **Colisiones conocidas y computacionalmente baratas.** Se han demostrado ataques de colisión prácticos: es posible construir dos archivos con contenido diferente que produzcan exactamente el mismo hash MD5. Un atacante puede reemplazar un ejecutable legítimo por uno malicioso conservando el mismo MD5, haciendo que el verificador no detecte el cambio.

2. **Velocidad excesiva.** MD5 fue diseñado para ser rápido, lo cual es una desventaja en seguridad: permite ataques de fuerza bruta y búsqueda en tablas rainbow a alta velocidad con hardware moderno (GPUs pueden calcular miles de millones de hashes MD5 por segundo).

SHA-256 con 256 bits hace que las colisiones sean computacionalmente inviables con la tecnología actual; es el mínimo recomendado para verificación de integridad de software.

---
### Problema 5

**¿Por qué la firma sigue siendo válida después de mutar un byte en uno de los archivos del paquete? ¿Qué sucede al ejecutar `verificar_paquete.py`?**

La firma digital en `SHA256SUMS.sig` autentica el contenido de `SHA256SUMS.txt`, no los archivos individuales del paquete. Cada capa protege una cosa distinta:

| Capa | Qué protege | Cómo |
|------|-------------|------|
| Firma RSA-PSS | `SHA256SUMS.txt` — el manifiesto | Criptografía asimétrica: solo MediSoft pudo generar `SHA256SUMS.sig` con su clave privada |
| Hashes SHA-256 en el manifiesto | Los archivos del paquete | Comparación de digest al recibirlos |

Si se muta un byte en, por ejemplo, `config.json`:

- `verificar_firma.py` reporta **firma válida** — el manifiesto `SHA256SUMS.txt` no fue tocado, la firma sobre él sigue siendo correcta.
- `verificar_paquete.py` reporta **paquete comprometido** — el SHA-256 recalculado de `config.json` no coincide con el hash registrado en el manifiesto.

Esto ilustra por qué ambas capas son necesarias y complementarias: la firma garantiza que el manifiesto proviene de MediSoft y no fue alterado; los hashes en el manifiesto garantizan que cada archivo individual llegó sin modificaciones.
