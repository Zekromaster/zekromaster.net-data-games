import os
import toml
from process_games import process_games_text

# Leggi le variabili d'ambiente
input_folder = os.environ.get("INPUT_FOLDER")
proof_base_path = os.environ.get("PROOF_BASE_PATH")

# Esci con il codice 1 se le variabili d'ambiente non sono impostate
if input_folder is None or proof_base_path is None:
    print("Le variabili d'ambiente INPUT_FOLDER e PROOF_BASE_PATH devono essere impostate.")
    exit(1)

# Ottieni l'elenco dei file ".games" nella cartella di input
games_files = [f for f in os.listdir(input_folder) if f.endswith(".games")]

completed_games = []

for games_file in games_files:
    # Leggi il contenuto del file di testo
    with open(os.path.join(input_folder, games_file), "r") as f:
        text = f.read()

    # Processa il testo utilizzando la funzione importata da process_games.py
    games = process_games_text(text, proof_base_path)
    completed_games.extend(games)

# Ordina l'elenco dei giochi completati per data di completamento in ordine crescente
completed_games.sort(key=lambda x: x["end"])

# Crea un dizionario con l'elenco dei giochi completati
toml_data = {"data": completed_games}

# Converte il dizionario in una stringa TOML
toml_string = toml.dumps(toml_data)
print(toml_string)