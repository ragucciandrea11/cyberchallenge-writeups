#!/usr/bin/env python3
"""Decodifica una stringa di byte esadecimali concatenati, ognuno col prefisso 0x.

Esempio:  0x480x650x6c0x6c0x6f  ->  Hello

Uso:
    python3 solve.py "<stringa>"
    echo "<stringa>" | python3 solve.py

Nessun dato della challenge è scritto in questo file: la stringa estratta dalla
cattura si passa da fuori (argomento o standard input).
"""
import re
import sys


def decode(s: str) -> str:
    byte_hex = re.findall(r"0x([0-9a-fA-F]{2})", s)
    if not byte_hex:
        raise ValueError("nessun byte nel formato 0xNN trovato nella stringa")
    return "".join(chr(int(b, 16)) for b in byte_hex)


def main() -> None:
    data = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    try:
        print(decode(data.strip()))
    except ValueError as e:
        sys.exit(f"Errore: {e}")


if __name__ == "__main__":
    main()
