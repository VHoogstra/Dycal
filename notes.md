# todo's
- dyflexis shift vars in config weg stoppen
  - nog in het config scherm laten zien
  - ook de optie wegschrijven voor uitlezen events, uitlezen collega's
  - optie voor * aan de naam toevoegen
  - optie voor tijden aanmerking als event inhoud niet overeenkomt met event tijden
  - 
- evenementen te verwijderen?? kan niet via ics

een test voor wanneer ik wel items heb in gevent maar niet in het returnobject. dit zou ontstaan doordat er geen update
van het event nodig is. heb er nu eenlosse array voor toegevoegd.

# test info
dyflexis functie
genereren van csv, ics en google van event data naar output


# ter dev info

https://pyinstaller.org/en/stable/
pyinstaller --onefile --windowed --specpath=build --name=dycal-file --icon=favicon.icns Main.py
pyinstaller --onedir --windowed --specpath=build --name=Dycal-dir --noconfirm --icon=favicon.icns Main.py