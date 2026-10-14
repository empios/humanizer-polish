# Przewodnik dla agentów

Ten plik mówi, jak zmieniać humanizer-polish, nie psując pakietu ani promptu.

## Co jest w repozytorium

humanizer-polish to umiejętność dla agentów zapisana w Markdownie. `SKILL.md` jest promptem, który czytają agenci; repozytorium nie ma kroku budowania. Skill ma działać w każdym agencie obsługującym umiejętności, więc nie pisz instrukcji ograniczonych do jednego narzędzia.

## Najważniejsze pliki

- `SKILL.md`: jedyny plik umiejętności i źródło prawdy. Metadane YAML, wyjaśnienie, skąd biorą się wzorce, kolejność pracy i 30 numerowanych wzorców w grupach A–G.
- `README.md`: instalacja, użycie, tabele wzorców, źródła, krótka część po angielsku.
- `CHANGELOG.md`: historia zmian, najnowsza na górze. Stare wpisy zachowują numerację wzorców z danej wersji.
- `references/zrodla.md`: streszczenia źródeł własnymi słowami, z pełnymi danymi bibliograficznymi.
- `references/jawnosc-ai.md`: kategorie GAIDeT i wzór deklaracji użycia AI.
- `scripts/tekst_pl.py`: wczytywanie .txt, .md i .docx, podział na akapity, zdania i słowa.
- `scripts/metryki_pl.py`: miary rytmu i frazy z list; numery w `FRAZY` odpowiadają numerom wzorców.
- `scripts/porownaj_wersje.py`: różnice elementów chronionych między wersjami.
- `scripts/validate-package.py`: sprawdza pakiet.
- `tests/`: testy skryptów (`unittest`, bez zależności).
- `.claude-plugin/plugin.json` i `.claude-plugin/marketplace.json`: wtyczka i marketplace Claude.

## Zasady zmian

- **Wzorce:** numeracja od 1 bez przerw, od najsilniejszych. Nowy sygnał dostaje osobny wzorzec tylko wtedy, gdy żaden istniejący go nie obejmuje. Po dodaniu, usunięciu albo przenumerowaniu wzorca popraw tabele i tytuł sekcji w README, każde odwołanie `§N` w `SKILL.md` i numery w `FRAZY` w `metryki_pl.py`.
- **Grupa G** ma pierwszeństwo przed A–F i przed próbką autora. Nie osłabiaj jej, żeby tekst brzmiał lepiej.
- **Wersja:** ta sama w `SKILL.md` (`metadata.version`), w pierwszym nagłówku `CHANGELOG.md`, w `plugin.json` i we wpisie wtyczki w `marketplace.json`.
- **Opis:** manifesty używają pierwszego zdania opisu z `SKILL.md`.
- **Długość:** agent czyta każde słowo `SKILL.md` przy każdym użyciu. Walidator ogranicza go do 5 500 słów.
- **Skill przestrzega własnych reguł:** walidator odrzuca pauzę (—) i podwójny łącznik poza §8 oraz angielski cudzysłów otwierający poza §20.
- **Źródła:** nie kopiuj tekstu źródeł; streszczaj własnymi słowami i podawaj dane bibliograficzne. Nie podawaj niepublikowanych wyników.
- **Historia:** dopisz krótką notkę do `CHANGELOG.md` przy każdej zmianie zachowania.
- **Sprawdzenie przed publikacją:**

```bash
python3 scripts/validate-package.py
python3 -m unittest discover -s tests
claude plugin validate .
```

## Styl

Prosty język w komentarzach, promptach, dokumentacji i komunikatach: najpierw główna myśl, zwykłe słowa, strona czynna, krótkie zdania, jeden termin na jedną rzecz. Zachowuj dokładnie identyfikatory, polecenia, ścieżki, cytaty, frazy z list wzorców i przykłady, od których zależy zachowanie skilla. Teksty dla użytkownika piszemy po polsku; komunikaty walidatora zostają po angielsku, jak w oryginale.
