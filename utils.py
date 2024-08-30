import json
import os
from config import Config

def load_data():
    # Verifica se o arquivo existe
    if not os.path.exists(Config.JSON_FILE_PATH):
        # Se não existir, cria o arquivo com um conteúdo inicial padrão
        with open(Config.JSON_FILE_PATH, 'w') as file:
            json.dump({"items": []}, file, indent=4)  # Inicia com uma lista de itens vazia
    
    # Carrega os dados do arquivo JSON
    with open(Config.JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(Config.JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
