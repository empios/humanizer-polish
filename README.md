# humanizer-polish

Umiejętność (skill) dla Claude i innych agentów, która redaguje polski tekst brzmiący jak wygenerowany przez AI, żeby brzmiał jak autor, i nie zmienia jego treści. Powstała na bazie [blader/humanizer](https://github.com/blader/humanizer), polskich reguł z [humanize-pl](https://github.com/empios/humanize-pl), badania stylometrycznego z UJ i wpisów bloga [hum/dev](https://blog.humanistyka.dev). Pilnuje tego, czego zwykłe narzędzia do „uczłowieczania” nie pilnują: liczb, przepisów, modalności, przeczeń, ról stron i terminów.

**Przed:**
> W dobie dynamicznego rozwoju sztucznej inteligencji warto podkreślić, że kompleksowa analiza orzecznictwa odgrywa kluczową rolę. Nie chodzi tu wyłącznie o szybkość, lecz przede wszystkim o rzetelność — to zmienia wszystko. W oparciu o zbiór złoty system osiągnął czułość 0.91, swoistość 0.88, i precyzję 0.85. Podsumowując, przedmiotowe rozwiązanie ma istotne znaczenie dla praktyki.

**Po:**
> System ma przede wszystkim rzetelnie analizować orzecznictwo. Na zbiorze wzorcowym osiągnął czułość 0,91, swoistość 0,88 i precyzję 0,85.

Liczby zostały, zmienił się tylko ich zapis. Zniknęły: otwarcie „w dobie”, zapowiedź „warto podkreślić”, kontrast „nie chodzi o X, lecz Y”, puenta, kalki („w oparciu o”, „zbiór złoty”), przecinek przed „i”, podsumowanie i nadawanie wagi.

Celem jest tekst dla czytelnika. Omijanie detektorów AI celem nie jest: detektory zawodzą w obie strony, a ich wynik nie rozstrzyga o autorstwie. Jeśli AI pomagała pisać tekst naukowy, skill proponuje deklarację według taksonomii GAIDeT.

## Pięć najsilniejszych wzorców

1. **Nie X, lecz Y:** „Nie chodzi tu o szybkość, lecz o wiarygodność.”
2. **Puenty:** „To zmienia wszystko.” „Wniosek jest prosty:”
3. **Pozorna głębia:** „U podstaw problemu leży fundamentalna kwestia…”
4. **Zapowiedź zamiast treści:** „Warto podkreślić, że…” „Należy wskazać, że…”
5. **Polemika z nikim:** „Można by sądzić, że…, jednak…”

Wszystkich [wzorców jest 30](#30-wzorców).

## Instalacja

Po instalacji skill odpowiada na `/humanizer-polish`.

### Claude Code

```text
/plugin marketplace add empios/humanizer-polish
/plugin install humanizer-polish@humanizer-polish
```

Wtyczka odpowiada na `/humanizer-polish:humanizer-polish`. Bez systemu wtyczek:

```bash
npx skills add empios/humanizer-polish --global --agent claude-code
```

### Claude.ai i Claude Desktop

Pobierz repozytorium jako ZIP (**Code → Download ZIP**) i wgraj je jako skill w ustawieniach.

### Inni agenci

```bash
npx skills add empios/humanizer-polish --global --agent '*'
```

Bez `--global` skill trafi tylko do bieżącego projektu. Agentowi, którego Skills CLI nie zna, skopiuj `SKILL.md`, `scripts/` i `references/` do jego folderu umiejętności.

## Użycie

```text
/humanizer-polish

[wklej tekst]
```

Albo zwykłym poleceniem: „Zredaguj ten akapit skillem humanizer-polish”, „Przejdź humanizer-polish po pliku wstep.md”. Jeśli dasz próbkę swojego tekstu, skill dopasuje się do niej (długość zdań, łączniki, interpunkcja). Zasady grupy G mają pierwszeństwo także przed próbką.

### Skrypty

Oba działają na samej bibliotece standardowej Pythona 3.10+ i czytają `.txt`, `.md` oraz `.docx`. Pomijają nagłówki, tabele, kod i bibliografię.

```bash
python3 scripts/metryki_pl.py tekst.docx
```

Podaje długość i zmienność (CV) zdań i akapitów, łączniki na 1000 słów, serie zdań od tego samego słowa, różnorodność słów funkcyjnych, frazy z list wzorców, trójki i uwagi typograficzne. Opcja `--json` daje wynik do dalszej obróbki. Progu uniwersalnego nie ma: porównuj z tekstami tego samego gatunku i autora.

```bash
python3 scripts/porownaj_wersje.py przed.docx po.docx
```

Wypisuje liczby, przepisy, sygnatury, cytowania, cytaty, symbole zastępcze, słowa modalne, przeczenia i nazwy stron, które zniknęły albo się pojawiły. Liczby porównuje po ujednoliceniu zapisu („0,53” = „0.53”, „1 804” = „1804”, „8” = „osiem”). Kod wyjścia 1 oznacza różnice do sprawdzenia.

Opcja `--linie` traktuje każdą linię pliku tekstowego jako osobny akapit.

## Jak to działa

`SKILL.md` wyjaśnia, skąd biorą się wzorce (model wybiera wariant pasujący do najszerszego odbiorcy), opisuje kolejność pracy (pomiar, oznaczenie wzorców, szkic, zmiana struktury, sprawdzenie, wersja końcowa) i 30 wzorców w siedmiu grupach. Grupy A–F to wzorce stylu, od najsilniejszych. Grupa G to zasady bezpieczeństwa treści dla tekstów prawnych i naukowych.

Dwie lekcje z praktyki, które skill zapisuje wprost: podmiana synonimów bez zmiany struktury prawie nie zmienia rytmu tekstu, a każdą redakcję trzeba sprawdzić porównaniem liczb i przepisów, bo parafraza gubi je po cichu.

## 30 wzorców

### A. Inscenizacja zamiast stwierdzenia

| # | Wzorzec | Przykład | Co zrobić |
|---|---|---|---|
| 1 | **Nie X, lecz Y** | „Nie chodzi o X, lecz o Y”, „Nie oznacza to, że X. Oznacza to, że Y.” | Podać myśl wprost; kontrast normatywny zostaje |
| 2 | **Puenty i dramatyczne równoważniki** | „To zmienia wszystko.”, „Wniosek jest prosty:”, „Bez kompromisów. Bez wyjątków.” | Wyciąć zamknięcie, które powtarza; połączyć równoważniki w zdanie |
| 3 | **Pozorna głębia** | „U podstaw leży…”, „Prawdziwe pytanie brzmi…”, „X to waluta Y” | Zastąpić konkretnym twierdzeniem |
| 4 | **Zapowiedź zamiast treści** | „Warto podkreślić, że”, „Należy wskazać, że”, „W tym kontekście” | Zacząć od tego, co po „że”; „należy” nakazujące zostaje |
| 5 | **Polemika z nikim** | „Można by sądzić, że…”, „Kuszące byłoby…” | Usunąć obronę przed zarzutem, którego nikt nie postawił |

### B. Rytm z reguły

| # | Wzorzec | Przykład | Co zrobić |
|---|---|---|---|
| 6 | **Wymuszone trójki** | „przejrzystość, rzetelność oraz odpowiedzialność” | Zostawić trzy człony tylko wtedy, gdy treść ma trzy części |
| 7 | **Powtarzane początki i łączniki** | „Ponadto… Co więcej… Dodatkowo…”, „więc” w co drugim zdaniu | Usunąć zbędny łącznik, zmienić powtarzany, połączyć zdania |
| 8 | **Myślnik jako uniwersalny łącznik** | „procedura—wprowadzona bez konsultacji—obejmuje” | Przecinek, dwukropek, nawias albo kropka; półpauza w przedziałach zostaje |
| 9 | **Piętrowe asekuracje** | „można by potencjalnie przypuszczać, że mogłoby w pewnym stopniu” | Jedno zastrzeżenie, jeśli uzasadnia je źródło |
| 10 | **Jednolity rytm i szyk** | zdania podobnej długości, każde od podmiotu | Zmieniać długość zdań i akapitów, używać inwersji |
| 11 | **Rzeczowniki zamiast czasowników** | „dokonano analizy w celu przeprowadzenia weryfikacji” | Czasownik zamiast rzeczownika odczasownikowego |

### C. Napuszenie i pożyczony autorytet

| # | Wzorzec | Przykład | Co zrobić |
|---|---|---|---|
| 12 | **Słowa nadużywane przez modele** | kluczowy, kompleksowy, holistyczny, w dobie, krajobraz | Konkretne słowo albo nic |
| 13 | **Nadawanie wagi** | „ma istotne znaczenie”, „odgrywa kluczową rolę”, „kamień milowy” | Zostawić fakt, usunąć wagę |
| 14 | **Zbędne wartościowanie i banalne otwarcia** | „cenne, unikatowe zbiory”, „W dobie dynamicznego rozwoju…” | Usunąć ocenę albo podać fakt, który ją uzasadnia |
| 15 | **Mgliste powiązanie** | „związany z”, „w kontekście”, „w odniesieniu do” | Nazwać relację, jeśli podaje ją źródło |
| 16 | **Imiesłowowe doczepki** | „…, podkreślając wagę…”, „…, co świadczy o…” | Zostawić fakt, doczepkę tylko ze źródłem |
| 17 | **Pożyczony autorytet i puste przypisy** | „Badania pokazują…” bez przypisu, `utm_source=chatgpt.com` | Wskazać źródło albo usunąć autorytet; nie dopisywać przypisów |
| 18 | **Kalki z angielskiego** | „w oparciu o”, „adresować problem”, „zbiór złoty”, „dedykowany” | Polski odpowiednik; przyjęty termin dziedzinowy zostaje |

### D. Formatowanie i typografia

| # | Wzorzec | Przykład | Co zrobić |
|---|---|---|---|
| 19 | **Pogrubienia, listy i nagłówki z reguły** | „**Szybkość:** …”, „Wyniki I Dyskusja” | Zdania zamiast list z etykietami; polska wielkość liter |
| 20 | **Angielska typografia** | "cudzysłów", 0.53, „A, B, i C” | „…”, przecinek dziesiętny, bez przecinka przed „i” |

### E. Pozostałości

| # | Wzorzec | Przykład | Co zrobić |
|---|---|---|---|
| 21 | **Formułki czatu i zastrzeżenia o wiedzy** | „Oto poprawiona wersja”, „Według mojej wiedzy…” | Usunąć |
| 22 | **Tekst o sobie samym** | „Jak wspomniano powyżej”, „W niniejszym artykule…” | Jedno zdanie o układzie pracy zostaje; reszta do usunięcia |
| 23 | **Podsumowanie po każdej sekcji** | „Podsumowując,”, „Reasumując,” | Jedno podsumowanie tam, gdzie wymaga go gatunek |

### F. Rozjechana treść

| # | Wzorzec | Przykład | Co zrobić |
|---|---|---|---|
| 24 | **Poszarpana parafraza** | akapit gubi zapowiedzianą myśl, zdania do siebie nie pasują | Jedna myśl na akapit; niejasny termin zgłosić |
| 25 | **Ogólnik zamiast faktu** | „liczne badania”, „znaczna poprawa” | Liczba, data, nazwa ze źródła; niczego nie wymyślać |
| 26 | **Tłumaczenie adresatowi tego, co wie** | „Jak Pan wie, umowa została zawarta…” | Zacząć od odpowiedzi albo decyzji |

### G. Czego redakcja nie może zepsuć

| # | Wzorzec | Przykład | Co zrobić |
|---|---|---|---|
| 27 | **Elementy chronione** | liczby, kwoty, daty, art., §, sygnatury, cytaty, [SYMBOLE] | Bez zmian; sprawdzić `porownaj_wersje.py` |
| 28 | **Modalność i przeczenie** | „musi” ≠ „może”, „należy złożyć” ≠ „należy wskazać, że” | Siła normy i każde „nie” zostają |
| 29 | **Role stron** | najemca i wynajmujący, powód i pozwany | Sprawdzić ręcznie po każdej zmianie szyku |
| 30 | **Terminy, których nie zastąpi synonim** | „modalność” ≠ „wydźwięk”, „co do zasady” ≠ „zasadniczo” | Powtórzyć termin, objaśnić raz |

## Źródła

Pełne opisy: [`references/zrodla.md`](references/zrodla.md).

- Siqi Chen, [blader/humanizer](https://github.com/blader/humanizer) (MIT), oparty na [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
- [humanize-pl](https://github.com/empios/humanize-pl): polskie listy fraz i kontrole elementów chronionych.
- hum/dev: [rozpoznawanie tekstu akademickiego AI bez detektora](https://blog.humanistyka.dev/2026/10/jak-bez-pangrama-rozpoznac-tekst-akademicki-wygenerowany-przez-ai), [stylometria tekstów maszynowych](https://blog.humanistyka.dev/2026/03/stylometryczne-cechy-tekstow-generowanych-maszynowo), [taksonomia GAIDeT](https://blog.humanistyka.dev/2025/09/taksonomia-gaidet-jak-raportowac-uzycie-sztucznej-inteligencji-w-pisaniu).
- Przystalski K, Argasiński JK, Grabska-Gradzińska I, Ochab JK. Stylometry recognizes human and LLM-generated texts in short samples. *Expert Systems with Applications*. 2026;296:129001. doi:[10.1016/j.eswa.2025.129001](https://doi.org/10.1016/j.eswa.2025.129001)
- Suchikova Y. i in. GAIDeT (Generative AI Delegation Taxonomy). *Accountability in Research*. 2025. doi:[10.1080/08989621.2025.2544331](https://doi.org/10.1080/08989621.2025.2544331)

## English

humanizer-polish is an agent skill that edits Polish prose with AI-writing tells so it reads like its author, without changing what it says. It adapts [blader/humanizer](https://github.com/blader/humanizer) to Polish: the watch lists are Polish (calques from English, Polish typography, nominal style, overused connectors), and a separate group G protects numbers, statutory references, deontic modality, negation, party roles, and domain terms in legal and academic text. Two stdlib-only scripts measure sentence and paragraph rhythm (`scripts/metryki_pl.py`) and diff protected elements between versions (`scripts/porownaj_wersje.py`). The goal is better text for readers; evading AI detectors is not a goal. Install in Claude Code with `/plugin marketplace add empios/humanizer-polish`, then `/plugin install humanizer-polish@humanizer-polish`.

## Historia wersji

[`CHANGELOG.md`](CHANGELOG.md).

## Licencja

MIT. Zawiera adaptację blader/humanizer, © 2025 Siqi Chen; zob. [`LICENSE`](LICENSE).
