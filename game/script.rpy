# Du kannst das Skript für Dein Spiel in diese Datei schreiben.

# Unterhalb dieser Zeile kannst Du Bilder definieren, indem Du das Wort "image" verwendest
# z. B. image eileen happy = "eileen_happy.png"

# Erstelle hier Charaktere, die in Deinem Spiel auftauchen werden
define f = Character('Faust-chan', color="#ffc8f3")
define w = Character('Wagner-san', color="#c52c2c")
define m = Character('Mephistopheles', color = "#6d0f0f" )
# Hier beginnt das Spiel.
label start:
    scene dhkdas

    f "Habe nun, ach! Philosophie," 

    extend "\nJuristerei und Medizin," 
    extend "\n      Und leider auch Theologie" 

    extend "\nDurchaus studiert, mit heißem Bemühn." 

    f "Da steh ich nun, ich armer Tor!"

    f "Und bin so klug als wie zuvor;"

    f "Heiße Magister, heiße Doktor gar"

    f "Und ziehe schon an die zehen Jahr"

    f "Herauf, herab und quer und krumm"

    f "Meine Schüler an der Nase herum –"

    f "Und sehe, daß wir nichts wissen können!"

    return
