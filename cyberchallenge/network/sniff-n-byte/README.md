---
title: "Sniff 'n' byte"
source: cyberchallenge
category: network
points: 493
difficulty: 
date: 2026-11-25
status: done
---

# Sniff 'n' byte

Autore: davidedellagiustina · File fornito: `sniff_n_byte.pcapng`

## Descrizione

> Oh no! Sembra che qualcuno abbia infettato il nostro server con uno spyware e stia esfiltrando dei dati sensibili! *Annusa* in giro e scopri quali informazioni il malware sta inviando ai malintenzionati!

Come per gli altri writeup di questo repo, la flag e la stringa estratta dalla cattura non sono riportate qui: `solve.py` riceve la stringa come argomento.

## TL;DR

Seguendo il TCP stream della cattura compare una stringa fatta di byte in esadecimale scritti uno dopo l'altro, ognuno col prefisso `0x`. Decodificandola byte per byte con Python si ottiene la flag.

## Analisi

Il testo parla di uno spyware che esfiltra dati, quindi il traffico da cercare è una comunicazione in cui vengono inviate informazioni. Ho applicato le tecniche viste nelle [challenge intro di Wireshark](../wireshark-intro/README.md) e quella decisiva è la [Challenge 7](../wireshark-intro/README.md#challenge-7--follow-tcp-stream): **Follow TCP Stream**.

Nel flusso compare una lunga stringa che a prima vista non è testo leggibile. Guardandola da vicino è una sequenza di byte in esadecimale, uniti senza separatori e ognuno preceduto da `0x`. Il formato è questo (esempio inventato, non i dati della challenge):

```
0x480x650x6c0x6c0x6f
```

Ogni byte occupa quindi esattamente 4 caratteri: `0x` più due cifre esadecimali. Ogni valore è il codice ASCII di un carattere.

## Soluzione

1. Apro `sniff_n_byte.pcapng` con Wireshark.
2. **Analyze → Follow → TCP Stream** e leggo il contenuto dello stream: lì c'è la stringa di byte esadecimali.
3. Copio la stringa e la decodifico con Python: la spezzo in blocchi da 4 caratteri, converto ogni blocco con `int(blocco, 16)` e poi con `chr()`, infine unisco i caratteri.

```python
s = "0x480x650x6c0x6c0x6f"  # esempio inventato, non i dati della challenge

blocchi = [s[i:i + 4] for i in range(0, len(s), 4)]  # ['0x48', '0x65', ...]
testo = "".join(chr(int(b, 16)) for b in blocchi)
print(testo)  # Hello
```

In alternativa, in una riga: `bytes.fromhex(s.replace("0x", "")).decode()`.

## Exploit / script

Vedi [`solve.py`](solve.py). La stringa non è scritta nel file, si passa da fuori:

```bash
python3 solve.py "<stringa copiata dallo stream>"
```

## Cosa ho imparato

- Quando un flusso contiene dati che sembrano illeggibili, conviene prima riconoscerne il **formato** (qui: byte esadecimali con prefisso `0x`) e poi scrivere la decodifica.
- In Python la conversione è `int(x, 16)` per passare da testo esadecimale a numero e `chr()` per passare dal numero al carattere. `chr()` vuole un intero, non una stringa.
- Per tagliare una stringa in blocchi di lunghezza fissa non si usa `split` (non accetta un separatore vuoto) ma lo slicing, oppure `textwrap.wrap`.
