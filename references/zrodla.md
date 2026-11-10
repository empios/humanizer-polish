# Źródła humanizer-polish

Streszczenia są napisane własnymi słowami i podają tylko to, co skill z danego źródła bierze. Szczegóły warto sprawdzić w oryginale.

## blader/humanizer

Siqi Chen (blader), *Humanizer*, wersja 3.1.0, licencja MIT. https://github.com/blader/humanizer

Umiejętność dla agentów, która usuwa z angielskiej prozy ślady pisania przez model. Z niej pochodzą: wyjaśnienie, skąd biorą się wzorce (model wybiera wariant pasujący do najszerszego odbiorcy), układ grup od najsilniejszych wzorców, kolejność pracy (szkic, sprawdzenie, wersja końcowa), zakaz dopisywania faktów, tryby zwracania wyniku i sekcja o tym, kiedy nie działać. Wzorce z grup A-F, które mają odpowiednik w tym repozytorium, są jego adaptacjami; przykłady napisano od nowa po polsku. Skrypt `validate-package.py` jest przeróbką walidatora z tego repozytorium.

## Wikipedia: Signs of AI writing

WikiProject AI Cleanup, *Wikipedia:Signs of AI writing*. https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

Poradnik redaktorów Wikipedii, na którym oparto blader/humanizer. Opisuje słownictwo, konstrukcje i formatowanie typowe dla tekstów modeli oraz ostrzega, że pojedynczy sygnał niczego nie dowodzi.

## humanize-pl

empios, *humanize-pl*. https://github.com/empios/humanize-pl

Narzędzie do redakcji polskich tekstów prawniczych z detektorem wzorców AI i kontrolami bezpieczeństwa treści. Z niego pochodzą polskie listy fraz: ramy dyskursu („warto wskazać, że”, „należy podkreślić”), łączniki („ponadto”, „co więcej”, „dodatkowo”), ramy nadające wagę („ma istotne znaczenie”, „odgrywa kluczową rolę”), pusty nacisk („to właśnie”), odesłania („powyższy”, „niniejszy”, „przedmiotowy”), schematy zdań („z jednej strony”, „nie oznacza to, że”, „Podsumowując”), sufiksy nominalizacji i reguła trójki (trzy zrównoważone człony, stosunek długości do 1,6). Z kontroli redakcji pochodzi grupa G: liczby, przepisy, daty, kwoty, terminy zdefiniowane, cytaty, symbole zastępcze, wyrażenia deontyczne, przeczenia i role stron. Pomiary w tym projekcie pokazały, że zamiana ról stron jest dla kontroli automatycznych najtrudniejsza, stąd zalecenie ręcznego sprawdzania w §29.

## hum/dev: rozpoznawanie tekstu akademickiego AI bez detektora

Redakcja hum/dev, *Jak bez Pangrama rozpoznać tekst akademicki wygenerowany przez AI?*, Humanistyka.dev, 1 października 2026. https://blog.humanistyka.dev/2026/10/jak-bez-pangrama-rozpoznac-tekst-akademicki-wygenerowany-przez-ai

Wpis zbiera sygnały, po których prowadzący zajęcia może podejrzewać pracę napisaną z pomocą modelu, bez polegania na detektorze:

- kontekst powstania pracy (brak udziału w zajęciach, nieproporcjonalnie obszerny tekst);
- zamknięta, wtórna sieć przypisów: teksty podstawowe i to, co one cytują;
- nieudolnie przetłumaczona terminologia, kalki z angielskiego i nienaturalny szyk (§18);
- parafraza „poszarpana”: akapit gubi zapowiedzianą myśl, zdania do siebie nie pasują, pojęcia są źle zrozumiane; autor łączy to z doklejaniem kolejnych odpowiedzi modelu i z parafrazowaniem w celu ominięcia detektora (§24);
- przypisy, które niczego nie wnoszą, oraz adresy ze znacznikiem `utm_source` wskazującym na czat (§17);
- styl, który Orwell nazwał pretensjonalną dykcją: ogólniki, oczywistości, uczony język bez konkretu i zbędne wartościowanie, porównany do treści pisanych pod pozycjonowanie (§14).

O detektorach wpis mówi, że wykrywają cechy trudne do nazwania dla człowieka, ale słabiej radzą sobie z tekstem mieszanym, reagują na drobne zmiany i nie powinny rozstrzygać o autorstwie. Zaleca traktowanie ich jako narzędzia przesiewowego i, tam gdzie AI jest dozwolona, deklarację według GAIDeT.

## hum/dev: stylometria tekstów generowanych maszynowo

Redakcja hum/dev, *Stylometryczne cechy tekstów generowanych maszynowo*, Humanistyka.dev, 21 marca 2026. https://blog.humanistyka.dev/2026/03/stylometryczne-cechy-tekstow-generowanych-maszynowo

Omówienie badania Przystalskiego i in. (poniżej). Wpis wylicza cechy, które drzewa decyzyjne uznały za odróżniające: TTR na lematach, częstość stopnia wyższego przymiotników, zróżnicowanie słów funkcyjnych (mniejsze u modeli), inwersję, większą standaryzację gramatyczną tekstów modeli, mniejsze nasycenie datami, liczebnikami i nazwami własnymi, nadużywanie niektórych słów przez GPT-4, wzorce interpunkcji zależne od modelu i artefakty w rodzaju nadmiarowych spacji. Zaznacza ograniczenia: tylko angielski, tylko wstępy haseł Wikipedii, wiele cech zależy od modelu, więc nie da się ich uogólnić. Skill bierze stąd §7, §10, §12, §20 i §25, zawsze jako wskazówki, nie progi.

## hum/dev: wpis na bloga wygenerowany przez AI

Redakcja hum/dev, *Próbowałem wygenerować w AI wpis na tego bloga i skończyło się to katastrofą*, Humanistyka.dev, 22 lutego 2026. https://blog.humanistyka.dev/2026/02/probowalem-wygenerowac-w-ai-wpis-na-tego-bloga-i-skonczylo-sie-to-katastrofa

Autor zlecił dwóm darmowym czatom napisanie wpisu na zadany temat i ocenił wynik jako redaktor. Skill bierze stąd: zbędne metafory, które tekst zaraz powtarza dosłownie (§3); przymiotniki nazywające emocje (§14); pytanie w zajawce, na które tekst nie odpowiada, i pusty komentarz po cytacie (§2); przekręcony związek frazeologiczny (§18); akapit „z polskiej perspektywy”, który pasuje do każdego kraju, bo model nie zna perspektywy autora (§25); DOI prowadzące do całego tomu albo do pracy o czymś innym (§17). Wpis pokazuje też, że model potrafi zmienić zadany temat (§24).

## hum/dev: slop w tekstach

Redakcja hum/dev, *Jak rozpoznawać slopy AI w tekstach? Na pewno nie maszynowo*, Humanistyka.dev, 8 grudnia 2025. https://blog.humanistyka.dev/2025/12/jak-rozpoznawac-slopy-ai-w-tekstach-na-pewno-nie-maszynowo

Omówienie dwóch prac o slopie, czyli masowych wytworach AI niskiej jakości. Ważniejsza dla skilla jest taksonomia slopu tekstowego z preprintu *Measuring AI "Slop" in Text* (arXiv, 2025, doi:10.48550/arXiv.2509.19163), zbudowana na wywiadach z ekspertami. Obejmuje m.in. małą gęstość informacji, powtarzanie tej samej myśli, rozwlekłość, zbędne formatowanie, niespójność, słownictwo niedopasowane do odbiorcy i bezbarwny ton. Skill bierze stąd powtórzenie (§2), żargon w tekście dla laików (§12) i omówienia zamiast nazw (§14). Według wpisu ludzie oceniający teksty tą taksonomią słabo się ze sobą zgadzali, a modele też słabo zgadzały się z ludźmi, co wspiera zasadę, że liczy się kilka wzorców naraz.

## hum/dev: akademicki slop

Redakcja hum/dev, *Janet H. Murray, Nick Monfort i mykotoksyny w krowim mleku*, Humanistyka.dev, 11 sierpnia 2026. https://blog.humanistyka.dev/2026/08/janet-h-murray-nick-monfort-i-mykotoksyny-w-krowim-mleku

Opis artykułu konferencyjnego o nowych gatunkach literackich, który okazał się wytworem modelu. Skill bierze stąd: definicje, które nic nie mówią, i pojęcia wymienione bez opisu (§25); napis „unsupported markdown” w schemacie (§21); wykres zbudowany na danych „hipotetycznych” i bibliografię z pracami spoza tematu (§17).

## hum/dev: perpleksja i wskazówki Wikipedii

Redakcja hum/dev, *Jak rozpoznać, czy tekst został wygenerowany przez AI? Ograniczenia perpleksji i propozycja Wikipedii*, Humanistyka.dev, 1 sierpnia 2025. https://blog.humanistyka.dev/2025/08/jak-rozpoznac-czy-tekst-zostal-wygenerowany-przez-ai-ograniczenia-perpleksji-i-propozycja-wikipedii

Wpis wyjaśnia, że detektory oparte na perpleksji oznaczają teksty o prostym słownictwie, i streszcza wskazówki Wikipedii dla prac studenckich. Skill bierze stąd formułki w rodzaju „Zgodnie z poleceniem” i niewypełnione pola szablonu (§21) oraz uwagę o perpleksji w części „Kiedy nie działać”.

Liang W, Yuksekgonul M, Mao Y, Wu E, Zou J. GPT detectors are biased against non-native English writers. Preprint arXiv, 2023. doi:10.48550/arXiv.2304.02819

Badanie, na które powołuje się wpis: detektory częściej uznają za maszynowe teksty osób, które nie piszą w języku ojczystym, bo ich słownictwo jest bardziej przewidywalne.

## hum/dev: pięć grup cech

Redakcja hum/dev, *Rozpoznawanie tekstów AI: pięć grup cech zamiast jednego wskaźnika*, Humanistyka.dev, 27 lutego 2026. https://blog.humanistyka.dev/2026/02/rozpoznawanie-tekstow-ai-piec-grup-cech-zamiast-jednego-wskaznika

Georgiou G. What Distinguishes AI-Generated from Human Writing? A Rapid Review of the Literature. *Big Data and Cognitive Computing*. 10(2):55. doi:10.3390/bdcc10020055

Przegląd 40 prac dzieli sygnały tekstu maszynowego na pięć grup: cechy powierzchniowe (stylometria, czytelność), dyskursywne, epistemiczne (ugruntowanie w faktach, doświadczenie autora), probabilistyczne i znaki wodne. Każda grupa zależy od gatunku, długości tekstu i parafrazy, więc jednego podpisu AI nie ma. Skill nie bierze stąd nowego wzorca. Przegląd potwierdza, że wzorce trzeba oceniać względem gatunku (część „Głos”) i że liczy się kilka wzorców naraz.

## hum/dev: opowiadania generowane dla 236 krajów

Redakcja hum/dev, *Syntetyczny prababkizm, czyli głęboki wymiar uprzedzeń dużych modeli językowych*, Humanistyka.dev, 22 września 2025. https://blog.humanistyka.dev/2025/09/syntetyczny-prababkizm-czyli-gleboki-wymiar-uprzedzen-duzych-modeli-jezykowych

Rettberg JW, Wigers H. Preprint arXiv, 2025. doi:10.48550/arXiv.2507.22445

Badacze z Bergen wygenerowali jednym modelem po 50 opowiadań dla każdego z 236 krajów. Fabuły powtarzały jeden schemat (powrót do małej miejscowości i ratowanie tradycji), słownictwo było cukierkowe, a realia kraju sprowadzały się do symboli widzianych z zewnątrz, więc po podmianie nazw własnych teksty były wymienne. Wpis pokazuje to na opowiadaniach „polskich”, w których klisze nie pasują do realiów okupacji. Skill bierze stąd realia z pocztówki w fikcji (§25).

## hum/dev: poezja generowana

Redakcja hum/dev, *Poezja bez ryzyka to tylko składnia: dlaczego ChatGPT nie sprawdzi się w tworzeniu poezji*, Humanistyka.dev, 23 lipca 2025. https://blog.humanistyka.dev/2025/07/poezja-bez-ryzyka-to-tylko-skladnia-dlaczego-chatgpt-nie-sprawdzi-sie-w-tworzeniu-poezji

Redakcja hum/dev, *Uprzedzenia wobec generatywnej poezji są w porządku*, Humanistyka.dev, 10 stycznia 2026. https://blog.humanistyka.dev/2026/01/uprzedzenia-wobec-generatywnej-poezji-sa-w-porzadku

Pierwszy wpis omawia pracę Olgi Vechtomovej (doi:10.48550/arXiv.2506.12634): duże modele dają wersy składniowo i znaczeniowo domknięte, dosłowne, z konwencjonalnymi obrazami, a wartość poetycką mają niedomknięcia, dwuznaczności i nieoczywiste zestawienia. Drugi omawia badania odbioru (doi:10.48550/arXiv.2511.21629, doi:10.1038/s41598-024-76900-1): czytelnicy bez przygotowania oceniają wiersze modeli wyżej, bo są prostsze i jednoznaczne. Skill bierze stąd zasadę z części „Głos”: w tekście literackim nie domykać tego, co autor zostawił otwarte.

## hum/dev: przypisy z czatu

Redakcja hum/dev, *Czasem przypis mówi więcej niż autor (?utm_source=chatgpt.com)*, Humanistyka.dev, 7 listopada 2025. https://blog.humanistyka.dev/2025/11/czasem-przypis-mowi-wiecej-niz-autor-utmsource-equal-chatgptcom

Wpis wyjaśnia, skąd bierze się parametr `utm_source=chatgpt.com`, i pokazuje go w przypisach polskich artykułów naukowych znalezionych w Google Scholar. Przypomina też, że bibliografia zebrana przez czat bywa zmyślona albo niepełna. Potwierdza §17.

## hum/dev: imitacja stylu przez dostrojone modele

Redakcja hum/dev, *Skuteczna maszynowa ekstrakcja stylu to poważne wyzwanie dla literatury*, Humanistyka.dev, 14 lipca 2026. https://blog.humanistyka.dev/2026/07/skuteczna-maszynowa-ekstrakcja-stylu-to-powazne-wyzwanie-dla-literatury

Redakcja hum/dev, *Być może model stylu literackiego powinien być chroniony*, Humanistyka.dev, 4 listopada 2025. https://blog.humanistyka.dev/2025/11/byc-moze-model-stylu-literackiego-powinien-byc-chroniony

Omówienia dwóch badań (doi:10.1145/3772318.3791276, doi:10.48550/arXiv.2510.13939): teksty modelu dostrojonego na książkach autora oceniano wyżej niż imitacje pisane przez ludzi, a detektory ich nie wykrywały. Skill nie bierze stąd wzorca. Wpisy wspierają dwie zasady: wynik detektora nie rozstrzyga o autorstwie, a wzorce A-F opisują domyślny styl modelu, nie każdy tekst maszynowy.

## Kutyła i in. (2026)

Kutyła M, Gryka P, Kozłowski M, Gradoń K, Janicki A. Feature comparison between human-written and LLM-generated documents – a case study. *Poznań Studies in Contemporary Linguistics*. 2026. doi:10.1515/psicl-2025-0063

Badanie z Politechniki Warszawskiej na polskim materiale: 2 400 par sprawozdań studenckich i ich odpowiedników napisanych przez model, 220 cech. Teksty modelu miały niższą perpleksję, mniej błędów, bardziej wyrównaną długość zdań i większą różnorodność słownictwa; do cech najsilniej odróżniających należały zaimki względne i słowa funkcyjne. Autorzy nazywają wyniki wstępnymi (jeden model, jeden gatunek). Skill bierze stąd sygnał „który” w §10 i miarę w `metryki_pl.py`, zawsze jako wskazówkę. Wynik o słownictwie przestrzega przed twierdzeniem, że modele piszą uboższym językiem.

## Reinhart i in. (2025)

Reinhart A, Markey B, Laudenbach M, Pantusen K, Yurko R, Weinberg G, Brown DW. Do LLMs write like humans? Variation in grammatical and rhetorical styles. *Proceedings of the National Academy of Sciences*. 2025;122(8). doi:10.1073/pnas.2422455122

Porównanie tekstów ludzi i modeli (Llama 3, GPT-4o) na wspólnych poleceniach, według cech gramatycznych i retorycznych Bibera. Różnice są systematyczne, nie znikają w większych modelach i są większe w modelach strojonych instrukcjami niż w bazowych. Modele strojone instrukcjami piszą stylem rzeczownikowym i gęstym informacyjnie, także gdy mają naśladować mowę potoczną: imiesłowowych zdań składowych używały 2-5 razy częściej niż ludzie, a nominalizacji 1,5-2 razy częściej. Dotyczy angielskiego. Skill powołuje się na to badanie w §11 i §16.

## Russell i in. (2025)

Russell J, Karpinska M, Iyyer M. People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text. Preprint arXiv, 2025. arXiv:2501.15654

Oceniający czytali 300 angielskich artykułów. Osoby, które rzadko używają modeli, rozpoznawały tekst maszynowy słabo i przeceniały swoją trafność. Pięć osób, które często piszą z modelami, pomyliło się w głosowaniu większościowym przy jednym tekście, także po parafrazie i „humanizacji”. Patrzyły na słownictwo, ale też na schematyczną budowę zdań i tekstu. Skill bierze stąd poprawkę w części „Kiedy nie działać” i uzasadnienie kroku 4.

## Wang i in. (2026)

Wang Z, Zhu G, Chen X. Humanized but Still True? Auditing Facts and Detection in AI-Text Humanizers. Preprint arXiv, 2026. arXiv:2611.00359

Audyt komercyjnych narzędzi, które przepisują tekst pod detektory. Wszystkie 11 zmieniało albo gubiło liczbę, datę, nazwę lub fragment w cudzysłowie w 35-65% dokumentów, które taki element zawierały; najczęściej zmieniały fragmenty w cudzysłowie. Preprint, bez recenzji. Uzasadnia grupę G i `porownaj_wersje.py`.

## The Economist (2026)

*How to spot AI writing*. The Economist, 30 lipca 2026. Przedruk: https://www.hindustantimes.com/lifestyle/art-culture/how-to-spot-ai-writing-101785491459334.html

Redakcja kazała czterem modelom napisać wersje własnych artykułów i porównała 55 940 zdań. Słowa uchodzące za znak modeli zanikły, a zostały słowa długie, uczone i nominalizacje; pauzę częściej niż ludzie stawiał już tylko jeden model; kontrast „nie X, lecz Y” i trójki nadal były częste. Dotyczy angielskiej publicystyki. Skill bierze stąd uwagę o starzeniu się list słów (§12) i nowe uzasadnienie §8.

## Prosty język na UMCS (2026)

Redakcja UMCS, *Po czym poznać, że tekst napisała sztuczna inteligencja?*, Prosty język na UMCS, 8 września 2026. https://www.umcs.pl/pl/aktualnosci,28839,po-czym-poznac-ze-tekst-napisala-sztuczna-inteligencja,186011.chtm

Poradnik uczelniany z polskimi sygnałami: „spotkanie” i „przestrzeń” w relacjach z wydarzeń, „nie tylko A, ale również B”, triady i wyliczenie „od X, przez Y, aż po Z”, cudzysłów po „tzw.”, tytuł naraz kursywą i w cudzysłowie. Poradnik nie podaje pomiarów. Skill bierze stąd frazy w §3 i §6 oraz dwa sygnały w §20.

## Mazur (2024)

Mazur R. O poprawności językowej tekstów generowanych przez SI na przykładzie ChatuGPT. *LingVaria*. 2024. https://journals.akademicka.pl/lv/article/view/5756

Analiza błędów językowych w wypracowaniach maturalnych napisanych przez ChatGPT. Najwięcej błędów było w złożonych konstrukcjach. Według omówień artykułu częstym błędem interpunkcyjnym był zbędny przecinek, także po okoliczniku na początku zdania; tego szczegółu nie sprawdzono w pełnym tekście, więc §20 podaje go jako sygnał do sprawdzenia, bez liczb.

## Przystalski i in. (2026)

Przystalski K, Argasiński JK, Grabska-Gradzińska I, Ochab JK. Stylometry recognizes human and LLM-generated texts in short samples. *Expert Systems with Applications*. 2026;296:129001. doi:10.1016/j.eswa.2025.129001

Badanie z Uniwersytetu Jagiellońskiego. Fragmenty po 10 zdań z wstępów haseł Wikipedii pisanych przez ludzi porównano z tekstami kilku modeli (od streszczaczy po GPT-4 i LLaMA), używając StyloMetrix, n-gramów i drzew decyzyjnych. Wynik ważny dla tego skilla: styl modeli rozkłada się na wiele cech naraz, a nie na jedną, którą da się „wyłączyć”.

## GAIDeT

Suchikova Y. i in. GAIDeT (Generative AI Delegation Taxonomy): A taxonomy for humans to delegate tasks to generative artificial intelligence in scientific research and publishing. *Accountability in Research*. 2025. doi:10.1080/08989621.2025.2544331

Redakcja hum/dev, *Taksonomia GAIDeT: jak raportować użycie sztucznej inteligencji w pisaniu*, Humanistyka.dev, 1 września 2025. https://blog.humanistyka.dev/2025/09/taksonomia-gaidet-jak-raportowac-uzycie-sztucznej-inteligencji-w-pisaniu

Taksonomia opisuje, jakie zadania badawcze i redakcyjne powierzono generatywnej AI, na dwóch poziomach: etapów pracy (od koncepcji po redakcję) i konkretnych zadań. Deklaracja wymienia tylko te zadania, przy których AI pomagała, zamiast ogólnego oświadczenia. Wpis wyjaśnia, dlaczego autorzy uznali CRediT i taksonomię NIST za niewystarczające, i proponuje dostosowanie GAIDeT do literatury i dziennikarstwa. Generator deklaracji: https://panbibliotekar.github.io/gaidet-declaration/index.html. Wzór po polsku: `jawnosc-ai.md`.

## Nature (2026)

*AI-detection tools have made huge leaps forward — how good are they?* Nature. 2026. doi:10.1038/d41586-026-02569-3

Przegląd stanu detektorów tekstu AI, na który powołuje się wpis hum/dev. Skill bierze stąd jedno: wynik detektora nie wystarcza, żeby rozstrzygać o autorstwie, zwłaszcza dla tekstu redagowanego z pomocą AI.

## Orwell

George Orwell, *Politics and the English Language* (1946).

Esej o języku, który ukrywa myśl za ogólnikami i napuszonymi słowami. Skill bierze z niego pojęcie pretensjonalnej dykcji (§14).
