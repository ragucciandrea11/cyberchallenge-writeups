---
title: "Useless"
source: cyberchallenge
category: network
points: 
difficulty: 
date: 2026-11-20
status: done
---

# Useless

## Descrizione

> Ho rubato questo file da un server molto importante, ma non riesco a trovare nulla di utile in questi pacchetti, la loro sicurezza è impenetrabile.

La challenge fornisce un file di cattura di rete (`.pcap`) da analizzare con Wireshark.

## TL;DR

La flag non sta nel contenuto dei pacchetti, ma nei **commenti della cattura**: si leggono da *Statistics → Capture File Properties*.

## Analisi

Il testo insiste sul fatto che nei pacchetti non c'è nulla di utile. Ho applicato le tecniche viste nelle [challenge intro di Wireshark](../wireshark-intro/README.md) e quella che ha portato alla soluzione è la [Challenge 5](../wireshark-intro/README.md#challenge-5--commenti-ai-pacchetti): guardare i commenti inseriti nel file di cattura.

## Soluzione

1. Apro il file pcap con Wireshark.
2. **Statistics → Capture File Properties**.
3. Nella sezione **Packet Comments** è presente la flag.

## Cosa ho imparato

- Un file pcap contiene anche **metadati**, non solo pacchetti: i commenti della cattura non compaiono nel contenuto dei pacchetti e vanno cercati a parte.
- Prima di analizzare i pacchetti uno a uno conviene dare un'occhiata a *Capture File Properties*: è un controllo veloce che può far risparmiare molto tempo.
