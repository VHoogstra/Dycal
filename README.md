# dyflexis-calendar-ics
een python script met interface die dyflexis uitleest en omzet naar een ICS voor agenda's

# todo's
- info enters komt op apple raar uit...
- als er 2 agenda items zijn, check of deze in dezeflde shift vallen en zo ja, voeg ze in de juiste volgorde toe aan ge agenda
- terugkoppeling bij ICS file kiezen en uploaden

    
# ter dev info
https://pyinstaller.org/en/stable/


# regels
1. deze software zal evenementen vanaf 24 uur voor nu pakken en niet eerder
2. de software leest de huidige maand en volgende maand uit
2. de software zoekt de naam op van de locatie (grote zaal of kleine zaal), mocht deze niet bestaan pakt hij de naam van je shift na de laatste >
    eg: zaandam > technische dienst > kleine zaal word kleine zaal
3. de browser opent fullscreen, als data niet op het scherm staat kan hij het niet lezen namelijk. 
    deze manier zorgt er ook voor dat het zichtbaar is wat de app doet

shifts: 
    diensten die je moet werken
agenda
    gewerkte uren (word nu niet geteld)
events:
    evenementen/verhuringen vanuit dyflexis

pyinstaller --onefile --windowed --specpath=build --name=Dyflexis-calendar-ics --icon=favicon.icns Main.py
pyinstaller --onedir --windowed --specpath=build --name=Dyflexis-calendar-ics --noconfirm --icon=favicon.icns Main.py