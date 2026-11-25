---
title: "G4tto"
source: cyberchallenge
category: network
points: 490
difficulty: 
date: 2026-11-25
status: done
---

# G4tto

Autore: minn3 · File fornito: `G4tt0.pcapng`

## Descrizione

> Riuscirai a trovare il gatto?

Come per gli altri writeup di questo repo, la flag non è riportata. Qui è scritta su un'immagine, per cui non allego nemmeno quella.

## TL;DR

Titolo e descrizione parlano di un gatto: l'indizio è che nella cattura viaggia un'immagine. Estraendo gli oggetti HTTP con **File → Export Objects → HTTP** si trova `Gatto.jpeg`, sulla cui foto è scritta la flag.

## Analisi

Il titolo "G4tto" è "gatto" scritto con il `4` al posto della `a`, e la descrizione chiede di trovare il gatto. All'inizio non avevo capito cosa cercare, così ho provato la strada già usata in altre challenge, il [Follow Stream](../wireshark-intro/README.md#challenge-7--follow-tcp-stream) (Challenge 7), ma gli stream non hanno dato nulla.

Rileggendo il titolo ho pensato che il "gatto" potesse essere un'**immagine** trasferita in rete. Se un file passa in HTTP, Wireshark può estrarlo come oggetto: è la tecnica della [Challenge 10](../wireshark-intro/README.md#challenge-10--esportare-oggetti-http).

## Soluzione

1. Apro `G4tt0.pcapng` con Wireshark.
2. **File → Export Objects → HTTP**, poi *Save All* in una cartella.
3. Vengono salvati molti file, quasi tutti rumore: risposte HTTP di vario tipo con nomi come `get%3fpattern=...`, `list-components`, `__locations`. In mezzo c'è `Gatto.jpeg`. La finestra di Export Objects permette anche di restringere l'elenco per tipo di contenuto, utile per trovare subito le immagini.
4. Apro `Gatto.jpeg`: la flag è scritta sulla foto.

A differenza della Challenge 10, qui l'immagine è stata estratta integra e si apre senza problemi, quindi non serve nessun passaggio con Export Packet Bytes.

## Cosa ho imparato

- **Titolo e descrizione** sono indizi: un titolo in leetspeak come "G4tto" va letto come la parola normale ("gatto"), e quella parola dice che cosa cercare (qui un'immagine).
- Follow Stream mostra il traffico come testo, ma quando i dati sono un file (immagine, programma, ...) lo strumento giusto è **Export Objects**.
- La flag non è per forza nel testo dei pacchetti: può stare *dentro* un file trasferito, e per leggerla bisogna prima estrarlo.
