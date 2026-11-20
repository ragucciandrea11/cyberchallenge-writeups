---
title: "Network Security - Intro: Wireshark"
source: cyberchallenge
category: network
points: 
difficulty: intro
date: 2026-11-20
status: done
---

# Network Security – Intro: Wireshark

Le 10 challenge introduttive di Network Security servono a prendere confidenza con l'analisi dei file `.pcap` tramite [Wireshark](https://www.wireshark.org/): struttura di una comunicazione TCP, filtri di visualizzazione, Follow Stream, esportazione di byte e oggetti, decifratura del traffico TLS.

Per ogni challenge riporto cosa serve capire e quali filtri o funzioni di Wireshark ho usato. Le flag non sono riportate.

## Setup

Wireshark è un ottimo software con interfaccia grafica per analizzare i file pcap. Su Linux basta installarlo dalle repository standard:

```bash
sudo apt install wireshark
```

## Riepilogo

| # | Tema | Strumento / filtro chiave |
|---|---|---|
| 1 | Struttura di una comunicazione TCP | three-way handshake |
| 2 | Anatomia di un pacchetto | MAC, IP, lunghezza, dati |
| 3 | Filtrare per protocollo | `http` |
| 4 | Filtro con espressione logica | `ip.src == 192.168.100.3 && dns` |
| 5 | Commenti ai pacchetti | Statistics → Capture File Properties |
| 6 | Cercare un contenuto | `frame contains "..."` |
| 7 | Seguire una sessione | Follow TCP Stream |
| 8 | Estrarre i byte di un pacchetto | Export Packet Bytes |
| 9 | Decifrare il traffico TLS | log delle chiavi (Pre)-Master-Secret |
| 10 | Estrarre oggetti HTTP | Export Objects + Export Packet Bytes |

## Challenge 1 – Struttura di una comunicazione TCP

Una comunicazione TCP ha una struttura ben definita. La connessione si stabilisce con il **three-way handshake**, che garantisce l'affidabilità e inizializza i numeri di sequenza (`Seq`) e di conferma (`Ack`):

1. il client invia un pacchetto `SYN`;
2. il server risponde con `SYN/ACK`;
3. il client conferma con `ACK`.

Dopo l'handshake i dati viaggiano in pacchetti con flag `PSH` (invio del messaggio) e ogni ricezione viene confermata da un `ACK`. L'andamento tipico è quindi:

```
SYN → SYN/ACK → ACK → PSH/ACK → ACK → …
```

## Challenge 2 – Anatomia di un pacchetto

Ogni pacchetto porta con sé le informazioni necessarie per essere elaborato e instradato:

- MAC address sorgente e destinatario (livello Ethernet)
- indirizzo IP sorgente e destinatario (livello IP)
- lunghezza
- byte dei dati (payload)
- altri campi degli header

In Wireshark ogni livello compare nel pannello dei dettagli del pacchetto, ed è da lì che si leggono questi campi.

## Challenge 3 – Filtrare per protocollo

Documentazione: [Display filters](https://www.wireshark.org/docs/wsug_html_chunked/ChWorkDisplayFilterSection.html)

Per trovare la soluzione basta filtrare i pacchetti in base al protocollo, mostrando solo quelli che usano HTTP.

```
http
```

## Challenge 4 – Espressione logica

Serve un'espressione logica che combini due condizioni: indirizzo IP sorgente (`192.168.100.3`) e protocollo (DNS). L'operatore `&&` richiede che siano vere entrambe.

```
ip.src == 192.168.100.3 && dns
```

## Challenge 5 – Commenti ai pacchetti

Bisogna trovare i commenti inseriti nella cattura. Si trovano dal menu:

**Statistics → Capture File Properties → Packet Comments**

## Challenge 6 – Cercare un contenuto

Tra molti pacchetti bisogna individuare quello che contiene un preciso contenuto. L'operatore `contains` cerca la stringa nei byte del frame, qualunque sia il protocollo:

```
frame contains "Pwn all the things!!!"
```

## Challenge 7 – Follow TCP Stream

Documentazione: [Following protocol streams](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html)

Il file pcap è di grandi dimensioni e contiene anche molti pacchetti ICMP sparsi che non interessano. La soluzione più efficiente è isolare la sessione di interesse e visualizzarla per intero, invece di scorrere i pacchetti uno a uno.

1. Filtro i pacchetti TCP:
   ```
   tcp
   ```
2. **Analyze → Follow → TCP Stream** ricostruisce l'intera comunicazione in un'unica finestra.

## Challenge 8 – Esportare i byte di un pacchetto

Documentazione: [Export](https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html)

La cattura contiene un breve scambio di pacchetti TCP. A noi interessa il frame con i dati inviati dall'IP `192.168.100.1` all'IP `192.168.100.2`: per ottenere la soluzione bisogna estrarre i byte di quel pacchetto e analizzarne il contenuto.

1. Individuo il three-way handshake della comunicazione e il pacchetto con flag `PSH`, quello in cui vengono trasmessi i dati:
   ```
   tcp && ip.src == 192.168.100.1 && ip.dst == 192.168.100.2
   ```
2. Seleziono il pacchetto e, nel pannello dei dettagli, il campo che contiene i dati (il payload).
3. **File → Export Packet Bytes** salva su file i byte del campo selezionato, che posso poi analizzare.

## Challenge 9 – Decifrare il traffico TLS

Per risolvere la challenge bisogna decifrare il traffico TLS usando il file con il log delle chiavi (formato NSS key log, quello che i browser producono con la variabile `SSLKEYLOGFILE`). Una volta decifrato con successo il traffico, Wireshark riconosce automaticamente il contenuto dei pacchetti cifrati.

1. **Edit → Preferences → Protocols → TLS → (Pre)-Master-Secret log filename**, e inserisco il file con le chiavi TLS.
2. Tra i pacchetti ora decifrati cerco quello HTTPS catturato da una `GET` al link `https://olicyber.it/`: la soluzione è nel suo header.

## Challenge 10 – Esportare oggetti HTTP

Documentazione: [Export Objects](https://www.wireshark.org/docs/wsug_html_chunked/ChIOExportSection.html#ChIOExportObjectsDialog)

Questa challenge fa scoprire l'esportazione degli oggetti trasferiti durante la comunicazione: pagine web, software, immagini, …

1. **File → Export Objects → HTTP**, poi *Save All* (opzionale, in base alle esigenze).
2. I file estratti sono due: una pagina web e un'immagine corrotta. L'immagine, nella fase di estrazione, si è portata dietro dei dati in più che la rendono illeggibile. Il body della risposta è infatti un messaggio multipart, e l'export dell'oggetto salva tutto il body, non solo i byte del PNG.
3. Estraggo allora solo la sezione del pacchetto che contiene l'immagine. Seleziono il pacchetto in cui è stata inviata e nel pannello dei dettagli scendo di livello in livello:

   *Hypertext Transfer Protocol → MIME Multipart Media Encapsulation → Encapsulated multipart → Portable Network Graphics*

4. Tasto destro sul livello **Portable Network Graphics → Export Packet Bytes**: il file salvato è un PNG valido.

## Cosa ho imparato

- Prima di scrivere filtri complessi conviene conoscere la struttura del protocollo: handshake, flag `PSH`, header dei vari livelli.
- Tre strumenti per tre esigenze: i **filtri** restringono i pacchetti, **Follow Stream** ricostruisce una sessione intera, **Export** estrae i dati.
- **Export Packet Bytes** salva i byte del *campo selezionato*: scegliere il livello giusto nel pannello dei dettagli fa la differenza (challenge 8 e 10).
- Per leggere traffico TLS serve il log delle chiavi, da indicare nelle preferenze del protocollo TLS.
