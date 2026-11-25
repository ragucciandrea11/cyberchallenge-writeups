# CyberChallenge writeups

Writeup delle challenge che risolvo sulla piattaforma [CyberChallenge.IT](https://cyberchallenge.it/) mentre mi alleno.
Li scrivo per fissare quello che imparo e, spero, per essere utili a chi si sta allenando come me.

<!-- TODO: due righe su di te (nome/nick, università, link a profilo CTFtime o LinkedIn) -->

## Indice

<!-- INDEX:START -->
**Writeup pubblicati: 4**

### cyberchallenge

| Challenge | Categoria | Difficoltà | Punti | Data |
|---|---|---|---|---|
| [Network Security - Intro: Wireshark](cyberchallenge/network/wireshark-intro/) | network | intro | - | 2026-11-20 |
| [Protocollo datagramma utente](cyberchallenge/network/protocollo-datagramma-utente/) | network | - | 494 | 2026-11-25 |
| [sniff-n-byte](cyberchallenge/network/sniff-n-byte/) | network | - | - | - |
| [Useless](cyberchallenge/network/useless/) | network | - | - | 2026-11-20 |
<!-- INDEX:END -->

## Struttura del repo

```
<piattaforma>/<categoria>/<nome-challenge>/
├── README.md     # il writeup (con intestazione YAML: titolo, punti, difficoltà, data, stato)
├── solve.py      # exploit / script risolutivo (se serve)
├── img/          # screenshot usati nel writeup
└── files/        # file della challenge (solo se è lecito ridistribuirli)
```

Categorie: `web`, `crypto`, `pwn`, `rev`, `forensics`, `network`, `misc`.
Altri CTF o piattaforme avranno una cartella di primo livello propria, accanto a `cyberchallenge/`.

## Aggiungere un writeup

```bash
# 1. crea la cartella dalla template
python3 ctf.py new web "SQL Injection 101" --points 100 --difficulty easy

# 2. scrivi il writeup in cyberchallenge/web/sql-injection-101/README.md
#    quando è finito, cambia "status: wip" in "status: done"

# 3. aggiorna l'indice qui sopra e pubblica
python3 ctf.py index
git add .
git commit -m "web: add sql-injection-101 writeup"
git push
```

Solo libreria standard di Python 3, nessuna dipendenza da installare.

## Nota

I writeup sono pubblicati a scopo didattico. I testi e i file delle challenge appartengono ai rispettivi autori e organizzatori.
