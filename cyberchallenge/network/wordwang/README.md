---
title: "wordwang"
source: cyberchallenge
category: network
points: 498
difficulty: 
date: 2026-11-26
status: done
---

# wordwang

Autore: kientuong114 · File fornito: `capture.pcap` · Servizio remoto: `nc wordwang.challs.olicyber.it 10601`

## Descrizione

> Dopo lo spettacolare successo di NumberWang siamo qui con una nuova edizione del gioco preferito dalle persone dai 25 ai 25 anni e mezzo: WordWang! Riuscirai ad ottenere il WordWang?
>
> Puoi collegarti al servizio remoto con: `nc wordwang.challs.olicyber.it 10601`

Come per gli altri writeup di questo repo, la flag non è riportata.

## TL;DR

Il pcap contiene la registrazione di una partita a WordWang giocata da qualcun altro, con la flag oscurata. Leggendola si capisce la regola del gioco: la risposta giusta è la parola mostrata dal server **in maiuscolo, preceduta da `?` e seguita da `!`**. La parola cambia a ogni connessione, quindi la regola si applica alla parola che mostra il servizio remoto al momento del collegamento.

## Analisi

La challenge ha due parti: un file di cattura e un servizio remoto a cui collegarsi con `nc`. Ho aperto il pcap con le tecniche delle [challenge intro di Wireshark](../wireshark-intro/README.md), in particolare il [Follow Stream](../wireshark-intro/README.md#challenge-7--follow-tcp-stream) (Challenge 7).

Lo stream mostra tutti i passaggi di un utente che gioca: il server saluta e propone una parola, l'utente prova diverse risposte e a quelle sbagliate il server replica con `That's NOT wordwang!`. Finché una risposta viene accettata e il server risponde con un messaggio di vittoria seguito dalla flag. Nella cattura però la flag è sostituita da `[REDACTED]`: il pcap non basta, bisogna giocare sul servizio remoto.

All'inizio ho pensato di dover rigiocare la soluzione dell'utente, cioè rimandare le stesse risposte. Non funziona: **a ogni connessione il server propone una parola diversa**, quindi le risposte dell'utente nella cattura valgono solo per la sua parola e vengono rifiutate. Ho capito allora che non bisognava copiare la soluzione, ma capire la regola che la rende giusta. L'ultima risposta dell'utente, quella accettata, è la parola del server in maiuscolo con un `?` davanti e un `!` dietro; le risposte rifiutate sono invece la parola in altre forme (minuscolo, solo maiuscolo, ...).

## Soluzione

1. Apro `capture.pcap` con Wireshark e leggo la partita con **Analyze → Follow → TCP Stream**: individuo la risposta accettata e il formato `?PAROLA!`.
2. Mi collego al servizio remoto:
   ```bash
   nc wordwang.challs.olicyber.it 10601
   ```
3. Il server saluta e mostra una parola (diversa a ogni connessione). La riscrivo in maiuscolo, con `?` davanti e `!` dietro. Per esempio, se il server propone `tree`, rispondo:
   ```
   ?TREE!
   ```
4. Il server risponde con il messaggio di vittoria e la flag. Se sbaglio, risponde `That's NOT wordwang!` e posso riprovare.

## Cosa ho imparato

- Una cattura non contiene per forza la flag, qui è oscurata: può servire invece a far capire **come funziona un servizio remoto**, da cui dedurre la regola da applicare dal vivo.
- Rigiocare (*replay*) le risposte di un'altra partita non funziona se il servizio cambia i dati a ogni connessione: bisogna capire la **regola**, non copiare la soluzione.
- Le risposte rifiutate (`That's NOT wordwang!`) sono informazione quanto quella accettata: dicono quali forme non vanno bene.
- `nc` (netcat) permette di parlare a mano con un servizio remoto, scrivendo le risposte direttamente nel terminale.
