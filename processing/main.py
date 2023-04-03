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

# Ordina l'elenco dei giochi completati per slug in ordine crescente
# Removes "The", "A", "An" from the beginning of a title given as a string
def remove_articles(title):
    articles = ["The", "A", "An"]
    for article in articles:
        if title.startswith(article):
            return title[len(article) + 1 :]
    return title

completed_games.sort(key=lambda x: remove_articles(x["name"]))

# Crea un dizionario con l'elenco dei giochi completati
toml_data = {"data": completed_games}

# Converte il dizionario in una stringa TOML
toml_string = toml.dumps(toml_data)
print(toml_string)