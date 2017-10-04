# Počítadlo lží politiků
Skript pro stáhnutí dat z demagog.cz a výpočtu "lživosti" jednotlivých politiků.

Princip je jednoduchý: stáhnout se data ze serveru demagog.cz a pro každý stažený subjekt se vypočítá míra lhaní podle následujícího vzorce:

míra\_lhaní = počet\_nepravd / (počet\_všech\_výroků)

kde počet\_všech\_výroků znamená součet počtu pravda, nepravd, zavádějících a neověřitelných. Pokud někdo nemá na kontě žádný výrok, je míra\_lhaní rovna 0.

V souboru demagog-lhari.csv je vygenerovaný soubor, jména jsou seřazena od největší míry lhaní po nejnižší.

