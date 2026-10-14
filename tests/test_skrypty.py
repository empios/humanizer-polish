"""Testy skryptów humanizer-polish. Uruchom: python3 -m unittest discover -s tests"""

from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import metryki_pl  # noqa: E402
import porownaj_wersje  # noqa: E402
from tekst_pl import slowa, wczytaj_akapity, zdania  # noqa: E402


class PodzialNaZdania(unittest.TestCase):
    def test_skroty_i_inicjaly_nie_koncza_zdania(self):
        tekst = "Zob. art. 5 ust. 2 k.c. Sąd uznał, że J. Kowalski ma rację. Dalej m.in. Dz. U. Nr 5. Tak."
        self.assertEqual(
            zdania(tekst),
            ["Zob. art. 5 ust. 2 k.c.", "Sąd uznał, że J. Kowalski ma rację.", "Dalej m.in. Dz. U. Nr 5.", "Tak."],
        )

    def test_rok_ze_skrotem_konczy_zdanie(self):
        self.assertEqual(zdania("Ustawa weszła w życie w 2020 r. Sąd ją stosuje."),
                         ["Ustawa weszła w życie w 2020 r.", "Sąd ją stosuje."])

    def test_wyraz_z_lacznikiem_to_jedno_slowo(self):
        self.assertEqual(slowa("spór polsko-niemiecki o 0,53"), ["spór", "polsko-niemiecki", "o", "0,53"])


class Wczytywanie(unittest.TestCase):
    def test_markdown_bez_naglowkow_kodu_i_bibliografii(self):
        with tempfile.TemporaryDirectory() as katalog:
            plik = Path(katalog) / "t.md"
            plik.write_text(
                "# Wstęp\n\nPierwszy akapit ma jedno zdanie.\n\n```\nkod()\n```\n\n"
                "Drugi akapit też.\n\n## Bibliografia\n\n[1] Kowalski J. Tytuł. 2020.\n",
                encoding="utf-8",
            )
            self.assertEqual(wczytaj_akapity(plik), ["Pierwszy akapit ma jedno zdanie.", "Drugi akapit też."])

    def test_docx(self):
        w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        xml = (
            f'<w:document xmlns:w="{w}"><w:body>'
            '<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Tytuł</w:t></w:r></w:p>'
            '<w:p><w:r><w:t>Zdanie pierwsze. </w:t></w:r><w:r><w:t>Zdanie drugie.</w:t></w:r></w:p>'
            "</w:body></w:document>"
        )
        with tempfile.TemporaryDirectory() as katalog:
            plik = Path(katalog) / "t.docx"
            with zipfile.ZipFile(plik, "w") as archiwum:
                archiwum.writestr("word/document.xml", xml)
            self.assertEqual(wczytaj_akapity(plik), ["Zdanie pierwsze. Zdanie drugie."])


class Metryki(unittest.TestCase):
    def test_frazy_trojki_i_typografia(self):
        akapity = [
            "W dobie zmian warto podkreślić, że metoda odgrywa kluczową rolę. "
            "Nie chodzi tu wyłącznie o szybkość, lecz o wiarygodność. "
            "Narzędzie zwiększa przejrzystość, poprawia czytelność oraz wzmacnia zaufanie. "
            "W oparciu o zbiór złoty uzyskano AUC 0.61 — to zmienia wszystko."
        ]
        wynik = metryki_pl.zmierz(akapity)
        for numer in (1, 2, 4, 13, 14, 18):
            self.assertIn(numer, wynik["frazy"], numer)
        self.assertEqual(wynik["trojki"]["liczba"], 1)
        self.assertEqual(wynik["typografia"]["pauza (—)"], 1)
        self.assertEqual(wynik["typografia"]["kropka dziesiętna (do sprawdzenia)"], 1)

    def test_zwrot_w_cudzyslowie_i_slowa_kluczowe_to_nie_wzorzec(self):
        wynik = metryki_pl.zmierz(["Reguła zamienia „warto wskazać” na nic. Słowa kluczowe: prawo, styl."])
        self.assertEqual(wynik["frazy"], {})

    def test_numer_sekcji_to_nie_kropka_dziesietna(self):
        wynik = metryki_pl.zmierz(["Opis jest w sekcji 3.2 i w tabeli 1.4 tego artykułu."])
        self.assertNotIn("kropka dziesiętna (do sprawdzenia)", wynik["typografia"])

    def test_zdanie_podrzedne_to_nie_trojka(self):
        self.assertEqual(metryki_pl.trojki("Nie ma reguł, które poprawiają styl i nie zmieniają treści."), [])

    def test_seria_tych_samych_poczatkow(self):
        wynik = metryki_pl.zmierz(["Model czyta tekst. Model wskazuje frazy. Model proponuje zmiany."])
        self.assertEqual(wynik["poczatki"]["serie_3_plus"], [{"slowo": "model", "zdan": 3}])


class Porownanie(unittest.TestCase):
    def test_zmiana_zapisu_liczby_to_nie_roznica(self):
        przed = "Czułość wyniosła 0.91 na 1804 dokumentach, a 8 z nich odrzucono."
        po = "Na 1 804 dokumentach czułość wyniosła 0,91; osiem z nich odrzucono."
        self.assertNotIn("liczby", porownaj_wersje.porownaj(przed, po))

    def test_zmiana_wartosci_przepisu_modalnosci_i_stron(self):
        przed = "Najemca musi zapłacić czynsz 1 200 zł do 10 dnia miesiąca (art. 659 § 1 k.c.)."
        po = "Wynajmujący może zapłacić czynsz 1 300 zł do 10 dnia miesiąca (art. 659 k.c.)."
        roznice = porownaj_wersje.porownaj(przed, po)
        self.assertEqual(roznice["liczby"], {"zniknelo": ["1200"], "pojawilo_sie": ["1300"]})
        self.assertEqual(roznice["przepisy"]["zniknelo"], ["§ 1"])
        self.assertEqual(roznice["modalność"]["zmiany"], {"musieć": [1, 0], "móc": [0, 1]})
        self.assertEqual(roznice["strony"]["zmiany"], {"najemca": [1, 0], "wynajmujący": [0, 1]})

    def test_przeczenie_i_cytat(self):
        roznice = porownaj_wersje.porownaj("Strona nie może „zrzec się prawa”.", "Strona może „zrzec się praw”.")
        self.assertEqual(roznice["przeczenia"]["zmiany"], {"nie": [1, 0]})
        self.assertEqual(roznice["cytaty"], {"zniknelo": ["zrzec się prawa"], "pojawilo_sie": ["zrzec się praw"]})

    def test_hash_commita_to_nie_liczba(self):
        self.assertNotIn("liczby", porownaj_wersje.porownaj("commit 65a8ec7", "commit 3e14aac"))


if __name__ == "__main__":
    unittest.main()
