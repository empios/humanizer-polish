# Historia zmian

## 1.3.0

- `metryki_pl.py` ma nowe miary z badań nad tekstem modeli: odsetek zdań o długości 10-30 słów i różnicę długości kolejnych zdań (§10), powtarzalność tekstu mierzoną kompresją zlib, częstość fraz i trójek na 1000 słów oraz niewidoczne znaki i cyrylicę w łacińskich słowach (§20). Szuka też „coś więcej niż” (§1).
- §1: nowy wariant kontrastu „to coś więcej niż X, to Y”. §12: synonim z tej samej rodziny zostawia wzorzec. §20: niewidoczne znaki i cyrylicę trzeba usunąć.
- „Kiedy nie działać”: poprawna pisownia nie świadczy o AI, więc skill nie dodaje błędów.

## 1.2.1

- `metryki_pl.py`: reguła przecinka po okoliczniku na początku zdania obejmuje też „przez”, „poprzez”, „dzięki”, „podczas”, „na podstawie” i dłuższe okoliczniki, a pomija przecinek przed spójnikiem („bo”, „więc”, „i”) i imiesłowem na „-ąc”. Na ok. 19 tys. słów tekstów pisanych przez ludzi nie dała fałszywego alarmu.
- `references/zrodla.md`: szczegóły z Mazura (2024) i z „The Economist” (2026) sprawdzono w pełnych tekstach; opis Mazura ma teraz DOI i liczby.

## 1.2.0

- Nowe sygnały dopisane do istniejących wzorców: „tam, gdzie X spotyka się z Y” i „tworzyć przestrzeń do” (§3), wyliczenie „od X, przez Y, aż po Z” (§6), zdania z „który” doklejane do co drugiego rzeczownika (§10), przecinek po okoliczniku na początku zdania, cudzysłów po „tzw.” i podwójne wyróżnienie tytułu (§20), realia z pocztówki w fikcji (§25).
- §8: pauza nie jest już pewnym śladem modelu (pomiar „The Economist”, 2026). Zakaz kresek typograficznych zostaje jako reguła redakcyjna.
- §12: lista słów się starzeje. §11 i §16: styl rzeczownikowy i imiesłowowe doczepki modeli potwierdza badanie Reinharta i in. (2025).
- „Głos”: w tekście literackim skill nie domyka wieloznaczności ani urwanych zdań. Krok 4: równego rytmu nie zastępuje serią krótkich puent.
- „Kiedy nie działać”: wprawni czytelnicy rozpoznają tekst modelu także po parafrazie (Russell i in., 2025). Grupa G powołuje się na audyt „humanizerów”, które gubią liczby i cytaty (Wang i in., 2026).
- `metryki_pl.py` szuka nowych fraz z §3 i §6, liczy „który” na 1000 słów, przecinek po okoliczniku na początku zdania i cudzysłów po „tzw.”.
- `references/zrodla.md`: nowe źródła, w tym pięć wpisów hum/dev, polskie badanie Kutyły i in. (2026) i poradnik prostego języka UMCS.

## 1.1.1

- `metryki_pl.py` nie dzieli zdania na przecinku dziesiętnym, więc „od 0,215 do 0,285” nie jest już liczone jako trójka (§6). Fałszywy alarm wyszedł na manuskrypcie naukowym.

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
