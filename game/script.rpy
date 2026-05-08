# Du kannst das Skript für Dein Spiel in diese Datei schreiben.

# Unterhalb dieser Zeile kannst Du Bilder definieren, indem Du das Wort "image" verwendest
# z. B. image eileen happy = "eileen_happy.png"

# Erstelle hier Charaktere, die in Deinem Spiel auftauchen werden
define f = Character('Faust-chan', color="#ffc8f3")
define w = Character('Wagner-san', color="#c52c2c")
define m = Character('Mephistopheles', color = "#6d0f0f" )
init python:

    renpy.music.register_channel("music2", mixer="music", loop=True)
    renpy.music.register_channel("music3", mixer="music", loop=True)
# Hier beginnt das Spiel.
label start:
    scene dhkdas
    show faust gluecklich at right
    show onimai peak 
    
    f "{space=350}Habe nun, ach! Philosophie," 

    extend "\nJuristerei und Medizin," 
    extend "\n{space=350}Und leider auch Theologie" 

    play music2 "Faust-chan.mp3" loop
   

    extend "\nDurchaus studiert, mit heißem Bemühn." 
    show wagner neutral at left

    f "Da steh ich nun, ich armer Tor!"
    play music3 "peak.ogg"
    extend "\nUnd bin so klug als wie zuvor;"

    extend "\n Heiße Magister, heiße Doktor gar"

    f "Und ziehe schon an die zehen Jahr"

    f "Herauf, herab und quer und krumm"

    f "Meine Schüler an der Nase herum –"

    f "Und sehe, daß wir nichts wissen können!"
   
    return
