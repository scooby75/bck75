import os
import pyrebase
import json

def initialize_firebase():
    # Lê as informações de configuração do arquivo JSON
    with open("firebase_config.json") as json_file:
        firebase_config = json.load(json_file)
    
    # Inicializa o Firebase
    firebase = pyrebase.initialize_app(firebase_config)
    
    # Retorna a instância de autenticação do Firebase
    return firebase.auth()
