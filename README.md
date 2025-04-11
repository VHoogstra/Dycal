# dyflexis-calendar-ics

Een python script met interface die dyflexis uitleest en omzet naar een ICS voor agenda's

# todo's

- als er 2 agenda-items zijn, check of deze in dezeflde shift vallen en zo ja, voeg ze in de juiste volgorde toe aan ge
  agenda
    - even een test case voor schrijven?
- bestand opslaan als en openen doen aan de hand van de laatste keer dat je dat in de app deed
- evenementen te verwijderen?? kan niet via ics
- load en save config moeten events worden zodat exportwidgets daar bij kunnen en op kunnen handelen
- dyflexis shift vars in config weg stoppen
- de shift genereer logica in de lijst weg werken.. en dan ideaal dat hij meteen eventData update zodat je in details in
  real time mee kan kijken
- in details menu ook de mogelijkheid geven om meer kopjes te laten zien? alle waardes van een shift bv

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
# ter dev info

https://pyinstaller.org/en/stable/
pyinstaller --onefile --windowed --specpath=build --name=Dyflexis-calendar-ics --icon=favicon.icns Main.py
pyinstaller --onedir --windowed --specpath=build --name=Dyflexis-calendar-ics --noconfirm --icon=favicon.icns Main.py