---
title: "Benvenvti!"
source: cyberchallenge
category: crypto
points: 497
difficulty: 
date: 2026-11-26
status: done
---

# Benvenvti!

Origine: Demo OliCyber.IT 2021 (gara nazionale)

## Descrizione

La challenge non ha testo né file allegati: nella descrizione c'è soltanto una stringa scritta come una flag, ma con le lettere cifrate. Come per gli altri writeup di questo repo non la riporto, perché decifrarla dà direttamente la flag.

## TL;DR

La stringa è una flag cifrata con il **cifrario di Cesare**, con spostamento 13 (ROT13). Spostando ogni lettera indietro di 13 posizioni nell'alfabeto si ottiene la flag.

## Analisi

La stringa ha la forma di una flag: un prefisso, le parentesi graffe e dentro parole separate da `_`. Ma il prefisso non è `flag`: le lettere sono state sostituite. Il cifrario più semplice che produce un effetto simile è quello di Cesare, in cui ogni lettera viene sostituita da quella a distanza fissa nell'alfabeto.

Per ricavare lo spostamento si può usare il fatto che il testo in chiaro deve iniziare con `flag{`: confrontando le prime quattro lettere cifrate con `f`, `l`, `a`, `g` la distanza è sempre 13.

Tre cose da notare:
- 13 è esattamente metà dell'alfabeto (26 lettere), quindi spostare in avanti o indietro di 13 dà lo stesso risultato: lo stesso procedimento cifra e decifra. Questo caso particolare si chiama **ROT13**.
- Si spostano solo le lettere, maiuscole e minuscole restano tali.
- I simboli (`{`, `}`, `_`, `!`) non cambiano.

## Soluzione

1. Copio la stringa dalla descrizione della challenge.
2. Sposto ogni lettera indietro di 13 posizioni. Con lo script del repo:
   ```bash
   python3 solve.py "<stringa copiata dalla challenge>"
   ```
3. Il risultato è la flag, da inviare alla piattaforma.

Gli stessi passaggi si possono fare in altri modi. Esempio inventato:

```bash
# da terminale, con tr
echo "Uryyb, jbeyq!" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# Hello, world!
```

```python
# da Python, con la libreria standard
import codecs
print(codecs.decode("Uryyb, jbeyq!", "rot_13"))  # Hello, world!
```

Esistono anche strumenti online come CyberChef, che ha un'operazione ROT13.

## Exploit / script

Vedi [`solve.py`](solve.py). Il testo cifrato non è scritto nel file, si passa da fuori. Se non si conosce lo spostamento, `--brute` stampa tutti i 25 tentativi possibili e basta riconoscere quello leggibile:

```bash
python3 solve.py "<testo cifrato>" --brute
```

## Cosa ho imparato

- Il **cifrario di Cesare** sostituisce ogni lettera con quella a distanza fissa nell'alfabeto; ROT13 è il caso con spostamento 13.
- Il **formato noto della flag** (`flag{`) è un pezzo di testo in chiaro conosciuto in anticipo e permette di ricavare lo spostamento.
- Con soli 25 spostamenti possibili il cifrario si rompe anche **provandoli tutti** (brute force), senza bisogno di conoscere la chiave.
