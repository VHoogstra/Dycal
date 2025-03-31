# dyflexis-calendar-ics
a python script to read planning from dyflexis and export as ICS

this script shall first read the webpage from Dyflexis.com and read the data

todo, click op event en dan daar de tekst uit slepen
flux-panel flux-ubuntu
    parrent
flx-middle->flx-canvas padded
vpaned




lijkt er op alsof de ics niet alle data na loopt.. mis de 23e bv maar staat wel in de json

https://pyinstaller.org/en/stable/
das een goeie, custom tkinter ook


als er 2 agenda items zijn, check of deze in dezeflde shift vallen en zo ja, voeg ze in de juiste volgorde toe aan ge agenda

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

pyinstaller.exe --onefile --windowed --icon= YOUR_ICON.ico YOUR_APP_NAME.py