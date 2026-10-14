# Historia zmian

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
