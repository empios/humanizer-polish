#!/usr/bin/env python3
"""Miary rytmu i frazy z list humanizer-polish dla polskiego tekstu.

Użycie: python3 scripts/metryki_pl.py PLIK [--json] [--linie]
PLIK: .txt, .md albo .docx. Wynik to wskazówka dla redaktora, nie wykrywacz AI.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tekst_pl import slowa, wczytaj_akapity, zdania  # noqa: E402

# Frazy według numerów wzorców w SKILL.md. Wyrażenia działają na pojedynczym zdaniu,
# więc ^ oznacza początek zdania.
FRAZY: dict[int, tuple[str, list[str]]] = {
    1: ("Nie X, lecz Y", [
        r"\bnie\s+(?:tylko|jedynie|wyłącznie)\b[^.!?]{0,120}?,\s*(?:lecz|ale)\b",
        r"\bnie chodzi\s+(?:\w+\s+){0,3}?o\b[^.!?]{0,120}?,\s*(?:lecz|ale)\b",
        r"\bnie oznacza to(?:\s+jednak)?,?\s+że\b",
        r"^to nie\s+\w+[^.!?]{0,60},\s*to\b",
    ]),
    2: ("Puenty i dramatyczne równoważniki", [
        r"\bto zmienia wszystko\b", r"\bwniosek jest (?:prosty|jasny|oczywisty)\b",
        r"\bwłaśnie o to chodzi\b", r"\bta różnica ma znaczenie\b",
        r"\bdobitnie (?:pokazuje|świadczy)\b", r"\bpokazuje to,? jak (?:ważn|istotn)\w*",
    ]),
    3: ("Pozorna głębia", [
        r"\bw istocie\b", r"\bu podstaw\w*(?:\s+\w+)?\s+leży\b", r"\bsedn\w+ (?:problemu|sprawy)\b",
        r"\bprawdziwe pytanie brzmi\b", r"\btak naprawdę liczy się\b", r"\bfundamentaln\w+ kwesti\w+",
        r"\bw gruncie rzeczy\b",
    ]),
    4: ("Zapowiedź zamiast treści", [
        r"\b(?:warto|należy)\s+(?:(?:również|także|przy tym|jednak)\s+)?(?:wskazać|zauważyć|podkreślić|"
        r"odnotować|zaznaczyć|nadmienić|przypomnieć|zwrócić uwagę)\b",
        r"\bnie sposób nie (?:zauważyć|wspomnieć)\b", r"\bna uwagę zasługuje\b", r"\bw tym kontekście\b",
        r"\bprzyjrzyjmy się\b", r"^spójrzmy\b", r"\bponiżej przedstawiono\b", r"^zacznijmy od\b",
    ]),
    5: ("Polemika z nikim", [
        r"\bmożna by (?:sądzić|pomyśleć|uznać)\b", r"\bkuszące (?:byłoby|jest)\b",
        r"\bnie zrozummy się źle\b", r"\bżeby było jasne\b", r"\bktoś mógłby (?:zarzucić|powiedzieć)\b",
        r"\bnie twierdzę, że\b", r"\bnie chodzi (?:tu )?o to, by\b",
    ]),
    9: ("Piętrowe asekuracje", [
        r"\bmoże potencjalnie\b", r"\bpotencjalnie mógłby\w*", r"\bw pewnym (?:stopniu|sensie)\b",
        r"\bdo pewnego stopnia\b", r"\bniejako\b", r"\bponiekąd\b", r"\bmożna by przypuszczać\b",
        r"\bnie jest wykluczone\b", r"\bwydaje się, że prawdopodobnie\b",
    ]),
    11: ("Rzeczowniki zamiast czasowników", [
        r"\bdokon\w*\s+(?:analizy|zmian\w*|weryfikacji|oceny|wyboru|podziału|przeglądu)\b",
        r"\bprzeprowadz\w*\s+(?:weryfikacj\w*|ocen\w*)\b",
        r"\bw celu (?:zapewnienia|realizacji|dokonania|przeprowadzenia)\b",
        r"\bma(?:ją)? miejsce\b", r"\bnastępuje (?:wzrost|spadek)\b", r"\bpodj\w+ działa\w*",
    ]),
    12: ("Słowa nadużywane przez modele", [
        r"\bkluczow\w*", r"\bkompleksow\w*", r"\bholistyczn\w*", r"\bwieloaspektow\w*",
        r"\binnowacyjn\w*", r"\bfundamentaln\w*", r"\bnieocenion\w*", r"\bbezprecedensow\w*",
        r"\bszeroko pojęt\w*", r"\bw dzisiejszych czasach\b", r"\bw obliczu\b", r"\bkrajobraz\w*",
        r"\bekosystem\w*", r"\bsynergi\w*", r"\brzuca\w* światło\b", r"\bwpisuj\w* się w\b",
        r"\botwiera\w* drogę\b", r"\bdynamiczn\w*",
    ]),
    13: ("Nadawanie wagi", [
        r"\b(?:ma|mają|miał\w*)\s+(?:bardzo\s+)?(?:istotne|kluczowe|szczególne|duże|ogromne|zasadnicze)"
        r"\s+znaczenie\b",
        r"\b(?:istotne|kluczowe|szczególne|duże|zasadnicze) znaczenie ma(?:ją)?\b",
        r"\b(?:odgrywa|odgrywają|odegrał\w*|pełni|pełnią)\s+(?:bardzo\s+)?(?:istotn|kluczow|ważn|"
        r"szczególn|znacząc|zasadnicz)\w*\s+(?:rolę|funkcję)\b",
        r"\bstanowi\w*\s+jed\w+ z (?:kluczowych|najważniejszych|podstawowych)\b",
        r"\bjedną z najważniejszych\b", r"\b(?:nie sposób|trudno) przecenić\b",
        r"\bw znacznym stopniu\b", r"\bzyskuj\w* na znaczeniu\b", r"\bkamie\w* milow\w*",
        r"\bwyznacza\w* nowy kierunek\b",
    ]),
    14: ("Zbędne wartościowanie i banalne otwarcia", [
        r"\bw dobie\b", r"\bod zarania dziejów\b", r"\bwspółczesny świat\b",
        r"\bnie ulega wątpliwości\b", r"\bjak powszechnie wiadomo\b", r"\bunikatow\w*",
        r"\bogromn\w+ potencja\w*", r"\bniezwykle (?:ciekaw|cenn|ważn|istotn)\w*", r"\bimponując\w*",
        r"\bcenn\w+ (?:zbi\w+|źród\w+|materia\w+|wkład\w*)",
    ]),
    15: ("Mgliste powiązanie", [
        r"\bw kontekście\b", r"\bw odniesieniu do\b", r"\bw nawiązaniu do\b", r"\bw powiązaniu z\b",
        r"\bpowiązan\w+ z\b",
    ]),
    16: ("Imiesłowowe doczepki", [
        r",\s*(?:podkreślając|ukazując|odzwierciedlając|wpisując się|przyczyniając się|uwypuklając|"
        r"akcentując)\b",
        r",\s*co (?:świadczy|wskazuje|czyni|stanowi dowód|potwierdza|podkreśla|pokazuje)\b",
    ]),
    17: ("Pożyczony autorytet i puste przypisy", [
        r"\b(?:liczne |najnowsze |dotychczasowe )?badania (?:pokazują|wskazują|dowodzą|wykazują)\b",
        r"\beksperci (?:wskazują|podkreślają|zauważają)\b",
        r"\bw literaturze (?:podkreśla|wskazuje|zauważa) się\b", r"\bpowszechnie przyjmuje się\b",
        r"\bjak (?:zauważają|wskazują|podkreślają) (?:naukowcy|badacze|eksperci)\b", r"utm_source=",
    ]),
    18: ("Kalki z angielskiego", [
        r"\bw oparciu o\b", r"\badres\w+ (?:problem\w*|wyzwani\w*|kwesti\w*|potrzeb\w*)",
        r"\bzbi\w+ złot\w+", r"\bdedykowan\w*", r"\bimplement\w*", r"\baplik\w+ (?:na|o)\b",
        r"\bfinalnie\b", r"\bbazuj\w*\s+na\b", r"\brekomend\w*", r"\brobi\w* różnicę\b",
        r"\bna koniec dnia\b", r"\bpozostaje do zobaczenia\b", r"\bbycie\b", r"\bkluczow\w+ gracz\w*",
    ]),
    21: ("Formułki czatu i zastrzeżenia o wiedzy", [
        r"\boto (?:poprawiona|zredagowana|przeredagowana|zaktualizowana) wersja\b",
        r"\bmam nadzieję, że (?:to|ta|te) (?:pomoże|pomogą|okaże)", r"\bchętnie pomogę\b",
        r"\bdaj(?:cie)? znać\b", r"\bświetne pytanie\b", r"\bjako model językowy\b",
        r"\bwedług mojej wiedzy\b", r"\bnie mam dostępu do\b",
    ]),
    22: ("Tekst o sobie samym", [
        r"\bw niniejsz\w+ (?:artykule|pracy|rozdziale|opracowaniu)\b",
        r"\bjak (?:wspomniano|wskazano|zaznaczono) (?:powyżej|wcześniej)\b",
        r"\bjak zostanie (?:pokazane|wykazane|omówione)\b",
        r"\bw dalszej części (?:pracy|artykułu|rozdziału)\b", r"\bponiżej omówiono\b",
        r"\bprzedmiotow\w+", r"\bpowyższ\w+", r"\bniniejsz\w+",
    ]),
    23: ("Podsumowanie po każdej sekcji", [
        r"^(?:podsumowując|reasumując|konkludując|jak widać)\b", r"\bwszystko to pokazuje\b",
        r"\bz powyższego wynika\b",
    ]),
}

LACZNIKI = [
    "więc", "zatem", "tym samym", "w konsekwencji", "co za tym idzie", "ponadto", "co więcej",
    "dodatkowo", "jednocześnie", "przy czym", "natomiast", "jednak", "również", "także", "a także",
    "oraz", "dlatego", "w rezultacie", "w efekcie", "z kolei", "tymczasem", "zaś", "mianowicie",
]

FUNKCYJNE = set("""
w we z ze na do od o po przez dla przy pod nad za przed między bez u ku według wobec wśród mimo
oprócz poza obok około dzięki zamiast i oraz a ale lecz jednak lub albo czy ani że żeby aby by gdy
kiedy jeśli jeżeli ponieważ bo więc zatem choć chociaż gdyż jak niż natomiast także również też zaś
czyli mianowicie ponadto dlatego toteż jednocześnie tymczasem nie się to już jeszcze tylko nawet
właśnie chyba
""".split())

_SPOJNIK_TROJKI = re.compile(r"\s(?:oraz|a także|i)\s")
_PODRZEDNE = re.compile(
    r"^(?:któr\w*|że|żeby|aby|by|gdy|gdyż|kiedy|jeśli|jeżeli|bo|ponieważ|choć|chociaż|"
    r"co|gdzie|jak|czy|a|ale|lecz)\b",
    re.IGNORECASE,
)


def cv(wartosci: list[float]) -> float | None:
    if len(wartosci) < 2 or statistics.mean(wartosci) == 0:
        return None
    return statistics.stdev(wartosci) / statistics.mean(wartosci)


def mattr(tokeny: list[str], okno: int) -> float | None:
    """Średni udział różnych tokenów w przesuwanym oknie (moving-average TTR)."""
    if len(tokeny) < okno:
        return len(set(tokeny)) / len(tokeny) if tokeny else None
    licznik = Counter(tokeny[:okno])
    suma = len(licznik)
    for i in range(okno, len(tokeny)):
        licznik[tokeny[i]] += 1
        stary = tokeny[i - okno]
        licznik[stary] -= 1
        if licznik[stary] == 0:
            del licznik[stary]
        suma += len(licznik)
    return suma / (len(tokeny) - okno + 1) / okno


def trojki(zdanie: str) -> list[str]:
    """Trzy krótkie, zrównoważone człony: „A, B i C” (stosunek długości członów ≤ 1,6)."""
    wynik = []
    for klauzula in re.split(r"[;:()]", zdanie):
        czesci = [c.strip() for c in klauzula.split(",")]
        for i in range(1, len(czesci)):
            m = _SPOJNIK_TROJKI.search(f" {czesci[i]} ")
            if not m:
                continue
            ostatni = f" {czesci[i]} "
            b, c = ostatni[:m.start()].strip(), ostatni[m.end():].strip()
            a = czesci[i - 1]
            dlugosci = [len(slowa(x)) for x in (a, b, c)]
            if min(dlugosci) == 0 or max(dlugosci) > 5:
                continue
            if any(_PODRZEDNE.match(x) or not re.search(r"[^\W\d_]", x) for x in (a, b, c)):
                continue
            if max(dlugosci) / min(dlugosci) <= 1.6:
                wynik.append(f"{a}, {b}{m.group(0).rstrip()} {c}")
    return wynik


def _kropki_dziesietne(tekst: str) -> int:
    """Liczby z kropką dziesiętną; pomija numery sekcji, tabel i wzorów oraz DOI."""
    n = 0
    for m in re.finditer(r"(?<![\d.§])\b\d+\.\d+\b(?![.\d/])", tekst):
        przed = tekst[max(0, m.start() - 20):m.start()].lower()
        if re.search(r"(?:sekcj|rozdzia|punkt|tabel|rys|ryc|wz[oó]r|wersj|doi|§)\S*\s*$", przed):
            continue
        n += 1
    return n


def zmierz(akapity: list[str]) -> dict:
    zd_akapitow = [zdania(a) for a in akapity]
    wszystkie = [z for zs in zd_akapitow for z in zs]
    dl_zdan = [len(slowa(z)) for z in wszystkie]
    tokeny = [s.lower() for z in wszystkie for s in slowa(z)]
    liczba_slow = len(tokeny) or 1

    poczatki = [(slowa(z) or [""])[0].lower() for z in wszystkie]
    serie, i = [], 0
    while i < len(poczatki):
        j = i
        while j + 1 < len(poczatki) and poczatki[j + 1] == poczatki[i] and poczatki[i]:
            j += 1
        if j - i + 1 >= 3:
            serie.append({"slowo": poczatki[i], "zdan": j - i + 1})
        i = j + 1

    tekst_maly = " ".join(wszystkie).lower()
    laczniki = {}
    for lacznik in LACZNIKI:
        n = len(re.findall(rf"(?<!\w){re.escape(lacznik)}(?!\w)", tekst_maly))
        if lacznik == "także":
            n -= len(re.findall(r"(?<!\w)a także(?!\w)", tekst_maly))
        if n:
            laczniki[lacznik] = n
    na_poczatku = sum(1 for z in wszystkie
                      if any(z.lower().startswith((lacznik + " ", lacznik + ",")) for lacznik in LACZNIKI))

    frazy = {}
    for nr, (nazwa, wzory) in FRAZY.items():
        trafienia = []
        for z in wszystkie:
            for wzor in wzory:
                for m in re.finditer(wzor, z, re.IGNORECASE):
                    trafienia.append(m.group(0))
        if trafienia:
            frazy[nr] = {"nazwa": nazwa, "liczba": len(trafienia),
                         "przyklady": [k for k, _ in Counter(t.lower() for t in trafienia).most_common(5)]}

    znalezione_trojki = [t for z in wszystkie for t in trojki(z)]
    caly = "\n".join(akapity)
    typografia = {
        "pauza (—)": caly.count("—"),
        "podwójny łącznik (--)": len(re.findall(r"\s--\s", caly)),
        "półpauza ze spacjami ( – )": caly.count(" – "),
        "cudzysłów prosty lub angielski": len(re.findall(r"[\"“]", caly)),
        "kropka dziesiętna (do sprawdzenia)": _kropki_dziesietne(caly),
        "przecinek przed i/oraz/lub/albo (do sprawdzenia)": len(re.findall(r",\s(?:i|oraz|lub|albo)\s", caly)),
        "podwójna spacja": len(re.findall(r"\S  +\S", caly)),
    }

    dl_akap_zd = [len(zs) for zs in zd_akapitow]
    dl_akap_sl = [sum(len(slowa(z)) for z in zs) for zs in zd_akapitow]
    tokeny_funkcyjne = [t for t in tokeny if t in FUNKCYJNE]
    return {
        "akapity": len(akapity),
        "zdania": len(wszystkie),
        "slowa": len(tokeny),
        "zdanie": {
            "srednia": round(statistics.mean(dl_zdan), 1) if dl_zdan else None,
            "mediana": statistics.median(dl_zdan) if dl_zdan else None,
            "odch_std": round(statistics.stdev(dl_zdan), 1) if len(dl_zdan) > 1 else None,
            "cv": _r(cv(dl_zdan)),
            "min": min(dl_zdan, default=None),
            "max": max(dl_zdan, default=None),
            "krotkie_do_8_proc": _proc(sum(d <= 8 for d in dl_zdan), len(dl_zdan)),
            "dlugie_od_35_proc": _proc(sum(d >= 35 for d in dl_zdan), len(dl_zdan)),
        },
        "akapit": {
            "srednia_zdan": round(statistics.mean(dl_akap_zd), 1) if dl_akap_zd else None,
            "cv_zdan": _r(cv(dl_akap_zd)),
            "srednia_slow": round(statistics.mean(dl_akap_sl), 1) if dl_akap_sl else None,
            "cv_slow": _r(cv(dl_akap_sl)),
        },
        "poczatki": {
            "rozne_pierwsze_slowa_proc": _proc(len(set(poczatki)), len(poczatki)),
            "serie_3_plus": serie,
        },
        "laczniki": {
            "na_1000_slow": round(1000 * sum(laczniki.values()) / liczba_slow, 1),
            "zdania_od_lacznika_proc": _proc(na_poczatku, len(wszystkie)),
            "liczby": dict(sorted(laczniki.items(), key=lambda kv: -kv[1])),
        },
        "roznorodnosc": {
            "mattr_slow_100": _r(mattr(tokeny, 100)),
            "mattr_funkcyjnych_50": _r(mattr(tokeny_funkcyjne, 50)),
        },
        "frazy": frazy,
        "trojki": {"liczba": len(znalezione_trojki), "przyklady": znalezione_trojki[:5]},
        "typografia": {k: v for k, v in typografia.items() if v},
    }


def _r(x: float | None) -> float | None:
    return round(x, 3) if x is not None else None


def _proc(a: int, b: int) -> float | None:
    return round(100 * a / b, 1) if b else None


def _liczba(x) -> str:
    return "brak" if x is None else str(x).replace(".", ",")


def raport(nazwa: str, w: dict) -> str:
    z, a, p, lacz, r = w["zdanie"], w["akapit"], w["poczatki"], w["laczniki"], w["roznorodnosc"]
    linie = [
        f"Plik: {nazwa}",
        f"Akapity: {w['akapity']}, zdania: {w['zdania']}, słowa: {w['slowa']} (bez nagłówków i tabel)",
        "",
        "Rytm (§10)",
        f"  zdanie: średnio {_liczba(z['srednia'])} słów, mediana {_liczba(z['mediana'])}, "
        f"CV {_liczba(z['cv'])}, od {_liczba(z['min'])} do {_liczba(z['max'])}",
        f"  zdania do 8 słów: {_liczba(z['krotkie_do_8_proc'])}%, od 35 słów: {_liczba(z['dlugie_od_35_proc'])}%",
        f"  akapit: średnio {_liczba(a['srednia_zdan'])} zdań (CV {_liczba(a['cv_zdan'])}), "
        f"{_liczba(a['srednia_slow'])} słów (CV {_liczba(a['cv_slow'])})",
        "",
        "Początki i łączniki (§7)",
        f"  różne pierwsze słowa zdań: {_liczba(p['rozne_pierwsze_slowa_proc'])}%",
    ]
    for s in p["serie_3_plus"]:
        linie.append(f"  seria: {s['zdan']} zdania z rzędu od „{s['slowo']}”")
    linie.append(f"  łączniki: {_liczba(lacz['na_1000_slow'])} na 1000 słów; zdania od łącznika: "
                 f"{_liczba(lacz['zdania_od_lacznika_proc'])}%")
    if lacz["liczby"]:
        linie.append("  " + ", ".join(f"{k} {v}" for k, v in list(lacz["liczby"].items())[:10]))
    linie += [
        f"  różnorodność słów funkcyjnych (MATTR, okno 50): {_liczba(r['mattr_funkcyjnych_50'])}",
        f"  różnorodność słów (MATTR, okno 100): {_liczba(r['mattr_slow_100'])}",
        "",
        "Frazy z list",
    ]
    if not w["frazy"]:
        linie.append("  brak")
    for nr, f in sorted(w["frazy"].items()):
        linie.append(f"  §{nr} {f['nazwa']}: {f['liczba']} ({'; '.join(f['przyklady'])})")
    linie += ["", f"Trójki (§6): {w['trojki']['liczba']}"]
    linie += [f"  {t}" for t in w["trojki"]["przyklady"]]
    linie += ["", "Typografia (§8, §20)"]
    linie += [f"  {k}: {v}" for k, v in w["typografia"].items()] or ["  bez uwag"]
    linie += ["", "Porównuj z tekstami tego samego gatunku i autora. Progu uniwersalnego nie ma."]
    return "\n".join(linie)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("plik")
    parser.add_argument("--json", action="store_true", help="wynik jako JSON")
    parser.add_argument("--linie", action="store_true", help="każda linia to osobny akapit")
    args = parser.parse_args()
    akapity = wczytaj_akapity(args.plik, linie=True if args.linie else None)
    if not akapity:
        print("Nie znaleziono prozy w pliku.", file=sys.stderr)
        return 1
    wynik = zmierz(akapity)
    if args.json:
        print(json.dumps(wynik, ensure_ascii=False, indent=2))
    else:
        print(raport(Path(args.plik).name, wynik))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
