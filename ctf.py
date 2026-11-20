#!/usr/bin/env python3
"""Helper per tenere in ordine i writeup.

Uso:
  python3 ctf.py new <categoria> "<nome challenge>" [--points N] [--difficulty easy|medium|hard] [--source cyberchallenge]
  python3 ctf.py index      # rigenera la tabella indice dentro README.md

Usa solo la libreria standard: non serve installare niente.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "templates" / "writeup.md"
README = ROOT / "README.md"

# Categorie ammesse: se ne serve una nuova, aggiungila qui.
CATEGORIES = ["web", "crypto", "pwn", "rev", "forensics", "network", "misc"]
DEFAULT_SOURCE = "cyberchallenge"

START = "<!-- INDEX:START -->"
END = "<!-- INDEX:END -->"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not slug:
        sys.exit(f"Nome non valido: {text!r}")
    return slug


def make_title(raw: str) -> str:
    title = re.sub(r"[-_]+", " ", raw).strip()
    return title[:1].upper() + title[1:]


def cmd_new(args: argparse.Namespace) -> None:
    category = args.category.lower()
    if category not in CATEGORIES:
        sys.exit(
            f"Categoria '{category}' sconosciuta. Usa una tra: {', '.join(CATEGORIES)} "
            "(oppure aggiungila a CATEGORIES in ctf.py)."
        )

    source = slugify(args.source)
    slug = slugify(args.name)
    dest = ROOT / source / category / slug
    if dest.exists():
        sys.exit(f"Esiste già: {dest.relative_to(ROOT).as_posix()}")

    title = make_title(args.name)
    values = {
        "title": title,
        "title_yaml": title.replace('"', '\\"'),
        "source": source,
        "category": category,
        "points": args.points,
        "difficulty": args.difficulty,
        "date": dt.date.today().isoformat(),
    }
    text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{%s}}" % key, value)

    dest.mkdir(parents=True)
    (dest / "files").mkdir()  # file forniti dalla challenge (vuote = non finiscono su git)
    (dest / "img").mkdir()  # screenshot
    (dest / "README.md").write_text(text, encoding="utf-8")

    rel = dest.relative_to(ROOT).as_posix()
    print(f"Creata {rel}/")
    print(f"  -> scrivi il writeup in {rel}/README.md")
    print(f"  -> exploit/script in {rel}/solve.py, screenshot in {rel}/img/")


def read_meta(path: Path) -> dict[str, str]:
    """Legge il front matter (--- ... ---) in cima a un README di challenge."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    meta: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1].replace('\\"', '"')
            meta[key.strip()] = value
    return meta


def cmd_index(_args: argparse.Namespace) -> None:
    rows = []
    for readme in sorted(ROOT.glob("*/*/*/README.md")):
        rel = readme.relative_to(ROOT)
        if any(part.startswith(".") for part in rel.parts):
            continue
        meta = read_meta(readme)
        if meta.get("status", "done").lower() == "wip":
            continue  # le bozze non compaiono nell'indice
        source, category, slug = rel.parts[:3]
        rows.append(
            {
                "source": source,
                "category": meta.get("category", category),
                "title": meta.get("title", slug),
                "difficulty": meta.get("difficulty", ""),
                "points": meta.get("points", ""),
                "date": meta.get("date", ""),
                "link": f"{source}/{category}/{slug}/",
            }
        )

    rows.sort(key=lambda r: (r["source"], r["category"], r["title"].lower()))

    def esc(s: str) -> str:
        return (s or "-").replace("|", "\\|")

    if not rows:
        block = "_Ancora nessun writeup pubblicato._"
    else:
        parts = [f"**Writeup pubblicati: {len(rows)}**"]
        for source in sorted({r["source"] for r in rows}):
            parts += [
                "",
                f"### {source}",
                "",
                "| Challenge | Categoria | Difficoltà | Punti | Data |",
                "|---|---|---|---|---|",
            ]
            for r in (r for r in rows if r["source"] == source):
                parts.append(
                    f"| [{esc(r['title'])}]({r['link']}) | {esc(r['category'])} | "
                    f"{esc(r['difficulty'])} | {esc(r['points'])} | {esc(r['date'])} |"
                )
        block = "\n".join(parts)

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit(f"Nel README mancano i marcatori {START} e {END}.")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    README.write_text(f"{head}{START}\n{block}\n{END}{tail}", encoding="utf-8")
    print(f"Indice aggiornato: {len(rows)} writeup.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gestione writeup CTF")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="crea la cartella di una nuova challenge")
    p_new.add_argument("category", help="una tra: " + ", ".join(CATEGORIES))
    p_new.add_argument("name", help='nome della challenge (es. "SQL Injection 101")')
    p_new.add_argument("--points", default="", help="punteggio della challenge")
    p_new.add_argument("--difficulty", default="", help="easy / medium / hard")
    p_new.add_argument("--source", default=DEFAULT_SOURCE, help="piattaforma o CTF di origine")
    p_new.set_defaults(func=cmd_new)

    p_index = sub.add_parser("index", help="rigenera l'indice nel README")
    p_index.set_defaults(func=cmd_index)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
