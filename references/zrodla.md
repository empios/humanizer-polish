# Źródła humanizer-polish

Streszczenia są napisane własnymi słowami i podają tylko to, co skill z danego źródła bierze. Szczegóły warto sprawdzić w oryginale.

## blader/humanizer

Siqi Chen (blader), *Humanizer*, wersja 3.1.0, licencja MIT. https://github.com/blader/humanizer

Umiejętność dla agentów, która usuwa z angielskiej prozy ślady pisania przez model. Z niej pochodzą: wyjaśnienie, skąd biorą się wzorce (model wybiera wariant pasujący do najszerszego odbiorcy), układ grup od najsilniejszych wzorców, kolejność pracy (szkic, sprawdzenie, wersja końcowa), zakaz dopisywania faktów, tryby zwracania wyniku i sekcja o tym, kiedy nie działać. Wzorce z grup A–F, które mają odpowiednik w tym repozytorium, są jego adaptacjami; przykłady napisano od nowa po polsku. Skrypt `validate-package.py` jest przeróbką walidatora z tego repozytorium.

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
