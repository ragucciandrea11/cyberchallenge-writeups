#!/usr/bin/env python3
"""Decifra un cifrario di Cesare spostando le lettere all'indietro.

Solo le lettere vengono spostate: maiuscole e minuscole restano tali, tutti gli
altri caratteri (cifre, graffe, underscore, punteggiatura) non cambiano.

Uso:
    python3 solve.py "<testo cifrato>"              # spostamento 13 (ROT13)
    python3 solve.py "<testo cifrato>" --shift 3    # spostamento a scelta
    python3 solve.py "<testo cifrato>" --brute      # prova tutti gli spostamenti
    echo "<testo cifrato>" | python3 solve.py       # testo da standard input

Nessun dato della challenge è scritto in questo file: il testo si passa da fuori.
"""
import argparse
import sys


def caesar_back(text: str, shift: int) -> str:
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") - shift) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") - shift) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Decifra un cifrario di Cesare")
    parser.add_argument("text", nargs="?", help="testo cifrato (altrimenti legge da stdin)")
    parser.add_argument("-s", "--shift", type=int, default=13, help="spostamento (default 13)")
    parser.add_argument("--brute", action="store_true", help="prova tutti gli spostamenti da 1 a 25")
    args = parser.parse_args()

    text = (args.text if args.text is not None else sys.stdin.read()).strip()
    if not text:
        sys.exit("Errore: nessun testo da decifrare")

    if args.brute:
        for shift in range(1, 26):
            print(f"{shift:2d}: {caesar_back(text, shift)}")
    else:
        print(caesar_back(text, args.shift))


if __name__ == "__main__":
    main()
