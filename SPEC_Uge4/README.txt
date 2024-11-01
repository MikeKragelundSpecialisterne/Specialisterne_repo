Jeg har fundet datasættet her: 
https://www.kaggle.com/datasets/namigabbasov/consumer-complaint-dataset

Det jeg syntes var mest udfordrende ved opgaven var, at lave datafiltrering. 
Jeg havde stor besvær med at konvertere og filtrere. 
Da data sættet var så stort, konkluderede jeg at det var smartest at filtere dataen og så lave min egen csv fil. 

Udover dette brugte jeg også ualmindelig lang tid på, at få memory_profiler til at fungerer.
Åbenbart har den en hovedprocess for programmet og en child, som måler.

Jeg fandt ud af at det hjalp markant på mine RAM, at jeg bruger en generator funktion til at loade testen, 
men det tager meget længere tid. 
Lige til mit datasæt på ca. 2.3 gb, var det måske okay, at have det i hukommelsen, især den denne pc. 
Men var datasættet større, eller min pc dårligere, kan jeg godt se logikken i at have en generator funktion. 