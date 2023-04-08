import re
from datetime import datetime
from slugify import slugify
import os

def remap_platform(platform):
    platforms = {
        "PC": "PC",
        "PSX": "Sony PlayStation",
        "PS2": "Sony PlayStation 2",
        "PS3": "Sony PlayStation 3",
        "PSP": "Sony PlayStation Portable",
        "GCN": "Nintendo GameCube",
        "Wii": "Nintendo Wii",
        "WiiU": "Nintendo Wii U",
        "NSW": "Nintendo Switch",
        "GBA": "Nintendo GameBoy Advance",
        "NDS": "Nintendo DS",
        "3DS": "Nintendo 3DS",
        "X360": "Microsoft Xbox 360",
    }

    return platforms.get(platform, platform)

def process_games_text(text, proof_base_path):
    lines = text.strip().split("\n")
    completed_games = []

    for line in lines:
        # Ignora le righe che non contengono giochi completati
        if "[✓]" not in line:
            continue

        # Estrai le informazioni utilizzando espressioni regolari
        name = re.search(r'\] (.+?) \|', line).group(1)
        completion = re.search(r'Finito (?:al|con) (.+?) \|', line).group(1)
        start = re.search(r'Inizio: (.+?) \|', line).group(1)
        end = re.search(r'Fine: (.+?) \|', line).group(1)
        platform = re.search(r'Piattaforma: (.+?)$', line).group(1)

        # Converte le date nel formato ISO
        start_iso = datetime.strptime(start, "%Y-%m-%d").date().isoformat()
        end_iso = datetime.strptime(end, "%Y-%m-%d").date().isoformat()

        # Genera uno slug ASCII per il nome del gioco
        slug = slugify(name)

        # Cerca i file di prova nella cartella corrispondente allo slug
        proof_folder = os.path.join(proof_base_path, slug)
        proof_files = []

        for root, dirs, files in os.walk(proof_folder):
            for file in files:
                # Calcola il percorso relativo del file di prova rispetto alla cartella di base
                relative_path = os.path.relpath(os.path.join(root, file), proof_base_path)
                proof_files.append(relative_path)

        # Cerca i file di prova con lo slug come nome e qualsiasi estensione
        for file in os.listdir(proof_base_path):
            file_path = os.path.join(proof_base_path, file)
            if os.path.isfile(file_path) and os.path.splitext(file)[0] == slug:
                proof_files.append(file)

        # Crea un oggetto gioco con le informazioni estratte e l'elenco dei file di prova
        game = {
            "name": name,
            "completion": completion,
            "start": start_iso,
            "end": end_iso,
            "platform": remap_platform(platform),
            "proof": proof_files,
            "slug": slug
        }

        completed_games.append(game)

    return completed_games