#!/usr/bin/env python3
"""Porównuje dwie wersje tekstu i wypisuje elementy chronione, które się zmieniły.

Użycie: python3 scripts/porownaj_wersje.py PRZED PO [--json] [--linie]
PRZED, PO: .txt, .md albo .docx. Kod wyjścia 1 oznacza różnice do sprawdzenia (§27-§29).
Liczby porównujemy po ujednoliceniu zapisu: „0,53” = „0.53”, „1 804” = „1804”, „8” = „osiem”.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tekst_pl import wczytaj_akapity  # noqa: E402

_LICZBA = re.compile(
    r"(?<![\w.,])−?\d{1,3}(?:[ \u00a0\u202f]\d{3})+(?:[.,]\d+)?(?![\w])"
    r"|(?<![\w.,])−?\d+(?:[.,]\d+)*(?!\w)"
)
# Liczebniki 2-20 zapisane słownie; „jeden” pomijamy, bo bywa zaimkiem („jeden z”).
LICZEBNIKI = {
    2: "dwa|dwie|dwóch|dwóm|dwoma", 3: "trzy|trzech|trzem|trzema", 4: "cztery|czterech|czterem|czterema",
    5: "pięć|pięciu|pięcioma", 6: "sześć|sześciu|sześcioma", 7: "siedem|siedmiu|siedmioma",
    8: "osiem|ośmiu|ośmioma", 9: "dziewięć|dziewięciu|dziewięcioma", 10: "dziesięć|dziesięciu|dziesięcioma",
    11: "jedenaście|jedenastu", 12: "dwanaście|dwunastu", 13: "trzynaście|trzynastu",
    14: "czternaście|czternastu", 15: "piętnaście|piętnastu", 16: "szesnaście|szesnastu",
    17: "siedemnaście|siedemnastu", 18: "osiemnaście|osiemnastu", 19: "dziewiętnaście|dziewiętnastu",
    20: "dwadzieścia|dwudziestu",
}
_PRZEPIS = re.compile(
    r"\b(?:art\.|ust\.|pkt|lit\.|par\.)\s*\d+[a-z]*|§\s*\d+[a-z]*|\bDz\.\s*U\.(?:\s*z\s*\d{4}\s*r\.)?"
    r"(?:\s*(?:Nr\s*\d+,?\s*)?poz\.\s*\d+)?|\b[kK]\.\s?(?:p\.\s?)?[cpk]\.(?:\s?a\.)?",
)
_CYTOWANIE = re.compile(
    r"\[\d+(?:\s*[–,-]\s*\d+)*\]|\((?:[A-ZĄĆĘŁŃÓŚŹŻ][^()]{0,80}?),?\s*\d{4}[a-z]?\)"
    r"|\b10\.\d{4,9}/[^\s,;)]+|https?://[^\s)]+"
)
_CYTAT = re.compile(r"„([^”]{1,400})”|\"([^\"]{1,400})\"|“([^”]{1,400})”")
_SYMBOL = re.compile(r"\[[A-ZĄĆĘŁŃÓŚŹŻ0-9 _]{2,}\]|\{\{[^}]+\}\}|<[A-Z_]{2,}>")
_SYGNATURA = re.compile(r"\b[IVXL]+\s+[A-Z][A-Za-z]{0,4}\s+\d+/\d{2,4}\b")

MODALNE = {
    "musieć": r"\bmus(?:i|zą|zę|isz|imy|icie|iał\w*|ieli|ieć|iano)\b",
    "powinien": r"\bpowin(?:ien|na|no|ni|ny|nam|nem|nyśmy|niśmy)\b",
    "móc": r"\b(?:może|mogą|mogę|możesz|możemy|możecie|mógł|mogła|mogło|mogli|mogły|móc|mogąc)\b",
    "nie móc": r"\bnie\s+(?:może|mogą|mógł|mogła|mogło|mogli|mogły|móc)\b",
    "można": r"\bmożna\b",
    "należy": r"\bnależy\b",
    "trzeba": r"\btrzeba\b",
    "wolno": r"\bwolno\b",
    "mieć prawo": r"\bma(?:ją)?\s+prawo\b|\bmiał\w*\s+prawo\b",
    "obowiązek": r"\bobowiąz(?:any|ana|ane|ani|ek|ku|kiem|ki|ków|uje|ują|ywać)\w*",
    "zakaz": r"\bzakaz\w*|\bzabroni\w*",
    "uprawnienie": r"\buprawni\w+",
}
PRZECZENIA = {
    "nie": r"\bnie\b",
    "nigdy": r"\bnigdy\b",
    "żaden": r"\bżadn\w*|\bżaden\b",
    "nikt": r"\bnikt\w*|\bnikogo\b|\bnikomu\b|\bnikim\b",
    "nic": r"\bnic\b|\bniczego\b|\bniczym\b|\bniczemu\b",
    "ani": r"\bani\b",
}
STRONY = {
    "najemca": r"\bnajemc\w*", "wynajmujący": r"\bwynajmując\w*",
    "wydzierżawiający": r"\bwydzierżawiając\w*", "dzierżawca": r"\bdzierżawc\w*",
    "powód": r"\bpow(?:ód|od\w+)\b", "pozwany": r"\bpozwan\w*",
    "wnioskodawca": r"\bwnioskodawc\w*", "uczestnik": r"\buczestni\w+",
    "pracodawca": r"\bpracodawc\w*", "pracownik": r"\bpracowni(?:k|ka|kowi|kiem|ku|cy|ków|kom|kami|kach)\b",
    "zamawiający": r"\bzamawiając\w*", "wykonawca": r"\bwykonawc\w*",
    "zleceniodawca": r"\bzleceniodawc\w*", "zleceniobiorca": r"\bzleceniobiorc\w*",
    "sprzedawca": r"\bsprzeda(?:wc|jąc)\w*", "kupujący": r"\bkupując\w*",
    "wierzyciel": r"\bwierzyciel\w*", "dłużnik": r"\bdłużni\w+",
    "darczyńca": r"\bdarczyńc\w*", "obdarowany": r"\bobdarowan\w*",
}


def _norm_liczba(s: str) -> str:
    s = re.sub(r"[ \u00a0\u202f]", "", s)
    if re.fullmatch(r"−?\d+,\d+", s):
        s = s.replace(",", ".")
    return s


def _norm(s: str) -> str:
    return " ".join(s.split())


def wyciagnij(tekst: str) -> dict[str, Counter]:
    tekst_bez_przepisow = _PRZEPIS.sub(" ", tekst)
    cytaty = Counter(_norm(next(g for g in m.groups() if g)) for m in _CYTAT.finditer(tekst))
    maly = tekst.lower()
    liczby = Counter(_norm_liczba(m.group(0)) for m in _LICZBA.finditer(tekst_bez_przepisow))
    for wartosc, wzor in LICZEBNIKI.items():
        n = len(re.findall(rf"\b(?:{wzor})\b", tekst_bez_przepisow.lower()))
        if n:
            liczby[str(wartosc)] += n
    return {
        "liczby": liczby,
        "przepisy": Counter(_norm(m.group(0)) for m in _PRZEPIS.finditer(tekst)),
        "sygnatury": Counter(_norm(m.group(0)) for m in _SYGNATURA.finditer(tekst)),
        # Półpauza w „[3–5]” zamieniona na łącznik (§8) to ten sam przedział.
        "cytowania i adresy": Counter(_norm(m.group(0)).rstrip(".").replace("–", "-")
                                      for m in _CYTOWANIE.finditer(tekst)),
        "cytaty": cytaty,
        "symbole zastępcze": Counter(m.group(0) for m in _SYMBOL.finditer(tekst)),
        "modalność": Counter({k: len(re.findall(w, maly)) for k, w in MODALNE.items()}),
        "przeczenia": Counter({k: len(re.findall(w, maly)) for k, w in PRZECZENIA.items()}),
        "strony": Counter({k: len(re.findall(w, maly)) for k, w in STRONY.items()}),
    }


ZLICZANE = {"modalność", "przeczenia", "strony"}


def porownaj(przed: str, po: str) -> dict[str, dict]:
    a, b = wyciagnij(przed), wyciagnij(po)
    wynik = {}
    for kategoria in a:
        if kategoria in ZLICZANE:
            zmiany = {k: [a[kategoria][k], b[kategoria][k]] for k in a[kategoria]
                      if a[kategoria][k] != b[kategoria][k]}
            if zmiany:
                wynik[kategoria] = {"zmiany": zmiany}
            continue
        zniknelo = a[kategoria] - b[kategoria]
        pojawilo = b[kategoria] - a[kategoria]
        if zniknelo or pojawilo:
            wynik[kategoria] = {"zniknelo": sorted(zniknelo.elements()),
                                "pojawilo_sie": sorted(pojawilo.elements())}
    return wynik


def raport(nazwa_a: str, nazwa_b: str, roznice: dict) -> str:
    if not roznice:
        return (f"{nazwa_a} → {nazwa_b}: liczby, przepisy, cytowania, cytaty, modalność, "
                "przeczenia i strony bez zmian.")
    linie = [f"{nazwa_a} → {nazwa_b}: różnice do sprawdzenia", ""]
    for kategoria, r in roznice.items():
        linie.append(kategoria)
        if "zmiany" in r:
            for k, (x, y) in r["zmiany"].items():
                linie.append(f"  {k}: {x} → {y}")
        else:
            if r["zniknelo"]:
                linie.append("  zniknęło: " + "; ".join(r["zniknelo"]))
            if r["pojawilo_sie"]:
                linie.append("  pojawiło się: " + "; ".join(r["pojawilo_sie"]))
    linie += ["", "Każda różnica to błąd, chyba że wzorzec z SKILL.md kazał coś wyciąć (§27-§29)."]
    return "\n".join(linie)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("przed")
    parser.add_argument("po")
    parser.add_argument("--json", action="store_true", help="wynik jako JSON")
    parser.add_argument("--linie", action="store_true", help="każda linia to osobny akapit")
    args = parser.parse_args()
    linie = True if args.linie else None
    przed = "\n".join(wczytaj_akapity(args.przed, linie=linie))
    po = "\n".join(wczytaj_akapity(args.po, linie=linie))
    roznice = porownaj(przed, po)
    if args.json:
        print(json.dumps(roznice, ensure_ascii=False, indent=2))
    else:
        print(raport(Path(args.przed).name, Path(args.po).name, roznice))
    return 1 if roznice else 0


if __name__ == "__main__":
    raise SystemExit(main())
