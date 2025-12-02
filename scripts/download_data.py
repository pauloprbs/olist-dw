import os
import json
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv

# --- Configurações ---
DATASET_NAME = "olistbr/brazilian-ecommerce"
DATA_DIR = "data"

# Pega o caminho absoluto da pasta raiz do projeto (onde está o script, volta uma pasta)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAGGLE_JSON_PATH = os.path.join(BASE_DIR, "kaggle.json")

def authenticate():
    """
    Tenta autenticar usando .env ou lendo o arquivo kaggle.json na raiz.
    """
    # 1. Tenta carregar do .env
    load_dotenv(os.path.join(BASE_DIR, ".env"))

    # 2. Se não achou no env, tenta ler o arquivo kaggle.json na raiz
    if not os.getenv("KAGGLE_USERNAME") and os.path.exists(KAGGLE_JSON_PATH):
        print(f"🔑 Lendo credenciais de: {KAGGLE_JSON_PATH}")
        with open(KAGGLE_JSON_PATH, 'r') as f:
            creds = json.load(f)
            os.environ['KAGGLE_USERNAME'] = creds['username']
            os.environ['KAGGLE_KEY'] = creds['key']
    
    # 3. Verifica se deu certo
    if not os.getenv("KAGGLE_USERNAME"):
        raise Exception("❌ Credenciais não encontradas! Crie um .env ou coloque o kaggle.json na raiz.")

    api = KaggleApi()
    api.authenticate()
    return api

def download_dataset():
    # Cria pasta data se não existir
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    print(f"⬇️ Iniciando download do dataset: {DATASET_NAME}...")
    
    try:
        api = authenticate()
        
        # Baixa os arquivos
        api.dataset_download_files(DATASET_NAME, path=DATA_DIR, unzip=False)
        print("✅ Download concluído!")
        
        # Descompactar
        print("📦 Descompactando arquivos...")
        zip_found = False
        for file in os.listdir(DATA_DIR):
            if file.endswith(".zip"):
                zip_found = True
                file_path = os.path.join(DATA_DIR, file)
                print(f"   Extraindo {file}...")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(DATA_DIR)
                os.remove(file_path) # Limpa o zip
        
        if not zip_found:
            print("⚠️ Nenhum arquivo zip encontrado (talvez já tenha sido baixado?)")
        else:
            print(f"✨ Sucesso! Arquivos disponíveis em: {DATA_DIR}/")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    download_dataset()