Jeg har fundet datasættet her: 
https://www.kaggle.com/datasets/namigabbasov/consumer-complaint-dataset

Det jeg syntes var mest udfordrende ved opgaven var, at lave datafiltrering. 
Jeg havde stor besvær med at konvertere og filtrere. 
Da data sættet var så stort, konkluderede jeg at det var smartest at filtere dataen og så lave min egen csv fil. 

Udover dette brugte jeg også ualmindelig lang tid på, at få memory_profiler til at fungerer.
Åbenbart har den en hovedprocess for programmet og en child, som måler.

Jeg fandt ud af at det hjalp markant på mine RAM, at jeg bruger en generator funktion til at loade teksten, 
men det tager meget længere tid. 
Til størrelsen på dette datasæt og med denne pc, kan man måske overveje at have det i hukommelsen på en gang,
Men var datasættet større, eller min pc dårligere, kan jeg godt se logikken i at have en generator funktion. 