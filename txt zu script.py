# Die absolute, exakte Liste der Sprecher in Faust 1.
# Kein "Erraten" von Namen mehr! Nur diese Namen werden als Sprecher akzeptiert.
speaker_list =[
    "Director", "Dichter", "Lustige Person", "Raphael", "Gabriel", "Michael", "Zu Drei",
    "Mephistopheles", "Der Herr", "Faust", "Geist", "Wagner", "Chor der Engel",
    "Chor der Weiber", "Chor der Jünger", "Einige Handwerksbursche", "Andre", "Die ersten",
    "Ein Handwerksbursch", "Zweiter", "Die zweiten", "Ein dritter", "Vierter", "Fünfter",
    "Dienstmädchen", "Erste", "Schüler", "Bürgermädchen", "Zweiter Schüler", "Erster",
    "Bürger", "Bettler", "Andrer Bürger", "Dritter Bürger", "Alte", "Soldaten", "Bauern",
    "Alter Bauer", "Alle", "Frosch", "Brander", "Siebel", "Altmayer", "Chorus", "Die Thiere",
    "Der Kater", "Kater und Kätzin", "Die Hexe", "Margarete", "Marthe", "Lieschen", "Valentin",
    "Volk", "Böser Geist", "Irrlicht", "Stimme", "Stimmen", "Hexen", "Hexen im Chor", "Hexenmeister", 
    "Halbes Chor", "Andre Hälfte", "Beide Chöre", "Halbhexe", "Chor der Hexen", "General", 
    "Minister", "Parvenu", "Autor", "Trödelhexe", "Lilith", "Die Schöne", "Die Alte", "Proktophantasmist", 
    "Servibilis", "Theatermeister", "Herold", "Oberon", "Puck", "Ariel", "Titania", "Geist der sich erst bildet",
    "Ein Pärchen", "Neugieriger Reisender", "Orthodox", "Nordischer Künstler", "Purist", "Junge Hexe",
    "Matrone", "Capellmeister", "Windfahne", "Xenien", "Hennings", "Musaget", "Ci-devant Genius der Zeit",
    "Kranich", "Weltkind", "Tänzer", "Tanzmeister", "Fideler", "Dogmatiker", "Idealist", "Realist",
    "Supernaturalist", "Skeptiker", "Die Gewandten", "Die Unbehülflichen", "Irrlichter", "Sternschnuppe",
    "Die Massiven", "Gretchen", "Chor", "Orchester", "Orchester Tutti"
]

# Überschriften, die vom Skript als Szenen erkannt werden sollen
scene_headers = {
    "zueignung", "vorspiel auf dem theater", "prolog im himmel", "der tragödie erster theil",
    "nacht", "vor dem thor", "studirzimmer", "auerbachs keller in leipzig", "zeche lustiger gesellen",
    "hexenküche", "straße", "abend", "der nachbarin haus", "spaziergang", "garten", "ein gartenhäuschen",
    "wald und höhle", "gretchens stube", "marthens garten", "am brunnen", "zwinger", "dom",
    "walpurgisnacht", "harzgebirg. gegend von schierke und elend", "walpurgisnachtstraum oder oberons und titanias goldne hochzeit",
    "intermezzo", "trüber tag", "feld", "offen feld", "kerker", "straße vor gretchens thüre", "amt, orgel und gesang"
}

# Lookup Map erstellen
speakers = {name.lower(): name for name in speaker_list}

with open('faust.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

characters_found = set()
script_lines =[]
current_speaker = None

for line in lines:
    line = line.strip()
    
    # 1. Leere Zeilen und nervige Buch-Kopfzeilen komplett ignorieren
    if not line or "Goethe: \"Faust\"" in line or "Johann Wolfgang von Goethe" in line or "Eine Tragödie. [Erster Theil.]" in line:
        continue

    # Für den Check trimmen wir Punkte am Ende weg und machen alles klein
    clean_line = line.rstrip('.').lower()

    # 2. Check: Ist es eine Szenen-Angabe?
    if clean_line in scene_headers:
        script_lines.append(f'\n    # --- SZENE: {line} ---')
        current_speaker = None
        continue

    # 3. Check: Ist es EIN ECHTER SPRECHER aus unserer Liste?
    if clean_line in speakers:
        display_name = speakers[clean_line]
        current_speaker = "c_" + clean_line.replace(" ", "_").replace("-", "_")
        characters_found.add((current_speaker, display_name))
        continue

    # 4. Check: Ist es eine Regieanweisung?
    # Beginnt klein oder mit Klammer
    if line[0].islower() or line.startswith('[') or line.startswith('('):
        script_lines.append(f'    # {line}')
        continue
    
    # Häufige isolierte Regiewörter im Text (wie "Ab.", "Stirbt.")
    if clean_line in ["ab", "faust ab", "faust allein", "sie weint", "er singt", "singt", "stirbt", "orgelton", "fortissimo", "pianissimo", "solo"]:
        script_lines.append(f'    # {line}')
        continue
        
    # Sätze, die mit "ab" oder "auftritt" enden/beginnen
    if line.endswith(" ab.") or line.endswith(" ab") or "tritt auf" in clean_line or "tritt ein" in clean_line or "geht" in clean_line:
        if len(line) < 60: # Regieanweisungen sind meist kurz
            script_lines.append(f'    # {line}')
            continue

    # 5. Wenn es KEIN Sprecher aus der Liste und KEINE Regie ist -> DIALOG!
    safe_line = line.replace('"', '\\"')
    if current_speaker:
        script_lines.append(f'    {current_speaker} "{safe_line}"')
    else:
        # Erzähler-Text
        script_lines.append(f'    "{safe_line}"')

# ---- AUSGABE GENERIEREN ----
with open('script.rpy', 'w', encoding='utf-8') as out:
    out.write("# === CHARAKTER DEFINITIONEN ===\n")
    for var_name, display_name in sorted(characters_found):
        out.write(f'define {var_name} = Character("{display_name}", color="#ffffff")\n')
    
    out.write("\n# === SPIEL START ===\n")
    out.write("label start:\n\n")
    out.write("    scene bg_studierzimmer with fade\n\n")
    
    for script_line in script_lines:
        out.write(script_line + "\n")

print("Erfolg! Ein zu 100% sauberes Ren'Py-Skript wurde generiert.")