---
title: "easy stream"
source: cyberchallenge
category: network
points: 492
difficulty: 
date: 2026-11-25
status: done
---

# easy stream

Autore: minn3 · File fornito: `easy_stream.pcapng`

## Descrizione

> Riesci a seguire lo stream?

Come per gli altri writeup di questo repo, la flag non è riportata.

## TL;DR

Titolo e descrizione dicono di seguire uno stream. La cattura contiene molte conversazioni HTTP: filtrando `http` e aprendole una alla volta con **Follow HTTP Stream**, in una la risposta del server è una pagina HTML che contiene la flag.

## Analisi

Il titolo "easy stream" e la descrizione "Riesci a seguire lo stream?" puntano al [Follow Stream](../wireshark-intro/README.md#challenge-7--follow-tcp-stream) (Challenge 7). Ho provato con Follow TCP Stream, ma gli stream che aprivo non mostravano nulla di utile.

Guardando meglio l'elenco dei pacchetti ho visto che c'erano molti scambi con dati inviati via HTTP, tutti su loopback (`127.0.0.1`, il server risponde sulla porta 8080). Sono molte connessioni TCP distinte, ognuna con il proprio numero di stream (`tcp.stream eq N`): per questo non basta aprirne una sola. Molte richieste `GET` si ripetono a intervalli regolari, sempre uguali.

## Soluzione

1. Apro `easy_stream.pcapng` con Wireshark.
2. Filtro i pacchetti HTTP, come nella [Challenge 3](../wireshark-intro/README.md#challenge-3--filtrare-per-protocollo):
   ```
   http
   ```
3. Seleziono un pacchetto e apro **Analyze → Follow → HTTP Stream**. Nella finestra la casella *Stream* permette di passare da uno stream all'altro senza tornare all'elenco.
4. Controllo gli stream uno per uno. Le richieste ripetute hanno risposte di altro tipo (per esempio in JSON), mentre un solo stream (nel mio caso `tcp.stream eq 10`) contiene una `GET` su `/HttpEcho/Echo` la cui risposta è una piccola pagina HTML: la flag è scritta in un titolo della pagina.

## Cosa ho imparato

- **Titolo e descrizione** indicano lo strumento da usare: qui "stream" voleva dire Follow Stream.
- Una cattura può contenere **molti stream**, e la flag sta in uno solo: non basta aprirne uno, bisogna passarli in rassegna. Il filtro `http` restringe l'elenco alle conversazioni applicative e la casella *Stream* della finestra Follow permette di scorrerle.
- In questa cattura le richieste ripetute identiche a intervalli regolari erano rumore, mentre la richiesta che compariva una volta sola era quella giusta.
