# dyflexis-calendar-ics
een python script met interface die dyflexis uitleest en omzet naar een ICS voor agenda's

# todo's
- als er 2 agenda items zijn, check of deze in dezeflde shift vallen en zo ja, voeg ze in de juiste volgorde toe aan ge agenda
  - even een test case voor schrijven?
- bestand opslaan als en openen doen aan de hand van de laatste keer dat je dat in de app deed
- config downloaden en uploaden? 
  - dit ivm nieuwere versies
- als de tijden in de omschrijving niet overeen komen met de agenda tijd iets aangeven
- evenementen te verwijderen?? kan niet via ics
- export naar csv zodat je ook gewerkte shifts mee kan nemen. mogelijkheid om een csv te updaten? 
  - mogelijk ook excel?
- load en save config moeten events worden zodat exportwidgets daar bij kunnen en op kunnen handelen
- detail scherm resizen zodat het beter leesbaar is

# regels
1. deze software zal evenementen vanaf 24 uur voor nu pakken en niet eerder
2. de software leest de huidige maand en volgende maand uit
2. de software zoekt de naam op van de locatie (grote zaal of kleine zaal), mocht deze niet bestaan pakt hij de naam van je shift na de laatste >
    eg: zaandam > technische dienst > kleine zaal word kleine zaal
3. de browser opent fullscreen, als data niet op het scherm staat kan hij het niet lezen namelijk. 
    deze manier zorgt er ook voor dat het zichtbaar is wat de app doet
4. de ics, csv en google naar hun eigen widget files overbrengen

# disclaimer
Deze applicatie is geschreven zodat het plannen van persoonlijke afspraken makkelijker is naast dyflexis. Wij zijn niet verantwoordelijk als het script een item mist 
wat resulteert in afwezigheid of laat komen. Dyflexis is *altijd* lijdend. 
Wij zijn ook niet verantwoordelijk als er dubbele afspraken in uw agenda komen door het verkeerd gebruik van het ICS bestand.

shifts: 
    diensten die je moet werken
agenda
    gewerkte uren (word nu niet geteld)
events:
    evenementen/verhuringen vanuit dyflexis


# ter dev info
https://pyinstaller.org/en/stable/
pyinstaller --onefile --windowed --specpath=build --name=Dyflexis-calendar-ics --icon=favicon.icns Main.py
pyinstaller --onedir --windowed --specpath=build --name=Dyflexis-calendar-ics --noconfirm --icon=favicon.icns Main.py