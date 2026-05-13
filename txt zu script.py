import re

# ganze leute
valid_speakers =[
    "Director", "Dichter", "Lustige Person", "Raphael", "Gabriel", "Michael", "Zu Drei",
    "Mephistopheles", "Der Herr", "Faust", "Geist", "Wagner", "Chor der Engel",
    "Chor der Weiber", "Chor der Jünger", "Einige Handwerksbursche", "Andre", "Die ersten",
    "Ein Handwerksbursch", "Zweiter", "Die zweiten", "Ein dritter", "Vierter", "Fünfter",
    "Dienstmädchen", "Erste", "Schüler", "Bürgermädchen", "Zweiter Schüler", "Erster",
    "Bürger", "Bettler", "Andrer Bürger", "Dritter Bürger", "Alte", "Soldaten", "Bauern",
    "Alter Bauer", "Alle", "Frosch", "Brander", "Siebel", "Altmayer", "Chorus", "Die Thiere",
    "Der Kater", "Kater und Kätzin", "Die Hexe", "Margarete", "Marthe", "Lieschen", "Valentin",
    "Volk", "Böser Geist", "Irrlicht", "Stimme", "Stimmen", "Hexen", "Hexen im Chor", "Hexenmeister", "Halbes Chor",
    "Andre Hälfte", "Beide Chöre", "Halbhexe", "Chor der Hexen", "General", "Minister", "Parvenu",
    "Autor", "Trödelhexe", "Lilith", "Die Schöne", "Die Alte", "Proktophantasmist", "Servibilis",
    "Theatermeister", "Herold", "Oberon", "Puck", "Ariel", "Titania", "Geist der sich erst bildet",
    "Ein Pärchen", "Neugieriger Reisender", "Orthodox", "Nordischer Künstler", "Purist", "Junge Hexe",
    "Matrone", "Capellmeister", "Windfahne", "Xenien", "Hennings", "Musaget", "Ci-devant Genius der Zeit",
    "Kranich", "Weltkind", "Tänzer", "Tanzmeister", "Fideler", "Dogmatiker", "Idealist", "Realist",
    "Supernaturalist", "Skeptiker", "Die Gewandten", "Die Unbehülflichen", "Irrlichter", "Sternschnuppe",
    "Die Massiven", "Gretchen", "Chor"
]


speaker_map = {s.lower(): s for s in valid_speakers}

#ganze szenen ding
scene_headers = [
    "zueignung", "vorspiel auf dem theater", "prolog im himmel", 
    "der tragödie erster theil", "walpurgisnachtstraum oder oberons und titanias goldne hochzeit"
]

with open('faust.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

characters_found = set()
script_lines =[]
current_speaker = None


stage_dir_pattern = re.compile(r'^[a-z\[(].*|^(Er|Sie|Es|Alle|Beide) [^\!\?"]+\.$') # regex dings

for i in range(len(lines)):
    line = lines[i].strip()
    

    if not line or "Goethe: \"Faust\"" in line or "Johann Wolfgang von Goethe" in line:
        continue

    
    if stage_dir_pattern.match(line):
        script_lines.append(f'    # {line}')
        continue

  
    clean_line = line.rstrip('.').strip().lower()
    

    if clean_line in speaker_map:
        display_name = speaker_map[clean_line]
        current_speaker = "c_" + clean_line.replace(" ", "_").replace("-", "_")
        characters_found.add((current_speaker, display_name))
        continue
        
  
    if clean_line in scene_headers:
        script_lines.append(f'\n    # --- {line} ---')
        current_speaker = None
        continue

    
    safe_line = line.replace('"', '\\"') 
    if current_speaker:
        script_lines.append(f'    {current_speaker} "{safe_line}"')
    else:
        
        script_lines.append(f'    "{safe_line}"')

with open('script.rpy', 'w', encoding='utf-8') as out:
    out.write("# === CHARAKTERE\n")
    for var_name, display_name in sorted(characters_found):
        out.write(f'define {var_name} = Character("{display_name}", color="#ffffff")\n')
    
    out.write("\n#START\n")
    out.write("label start:\n\n")
  
    
    for script_line in script_lines:
        out.write(script_line + "\n")

