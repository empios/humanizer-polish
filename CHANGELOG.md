# Historia zmian

## 1.1.0

- §8: w wersji końcowej nie ma pauzy (—) ani półpauzy (–). Jedyną kreską jest łącznik ASCII (-), także w przedziałach („2019-2024”). Myślniki z próbki autora skill zapisuje jako ` - `. Walidator odrzuca półpauzę w `SKILL.md` poza §8, a `metryki_pl.py` liczy każdą półpauzę i łącznik ze spacjami.
- Zakaz wymyślania zdań: każde zdanie szkicu pochodzi ze zdania źródła, bez nowych przykładów, opinii, metafor, pytań, przejść i związków przyczynowych, także w fikcji. Krok 5 sprawdza, czy każde zdanie ma odpowiednik w źródle. Przykłady w §1, §2, §3, §6, §26 i §30 poprawiono, żeby niczego nie dopisywały; §30 nie każe już dopisywać definicji.
- Nowe sygnały z bloga hum/dev, dopisane do istniejących wzorców: zdanie powtarzające poprzednie, pusty komentarz po cytacie i pytanie retoryczne bez odpowiedzi (§2), ozdobne metafory (§3), żargon w tekście dla laików (§12), przymiotniki emocjonalne i omówienia (§14), błędne DOI, bibliografia spoza tematu i wykresy z danymi „hipotetycznymi” (§17), przekręcone związki frazeologiczne (§18), „Zgodnie z poleceniem”, pola szablonu i resztki Markdownu (§21), akapit „z polskiej perspektywy”, pusta definicja i pojęcie bez opisu (§25). W „Kiedy nie działać” jest uwaga o detektorach opartych na perpleksji.
- `metryki_pl.py` szuka nowych fraz z §3, §21 i §25. `porownaj_wersje.py` nie zgłasza różnicy, gdy półpauza w cytowaniu („[3–5]”) zmienia się w łącznik.

## 1.0.1

- `metryki_pl.py` nie liczy zwrotów w cudzysłowie, bo tekst je omawia, a nie stosuje (zgodnie z „Kiedy nie działać”), ani etykiety „Słowa kluczowe” jako wzorca §12. Oba fałszywe alarmy wyszły na prawdziwych manuskryptach naukowych.

## 1.0.0

Pierwsza wersja. 30 wzorców w siedmiu grupach (A–G).

- Grupy A–F przenoszą na polszczyznę strukturę blader/humanizer 3.1.0: inscenizację, rytm z reguły, napuszenie, formatowanie, pozostałości czatu i tłumaczenie adresatowi tego, co wie. Listy fraz pochodzą z reguł i detektora humanize-pl.
- Nowe wzorce dla polszczyzny: kalki z angielskiego (§18), angielska typografia, w tym kropka dziesiętna i przecinek przed „i” (§20), rzeczowniki zamiast czasowników (§11), jednolity rytm i szyk bez inwersji (§10, na podstawie badania stylometrycznego z UJ), poszarpana parafraza (§24) i ogólnik zamiast faktu (§25).
- Reguła myślnika (§8) uwzględnia polską typografię: półpauza ze spacjami jest dopuszczalna, wzorcem jest angielska pauza i myślnik w co drugim zdaniu.
- Grupa G (§27–§30) chroni liczby, przepisy, modalność, przeczenia, role stron i terminy dziedzinowe w tekstach prawnych i naukowych. Ma pierwszeństwo przed A–F i przed próbką autora.
- Skrypty bez zależności: `metryki_pl.py` (rytm, łączniki, słowa funkcyjne, frazy, trójki, typografia) i `porownaj_wersje.py` (elementy chronione przed i po redakcji; liczby porównywane po ujednoliceniu zapisu, także słownego).
- `references/zrodla.md` streszcza źródła, `references/jawnosc-ai.md` daje wzór deklaracji użycia AI według GAIDeT.
