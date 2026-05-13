import re

# 1. Die Liste der einzig wahren Charaktere (Variablennamen)
VALID_IDS = {
    "c_faust", "c_mephistopheles", "c_margarete", "c_gretchen", "c_wagner", 
    "c_marthe", "c_valentin", "c_director", "c_dichter", "c_lustige_person",
    "c_raphael", "c_gabriel", "c_michael", "c_zu_drei", "c_geist", "c_lieschen",
    "c_chor_der_engel", "c_chor_der_weiber", "c_chor_der_jünger", "c_chor", "c_chorus",
    "c_böser_geist", "c_irrlicht", "c_stimme", "c_stimmen", "c_hexen", "c_hexen_im_chor",
    "c_oberon", "c_titania", "c_puck", "c_ariel", "c_tanz_und_gesang", "c_alter_bauer",
    "c_alle", "c_frosch", "c_brander", "c_siebel", "c_altmayer", "c_soldaten", "c_bauern"
}

def fix_renpy_script(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    last_valid_speaker = None
    in_definitions = True

    # Regex für: c_name "Text"
    dialog_pattern = re.compile(r'^(\s+)(c_[a-z0-9_\']+)\s+(.*)$')
    # Regex für: define c_name = ...
    define_pattern = re.compile(r'^define\s+(c_[a-z0-9_\']+)\s+=.*$')

    for line in lines:
        stripped = line.strip()
        
        # Sobald "label start:" kommt, sind wir im Spielteil
        if "label start:" in line:
            in_definitions = False
            new_lines.append(line)
            continue

        # --- TEIL 1: Definitionen am Anfang filtern ---
        if in_definitions:
            match = define_pattern.match(stripped)
            if match:
                char_id = match.group(1)
                if char_id in VALID_IDS:
                    new_lines.append(line)
                # Fake-Charaktere werden hier einfach übersprungen (gelöscht)
            else:
                new_lines.append(line)
            continue

        # --- TEIL 2: Dialoge im Spielteil korrigieren ---
        dialog_match = dialog_pattern.match(line)
        if dialog_match:
            indent = dialog_match.group(1)
            char_id = dialog_match.group(2)
            dialog_text = dialog_match.group(3)

            if char_id in VALID_IDS:
                # Ein echter Sprecher! Wir merken ihn uns.
                last_valid_speaker = char_id
                new_lines.append(line)
            else:
                # Ein falscher Sprecher (z.B. c_ab)!
                # Wir weisen den Text dem letzten echten Sprecher zu oder machen ihn zum Erzähler.
                if last_valid_speaker:
                    new_lines.append(f"{indent}{last_valid_speaker} {dialog_text}\n")
                else:
                    new_lines.append(f"{indent}{dialog_text}\n")
        else:
            # Kommentare oder Szenenanweisungen einfach behalten
            new_lines.append(line)

    # Datei speichern
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Reparatur abgeschlossen! Datei '{output_file}' wurde erstellt.")

# Starte die Reparatur
# Stelle sicher, dass deine aktuelle Datei 'script.rpy' heißt
fix_renpy_script('script.rpy', 'script_fixed.rpy')