---
title: "Protocollo datagramma utente"
source: cyberchallenge
category: network
points: 494
difficulty: 
date: 2026-11-25
status: done
---

# Protocollo datagramma utente

Autore: killua · File fornito: `chall.pcapng`

## Descrizione

> Riesci a ricostruire la flag tra tutti questi pacchetti?

Come per gli altri writeup di questo repo, la flag non è riportata.

## TL;DR

Il titolo è la traduzione di *User Datagram Protocol*, quindi la flag viaggia in UDP. Filtrando i pacchetti UDP e usando **Follow UDP Stream** i datagrammi vengono ricomposti in un unico testo, in fondo al quale si legge la flag.

## Analisi

Il titolo "Protocollo datagramma utente" è la traduzione italiana di *User Datagram Protocol*, cioè UDP: è l'indizio da cui partire.

Ho usato le tecniche delle [challenge intro di Wireshark](../wireshark-intro/README.md): il [filtro per protocollo](../wireshark-intro/README.md#challenge-3--filtrare-per-protocollo) (Challenge 3) e il [Follow Stream](../wireshark-intro/README.md#challenge-7--follow-tcp-stream) (Challenge 7), qui nella versione per UDP.

Nell'elenco dei pacchetti UDP c'è anche traffico che non fa parte della soluzione, per esempio datagrammi multicast verso `239.255.255.250`. La conversazione utile è quella tra due host, `192.168.75.145` e `192.168.75.141`: il primo chiede al server il "segreto" e il server risponde con molti datagrammi consecutivi.

## Soluzione

1. Apro `chall.pcapng` con Wireshark.
2. Filtro i pacchetti che usano il protocollo UDP:
   ```
   udp
   ```
3. Seleziono uno dei pacchetti della conversazione tra i due host (non quelli multicast) e apro **Analyze → Follow → UDP Stream**. Nel mio caso Wireshark applica il filtro `udp.stream eq 1`.
4. Nella finestra i datagrammi sono ricomposti in un unico testo: dopo lo scambio iniziale tra client e server, in fondo allo stream si legge la flag.

## Cosa ho imparato

- Il **titolo** di una challenge può essere un indizio: qui "Protocollo datagramma utente" dice già quale protocollo guardare.
- UDP non ha connessione né handshake come TCP, quindi non ci sono `SYN`/`ACK` da cercare. Wireshark raggruppa comunque i datagrammi in stream in base a indirizzi e porte, e **Follow UDP Stream** li mostra uno dopo l'altro come un unico testo.
- Un filtro per protocollo (`udp`) toglie il rumore degli altri protocolli, ma poi serve isolare la singola conversazione.
