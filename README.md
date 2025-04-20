# dyflexis-calendar-ics

Een python script met interface die dyflexis uitleest en omzet naar een ICS,csv en Google agenda. 
de app zal vragen om lokaal data op te slaan, dit is niet vereist voor het gebruik van de app. Het gaat hier om log data voor wanneer er 
iets niet goed gaat en configuratie data zoals het wachtwoord voor dyflexis

# regels
1. deze software zal alleen shifts vanaf 24 uur voor nu mee pakken. Dit omdat oudere diensten in dyflexis omgezet worden naar gewerkte uren
2. de software bied de mogelijkheid om een periode bereik te maken die gescanned zullen worden
3. de software zoekt de naam op van de locatie (grote zaal of kleine zaal), mocht deze niet bestaan pakt hij de naam van
   je shift na de laatste >
   eg: zaandam > technische dienst > kleine zaal wordt kleine zaal
4. de browser opent fullscreen, als data niet op het scherm staat kan hij het niet lezen namelijk.
   deze manier zorgt er ook voor dat het zichtbaar is wat de app doet

# gebruik

## apple

Voor apple hebben wij een portable executable gemaakt. dit houd in dat het niet geinstalleerd hoeft en makkelijk te
verplaatsen is van computer naar computer
ookal is het portable, als je kiest om data op te laten slaan gebeurd dit onder je gebruikers folder.. mocht je je data
naar een andere computer verplaatsen kan je deze computer kopieren plakken of je config exporteren.

## windows

## overig

## data

hier iets over verplaatsen en data, wat slaan we op en hoe. is dit nodig?

# disclaimer

Deze applicatie is geschreven zodat het plannen van persoonlijke afspraken makkelijker is naast dyflexis. Wij zijn niet
verantwoordelijk als het script een item mist
wat resulteert in afwezigheid of laat komen. Dyflexis is *altijd* lijdend.
Wij zijn ook niet verantwoordelijk als er dubbele afspraken in uw agenda komen door het verkeerd gebruik van het ICS-bestand.

shifts: 
diensten die je moet werken \
agenda:
gewerkte uren  \
events:
evenementen/verhuringen vanuit dyflexis 

# toekomstige features
- optie om een extra karakter toe te voegen aan het agenda item als de start/stop tijden niet overeen komen met de tijden van het evenement
