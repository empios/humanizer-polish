"""Wspólne funkcje skryptów: wczytanie tekstu, akapity, zdania i słowa.

Tylko biblioteka standardowa, żeby skrypty działały w każdym środowisku agenta.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Skróty, po których kropka nie kończy zdania (małymi literami, bez kropki końcowej).
# Skróty, które często stoją na końcu zdania („r.”, „itd.”, „k.c.”, „zł”), tu nie należą:
# po nich wielka litera częściej zaczyna nowe zdanie, niż kontynuuje stare.
SKROTY = {
    "np", "tj", "tzw", "tzn", "m.in", "art", "ust", "pkt", "par", "lit", "s", "t", "nr", "poz",
    "zob", "por", "ok", "dr", "prof", "hab", "inż", "mgr", "godz", "ul", "al", "red", "wyd",
    "dz", "u", "ww", "jw", "tab", "rys", "ryc", "zm", "sygn", "ws", "wg", "im", "św", "rozdz",
    "ang", "łac", "niem", "fr", "ds", "sp", "pt", "ub", "vs", "cz", "zw", "przyp",
}

_GRANICA = re.compile(r"([.!?…]+[\"”»)\]]*)\s+(?=[\"„«(\[]?[A-ZĄĆĘŁŃÓŚŹŻ0-9])")
_SLOWO = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*|\d+(?:[.,]\d+)*")
_KONIEC_ZDANIA = re.compile(r"[.!?…:;\"”»)]\s*$")


_BIBLIOGRAFIA = re.compile(
    r"^(?:\d+\.?\s*)?(?:bibliografia|literatura(?: cytowana)?|piśmiennictwo|references|"
    r"źródła|przypisy|bibliography)\s*:?\s*$",
    re.IGNORECASE,
)
_POZYCJA_BIBLIOGRAFII = re.compile(r"^\[\d+\]|\bdoi:\s*10\.|\bdoi\.org/")


def wczytaj_akapity(sciezka: str | Path, linie: bool | None = None) -> list[str]:
    """Akapity prozy z pliku .txt, .md albo .docx.

    Pomija nagłówki, podpisy, tabele, kod, pozycje bibliografii i wszystko po nagłówku
    „Bibliografia” (albo „Literatura”, „References”). `linie=True` traktuje każdą niepustą
    linię jako akapit; `None` wybiera sam: akapity rozdzielone pustą linią, a gdy pustych
    linii brak, każda linia osobno.
    """
    p = Path(sciezka)
    if p.suffix.lower() == ".docx":
        surowe = _akapity_docx(p)
    else:
        surowe = _akapity_tekstu(p.read_text(encoding="utf-8"), linie)
    wynik = []
    for tekst, naglowek in surowe:
        if _BIBLIOGRAFIA.match(tekst):
            break
        if naglowek or _to_naglowek(tekst) or _POZYCJA_BIBLIOGRAFII.search(tekst):
            continue
        wynik.append(tekst)
    return wynik


def _akapity_tekstu(tekst: str, linie: bool | None) -> list[tuple[str, bool]]:
    wiersze: list[tuple[str, bool]] = []
    w_kodzie = False
    for wiersz in tekst.splitlines():
        if wiersz.strip().startswith("```"):
            w_kodzie = not w_kodzie
            wiersze.append(("", False))
            continue
        if w_kodzie or wiersz.lstrip().startswith("|"):
            wiersze.append(("", False))
            continue
        if wiersz.lstrip().startswith("#"):
            wiersze += [("", False), (wiersz.lstrip("# ").strip(), True), ("", False)]
            continue
        wiersz = re.sub(r"^\s*(?:>\s*)+", "", wiersz)
        wiersz = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", wiersz)
        wiersze.append((wiersz, False))
    niepuste = [w for w in wiersze if w[0].strip()]
    if linie is None:
        puste_przerwy = any(not w[0].strip() for w in wiersze[1:-1])
        linie = not puste_przerwy and len(niepuste) > 3
    if linie:
        return [(w.strip(), n) for w, n in niepuste]
    wynik, blok = [], []
    for w, n in wiersze + [("", False)]:
        if n:
            wynik.append((w, True))
        elif w.strip():
            blok.append(w)
            continue
        if blok:
            wynik.append((" ".join(" ".join(blok).split()), False))
            blok = []
    return wynik


def _akapity_docx(p: Path) -> list[tuple[str, bool]]:
    with zipfile.ZipFile(p) as archiwum:
        korzen = ElementTree.fromstring(archiwum.read("word/document.xml"))
    cialo = korzen.find(f"{W}body")
    wynik = []
    for akapit in cialo.findall(f"{W}p") if cialo is not None else []:
        styl = akapit.find(f"{W}pPr/{W}pStyle")
        nazwa = (styl.get(f"{W}val") or "").lower() if styl is not None else ""
        naglowek = any(s in nazwa for s in ("heading", "nagłówek", "naglowek", "title", "tytuł", "caption"))
        tekst = "".join(t.text or "" for t in akapit.iter(f"{W}t"))
        if tekst.strip():
            wynik.append((" ".join(tekst.split()), naglowek))
    return wynik


def _to_naglowek(akapit: str) -> bool:
    """Krótki akapit bez znaku końca zdania traktujemy jak nagłówek albo podpis."""
    return len(slowa(akapit)) <= 12 and not _KONIEC_ZDANIA.search(akapit)


def zdania(akapit: str) -> list[str]:
    """Dzieli akapit na zdania z pominięciem skrótów i inicjałów."""
    wynik, poczatek = [], 0
    for m in _GRANICA.finditer(akapit):
        przed = akapit[poczatek:m.start(1)]
        ostatnie = re.search(r"(\S+)$", przed)
        surowy = ostatnie.group(1).lstrip("(„\"[").rstrip(".") if ostatnie else ""
        znak = m.group(1).rstrip("\"”»)]")
        inicjal = re.fullmatch(r"[A-ZĄĆĘŁŃÓŚŹŻ]", surowy)
        if znak == "." and (surowy.lower() in SKROTY or inicjal):
            continue
        wynik.append(akapit[poczatek:m.end(1)].strip())
        poczatek = m.end()
    reszta = akapit[poczatek:].strip()
    if reszta:
        wynik.append(reszta)
    return wynik


def slowa(tekst: str) -> list[str]:
    """Słowa i liczby; łącznik wewnątrz wyrazu nie dzieli go na dwa."""
    return _SLOWO.findall(tekst)
