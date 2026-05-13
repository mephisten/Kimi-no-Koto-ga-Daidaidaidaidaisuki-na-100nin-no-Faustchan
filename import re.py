import re

# 1. Die DEFINITIVE Liste der echten Faust-Charaktere
VALID_CHARACTERS = {
    "c_faust", "c_mephistopheles", "c_margarete", "c_gretchen", "c_wagner", 
    "c_marthe", "c_valentin", "c_director", "c_dichter", "c_lustige_person",
    "c_raphael", "c_gabriel", "c_michael", "c_zu_drei", "c_geist", "c_lieschen",
    "c_chor_der_engel", "c_chor_der_weiber", "c_chor_der_jünger", "c_chor", "c_chorus",
    "c_böser_geist", "c_irrlicht", "c_stimme", "c_stimmen", "c_hexen", "c_hexen_im_chor",
    "c_oberon", "c_titania", "c_puck", "c_ariel", "c_alter_bauer",
    "c_alle", "c_frosch", "c_brander", "c_siebel", "c_altmayer", "c_soldaten", "c_bauern",
    "c_theatermeister", "c_herold", "c_geister", "c_die_hexe", "c_der_herr", "c_der_kater",
    "c_kater_und_kätzin", "c_schüler", "c_zweiter_schüler", "c_einige_handwerksbursche"
}

def clean_script(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    final_lines = []
    current_real_speaker = None
    in_definitions = True

    # Regex für: c_name "Text"
    dialog_pattern = re.compile(r'^(\s+)(c_[a-z0-9_\']+)\s+"(.*)"$')
    # Regex für: define c_name = ...
    define_pattern = re.compile(r'^define\s+(c_[a-z0-9_\']+)\s+=.*$')

    for line in lines:
        stripped = line.strip()
        
        if "label start:" in line:
            in_definitions = False
            final_lines.append(line)
            continue

        # --- TEIL 1: Header aufräumen ---
        if in_definitions:
            match = define_pattern.match(stripped)
            if match:
                char_id = match.group(1)
                if char_id in VALID_CHARACTERS:
                    final_lines.append(line)
            else:
                final_lines.append(line)
            continue

        # --- TEIL 2: Dialoge korrigieren ---
        # "Goethe: Faust" Zeilen komplett ignorieren
        if 'Goethe: \\"Faust\\"' in line or 'Johann Wolfgang von Goethe' in line:
            continue

        dialog_match = dialog_pattern.match(line)
        if dialog_match:
            indent = dialog_match.group(1)
            char_id = dialog_match.group(2)
            content = dialog_match.group(3)

            if char_id in VALID_CHARACTERS:
                current_real_speaker = char_id
                final_lines.append(f'{indent}{char_id} "{content}"\n')
            else:
                # Es war ein Fake-Charakter (z.B. c_ab)! 
                # Wir hängen den Text einfach an den letzten echten Sprecher an.
                if current_real_speaker:
                    final_lines.append(f'{indent}{current_real_speaker} "{content}"\n')
                else:
                    final_lines.append(f'{indent}"{content}"\n')
        else:
            final_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

# Ausführen
clean_script('script_fixed.rpy', 'script_repaired.rpy')
print("Reparatur fertig! Nutze 'script_repaired.rpy'.")