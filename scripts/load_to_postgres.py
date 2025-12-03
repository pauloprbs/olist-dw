import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# --- Configurações ---
DATA_DIR = "data"
# Conecta como localhost pois o script roda na sua máquina
DB_URI = os.getenv("DB_URI", "postgresql://user:password@localhost:5432/olist_dw")

def load_data():
    print("🔌 Conectando ao Banco de Dados...")
    engine = create_engine(DB_URI)

    try:
        with engine.connect() as conn:
            # 1. Criação da Estrutura de Schemas (Layers)
            print("🏗️  Criando schemas (raw, dw, marts)...")
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw;"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS marts;"))
            conn.commit() # Confirma a transação
            print("✅ Schemas garantidos!")
            
    except Exception as e:
        print(f"❌ Erro ao criar schemas: {e}")
        return

    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    print(f"📦 Encontrados {len(files)} arquivos CSV para processar.")

    for filename in files:
        file_path = os.path.join(DATA_DIR, filename)
        
        # Limpeza do nome: olist_customers_dataset.csv -> customers
        table_name = filename.replace('olist_', '').replace('_dataset.csv', '').replace('.csv', '')
        
        print(f"🔄 Processando: {filename} -> Tabela: raw.{table_name}")
        
        try:
            df = pd.read_csv(file_path)
            
            # 2. Salva explicitamente no schema 'raw'
            df.to_sql(
                table_name, 
                engine, 
                schema='raw',
                if_exists='replace',
                index=False
            )
            
            print(f"   ✅ Tabela 'raw.{table_name}' criada com {len(df)} registros.")
            
        except Exception as e:
            print(f"   ❌ Erro ao carregar {filename}: {e}")

    print("🏁 Ingestão no schema 'raw' finalizada!")

if __name__ == "__main__":
    load_data()