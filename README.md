# dyflexis-calendar-ics

Een python script met interface die dyflexis uitleest en omzet naar een ICS voor agenda's

# regels

1. deze software zal evenementen vanaf 24 uur voor nu pakken en niet eerder
2. de software leest de huidige maand en volgende maand uit
3. de software zoekt de naam op van de locatie (grote zaal of kleine zaal), mocht deze niet bestaan pakt hij de naam van
   je shift na de laatste >
   eg: zaandam > technische dienst > kleine zaal wordt kleine zaal
4. de browser opent fullscreen, als data niet op het scherm staat kan hij het niet lezen namelijk.
   deze manier zorgt er ook voor dat het zichtbaar is wat de app doet
5. de ics, csv en google naar hun eigen widget files overbrengen

# disclaimer

Deze applicatie is geschreven zodat het plannen van persoonlijke afspraken makkelijker is naast dyflexis. Wij zijn niet
verantwoordelijk als het script een item mist
wat resulteert in afwezigheid of laat komen. Dyflexis is *altijd* lijdend.
Wij zijn ook niet verantwoordelijk als er dubbele afspraken in uw agenda komen door het verkeerd gebruik van het ICS-bestand.

shifts:
diensten die je moet werken
agenda
gewerkte uren (word nu niet geteld)
events:
evenementen/verhuringen vanuit dyflexis

# toekomstige features
- export naar csv zodat er ook een uitdraai van gewerkte diensten mee genomen kan worden. 
- optie om een extra karakter toe te voegen aan het agenda item als de start/stop tijden niet overeen komen met de tijden van het evenement
